<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AlgoTrader Pro</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;700&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
:root{
  --ink:#0a0c0f;--ink2:#12161c;--ink3:#1a2030;--ink4:#242d3d;
  --gold:#c8a96e;--gold2:#e8c878;--gold3:#f5dfa0;--gdim:rgba(200,169,110,.12);
  --gr:#2dd88a;--re:#e85555;--am:#e8a832;--bl:#4488ee;
  --text:#e8e4dc;--dim:#6a7a8a;--d2:#3a4a5a;
  --br:rgba(200,169,110,.12);--br2:rgba(200,169,110,.25);--br3:rgba(200,169,110,.4);
  --fn:'DM Sans',sans-serif;--se:'Instrument Serif',serif;--mo:'IBM Plex Mono',monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:var(--ink);color:var(--text);font-family:var(--fn);font-size:12px;-webkit-font-smoothing:antialiased}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse 70% 60% at 5% 0,rgba(200,169,110,.04),transparent 50%),radial-gradient(ellipse 50% 40% at 95% 100%,rgba(45,216,138,.025),transparent 50%);pointer-events:none;z-index:0}
body::after{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(200,169,110,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(200,169,110,.018) 1px,transparent 1px);background-size:48px 48px;pointer-events:none;z-index:0}
::-webkit-scrollbar{width:3px}::-webkit-scrollbar-thumb{background:var(--ink4);border-radius:3px}

/* HEADER */
.hdr{display:flex;align-items:center;gap:12px;padding:0 20px;height:54px;background:rgba(10,12,15,.94);border-bottom:1px solid var(--br);position:sticky;top:0;z-index:300;backdrop-filter:blur(24px);flex-wrap:wrap}
.logo{display:flex;align-items:center;gap:10px;flex-shrink:0}
.logo-mark{width:28px;height:28px;border:1.5px solid var(--gold);border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:14px;box-shadow:0 0 18px rgba(200,169,110,.2),inset 0 0 8px rgba(200,169,110,.05)}
.logo-name{font-family:var(--se);font-size:17px;color:var(--text)}
.logo-name span{color:var(--gold);font-style:italic}
.logo-sub{font-family:var(--mo);font-size:8px;color:var(--dim);letter-spacing:2px;text-transform:uppercase}

.dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.d-live{background:var(--gr);box-shadow:0 0 8px var(--gr);animation:pulse 1.8s ease-in-out infinite}
.d-wait{background:var(--am);animation:pulse .9s ease-in-out infinite}
.d-err{background:var(--re)}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.35;transform:scale(.7)}}

.pill{display:inline-flex;align-items:center;gap:5px;padding:3px 10px;border-radius:3px;font-size:9px;font-family:var(--mo);border:1px solid;letter-spacing:.4px}
.pg{background:rgba(45,216,138,.07);border-color:rgba(45,216,138,.25);color:var(--gr)}
.pa{background:var(--gdim);border-color:var(--br2);color:var(--gold)}
.pr{background:rgba(232,85,85,.07);border-color:rgba(232,85,85,.25);color:var(--re)}
.pam{background:rgba(232,168,50,.07);border-color:rgba(232,168,50,.25);color:var(--am)}
.pdim{background:rgba(58,74,90,.12);border-color:rgba(58,74,90,.3);color:var(--dim)}

