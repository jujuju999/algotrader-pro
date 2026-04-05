"""
AlgoTrader Pro — Cloud Backend
================================
Finnhub Live Daten + 7 Strategien + KI-Lernfunktion
Deployment: Railway.app
"""

import asyncio, json, logging, math, os, random, sqlite3, time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

try:
    import httpx
    HTTPX_OK = True
except ImportError:
    HTTPX_OK = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()]
)
log = logging.getLogger("AlgoTrader")

FINNHUB_KEY = os.getenv("FINNHUB_KEY", "d6s6mg1r01qqlgbk3hhgd6s6mg1r01qqlgbk3hi0")
IC          = 10_000.0

# ══════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════

def init_db():
    c = sqlite3.connect("algotrader.db")
    c.executescript("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, sym TEXT, side TEXT, strategy TEXT,
            price REAL, qty REAL, value REAL, pnl REAL,
            score REAL, cash_after REAL,
            dominant_strat TEXT, strat_scores TEXT
        );
        CREATE TABLE IF NOT EXISTS equity_curve (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, value REAL, cash REAL, pnl REAL
        );
        CREATE TABLE IF NOT EXISTS learning_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, weights TEXT, accuracy REAL,
            total_trades INTEGER, win_rate REAL, note TEXT
        );
    """)
    c.commit(); c.close()
    log.info("DB initialisiert")

def db_exec(sql, params=()):
    c = sqlite3.connect("algotrader.db")
    c.execute(sql, params)
    c.commit(); c.close()

# ══════════════════════════════════════════════════════
# KI-LERNFUNKTION (Reinforcement Learning)
# ══════════════════════════════════════════════════════

class StrategyLearner:
    """
    Adaptives Gewichtungssystem.
    Jede Strategie bekommt nach jedem Trade ein Feedback:
    - Gewinn → Strategie die Signal auslöste wird belohnt
    - Verlust → Strategie wird bestraft
    - Lernrate nimmt über Zeit ab (Exploration → Exploitation)
    """

    STRAT_NAMES = [
        "Trend Following", "Momentum", "Mean Reversion",
        "Breakout", "Volume", "News Sentiment", "Volatility"
    ]

    def __init__(self):
        # Startgewichte
        self.weights = {
            "Trend Following": 0.15,
            "Momentum":        0.20,
            "Mean Reversion":  0.15,
            "Breakout":        0.15,
            "Volume":          0.10,
            "News Sentiment":  0.15,
            "Volatility":      0.10,
        }
        self.base_weights = dict(self.weights)  # unveränderter Ausgangspunkt

        self.learning_rate   = 0.08   # Lernrate (nimmt ab)
        self.lr_decay        = 0.995  # Decay pro Trade
        self.min_lr          = 0.005
        self.trade_count     = 0
        self.correct_signals = 0      # Score-Richtung = P&L-Richtung
        self.history: List[dict] = [] # Lernhistorie

        # Performance-Tracking pro Strategie
        self.strat_wins  = {s: 0 for s in self.STRAT_NAMES}
        self.strat_total = {s: 0 for s in self.STRAT_NAMES}

    def update(self, dominant_strat: str, strat_scores: dict, pnl: float, signal_score: float):
        """
        Nach jedem SELL-Trade das Modell anpassen.
        dominant_strat: welche Strategie den stärksten Einfluss hatte
        strat_scores:   alle Strategie-Scores zur Trade-Zeit
        pnl:            realisierter Gewinn/Verlust in €
        signal_score:   der Composite Score bei Kauf
        """
        self.trade_count += 1
        reward = math.tanh(pnl / 100)  # normalisierter Reward: [-1, 1]
        lr = max(self.min_lr, self.learning_rate * (self.lr_decay ** self.trade_count))

        # Prediction Accuracy
        if (signal_score > 0 and pnl > 0) or (signal_score < 0 and pnl < 0):
            self.correct_signals += 1

        # Gewichte anpassen
        for strat, score in strat_scores.items():
            if strat not in self.weights:
                continue
            # Einfluss dieser Strategie auf das Signal
            influence = abs(score) * self.weights[strat]
            # Belohnung proportional zum Einfluss
            delta = lr * reward * influence
            self.weights[strat] = max(0.02, min(0.50, self.weights[strat] + delta))
            self.strat_total[strat] += 1
            if pnl > 0:
                self.strat_wins[strat] += 1

        # Gewichte normalisieren (Summe = 1)
        total = sum(self.weights.values())
        if total > 0:
            for k in self.weights:
                self.weights[k] = round(self.weights[k] / total, 4)

        # In DB loggen
        accuracy = self.correct_signals / self.trade_count if self.trade_count else 0
        win_rate = self.get_win_rate()
        db_exec(
            "INSERT INTO learning_log (ts,weights,accuracy,total_trades,win_rate,note) VALUES (?,?,?,?,?,?)",
            (datetime.now().isoformat(), json.dumps(self.weights), round(accuracy,4),
             self.trade_count, round(win_rate,4), f"LR={lr:.4f} reward={reward:.3f}")
        )
        self.history.append({
            "trade": self.trade_count,
            "lr": round(lr, 5),
            "reward": round(reward, 3),
            "accuracy": round(accuracy, 3),
            "weights": dict(self.weights),
        })
        if len(self.history) > 500:
            self.history.pop(0)

        log.info(f"🧠 Learn: #{self.trade_count} reward={reward:+.3f} LR={lr:.4f} "
                 f"acc={accuracy:.1%} dominant={dominant_strat}")

    def get_strat_winrates(self) -> dict:
        return {
            s: round(self.strat_wins[s] / max(self.strat_total[s], 1) * 100, 1)
            for s in self.STRAT_NAMES
        }

    def get_win_rate(self) -> float:
        c = sqlite3.connect("algotrader.db")
        row = c.execute("SELECT COUNT(*) FROM trades WHERE side='SELL'").fetchone()
        total = row[0] if row else 0
        row2 = c.execute("SELECT COUNT(*) FROM trades WHERE side='SELL' AND pnl>0").fetchone()
        wins = row2[0] if row2 else 0
        c.close()
        return wins / max(total, 1)

    def get_accuracy(self) -> float:
        return self.correct_signals / max(self.trade_count, 1)

    def to_dict(self) -> dict:
        return {
            "weights":      self.weights,
            "base_weights": self.base_weights,
            "lr":           round(max(self.min_lr, self.learning_rate * (self.lr_decay ** self.trade_count)), 5),
            "trade_count":  self.trade_count,
            "accuracy":     round(self.get_accuracy(), 3),
            "strat_winrates": self.get_strat_winrates(),
        }


# ══════════════════════════════════════════════════════
# INDIKATOREN
# ══════════════════════════════════════════════════════

def clp(v, a=-1.0, b=1.0): return max(a, min(b, v))

def sma(a, n):
    if not a or len(a) < n: return None
    return sum(a[-n:]) / n

def ema(a, n):
    if not a or len(a) < n: return None
    k = 2/(n+1); v = sum(a[:n])/n
    for x in a[n:]: v = x*k + v*(1-k)
    return v

def ema_ser(a, n):
    if not a or len(a) < n: return []
    k = 2/(n+1); v = sum(a[:n])/n
    out = [None]*(n-1) + [v]
    for x in a[n:]:
        v = x*k + v*(1-k); out.append(v)
    return out

def rsi(a, n=14):
    if not a or len(a) < n+1: return 50.0
    d = [a[i]-a[i-1] for i in range(-n, 0)]
    g = sum(x for x in d if x>0)/n
    l = sum(-x for x in d if x<0)/n
    return 100.0 if l==0 else 100-(100/(1+g/l))

def macd_hist(a):
    e12 = ema_ser(a, 12); e26 = ema_ser(a, 26)
    line = [e12[i]-e26[i] if e12[i] and e26[i] else None for i in range(len(a))]
    vals = [v for v in line if v is not None]
    sig  = ema(vals, 9) if len(vals) >= 9 else None
    return round(vals[-1]-sig, 5) if sig and vals else None

def bollinger(a, n=20):
    if not a or len(a)<n: return 0.5, None, None
    w   = a[-n:]; mid = sum(w)/n
    std = math.sqrt(sum((x-mid)**2 for x in w)/(n-1))
    u, l = mid+2*std, mid-2*std
    return clp((a[-1]-l)/(u-l) if u!=l else 0.5, 0, 1), round(u,3), round(l,3)

def atr(h, l, c, n=14):
    if len(c)<n+1: return None
    tr = [max(h[i]-l[i], abs(h[i]-c[i-1]), abs(l[i]-c[i-1])) for i in range(-n,0)]
    return sum(tr)/n

# ══════════════════════════════════════════════════════
# 7 STRATEGIEN
# ══════════════════════════════════════════════════════

def s_trend(closes):
    m50=sma(closes,50); m200=sma(closes,200)
    e12=ema(closes,12); e26=ema(closes,26)
    sc = 0.0
    if m50 and m200:
        cr = (m50-m200)/m200
        sc += min(cr*20,.8) if cr>0 else max(cr*20,-.8)
    if e12 and e26: sc += .2 if e12>e26 else -.2
    if len(closes)>=5: sc += .1 if closes[-1]>closes[-5] else -.1
    return clp(sc), f"MA50={m50:.2f}" if m50 else "n/a"

def s_momentum(closes):
    r = rsi(closes); m = macd_hist(closes)
    sc = .9 if r<25 else .6 if r<30 else .25 if r<40 else -.9 if r>75 else -.6 if r>70 else -.25 if r>60 else 0
    if m is not None: sc += .4 if m>0 else -.4
    return clp(sc), f"RSI={r:.1f} MACD={'↑' if m and m>0 else '↓'}"

def s_mean_rev(closes):
    pctb, u, l = bollinger(closes)
    sc = 1 if pctb<.05 else .75 if pctb<.15 else .4 if pctb<.3 else -1 if pctb>.95 else -.75 if pctb>.85 else -.4 if pctb>.7 else 0
    return clp(sc), f"BB%b={pctb*100:.0f}% U={u}"

def s_breakout(closes):
    if len(closes)<20: return 0.0, "n/a"
    hh=max(closes[-20:]); ll=min(closes[-20:])
    pv=(hh+ll+closes[-1])/3
    r1=2*pv-ll; s1=2*pv-hh
    sc = .6 if closes[-1]>r1 else -.6 if closes[-1]<s1 else 0
    return clp(sc), f"R1={r1:.2f} S1={s1:.2f}"

def s_volume(vol, avg_vol, price_dir):
    spike = 1.0 if vol>avg_vol*2 else .5 if vol>avg_vol*1.5 else 0
    return clp(spike*price_dir*.7), f"Vol:{vol/1e6:.1f}M Spike:{'JA' if spike else 'nein'}"

def s_sentiment(sent_score):
    return clp(sent_score), f"{'BULLISH' if sent_score>.15 else 'BEARISH' if sent_score<-.15 else 'NEUTRAL'}"

def s_volatility(closes):
    if len(closes)<15: return 0.0, "n/a"
    rv = sum(abs(closes[i]-closes[i-1]) for i in range(-5,0))/4
    ov = sum(abs(closes[i]-closes[i-1]) for i in range(-15,-5))/9
    exp = rv/ov if ov>0 else 1
    trend = 1 if len(closes)>=5 and closes[-1]>closes[-5] else -1
    sc = .5*trend if exp>1.5 else .25*trend if exp>1.2 else 0
    return clp(sc), f"Exp={exp:.2f}"

def composite(closes, vol, avg_vol, sentiment, weights):
    price_dir = 1 if len(closes)>=2 and closes[-1]>closes[-2] else -1
    scores = {}
    details = {}
    fns = {
        "Trend Following": lambda: s_trend(closes),
        "Momentum":        lambda: s_momentum(closes),
        "Mean Reversion":  lambda: s_mean_rev(closes),
        "Breakout":        lambda: s_breakout(closes),
        "Volume":          lambda: s_volume(vol, avg_vol, price_dir),
        "News Sentiment":  lambda: s_sentiment(sentiment),
        "Volatility":      lambda: s_volatility(closes),
    }
    for name, fn in fns.items():
        sc, detail = fn()
        scores[name] = round(sc, 4)
        details[name] = detail

    comp = clp(sum(scores[n]*weights.get(n, 0) for n in scores))
    dominant = max(scores, key=lambda k: abs(scores[k]))
    return round(comp, 4), scores, details, dominant


# ══════════════════════════════════════════════════════
# TRADING ENGINE
# ══════════════════════════════════════════════════════

class Engine:
    def __init__(self):
        self.learner    = StrategyLearner()
        self.symbols    = ["AAPL", "TSLA", "MSFT"]
        self.cash       = IC
        self.pos        = {}       # {sym: {qty, avg, buy_score, buy_strat_scores}}
        self.trades     = []
        self.eq_curve   = []
        self.sentiment  = {}
        self.closes     = {}       # {sym: [float]}
        self.highs      = {}
        self.lows       = {}
        self.prices     = {}       # {sym: {price, pct, high, low, vol, src}}
        self.avg_vol    = {}       # rolling avg volume
        self.sig_map    = {}
        self.tick_count = 0
        self.ws_ticks   = 0
        self.rest_polls = 0
        self.params     = {
            "buyThr":0.20, "sellThr":-0.15,
            "riskPct":0.12, "stopLoss":0.05, "takeProfit":0.10
        }

    def pos_val(self):
        return sum(p["qty"]*(self.prices.get(sym,{}).get("price",0))
                   for sym,p in self.pos.items() if p["qty"]>0)

    def total(self): return self.cash + self.pos_val()

    def process_price(self, sym, price, vol=0, src="rest"):
        """Neuen Preis verarbeiten → Indikatoren → Bot-Entscheidung."""
        if sym not in self.closes: self.closes[sym] = []
        self.closes[sym].append(price)
        if len(self.closes[sym]) > 600: self.closes[sym].pop(0)

        prev = self.prices.get(sym, {})
        prev_close = prev.get("prev_close", price)
        self.prices[sym] = {
            "price":      round(price, 4),
            "change":     round(price - prev_close, 4),
            "pct":        round((price-prev_close)/prev_close*100, 3) if prev_close else 0,
            "high":       max(prev.get("high", price), price),
            "low":        min(prev.get("low",  price), price),
            "open":       prev.get("open", price),
            "prev_close": prev.get("prev_close", price),
            "vol":        prev.get("vol", 0) + vol,
            "src":        src,
        }

        # Rolling avg volume
        avol = self.avg_vol.get(sym, vol or 1e6)
        self.avg_vol[sym] = avol * 0.98 + (vol or avol) * 0.02

        if len(self.closes[sym]) < 20: return

        # Composite berechnen
        comp, scores, details, dominant = composite(
            self.closes[sym], self.prices[sym]["vol"],
            self.avg_vol[sym], self.sentiment.get(sym, 0),
            self.learner.weights
        )
        self.sig_map[sym] = {
            "composite": comp, "scores": scores,
            "details": details, "dominant": dominant,
            "signal": "BUY" if comp>self.params["buyThr"] else "SELL" if comp<self.params["sellThr"] else "HOLD"
        }

        # Bot-Entscheidung
        pos = self.pos.get(sym, {"qty":0,"avg":0})
        if pos["qty"] > 0:
            chg = (price - pos["avg"]) / pos["avg"]
            if chg <= -self.params["stopLoss"]:
                self._sell(sym, price, comp, scores, dominant, "Stop Loss")
            elif chg >= self.params["takeProfit"]:
                self._sell(sym, price, comp, scores, dominant, "Take Profit")
            elif comp < self.params["sellThr"]:
                self._sell(sym, price, comp, scores, dominant, dominant)
        else:
            if comp > self.params["buyThr"]:
                self._buy(sym, price, comp, scores, dominant)

        # Sentiment leicht driften
        if random.random() < 0.02:
            self.sentiment[sym] = clp(
                self.sentiment.get(sym,0)*0.88 + random.uniform(-.25,.25)
            )

        # Equity Snapshot
        self.tick_count += 1
        if self.tick_count % 20 == 0:
            tv = self.total()
            self.eq_curve.append({"t": int(time.time()*1000), "v": round(tv,2)})
            if len(self.eq_curve) > 500: self.eq_curve.pop(0)
            db_exec(
                "INSERT INTO equity_curve (ts,value,cash,pnl) VALUES (?,?,?,?)",
                (datetime.now().isoformat(), round(tv,2), round(self.cash,2), round(tv-IC,2))
            )

    def _buy(self, sym, price, comp, scores, dominant, reason=None):
        tv    = self.total()
        alloc = min(self.cash * self.params["riskPct"], tv * 0.33)
        if alloc < 5: return
        qty = alloc / price
        self.cash -= qty * price
        if sym not in self.pos: self.pos[sym] = {"qty":0,"avg":0}
        pos = self.pos[sym]
        nq  = pos["qty"] + qty
        pos["avg"] = (pos["avg"]*pos["qty"] + price*qty) / nq
        pos["qty"] = nq
        pos["buy_score"]       = comp
        pos["buy_strat_scores"] = scores
        t = {
            "ts": datetime.now().isoformat(), "sym": sym, "side": "BUY",
            "strategy": dominant, "price": round(price,4),
            "qty": round(qty,5), "val": round(qty*price,2),
            "pnl": 0, "score": round(comp,4),
            "src": self.prices[sym].get("src","?"),
            "dominant_strat": dominant, "strat_scores": json.dumps(scores),
            "cash_after": round(self.cash,2),
        }
        self.trades.insert(0, t)
        if len(self.trades) > 300: self.trades.pop()
        db_exec(
            "INSERT INTO trades (ts,sym,side,strategy,price,qty,value,pnl,score,cash_after,dominant_strat,strat_scores) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (t["ts"],t["sym"],t["side"],t["strategy"],t["price"],t["qty"],t["val"],t["pnl"],t["score"],t["cash_after"],t["dominant_strat"],t["strat_scores"])
        )
        log.info(f"  BUY  {sym} @${price:.2f} qty={qty:.4f} score={comp:+.3f} [{dominant}]")

    def _sell(self, sym, price, comp, scores, dominant, reason):
        pos = self.pos.get(sym)
        if not pos or pos["qty"] <= 0: return
        qty = pos["qty"]; pnl = (price - pos["avg"]) * qty
        self.cash += qty * price

        # 🧠 KI lernt aus dem Trade
        buy_scores = pos.get("buy_strat_scores", scores)
        buy_score  = pos.get("buy_score", comp)
        self.learner.update(dominant, buy_scores, pnl, buy_score)

        self.pos[sym] = {"qty":0,"avg":0}
        t = {
            "ts": datetime.now().isoformat(), "sym": sym, "side": "SELL",
            "strategy": reason, "price": round(price,4),
            "qty": round(qty,5), "val": round(qty*price,2),
            "pnl": round(pnl,2), "score": round(comp,4),
            "src": self.prices[sym].get("src","?"),
            "dominant_strat": dominant, "strat_scores": json.dumps(scores),
            "cash_after": round(self.cash,2),
        }
        self.trades.insert(0, t)
        if len(self.trades) > 300: self.trades.pop()
        db_exec(
            "INSERT INTO trades (ts,sym,side,strategy,price,qty,value,pnl,score,cash_after,dominant_strat,strat_scores) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (t["ts"],t["sym"],t["side"],t["strategy"],t["price"],t["qty"],t["val"],t["pnl"],t["score"],t["cash_after"],t["dominant_strat"],t["strat_scores"])
        )
        emoji = "🟢" if pnl>=0 else "🔴"
        log.info(f"  SELL {sym} @${price:.2f} P&L={pnl:+.2f}€ {emoji} [{reason}]")

    def get_portfolio(self):
        tv  = self.total(); pnl = tv - IC
        closed = [t for t in self.trades if t["side"]=="SELL"]
        wins   = [t for t in closed if t["pnl"]>0]
        return {
            "total_value": round(tv,2), "cash": round(self.cash,2),
            "pnl": round(pnl,2), "pnl_pct": round(pnl/IC*100,2),
            "win_rate": round(len(wins)/max(len(closed),1)*100,1),
            "total_trades": len(self.trades),
            "positions": [
                {"sym":sym, "qty":round(p["qty"],5), "avg":round(p["avg"],4),
                 "price":round(self.prices.get(sym,{}).get("price",0),4),
                 "pnl":round((self.prices.get(sym,{}).get("price",0)-p["avg"])*p["qty"],2),
                 "pnl_pct":round((self.prices.get(sym,{}).get("price",0)-p["avg"])/max(p["avg"],0.01)*100,2)}
                for sym,p in self.pos.items() if p["qty"]>0
            ],
        }

    def get_analytics(self):
        closed   = [t for t in self.trades if t["side"]=="SELL"]
        wins     = [t for t in closed if t["pnl"]>0]
        losses   = [t for t in closed if t["pnl"]<=0]
        tp       = sum(t["pnl"] for t in closed)
        aw       = sum(t["pnl"] for t in wins)/max(len(wins),1)
        al       = abs(sum(t["pnl"] for t in losses)/max(len(losses),1))
        tv       = self.total()
        peak     = max((e["v"] for e in self.eq_curve), default=IC)
        acc      = self.learner.get_accuracy()
        return {
            "win_rate":     round(len(wins)/max(len(closed),1)*100,1),
            "total_pnl":    round(tp,2), "avg_win":round(aw,2), "avg_loss":round(al,2),
            "risk_reward":  round(aw/max(al,0.01),2),
            "max_dd":       round((peak-tv)/max(peak,1)*100,2),
            "accuracy":     round(acc*100,1),
            "total":        len(self.trades), "closed":len(closed),
            "return_pct":   round((tv-IC)/IC*100,2),
            "ws_ticks":     self.ws_ticks, "rest_polls": self.rest_polls,
        }


# ══════════════════════════════════════════════════════
# FINNHUB PROVIDER
# ══════════════════════════════════════════════════════

class FinnhubProvider:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.ws     = None
        self.client = None

    async def fetch_quote(self, sym: str) -> dict | None:
        if not HTTPX_OK: return None
        try:
            async with httpx.AsyncClient(timeout=8) as c:
                r = await c.get(f"https://finnhub.io/api/v1/quote?symbol={sym}&token={FINNHUB_KEY}")
                d = r.json()
                if d.get("c",0) == 0: return None
                return {"price":d["c"],"pct":d.get("dp",0),"high":d.get("h",d["c"]),"low":d.get("l",d["c"]),"open":d.get("o",d["c"]),"prev_close":d.get("pc",d["c"])}
        except Exception as e:
            log.warning(f"Quote {sym}: {e}")
            return None

    async def fetch_candles(self, sym: str) -> list | None:
        if not HTTPX_OK: return None
        to   = int(time.time())
        frm  = to - 30*24*3600
        try:
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(f"https://finnhub.io/api/v1/stock/candle?symbol={sym}&resolution=60&from={frm}&to={to}&token={FINNHUB_KEY}")
                d = r.json()
                if d.get("s") != "ok" or not d.get("c"): return None
                log.info(f"✅ {sym}: {len(d['c'])} Candles geladen")
                return d["c"]
        except Exception as e:
            log.warning(f"Candles {sym}: {e}")
            return None

    async def init_symbol(self, sym: str):
        self.engine.sentiment[sym] = 0.0
        candles = await self.fetch_candles(sym)
        if candles:
            self.engine.closes[sym] = list(candles)
        quote = await self.fetch_quote(sym)
        if quote:
            self.engine.prices[sym] = {**quote, "vol":0, "src":"rest", "change":0}
            if sym not in self.engine.closes:
                self.engine.closes[sym] = []
            self.engine.closes[sym].append(quote["price"])
            log.info(f"✅ {sym}: ${quote['price']:.2f} ({quote['pct']:+.2f}%)")
        return bool(quote)

    async def rest_poll(self):
        """Alle 15s echte Quotes holen."""
        for sym in self.engine.symbols:
            q = await self.fetch_quote(sym)
            if q:
                self.engine.process_price(sym, q["price"], 0, "rest")
                old = self.engine.prices[sym]
                self.engine.prices[sym].update({
                    "high": max(old.get("high",q["price"]), q["high"]),
                    "low":  min(old.get("low", q["price"]), q["low"]),
                    "pct":  q["pct"], "prev_close": q["prev_close"],
                })
        self.engine.rest_polls += 1

    async def run_ws(self):
        """Finnhub WebSocket für Echtzeit-Trade-Daten."""
        import websockets
        uri = f"wss://ws.finnhub.io?token={FINNHUB_KEY}"
        while True:
            try:
                log.info("WS: Verbinde…")
                async with websockets.connect(uri, ping_interval=20) as ws:
                    self.ws = ws
                    # Symbole subscriben
                    for sym in self.engine.symbols:
                        await ws.send(json.dumps({"type":"subscribe","symbol":sym}))
                    log.info("✅ Finnhub WS verbunden")
                    async for msg in ws:
                        try:
                            d = json.loads(msg)
                            if d.get("type") == "trade" and d.get("data"):
                                for trade in d["data"]:
                                    sym   = trade["s"]
                                    price = trade["p"]
                                    vol   = trade.get("v", 0)
                                    if sym in self.engine.symbols:
                                        self.engine.process_price(sym, price, vol, "ws")
                                        self.engine.ws_ticks += 1
                        except Exception:
                            pass
            except Exception as e:
                log.warning(f"WS Fehler: {e} — Retry in 5s")
                await asyncio.sleep(5)


# ══════════════════════════════════════════════════════
# FASTAPI APP
# ══════════════════════════════════════════════════════

engine   = Engine()
provider = FinnhubProvider(engine)
clients: List[WebSocket] = []

async def broadcast(data: dict):
    dead = []
    msg  = json.dumps(data, default=str)
    for ws in clients:
        try: await ws.send_text(msg)
        except: dead.append(ws)
    for ws in dead:
        try: clients.remove(ws)
        except: pass

async def main_loop():
    log.info("Main Loop gestartet")
    tick = 0
    while True:
        try:
            tick += 1
            payload = {
                "type":      "tick",
                "portfolio": engine.get_portfolio(),
                "prices":    engine.prices,
                "signals":   engine.sig_map,
                "learner":   engine.learner.to_dict(),
                "new_trades":engine.trades[:3],
                "ws_ticks":  engine.ws_ticks,
                "rest_polls":engine.rest_polls,
            }
            if tick % 5 == 0:
                payload["analytics"]    = engine.get_analytics()
                payload["eq_curve"]     = engine.eq_curve[-100:]
                payload["learn_history"]= engine.learner.history[-50:]
                payload["charts"]       = {sym: engine.closes[sym][-120:] for sym in engine.symbols if sym in engine.closes}
            await broadcast(payload)
        except Exception as e:
            log.error(f"Loop: {e}")
        await asyncio.sleep(3)

async def rest_poll_loop():
    while True:
        await asyncio.sleep(15)
        try:
            await provider.rest_poll()
        except Exception as e:
            log.warning(f"REST Poll: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    log.info("Initialisiere Symbole…")
    for sym in engine.symbols:
        await provider.init_symbol(sym)
    log.info("✅ Engine bereit")
    t1 = asyncio.create_task(main_loop())
    t2 = asyncio.create_task(rest_poll_loop())
    t3 = asyncio.create_task(provider.run_ws())
    yield
    t1.cancel(); t2.cancel(); t3.cancel()

app = FastAPI(title="AlgoTrader Pro", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
async def root():
    index = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return {"status": "AlgoTrader Pro API"}

@app.get("/api/portfolio")  
def api_portfolio(): return engine.get_portfolio()

@app.get("/api/analytics")
def api_analytics(): return engine.get_analytics()

@app.get("/api/signals")
def api_signals(): return engine.sig_map

@app.get("/api/trades")
def api_trades(limit:int=50): return engine.trades[:limit]

@app.get("/api/learner")
def api_learner(): return engine.learner.to_dict()

@app.get("/api/equity")
def api_equity(): return engine.eq_curve[-200:]

@app.get("/api/charts/{sym}")
def api_chart(sym:str): return engine.closes.get(sym.upper(),[])[-120:]

@app.post("/api/reset")
def api_reset():
    engine.cash=IC; engine.pos={}; engine.trades=[]; engine.eq_curve=[]
    return {"status":"ok"}

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    log.info(f"Client verbunden ({len(clients)} gesamt)")
    try:
        await ws.send_text(json.dumps({
            "type":"init",
            "portfolio": engine.get_portfolio(),
            "prices":    engine.prices,
            "signals":   engine.sig_map,
            "learner":   engine.learner.to_dict(),
            "analytics": engine.get_analytics(),
            "eq_curve":  engine.eq_curve[-100:],
            "charts":    {s:engine.closes.get(s,[])[-120:] for s in engine.symbols},
            "trades":    engine.trades[:30],
            "symbols":   engine.symbols,
        }, default=str))
        while True:
            msg = await ws.receive_text()
            try:
                d = json.loads(msg)
                if d["type"] == "set_symbols":
                    new = [s.upper() for s in d["symbols"][:5]]
                    for sym in new:
                        if sym not in engine.symbols:
                            engine.symbols.append(sym)
                            await provider.init_symbol(sym)
                    engine.symbols = new
                elif d["type"] == "set_param":
                    if d["key"] in engine.params:
                        engine.params[d["key"]] = float(d["value"])
                elif d["type"] == "reset":
                    engine.cash=IC; engine.pos={}; engine.trades=[]; engine.eq_curve=[]
            except Exception:
                pass
    except WebSocketDisconnect:
        try: clients.remove(ws)
        except: pass
        log.info(f"Client getrennt ({len(clients)} verbleibend)")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