.ticker{flex:1;overflow:hidden;display:flex;align-items:center;gap:8px;mask-image:linear-gradient(to right,transparent,#000 6%,#000 94%,transparent)}
.tick{display:flex;align-items:center;gap:5px;padding:3px 10px;border-radius:3px;background:var(--ink2);border:1px solid var(--br);font-family:var(--mo);font-size:10px;white-space:nowrap;flex-shrink:0}

.tabs{display:flex;background:var(--ink2);border:1px solid var(--br);border-radius:4px;overflow:hidden;margin:0 4px}
.tab{background:none;border:none;cursor:pointer;color:var(--dim);font-size:10px;padding:5px 14px;font-weight:500;font-family:var(--fn);transition:all .2s;border-right:1px solid var(--br)}
.tab:last-child{border-right:none}
.tab:hover{color:var(--text);background:var(--ink3)}
.tab.on{color:var(--gold);background:var(--gdim)}

.hctrl{margin-left:auto;display:flex;gap:8px;align-items:center}
.btn{padding:5px 13px;border-radius:3px;font-size:10px;font-weight:500;cursor:pointer;border:1px solid;transition:all .2s;font-family:var(--fn)}
.btn-g{background:var(--gdim);border-color:var(--br2);color:var(--gold)}.btn-g:hover{background:rgba(200,169,110,.18)}
.btn-r{background:rgba(232,85,85,.08);border-color:rgba(232,85,85,.25);color:var(--re)}

/* LAYOUT */
.body{display:grid;grid-template-columns:210px 1fr 240px;height:calc(100vh - 54px);position:relative;z-index:1}
.sb,.rb{overflow-y:auto;padding:14px 12px;background:var(--ink2)}
.sb{border-right:1px solid var(--br)}.rb{border-left:1px solid var(--br)}
.center{overflow-y:auto;padding:16px 20px;background:var(--ink)}

/* SIDEBAR */
.slbl{font-size:8px;text-transform:uppercase;letter-spacing:2px;color:var(--d2);font-weight:600;margin:12px 0 6px;font-family:var(--mo)}
.scard{background:var(--ink);border:1px solid var(--br);border-radius:4px;padding:10px 12px;margin-bottom:5px;position:relative;overflow:hidden}
.scard::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(to right,transparent,var(--gold),transparent);opacity:.18}
.sc-l{font-size:8px;color:var(--dim);margin-bottom:2px;font-family:var(--mo);text-transform:uppercase;letter-spacing:1px}
.sc-v{font-size:21px;font-weight:300;font-family:var(--mo);line-height:1;letter-spacing:-1px}
.sc-s{font-size:9px;color:var(--dim);margin-top:2px;font-family:var(--mo)}
.sep{height:1px;background:linear-gradient(to right,transparent,var(--br2),transparent);margin:10px 0}
.pos-it{background:var(--ink);border:1px solid var(--br);border-left:2px solid;border-radius:3px;padding:8px 10px;margin-bottom:4px}
.str-row{display:flex;align-items:center;gap:5px;padding:3px 0}
.str-nm{font-size:9px;color:var(--dim);flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-family:var(--mo)}
.str-tr{flex:2;height:2px;background:var(--ink3);border-radius:1px;overflow:hidden}
.str-fi{height:100%;border-radius:1px;transition:width .6s}
.str-vl{font-size:9px;font-family:var(--mo);width:30px;text-align:right;font-weight:700}
.fh-panel{background:var(--ink);border:1px solid var(--br2);border-radius:4px;padding:11px;margin-bottom:9px}
.fh-t{font-size:8px;font-weight:600;color:var(--gold);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:7px;font-family:var(--mo);display:flex;align-items:center;gap:6px}
.fh-r{display:flex;justify-content:space-between;font-size:9px;color:var(--dim);margin-bottom:3px;font-family:var(--mo)}
.fh-r span:last-child{color:var(--text)}
.ai-panel{background:linear-gradient(135deg,rgba(45,216,138,.04),rgba(200,169,110,.04));border:1px solid rgba(45,216,138,.15);border-radius:4px;padding:11px;margin-bottom:9px}
.ai-t{font-size:8px;font-weight:600;color:var(--gr);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:7px;font-family:var(--mo);display:flex;align-items:center;gap:6px}
.ai-r{display:flex;justify-content:space-between;font-size:9px;color:var(--dim);margin-bottom:4px;font-family:var(--mo)}
.ai-r span:last-child{color:var(--text)}
.learn-bar{height:3px;background:var(--ink3);border-radius:2px;overflow:hidden;margin-top:4px}
.learn-fi{height:100%;background:linear-gradient(to right,var(--gr),var(--gold));border-radius:2px;transition:width .8s}

/* CENTER */
.sec{font-size:8px;text-transform:uppercase;letter-spacing:2px;color:var(--dim);font-weight:600;margin:2px 0 12px;display:flex;align-items:center;gap:8px;font-family:var(--mo)}
.sec::after{content:'';flex:1;height:1px;background:linear-gradient(to right,var(--br),transparent)}
.cscard{background:var(--ink2);border:1px solid var(--br);border-radius:6px;padding:14px;margin-bottom:8px;position:relative;overflow:hidden;transition:border-color .3s,box-shadow .3s}
.cscard:hover{border-color:var(--br2);box-shadow:0 4px 24px rgba(200,169,110,.04)}
.cscard::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(to right,transparent,var(--gold) 40%,transparent);opacity:.15}
.cs-hd{display:flex;align-items:center;gap:8px;margin-bottom:9px;flex-wrap:wrap}
.cs-bar{flex:1;height:4px;background:var(--ink3);border-radius:2px;overflow:hidden;position:relative}
.cs-mid{position:absolute;left:50%;top:0;width:1px;height:100%;background:rgba(255,255,255,.08)}
.cs-fi{height:100%;border-radius:2px;position:absolute;top:0;transition:all .5s}
.sig-b{font-size:11px;font-weight:700;padding:4px 14px;border-radius:3px;font-family:var(--mo);letter-spacing:1px;border:1px solid}
.sb-buy{background:rgba(45,216,138,.1);border-color:rgba(45,216,138,.3);color:var(--gr)}
.sb-sell{background:rgba(232,85,85,.1);border-color:rgba(232,85,85,.3);color:var(--re)}
.sb-hold{background:rgba(232,168,50,.08);border-color:rgba(232,168,50,.25);color:var(--am)}
.cgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:14px}
.cc{background:var(--ink2);border:1px solid var(--br);border-radius:6px;overflow:hidden;transition:border-color .3s}
.cc:hover{border-color:var(--br2)}
.cc-hd{display:flex;align-items:center;gap:6px;padding:10px 12px 0}
.cw{height:110px;padding:3px 7px 7px;position:relative}
.pills{display:flex;gap:3px;padding:4px 12px;flex-wrap:wrap}
.p2{font-size:8px;padding:1px 6px;border-radius:3px;border:1px solid;font-weight:500;font-family:var(--mo)}
.p2g{background:rgba(45,216,138,.07);border-color:rgba(45,216,138,.2);color:var(--gr)}
.p2r{background:rgba(232,85,85,.07);border-color:rgba(232,85,85,.2);color:var(--re)}
.p2n{background:rgba(58,74,90,.1);border-color:rgba(58,74,90,.25);color:var(--dim)}
.p2a{background:var(--gdim);border-color:var(--br2);color:var(--gold)}
.sc-row{display:flex;align-items:center;gap:6px;padding:0 12px 9px}
.sc-tr{flex:1;height:3px;background:var(--ink3);border-radius:2px;overflow:hidden;position:relative}
.sc-mid2{position:absolute;left:50%;top:0;width:1px;height:100%;background:rgba(255,255,255,.06)}
.sc-fi2{height:100%;border-radius:2px;position:absolute;top:0;transition:all .5s}
.tcard{background:var(--ink2);border:1px solid var(--br);border-radius:6px;overflow:hidden;margin-bottom:12px}
.tt{width:100%;border-collapse:collapse}
.tt th{padding:8px 10px;text-align:left;font-size:8px;text-transform:uppercase;letter-spacing:1px;color:var(--d2);background:var(--ink3);border-bottom:1px solid var(--br);font-weight:600;font-family:var(--mo);white-space:nowrap}
.tt td{padding:7px 10px;font-size:10px;border-bottom:1px solid rgba(200,169,110,.04);font-family:var(--mo)}
.tt tr:last-child td{border-bottom:none}
.tt tr:hover td{background:rgba(200,169,110,.015)}
.bdg{font-size:8px;font-weight:700;padding:2px 7px;border-radius:3px;font-family:var(--mo);letter-spacing:.4px}
.bdg-buy{background:rgba(45,216,138,.12);color:var(--gr);border:1px solid rgba(45,216,138,.2)}
.bdg-sell{background:rgba(232,85,85,.12);color:var(--re);border:1px solid rgba(232,85,85,.2)}
.bdg-src{background:rgba(68,136,238,.1);color:var(--bl);border:1px solid rgba(68,136,238,.2)}
.up{color:var(--gr);font-weight:700}.dn{color:var(--re);font-weight:700}
.an-g{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-bottom:12px}
.an-c{background:var(--ink2);border:1px solid var(--br);border-radius:4px;padding:11px;position:relative;overflow:hidden}
.an-c::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(to right,transparent,var(--gold),transparent);opacity:.1}
.an-l{font-size:8px;text-transform:uppercase;letter-spacing:1px;color:var(--d2);font-weight:600;margin-bottom:3px;font-family:var(--mo)}
.an-v{font-size:20px;font-weight:300;font-family:var(--mo);line-height:1;letter-spacing:-1px}
.an-s{font-size:9px;color:var(--dim);margin-top:3px;font-family:var(--mo)}
.an-ch{background:var(--ink2);border:1px solid var(--br);border-radius:6px;padding:14px;margin-bottom:10px}
.an-ch-t{font-size:8px;font-family:var(--mo);font-weight:600;margin-bottom:10px;color:var(--dim);text-transform:uppercase;letter-spacing:1.5px}
.ai-card{background:linear-gradient(135deg,rgba(45,216,138,.04),rgba(200,169,110,.04));border:1px solid rgba(45,216,138,.15);border-radius:6px;padding:16px;margin-bottom:12px}
.sb-card{background:var(--ink2);border:1px solid var(--br);border-radius:6px;padding:14px;margin-bottom:10px}
.sb-bar{height:3px;background:var(--ink3);border-radius:2px;overflow:hidden}
.sb-fi{height:100%;border-radius:2px;transition:width .6s}
.set-g{display:grid;grid-template-columns:1fr 1fr;gap:11px}
.set-c{background:var(--ink2);border:1px solid var(--br);border-radius:6px;padding:14px}
.set-t{font-size:9px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:11px;color:var(--gold);font-family:var(--mo)}
.p-row{display:grid;grid-template-columns:1fr 90px 42px;align-items:center;gap:6px;margin-bottom:8px;font-size:9px;color:var(--dim);font-family:var(--mo)}
.p-row input{background:var(--ink);border:1px solid var(--br2);color:var(--text);padding:5px 8px;border-radius:3px;font-family:var(--mo);font-size:10px;text-align:right;width:100%;outline:none;transition:border-color .2s}
.p-row input:focus{border-color:var(--gold)}
.s-btn{background:var(--gdim);border:1px solid var(--br2);color:var(--gold);padding:4px 9px;border-radius:3px;font-size:9px;cursor:pointer;font-weight:600;font-family:var(--mo)}
.chip{display:inline-flex;align-items:center;gap:4px;background:var(--gdim);border:1px solid var(--br2);color:var(--gold);padding:3px 9px;border-radius:3px;font-size:10px;font-weight:500;margin:2px;font-family:var(--mo)}
.chip button{background:none;border:none;color:var(--re);cursor:pointer;font-size:13px;line-height:1}
.dzone{border-color:rgba(232,85,85,.2)!important}.dzone .set-t{color:var(--re)}
.sym-add{display:flex;gap:5px;margin-top:8px}
.sym-add input{background:var(--ink);border:1px solid var(--br2);color:var(--text);padding:5px 8px;border-radius:3px;font-family:var(--mo);font-size:10px;width:80px;outline:none}
.sym-add input:focus{border-color:var(--gold)}
.ni{background:var(--ink2);border:1px solid var(--br);border-radius:4px;padding:9px;margin-bottom:5px;transition:border-color .2s}
.ni:hover{border-color:var(--br2)}
.ns{font-size:8px;font-weight:600;padding:1px 6px;border-radius:3px;font-family:var(--mo);letter-spacing:.4px}
.ns-p{background:rgba(45,216,138,.1);color:var(--gr)}.ns-n{background:rgba(232,85,85,.1);color:var(--re)}
.nh{font-size:10px;line-height:1.45;font-weight:500;margin-bottom:2px}
.nm{font-size:8px;color:var(--d2);font-family:var(--mo)}
.load-card{background:var(--ink2);border:1px solid var(--br);border-radius:6px;padding:32px;text-align:center;margin-bottom:10px}
.spin{font-size:28px;animation:spn 1.5s linear infinite;display:inline-block}
@keyframes spn{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
.empty{color:var(--d2);font-size:10px;padding:14px;text-align:center;font-family:var(--mo)}
.toast{position:fixed;bottom:20px;right:20px;padding:10px 16px;border-radius:4px;font-size:10px;font-weight:500;z-index:9999;border:1px solid;font-family:var(--mo);backdrop-filter:blur(20px);max-width:320px;letter-spacing:.3px}
.t-ok{background:rgba(45,216,138,.1);border-color:rgba(45,216,138,.3);color:var(--gr)}
.t-err{background:rgba(232,85,85,.1);border-color:rgba(232,85,85,.3);color:var(--re)}
.t-warn{background:rgba(232,168,50,.1);border-color:rgba(232,168,50,.3);color:var(--am)}
@keyframes fl-g{0%,100%{background:transparent}25%{background:rgba(45,216,138,.1)}}
@keyframes fl-r{0%,100%{background:transparent}25%{background:rgba(232,85,85,.1)}}
.fup{animation:fl-g .5s ease}.fdn{animation:fl-r .5s ease}
@keyframes wpop{0%{transform:scale(1)}50%{transform:scale(1.25)}100%{transform:scale(1)}}
.wpop{animation:wpop .4s ease}
.w-up{color:var(--gr);background:rgba(45,216,138,.1);padding:1px 5px;border-radius:2px;font-size:8px;font-family:var(--mo)}
.w-dn{color:var(--re);background:rgba(232,85,85,.1);padding:1px 5px;border-radius:2px;font-size:8px;font-family:var(--mo)}
.w-nm{color:var(--dim);font-size:8px;font-family:var(--mo)}
.slr-bar{height:3px;background:var(--ink3);border-radius:2px;overflow:hidden}
.slr-fi{height:100%;border-radius:2px;transition:width .8s}
@media(max-width:1100px){.body{grid-template-columns:190px 1fr 215px}}
@media(max-width:800px){.body{grid-template-columns:1fr}.sb,.rb{display:none}}
</style>
</head>
<body>
<div class="hdr">
  <div class="logo">
    <div class="logo-mark">⚡</div>
    <div>
      <div class="logo-name">Algo<span>Trader</span> Pro</div>
      <div class="logo-sub">Intelligence System</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:7px">
    <div class="pill pa"><div class="dot d-wait" id="dot-ws"></div><span id="ws-lbl">Verbinde…</span></div>
    <div class="pill pg"><div class="dot d-live"></div>KI Aktiv</div>
  </div>
  <div class="ticker" id="ticker"></div>
  <div class="tabs">
    <button class="tab on"  onclick="sw('dashboard',this)">Dashboard</button>
    <button class="tab"     onclick="sw('strategies',this)">Strategien</button>
    <button class="tab"     onclick="sw('ai',this)">KI-Lernen</button>
    <button class="tab"     onclick="sw('analytics',this)">Analytics</button>
    <button class="tab"     onclick="sw('settings',this)">Settings</button>
  </div>
  <div class="hctrl">
    <span style="font-size:9px;color:var(--dim);font-family:var(--mo)" id="upd">—</span>
    <button class="btn btn-g" onclick="reconnect()">↻</button>
  </div>
</div>

<div class="body">
<div class="sb">
  <div class="slbl">Portfolio</div>
  <div class="scard"><div class="sc-l">Total Value</div><div class="sc-v" id="s-total" style="color:var(--gold)">€—</div><div class="sc-s" id="s-pct">—</div></div>
  <div class="scard"><div class="sc-l">Cash</div><div class="sc-v" id="s-cash">€—</div><div class="sc-s" id="s-cashpct">—</div></div>
  <div class="scard"><div class="sc-l">P&amp;L</div><div class="sc-v" id="s-pnl">€—</div><div class="sc-s" id="s-tct">—</div></div>
  <div class="sep"></div>
  <div class="slbl">Positionen</div>
  <div id="pos-list"><div class="empty">Keine Positionen</div></div>
  <div class="sep"></div>
  <div class="slbl">KI-Gewichte</div>
  <div id="strat-sb"></div>
  <div class="sep"></div>
  <div class="fh-panel">
    <div class="fh-t"><div class="dot d-wait" id="dot-fh"></div>Finnhub</div>
    <div class="fh-r"><span>WebSocket</span><span id="fb-ws">—</span></div>
    <div class="fh-r"><span>WS Ticks</span><span id="fb-ticks">0</span></div>
    <div class="fh-r"><span>REST Updates</span><span id="fb-rest">0</span></div>
    <div class="fh-r"><span>Letzter Kurs</span><span id="fb-last">—</span></div>
    <div class="fh-r"><span>Markt</span><span id="fb-market">—</span></div>
  </div>
  <div class="ai-panel">
    <div class="ai-t">🧠 KI-Status</div>
    <div class="ai-r"><span>Lernrate</span><span id="ai-lr">—</span></div>
    <div class="ai-r"><span>Trades gelernt</span><span id="ai-tc">0</span></div>
    <div class="ai-r"><span>Genauigkeit</span><span id="ai-acc">—</span></div>
    <div style="margin-top:6px;font-size:8px;color:var(--d2);font-family:var(--mo);margin-bottom:3px">LERNFORTSCHRITT</div>
    <div class="learn-bar"><div class="learn-fi" id="ai-bar" style="width:0%"></div></div>
  </div>
</div>

<div class="center">
  <div id="tab-dashboard">
    <div class="sec">Echtzeit Composite Scores — Finnhub Live</div>
    <div id="composite-row"><div class="load-card"><div class="spin">📡</div><br><span style="font-size:11px;color:var(--dim);font-family:var(--mo)">Verbinde mit Backend…</span></div></div>
    <div class="sec">Live Charts</div>
    <div class="cgrid" id="charts-grid"></div>
    <div class="sec">Trade Protokoll</div>
    <div class="tcard"><div style="overflow-x:auto">
      <table class="tt">
        <thead><tr><th>Zeit</th><th>Symbol</th><th>Typ</th><th>Strategie</th><th>Preis</th><th>Qty</th><th>Wert</th><th>P&amp;L</th><th>Score</th><th>Src</th></tr></thead>
        <tbody id="trades-body"><tr><td colspan="10" class="empty">Warte auf Trade…</td></tr></tbody>
      </table>
    </div></div>
  </div>

  <div id="tab-strategies" style="display:none">
    <div class="sec">7-Strategie Analyse</div>
    <div id="strat-bd"></div>
  </div>

  <div id="tab-ai" style="display:none">
    <div class="sec">KI-Lernfunktion — Adaptives Gewichtungssystem</div>
    <div style="background:var(--ink2);border:1px solid rgba(45,216,138,.15);border-radius:6px;padding:18px;margin-bottom:12px">
      <div style="font-family:var(--se);font-size:17px;margin-bottom:10px;color:var(--text)">
        Wie der Bot <em style="color:var(--gr);font-style:normal">lernt</em>
      </div>
      <div style="font-size:11px;color:var(--dim);line-height:1.9;font-family:var(--fn)">
        Nach jedem abgeschlossenen Trade analysiert die KI welche Strategie den stärksten Einfluss hatte.<br>
        → <span style="color:var(--gr)">Gewinn</span>: Einflussreiche Strategien werden mit höherem Gewicht <strong>belohnt</strong><br>
        → <span style="color:var(--re)">Verlust</span>: Einflussreiche Strategien werden <strong>bestraft</strong> (Gewicht sinkt)<br>
        → Die <span style="color:var(--gold)">Lernrate</span> nimmt mit jedem Trade ab — Exploration → Exploitation
      </div>
    </div>
    <div class="ai-card">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">
        <div style="font-family:var(--se);font-size:15px;color:var(--text)">Strategie-Gewichte</div>
        <div class="pill pg" id="ai-tc2"><div class="dot d-live" style="width:5px;height:5px"></div>0 Trades</div>
      </div>
      <div style="display:grid;grid-template-columns:130px 1fr 60px 55px 55px;gap:0 8px;margin-bottom:6px">
        <div style="font-size:8px;color:var(--d2);font-family:var(--mo);padding:3px 0;border-bottom:1px solid var(--br);letter-spacing:.8px">STRATEGIE</div>
        <div style="font-size:8px;color:var(--d2);font-family:var(--mo);padding:3px 0;border-bottom:1px solid var(--br)">GEWICHT</div>
        <div style="font-size:8px;color:var(--d2);font-family:var(--mo);padding:3px 0;border-bottom:1px solid var(--br);text-align:right">AKTUELL</div>
        <div style="font-size:8px;color:var(--d2);font-family:var(--mo);padding:3px 0;border-bottom:1px solid var(--br);text-align:right">BASIS</div>
        <div style="font-size:8px;color:var(--d2);font-family:var(--mo);padding:3px 0;border-bottom:1px solid var(--br);text-align:right">DELTA</div>
      </div>
      <div id="ai-wtbl"></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
      <div class="an-ch"><div class="an-ch-t">Lernkurve (Accuracy über Trades)</div><div style="height:150px;position:relative"><canvas id="lrn-c"></canvas></div></div>
      <div class="an-ch"><div class="an-ch-t">Strategie Win-Rate</div><div style="height:150px;position:relative"><canvas id="wr-c"></canvas></div></div>
    </div>
  </div>

  <div id="tab-analytics" style="display:none">
    <div class="sec">Performance</div>
    <div class="an-g" id="an-m"></div>
    <div class="sec">Equity Kurve</div>
    <div class="an-ch"><div class="an-ch-t">Portfolio Value</div><div style="height:180px;position:relative"><canvas id="eq-c"></canvas></div></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
      <div class="an-ch"><div class="an-ch-t">P&amp;L nach Symbol</div><div style="height:130px;position:relative"><canvas id="sym-c"></canvas></div></div>
      <div class="an-ch"><div class="an-ch-t">Strategie Scores</div><div style="height:130px;position:relative"><canvas id="str-c"></canvas></div></div>
    </div>
  </div>

  <div id="tab-settings" style="display:none">
    <div class="sec">Konfiguration</div>
    <div class="set-g">
      <div class="set-c">
        <div class="set-t">Symbole (Finnhub)</div>
        <div id="sym-chips"></div>
        <div class="sym-add">
          <input id="sym-inp" placeholder="NVDA" maxlength="8" onkeydown="if(event.key==='Enter')addSym()">
          <button class="btn btn-g" onclick="addSym()">+ Add</button>
        </div>
        <p style="font-size:9px;color:var(--d2);margin-top:7px;font-family:var(--mo)">US-Aktien · Max 5</p>
      </div>
      <div class="set-c"><div class="set-t">Risk Management</div><div id="risk-params"></div></div>
      <div class="set-c">
        <div class="set-t">KI-Lernrate</div>
        <p style="font-size:9px;color:var(--dim);margin-bottom:10px;line-height:1.8;font-family:var(--mo)">Automatisch gesteuert. Sinkt mit jedem Trade.</p>
        <div style="font-size:9px;color:var(--dim);font-family:var(--mo);line-height:2.2">LR: <span id="s-lr" style="color:var(--gold)">—</span><br>Trades: <span id="s-tc" style="color:var(--gr)">0</span><br>Acc: <span id="s-ac" style="color:var(--text)">—</span></div>
      </div>
      <div class="set-c dzone">
        <div class="set-t">Danger Zone</div>
        <p style="font-size:9px;color:var(--dim);margin-bottom:12px;line-height:1.7;font-family:var(--mo)">Portfolio zurücksetzen. KI-Lernfortschritt bleibt erhalten.</p>
        <button class="btn btn-r" onclick="resetAll()">🗑 Reset</button>
      </div>
    </div>
  </div>
</div>

<div class="rb">
  <div class="slbl">News &amp; Sentiment</div>
  <div id="news-feed"><div class="empty">Lade…</div></div>
  <div class="sep"></div>
  <div class="slbl">Markt Events</div>
  <div id="events-feed"></div>
</div>
</div>

<script>
const HOST = location.protocol==='https:'
  ? `wss://${location.host}/ws`
  : `ws://${location.host}/ws`;

const CL={AAPL:'#c8a96e',TSLA:'#e85555',MSFT:'#4488ee',NVDA:'#2dd88a',GOOGL:'#e8a832',AMZN:'#dd66aa',META:'#8866ff',NFLX:'#e86666',AMD:'#88aaff',INTC:'#44aaee'};
const SCOLS=['#2dd88a','#4488ee','#aa66ff','#e86622','#e8a832','#e85555','#6a8a7a'];
const STRATS=['Trend Following','Momentum','Mean Reversion','Breakout','Volume','News Sentiment','Volatility'];
const gc=s=>CL[s]||'#8899aa';
const clp=(v,a=-1,b=1)=>Math.max(a,Math.min(b,v));
const fmt=n=>isNaN(n)||n==null?'0.00':Math.abs(+n).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g,',');
const $=id=>document.getElementById(id);

let D={connected:false,portfolio:null,prices:{},signals:{},trades:[],eq_curve:[],analytics:null,charts:{},learner:null,learn_history:[],symbols:['AAPL','TSLA','MSFT'],ws_ticks:0,rest_polls:0};
const CHO={};let EQC=null,SYMC=null,STRC=null,LRNC=null,WRC=null;
let newsItems=[],evItems=[],_tt=null,lastPx={},prevW={};

let ws=null,wsR=0;
function connectWS(){
  setSt('wait');
  try{
    ws=new WebSocket(HOST);
    ws.onopen=()=>{wsR=0;D.connected=true;setSt('ok');toast('✅ Backend verbunden','ok',3000);};
    ws.onmessage=e=>{try{handleMsg(JSON.parse(e.data));}catch(err){}};
    ws.onclose=()=>{D.connected=false;setSt('err');setTimeout(connectWS,Math.min(++wsR*3000,30000));};
    ws.onerror=()=>setSt('err');
  }catch(e){setSt('err');setTimeout(connectWS,5000);}
}
function reconnect(){wsR=0;if(ws)try{ws.close();}catch(e){}connectWS();}
function send(d){if(ws&&ws.readyState===1)ws.send(JSON.stringify(d));}
function setSt(s){
  const d=$('dot-ws'),l=$('ws-lbl'),df=$('dot-fh');
  const map={ok:['d-live','● LIVE'],wait:['d-wait','Verbinde…'],err:['d-err','Getrennt']};
  const[cls,txt]=map[s]||map.err;
  if(d)d.className='dot '+cls;if(l)l.textContent=txt;if(df)df.className='dot '+cls;
}

function handleMsg(msg){
  if(msg.portfolio) D.portfolio=msg.portfolio;
  if(msg.prices)    D.prices=msg.prices;
  if(msg.signals)   D.signals=msg.signals;
  if(msg.learner)   D.learner=msg.learner;
  if(msg.symbols)   D.symbols=msg.symbols;
  if(msg.eq_curve)  D.eq_curve=msg.eq_curve;
  if(msg.analytics) D.analytics=msg.analytics;
  if(msg.learn_history) D.learn_history=msg.learn_history;
  if(msg.charts)    Object.assign(D.charts,msg.charts);
  if(msg.ws_ticks!=null) D.ws_ticks=msg.ws_ticks;
  if(msg.rest_polls!=null) D.rest_polls=msg.rest_polls;
  if(msg.new_trades?.length){
    const ex=new Set(D.trades.map(t=>t.ts+t.sym+t.side));
    msg.new_trades.forEach(t=>{
      if(!ex.has(t.ts+t.sym+t.side)){
        D.trades.unshift(t);
        if(t.side==='BUY')toast(`▲ BUY ${t.sym} @$${(+t.price).toFixed(2)} [${t.strategy}]`,'ok');
        else toast(`${+t.pnl>=0?'▲':'▼'} SELL ${t.sym} P&L=${+t.pnl>=0?'+':''}€${fmt(t.pnl)}`,+t.pnl>=0?'ok':'err');
      }
    });
    D.trades=D.trades.slice(0,300);renderTrades();
  }
  // Flash
  Object.entries(D.prices).forEach(([sym,p])=>{
    if(lastPx[sym]&&p.price!==lastPx[sym]){
      const el2=$('cc-'+sym);if(el2){el2.classList.remove('fup','fdn');void el2.offsetWidth;el2.classList.add(p.price>=lastPx[sym]?'fup':'fdn');}
    }
    lastPx[sym]=p.price;
  });
  // KI delta flash
  if(D.learner?.weights&&prevW){
    Object.entries(D.learner.weights).forEach(([s,w])=>{
      const old=prevW[s];if(old&&Math.abs(w-old)>.001){const el2=$('wv-'+s.replace(/ /g,'_'));if(el2){el2.classList.remove('wpop');void el2.offsetWidth;el2.classList.add('wpop');}}
    });
    prevW={...D.learner.weights};
  }
  renderAll();updateTicker();updateStatus();
}

function buildChartCards(){
  const g=$('charts-grid');if(!g)return;
  Object.values(CHO).forEach(ch=>{try{ch.destroy();}catch(e){}});for(const k in CHO)delete CHO[k];
  g.innerHTML=D.symbols.map(sym=>`<div class="cc" id="cc-${sym}">
    <div class="cc-hd"><span style="font-weight:700;font-size:12px;font-family:var(--mo);color:${gc(sym)}">${sym}</span><span id="cpr-${sym}" style="font-size:12px;margin-left:auto;font-family:var(--mo);font-weight:300">$—</span><span id="cch-${sym}" style="font-size:10px;padding:2px 6px;border-radius:3px;font-weight:600;font-family:var(--mo)">—</span></div>
    <div class="pills" id="pills-${sym}"></div>
    <div class="cw"><canvas id="ch-${sym}"></canvas></div>
    <div class="sc-row"><span style="font-size:8px;color:var(--dim);font-family:var(--mo)">SIGNAL</span><div class="sc-tr"><div class="sc-mid2"></div><div class="sc-fi2" id="sf-${sym}"></div></div><span id="sn-${sym}" style="font-size:10px;font-family:var(--mo);font-weight:700;width:36px;text-align:right">—</span></div>
  </div>`).join('');
  setTimeout(()=>D.symbols.forEach(buildChart),0);
}
function buildChart(sym){
  const cv=$('ch-'+sym);if(!cv)return;if(CHO[sym])try{CHO[sym].destroy();}catch(e){}
  const c=gc(sym),data=D.charts[sym]||[];
  const sm20=data.map((_,i,a)=>i<19?null:a.slice(i-19,i+1).reduce((x,y)=>x+y,0)/20);
  try{CHO[sym]=new Chart(cv,{type:'line',data:{labels:data.map((_,i)=>i),datasets:[{data,borderColor:c,backgroundColor:c+'10',borderWidth:1.5,pointRadius:0,tension:.3,fill:true},{data:sm20,borderColor:'rgba(200,169,110,.35)',borderWidth:1,pointRadius:0,tension:.3,borderDash:[4,3]}]},options:{responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{display:false},tooltip:{backgroundColor:'#12161c',titleColor:c,bodyColor:c+'80',borderColor:c+'25',borderWidth:1,callbacks:{label:ctx=>'$'+ctx.parsed.y.toFixed(2)}}},scales:{x:{display:false},y:{grid:{color:'rgba(200,169,110,.03)'},ticks:{color:'#3a4a5a',callback:v=>'$'+v.toFixed(0),font:{size:8,family:'IBM Plex Mono'},maxTicksLimit:4}}}}});}catch(e){}
}
function updateCharts(){
  D.symbols.forEach(sym=>{
    const ch=CHO[sym];if(!ch)return;
    const data=D.charts[sym]||[];if(!data.length)return;
    const sm20=data.map((_,i,a)=>i<19?null:a.slice(i-19,i+1).reduce((x,y)=>x+y,0)/20);
    ch.data.labels=data.map((_,i)=>i);ch.data.datasets[0].data=data;ch.data.datasets[1].data=sm20;
    try{ch.update('none');}catch(e){}
    const p=D.prices[sym];if(!p)return;
    const pe=$('cpr-'+sym);if(pe)pe.textContent='$'+p.price.toFixed(2);
    const ce=$('cch-'+sym);if(ce){ce.textContent=(p.pct>=0?'+':'')+p.pct.toFixed(2)+'%';ce.style.color=p.pct>=0?'var(--gr)':'var(--re)';ce.style.background=p.pct>=0?'rgba(45,216,138,.08)':'rgba(232,85,85,.08)';}
    const sig=D.signals[sym];if(!sig)return;
    const sc=sig.composite;
    const sf=$('sf-'+sym);if(sf){sf.style.width=Math.abs(sc)*50+'%';sf.style.left=sc>=0?'50%':(50-Math.abs(sc)*50)+'%';sf.style.background=sc>.2?'var(--gr)':sc<-.15?'var(--re)':sc>0?'rgba(45,216,138,.4)':'rgba(232,85,85,.4)';}
    const sn=$('sn-'+sym);if(sn){sn.textContent=(sc>0?'+':'')+sc.toFixed(2);sn.style.color=sc>0?'var(--gr)':'var(--re)';}
    const det=sig.details||{};
    const rm=det['Momentum']?.match(/RSI=([\d.]+)/),mm=det['Momentum']?.match(/MACD=([↑↓])/),bm=det['Mean Reversion']?.match(/BB%b=(\d+)/);
    const pe2=$('pills-'+sym);if(pe2)pe2.innerHTML=(rm?`<span class="p2 ${+rm[1]<30?'p2g':+rm[1]>70?'p2r':'p2n'}">RSI ${rm[1]}</span>`:'')+  (mm?`<span class="p2 ${mm[1]==='↑'?'p2g':'p2r'}">MACD ${mm[1]}</span>`:'')+  (bm?`<span class="p2 ${+bm[1]<25?'p2g':+bm[1]>75?'p2r':'p2n'}">BB ${bm[1]}%</span>`:'')+  `<span class="p2 p2a">${p.src==='ws'?'📡 WS':'🔄 REST'}</span>`;
  });
}

function buildAnCharts(){
  const bo=()=>({responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{display:false}},scales:{x:{display:false},y:{grid:{color:'rgba(200,169,110,.03)'},ticks:{color:'#3a4a5a',font:{size:8,family:'IBM Plex Mono'}}}}});
  if(EQC)try{EQC.destroy();}catch(e){}
  const e1=$('eq-c');if(e1)EQC=new Chart(e1,{type:'line',data:{labels:[],datasets:[{label:'Portfolio',data:[],borderColor:'#c8a96e',backgroundColor:'rgba(200,169,110,.06)',borderWidth:1.5,pointRadius:0,tension:.3,fill:true},{label:'€10k',data:[],borderColor:'rgba(58,74,90,.35)',borderWidth:1,pointRadius:0,borderDash:[4,3]}]},options:{...bo(),plugins:{legend:{display:true,labels:{color:'#6a7a8a',font:{size:9,family:'IBM Plex Mono'},boxWidth:10}}}}});
  if(SYMC)try{SYMC.destroy();}catch(e){}
  const e2=$('sym-c');if(e2)SYMC=new Chart(e2,{type:'bar',data:{labels:[],datasets:[{data:[],backgroundColor:[],borderRadius:3}]},options:{...bo(),scales:{x:{grid:{display:false},ticks:{color:'var(--text)',font:{size:9,family:'IBM Plex Mono'}}},y:{grid:{color:'rgba(200,169,110,.03)'},ticks:{color:'#3a4a5a',callback:v=>'€'+v,font:{size:8,family:'IBM Plex Mono'}}}}}});
  if(STRC)try{STRC.destroy();}catch(e){}
  const e3=$('str-c');if(e3)STRC=new Chart(e3,{type:'bar',data:{labels:STRATS.map(s=>s.split(' ')[0]),datasets:[{data:new Array(7).fill(0),backgroundColor:SCOLS,borderRadius:3}]},options:{responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},ticks:{color:'#3a4a5a',font:{size:8,family:'IBM Plex Mono'}}},y:{min:-1,max:1,grid:{color:'rgba(200,169,110,.03)'},ticks:{color:'#3a4a5a',font:{size:8,family:'IBM Plex Mono'}}}}}});
  if(LRNC)try{LRNC.destroy();}catch(e){}
  const e4=$('lrn-c');if(e4)LRNC=new Chart(e4,{type:'line',data:{labels:[],datasets:[{data:[],borderColor:'#2dd88a',backgroundColor:'rgba(45,216,138,.07)',borderWidth:1.5,pointRadius:0,tension:.4,fill:true}]},options:{...bo(),scales:{x:{display:false},y:{min:0,max:1,grid:{color:'rgba(200,169,110,.03)'},ticks:{color:'#3a4a5a',callback:v=>(v*100).toFixed(0)+'%',font:{size:8,family:'IBM Plex Mono'}}}}}});
  if(WRC)try{WRC.destroy();}catch(e){}
  const e5=$('wr-c');if(e5)WRC=new Chart(e5,{type:'bar',data:{labels:STRATS.map(s=>s.split(' ')[0]),datasets:[{data:new Array(7).fill(50),backgroundColor:SCOLS,borderRadius:3}]},options:{...bo(),scales:{x:{grid:{display:false},ticks:{color:'#3a4a5a',font:{size:8,family:'IBM Plex Mono'}}},y:{min:0,max:100,grid:{color:'rgba(200,169,110,.03)'},ticks:{color:'#3a4a5a',callback:v=>v+'%',font:{size:8,family:'IBM Plex Mono'}}}}}});
}
function refreshAn(){
  if(EQC&&D.eq_curve.length){EQC.data.labels=D.eq_curve.map((_,i)=>i);EQC.data.datasets[0].data=D.eq_curve.map(e=>e.v);EQC.data.datasets[1].data=D.eq_curve.map(()=>10000);try{EQC.update('none');}catch(e){}}
  if(SYMC){const byS={};D.trades.filter(t=>t.side==='SELL').forEach(t=>{byS[t.sym]=(byS[t.sym]||0)+(+t.pnl);});const lb=Object.keys(byS),vl=lb.map(s=>+byS[s].toFixed(2));SYMC.data.labels=lb.length?lb:['—'];SYMC.data.datasets[0].data=vl.length?vl:[0];SYMC.data.datasets[0].backgroundColor=vl.map(v=>v>=0?'rgba(45,216,138,.6)':'rgba(232,85,85,.6)');try{SYMC.update('none');}catch(e){}}
  if(STRC){const sym=D.symbols[0],sig=D.signals[sym];if(sig?.scores){STRC.data.datasets[0].data=STRATS.map(s=>+(sig.scores[s]||0).toFixed(3));try{STRC.update('none');}catch(e){}}}
  if(LRNC&&D.learn_history.length){LRNC.data.labels=D.learn_history.map((_,i)=>i);LRNC.data.datasets[0].data=D.learn_history.map(h=>h.accuracy);try{LRNC.update('none');}catch(e){}}
  if(WRC&&D.learner?.strat_winrates){WRC.data.datasets[0].data=STRATS.map(s=>D.learner.strat_winrates[s]||50);try{WRC.update('none');}catch(e){}}
}

function updateTicker(){
  const bar=$('ticker');if(!bar)return;
  bar.innerHTML=D.symbols.map(sym=>{const p=D.prices[sym];if(!p?.price)return'';const up=p.pct>=0;return`<span class="tick"><span style="font-weight:700;color:${gc(sym)}">${sym}</span><span>$${p.price.toFixed(2)}</span><span style="color:${up?'var(--gr)':'var(--re)'}">${up?'+':''}${p.pct.toFixed(2)}%</span></span>`;}).join('');
}
function updateStatus(){
  $('fb-ticks').textContent=(D.ws_ticks||0).toLocaleString();
  $('fb-rest').textContent=D.rest_polls||0;
  $('fb-last').textContent=new Date().toLocaleTimeString('de-DE');
  $('fb-ws').textContent=D.connected?'✅ Verbunden':'❌ Getrennt';
  const now=new Date();const h=now.getUTCHours(),m=now.getUTCMinutes(),day=now.getUTCDay();
  $('fb-market').textContent=(day>=1&&day<=5&&(h>14||(h===14&&m>=30))&&h<21)?'🟢 NYSE Offen':'🔴 Geschlossen';
  $('upd').textContent=new Date().toLocaleTimeString('de-DE');
  if(D.learner){
    $('ai-lr').textContent=D.learner.lr?.toFixed(5)||'—';
    $('ai-tc').textContent=D.learner.trade_count||0;
    $('ai-acc').textContent=D.learner.accuracy!=null?(D.learner.accuracy*100).toFixed(1)+'%':'—';
    const bar2=$('ai-bar');if(bar2)bar2.style.width=((D.learner.accuracy||0)*100)+'%';
    $('s-lr').textContent=D.learner.lr?.toFixed(5)||'—';
    $('s-tc').textContent=D.learner.trade_count||0;
    $('s-ac').textContent=D.learner.accuracy!=null?(D.learner.accuracy*100).toFixed(1)+'%':'—';
  }
}

function renderAll(){
  renderPortfolio();renderComposite();updateCharts();renderTrades();renderStratBD();renderAN();renderAITab();renderSettings();refreshAn();genNews();
}

function renderPortfolio(){
  const pf=D.portfolio;if(!pf)return;
  const up=pf.pnl>=0;
  $('s-total').textContent='€'+fmt(pf.total_value);$('s-total').style.color=up?'var(--gold)':'var(--re)';
  $('s-pct').textContent=(up?'+':'')+pf.pnl_pct+'%';
  $('s-cash').textContent='€'+fmt(pf.cash);$('s-cashpct').textContent=((pf.cash/Math.max(pf.total_value,.01))*100).toFixed(1)+'% liquid';
  $('s-pnl').textContent=(up?'+':'-')+'€'+fmt(Math.abs(pf.pnl));$('s-pnl').style.color=up?'var(--gr)':'var(--re)';
  $('s-tct').textContent=pf.total_trades+' Trades · WR '+pf.win_rate+'%';
  $('pos-list').innerHTML=(pf.positions||[]).length?(pf.positions||[]).map(p=>`<div class="pos-it" style="border-color:${gc(p.sym)}60"><div style="font-weight:700;font-size:11px;color:${gc(p.sym)};font-family:var(--mo)">${p.sym}</div><div style="font-size:10px;font-family:var(--mo)">$${p.price?.toFixed(2)||'—'} · ${p.qty?.toFixed(4)}sh</div><div style="font-size:10px;font-weight:700;color:${p.pnl>=0?'var(--gr)':'var(--re)'};font-family:var(--mo)">${p.pnl>=0?'+':'-'}€${fmt(Math.abs(p.pnl))} (${p.pnl_pct}%)</div></div>`).join(''):'<div class="empty">Keine Positionen</div>';
  const L=D.learner;if(L?.weights){const ss=$('strat-sb');if(ss)ss.innerHTML=STRATS.map((n,i)=>{const w=L.weights[n]||0;const pct=((w+1)/2*100).toFixed(0);return`<div class="str-row"><div class="str-nm">${n}</div><div class="str-tr"><div class="str-fi" style="width:${(w*300).toFixed(0)}%;background:${SCOLS[i]}"></div></div><div class="str-vl" id="wv-${n.replace(/ /g,'_')}" style="color:${SCOLS[i]};font-size:8px">${(w*100).toFixed(1)}%</div></div>`;}).join('');}
}

function renderComposite(){
  const cr=$('composite-row');if(!cr)return;
  if(!D.symbols.some(s=>D.prices[s]?.price)){cr.innerHTML='<div class="load-card"><div class="spin">📡</div><br><span style="font-size:11px;color:var(--dim);font-family:var(--mo)">Verbinde mit Finnhub…</span></div>';return;}
  cr.innerHTML=D.symbols.map(sym=>{
    const sig=D.signals[sym];const p=D.prices[sym];if(!sig||!p?.price)return'';
    const c=sig.composite,signal=sig.signal||'HOLD';
    const pos2=D.portfolio?.positions?.find(x=>x.sym===sym);
    return`<div class="cscard"><div class="cs-hd">
      <span style="font-weight:700;font-size:14px;font-family:var(--mo);color:${gc(sym)}">${sym}</span>
      <span style="font-size:14px;font-family:var(--mo);font-weight:300">$${p.price.toFixed(2)}</span>
      <span style="font-size:11px;font-weight:600;color:${p.pct>=0?'var(--gr)':'var(--re)'};font-family:var(--mo)">${p.pct>=0?'+':''}${p.pct.toFixed(2)}%</span>
      <span class="p2 p2a">${p.src==='ws'?'📡 WS':'🔄 REST'}</span>
      ${pos2?`<span style="font-size:9px;color:var(--dim);background:var(--ink3);padding:2px 8px;border-radius:3px;font-family:var(--mo)">LONG ${pos2.qty.toFixed(4)}sh</span>`:''}
      <span class="sig-b ${signal==='BUY'?'sb-buy':signal==='SELL'?'sb-sell':'sb-hold'}">${signal}</span>
      <span style="font-size:9px;color:var(--dim);margin-left:auto;font-family:var(--mo)">SCORE <strong style="color:${c>0?'var(--gr)':'var(--re)'}">${c>0?'+':''}${c.toFixed(4)}</strong></span>
    </div>
    ${p.high?`<div style="font-size:9px;color:var(--dim);font-family:var(--mo);margin-bottom:8px">H $${p.high.toFixed(2)} · L $${p.low.toFixed(2)} · O $${p.open?.toFixed(2)||'—'}</div>`:''}
    <div style="display:flex;align-items:center;gap:8px">
      <span style="font-size:8px;color:var(--d2);font-family:var(--mo)">SELL</span>
      <div class="cs-bar"><div class="cs-mid"></div><div class="cs-fi" style="width:${Math.abs(c)*50}%;left:${c>=0?50:(50-Math.abs(c)*50)}%;background:${c>.2?'var(--gr)':c<-.15?'var(--re)':c>0?'rgba(45,216,138,.4)':'rgba(232,85,85,.4)'}"></div></div>
      <span style="font-size:8px;color:var(--d2);font-family:var(--mo)">BUY</span>
      <span style="font-size:14px;font-family:var(--mo);font-weight:300;width:44px;text-align:right;color:${c>0?'var(--gr)':'var(--re)'}">${c>0?'+':''}${c.toFixed(2)}</span>
    </div></div>`;
  }).join('');
}

function renderTrades(){
  const tb=$('trades-body');if(!tb)return;
  if(!D.trades.length){tb.innerHTML='<tr><td colspan="10" class="empty">Warte auf Signal…</td></tr>';return;}
  tb.innerHTML=D.trades.slice(0,25).map(t=>`<tr>
    <td style="color:var(--d2)">${t.ts?.split('T')[1]?.substring(0,8)||'—'}</td>
    <td style="color:${gc(t.sym)};font-weight:700">${t.sym}</td>
    <td><span class="bdg ${t.side==='BUY'?'bdg-buy':'bdg-sell'}">${t.side}</span></td>
    <td style="color:var(--dim);font-size:9px;white-space:nowrap">${t.strategy||'—'}</td>
    <td>$${(+t.price||0).toFixed(2)}</td>
    <td>${(+t.qty||0).toFixed(4)}</td>
    <td>€${fmt(t.val)}</td>
    <td class="${t.side==='SELL'?(+t.pnl>=0?'up':'dn'):''}">${t.side==='SELL'?(+t.pnl>=0?'+':'-')+'€'+fmt(Math.abs(+t.pnl)):'—'}</td>
    <td class="${(+t.score||0)>0?'up':'dn'}">${(+t.score||0)>0?'+':''}${(+t.score||0).toFixed(3)}</td>
    <td><span class="bdg bdg-src">${t.src==='ws'?'WS':'REST'}</span></td>
  </tr>`).join('');
}

function renderStratBD(){
  const sbd=$('strat-bd');if(!sbd)return;
  const W=D.learner?.weights||{};
  sbd.innerHTML=D.symbols.map(sym=>{
    const sig=D.signals[sym];if(!sig)return'';const p=D.prices[sym];const c=sig.composite;
    return`<div class="sb-card"><div style="font-size:13px;font-weight:700;color:${gc(sym)};font-family:var(--mo);margin-bottom:10px;display:flex;align-items:center;gap:8px">${sym}${p?` <span style="font-weight:300">$${p.price.toFixed(2)}</span>`:''}<span class="p2 p2a">${p?.src==='ws'?'📡 WS':'🔄 REST'}</span><span style="font-size:10px;color:var(--dim);font-family:var(--fn);margin-left:4px">Composite: <strong style="color:${c>0?'var(--gr)':'var(--re)'}">${c>0?'+':''}${c.toFixed(4)}</strong></span></div>
    <div style="display:grid;grid-template-columns:130px 1fr 36px 80px;gap:0 8px">
      ${['STRATEGIE','SCORE','SIG','DETAIL'].map(h=>`<div style="font-size:8px;color:var(--d2);font-weight:600;padding:3px 0;border-bottom:1px solid var(--br);font-family:var(--mo);letter-spacing:.8px">${h}</div>`).join('')}
      ${STRATS.map((name,i)=>{const sc=sig.scores?.[name]||0,det=sig.details?.[name]||'—';const pct=((sc+1)/2*100);const sign=sc>.3?'BULL':sc<-.25?'BEAR':sc>0?'↑':sc<0?'↓':'—';const cl=sc>.2?'var(--gr)':sc<-.15?'var(--re)':sc>0?'rgba(45,216,138,.5)':'rgba(232,85,85,.5)';const kw=((W[name]||0)*100).toFixed(1);return`<div style="font-size:10px;font-weight:600;padding:5px 0;border-bottom:1px solid rgba(200,169,110,.05);font-family:var(--mo)">${name}<span style="font-size:8px;color:var(--d2);margin-left:4px">${kw}%</span></div><div style="padding:5px 0;border-bottom:1px solid rgba(200,169,110,.05);display:flex;align-items:center;gap:5px"><div class="sb-bar" style="flex:1"><div class="sb-fi" style="width:${pct}%;background:${SCOLS[i]}"></div></div><span style="font-size:10px;font-family:var(--mo);font-weight:700;color:${sc>0?SCOLS[i]:'var(--re)'};width:34px;text-align:right">${sc>0?'+':''}${sc.toFixed(2)}</span></div><div style="padding:5px 0;border-bottom:1px solid rgba(200,169,110,.05);text-align:center"><span style="font-size:8px;font-weight:700;padding:2px 5px;border-radius:3px;color:${cl};background:${cl}15;font-family:var(--mo)">${sign}</span></div><div style="font-size:9px;color:var(--d2);padding:5px 0;border-bottom:1px solid rgba(200,169,110,.05);font-family:var(--mo);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${det}</div>`;}).join('')}
    </div></div>`;
  }).join('');
}

function renderAN(){
  const an=D.analytics;const pf=D.portfolio;if(!an||!pf)return;
  const am=$('an-m');if(!am)return;
  am.innerHTML=[
    {l:'Win Rate',v:`${an.win_rate}%`,s:`${an.closed} closed`,c:an.win_rate>50?'var(--gr)':'var(--re)'},
    {l:'Total P&L',v:(an.total_pnl>=0?'+':'-')+'€'+fmt(Math.abs(an.total_pnl)),s:`${an.total} Trades`,c:an.total_pnl>=0?'var(--gr)':'var(--re)'},
    {l:'Risk/Reward',v:an.risk_reward||'—',s:`Avg Win €${fmt(an.avg_win)}`,c:'var(--text)'},
    {l:'KI-Genauigkeit',v:`${an.accuracy||0}%`,s:'Signal korrekt',c:an.accuracy>50?'var(--gr)':'var(--re)'},
    {l:'Drawdown',v:`${an.max_dd||0}%`,s:'vom Peak',c:'var(--am)'},
    {l:'Datenquelle',v:'Finnhub',s:`WS: ${an.ws_ticks||0}`,c:'var(--gold)'},
    {l:'Portfolio',v:'€'+fmt(pf.total_value),s:`${an.return_pct||0}% Return`,c:pf.total_value>=10000?'var(--gr)':'var(--re)'},
    {l:'KI Trades',v:D.learner?.trade_count||0,s:`LR: ${D.learner?.lr?.toFixed(4)||'—'}`,c:'var(--text)'},
  ].map(d=>`<div class="an-c"><div class="an-l">${d.l}</div><div class="an-v" style="color:${d.c}">${d.v}</div><div class="an-s">${d.s}</div></div>`).join('');
}

function renderAITab(){
  const L=D.learner;if(!L?.weights)return;
  const tc2=$('ai-tc2');if(tc2)tc2.innerHTML=`<div class="dot d-live" style="width:5px;height:5px"></div>${L.trade_count||0} Trades`;
  const tbl=$('ai-wtbl');if(!tbl)return;
  const W=L.weights,B=L.base_weights||{},WR=L.strat_winrates||{};
  tbl.innerHTML=STRATS.map((name,i)=>{
    const w=W[name]||0,b=B[name]||0.14,delta=w-b;
    const wr=WR[name]||50;
    return`<div style="display:grid;grid-template-columns:130px 1fr 60px 55px 55px;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--br)">
      <div style="font-size:10px;font-family:var(--mo);font-weight:500">${name}</div>
      <div><div class="slr-bar"><div class="slr-fi" style="width:${Math.min(w*500,100)}%;background:${delta>0.001?'var(--gr)':delta<-0.001?'var(--re)':SCOLS[i]}"></div></div><div style="font-size:8px;color:var(--dim);font-family:var(--mo);margin-top:2px">WR: ${wr}%</div></div>
      <div style="font-size:11px;font-family:var(--mo);font-weight:700;text-align:right;color:${SCOLS[i]}" id="wv2-${name.replace(/ /g,'_')}">${(w*100).toFixed(1)}%</div>
      <div style="font-size:9px;font-family:var(--mo);text-align:right;color:var(--dim)">${(b*100).toFixed(1)}%</div>
      <div style="text-align:right"><span class="${delta>0.001?'w-up':delta<-0.001?'w-dn':'w-nm'}">${delta>0.001?'+':''} ${(delta*100).toFixed(1)}%</span></div>
    </div>`;
  }).join('');
}

function renderSettings(){
  const sc=$('sym-chips');if(sc)sc.innerHTML=D.symbols.map(s=>`<span class="chip">${s}<button onclick="removeSym('${s}')">×</button></span>`).join('');
  const rp=$('risk-params');if(rp)rp.innerHTML=[{k:'buyThr',l:'Buy Threshold',v:.20,s:.05},{k:'sellThr',l:'Sell Threshold',v:-.15,s:.05},{k:'riskPct',l:'Risk Per Trade',v:.12,s:.01},{k:'stopLoss',l:'Stop Loss %',v:.05,s:.01},{k:'takeProfit',l:'Take Profit %',v:.10,s:.01}].map(d=>`<div class="p-row"><label>${d.l}</label><input type="number" id="rp-${d.k}" value="${d.v}" step="${d.s}"><button class="s-btn" onclick="applyP('${d.k}')">OK</button></div>`).join('');
}

function sw(name,btn){
  ['dashboard','strategies','ai','analytics','settings'].forEach(t=>{const e=$('tab-'+t);if(e)e.style.display=t===name?'block':'none';});
  document.querySelectorAll('.tab').forEach(b=>b.classList.remove('on'));btn.classList.add('on');
  if(name==='analytics'||name==='ai')setTimeout(()=>{buildAnCharts();refreshAn();},80);
}
async function addSym(){const inp=$('sym-inp');const sym=inp.value.trim().toUpperCase();if(!sym||D.symbols.includes(sym)||D.symbols.length>=5){toast('Ungültig','err');return;}inp.value='';D.symbols.push(sym);send({type:'set_symbols',symbols:D.symbols});toast(`${sym} hinzugefügt`,'ok');buildChartCards();}
function removeSym(sym){if(D.symbols.length<=1){toast('Min. 1 Symbol','err');return;}D.symbols=D.symbols.filter(s=>s!==sym);send({type:'set_symbols',symbols:D.symbols});buildChartCards();renderAll();}
function applyP(k){const inp=$('rp-'+k);if(!inp)return;send({type:'set_param',key:k,value:parseFloat(inp.value)});toast(`${k} = ${inp.value}`,'ok');}
function resetAll(){if(!confirm('Portfolio zurücksetzen?'))return;send({type:'reset'});D.trades=[];D.eq_curve=[];toast('Reset ✅','ok');}

const NT=[{t:'{s} Earnings schlagen Konsens — Finnhub Alert',pos:true,type:'earnings'},{t:'Analyst: {s} Strong Buy, Ziel ${n}',pos:true,type:'upgrade'},{t:'KI-Signal: Breakout-Muster bei {s} erkannt',pos:true,type:'ai'},{t:'Finnhub: {s} verfehlt EPS-Schätzungen',pos:false,type:'miss'},{t:'Downgrade {s}: Margendruck Q{q}',pos:false,type:'downgrade'},{t:'Block Trade: Institutionelle kaufen {s}',pos:true,type:'flow'},{t:'KI warnt: {s} RSI überkauft',pos:false,type:'ai-warn'}];
const EV=['Fed Meeting — Zinsentscheid','CPI Report 14:30 UTC','Options Expiry Freitag','VIX steigt — Volatilität','Tech-Rotation aktiv'];
function genNews(){
  if(newsItems.length&&Math.random()>.3){renderNews();return;}
  const sym=D.symbols[Math.floor(Math.random()*D.symbols.length)];const tp=NT[Math.floor(Math.random()*NT.length)];
  const hl=tp.t.replace('{s}',sym).replace('{n}',Math.floor(Math.random()*50+10)).replace('{q}',Math.ceil(Math.random()*4));
  newsItems.unshift({sym,hl,pos:tp.pos,type:tp.type,ts:new Date().toLocaleTimeString('de-DE')});if(newsItems.length>10)newsItems.pop();
  if(Math.random()<.12){evItems.unshift({text:EV[Math.floor(Math.random()*EV.length)],ts:new Date().toLocaleTimeString('de-DE')});if(evItems.length>4)evItems.pop();}
  renderNews();
}
function renderNews(){
  const nf=$('news-feed');if(!nf||!newsItems.length)return;
  nf.innerHTML=newsItems.slice(0,8).map(n=>`<div class="ni"><div style="display:flex;align-items:center;gap:5px;margin-bottom:4px"><span style="font-size:8px;padding:1px 5px;border-radius:3px;background:var(--ink3);color:var(--dim);font-weight:600;font-family:var(--mo)">${n.sym}</span><span class="ns ${n.pos?'ns-p':'ns-n'}">${n.pos?'▲ BULL':'▼ BEAR'}</span><span style="font-size:8px;color:var(--d2);font-family:var(--mo)">${n.type}</span></div><div class="nh">${n.hl}</div><div class="nm">${n.ts} · Finnhub</div></div>`).join('');
  const ef=$('events-feed');if(!ef)return;
  ef.innerHTML=evItems.length?evItems.map(e=>`<div style="background:var(--ink2);border:1px solid rgba(232,168,50,.15);border-radius:4px;padding:9px;margin-bottom:4px"><div style="font-size:8px;font-weight:600;color:var(--am);text-transform:uppercase;font-family:var(--mo);letter-spacing:.8px;margin-bottom:3px">⚡ Event</div><div style="font-size:10px;line-height:1.4">${e.text}</div><div class="nm" style="margin-top:3px">${e.ts}</div></div>`).join(''):'<div class="empty">—</div>';
}

function toast(msg,type='ok',dur=3000){let t=document.querySelector('.toast');if(!t){t=document.createElement('div');t.className='toast';document.body.appendChild(t);}t.textContent=msg;t.className=`toast t-${type}`;clearTimeout(_tt);_tt=setTimeout(()=>{if(t.parentNode)t.remove();},dur);}

window.addEventListener('load',()=>{
  buildChartCards();buildAnCharts();renderSettings();
  connectWS();
  for(let i=0;i<4;i++)setTimeout(()=>genNews(),i*600);
  setInterval(genNews,7000);
  setInterval(updateStatus,5000);
});
</script>
</body>
</html>
