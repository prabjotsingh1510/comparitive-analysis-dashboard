"""
Add 9 visualizations as a new 'Insights' tab.
Reuses existing: el, txt, bar, ticks, bind, tip, R, Rs, P, esc, nf, QC, QN, ACTN,
                 D, D_AMZ, D_FC, D_BL, chartWaterfallC, chartParetoC, etc.
NO changes to existing sections, data, or logic.
"""

# ── 1. CSS additions (scoped, no conflicts) ───────────────────────────────
CSS = """
  /* Insights tab additions */
  .ins-grid2 { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:14px; }
  @media(max-width:860px){ .ins-grid2{ grid-template-columns:1fr; } }
  .ins-section { margin-bottom: 28px; }
  .ins-h { font-size:15px; font-weight:700; margin:0 0 4px; letter-spacing:-0.01em; }
  .ins-sub { font-size:12.5px; color:var(--ink-2); margin:0 0 10px; max-width:72ch; }
  .matrix-cell { width:88px; }
  .matrix-tag { display:inline-block; font-size:10px; font-weight:700;
    padding:2px 6px; border-radius:4px; border:1px solid var(--border);
    background:var(--wash); white-space:nowrap; }
  .matrix-tag.star   { color:var(--good); border-color:var(--good); }
  .matrix-tag.overhead { color:#8a6100; border-color:var(--warn); }
  .matrix-tag.loss   { color:var(--crit); border-color:var(--crit); }
  .matrix-tag.notlisted { color:var(--ink-3); }
  .bar-label-inline { font-size:10px; fill:var(--ink-2); font-variant-numeric:tabular-nums; }
  .action-bar { cursor:default; }
"""

# ── 2. HTML nav button ────────────────────────────────────────────────────
NAV_BTN = '    <button role="tab" aria-selected="false" data-chan="insights">Insights</button>'

# ── 3. HTML panel skeleton ────────────────────────────────────────────────
PANEL_HTML = """
<div class="chan-panel" id="chan-insights" hidden>
<header class="top">
  <div class="top-in">
    <h1>Visual Insights — Apr–Jun 2026</h1>
    <p class="sub">Nine business-question-driven charts. All numbers sourced from channel pages — no recalculation.</p>
  </div>
</header>
<div class="wrap" style="padding-top:26px">

  <div class="ins-section" id="vis-A">
    <div class="ins-h">A. Channel Profitability Ranking</div>
    <p class="ins-sub">Which channel actually contributes profit? Ranked by EBITDA.</p>
    <div class="chart" id="vis-A-chart"></div>
  </div>

  <div class="ins-section" id="vis-B">
    <div class="ins-h">B. Profitable SKU Rate by Channel</div>
    <p class="ins-sub">How broad is profitability? CM2+ and EBITDA+ products as a share of each channel's catalogue.</p>
    <div class="chart" id="vis-B-chart"></div>
  </div>

  <div class="ins-section" id="vis-C">
    <div class="ins-h">C. Product Profitability Quadrant — CM2/unit vs EBITDA/unit</div>
    <p class="ins-sub">Which products are economically attractive? Zero is the break-even boundary on both axes. Bubble = revenue. Channel toggle loads that dataset.</p>
    <div class="ctrls" id="vis-C-ctrls"></div>
    <div class="chart" id="vis-C-chart"></div>
  </div>

  <div class="ins-section" id="vis-D">
    <div class="ins-h">D. Revenue vs EBITDA — Are our biggest products profitable?</div>
    <p class="ins-sub">High revenue with negative EBITDA reveals the paradox of scaling a loss. Bubble = units sold.</p>
    <div class="ctrls" id="vis-D-ctrls"></div>
    <div class="chart" id="vis-D-chart"></div>
  </div>

  <div class="ins-section" id="vis-E">
    <div class="ins-h">E. Top / Bottom EBITDA Products</div>
    <p class="ins-sub">Where is money made and lost? Toggle metric and view.</p>
    <div class="ctrls" id="vis-E-ctrls"></div>
    <div class="chart" id="vis-E-chart"></div>
  </div>

  <div class="ins-section" id="vis-F">
    <div class="ins-h">F. Cost Structure — Where does ₹100 of revenue go?</div>
    <p class="ins-sub">Waterfall from gross revenue to EBITDA per channel. Select channel below.</p>
    <div class="ctrls" id="vis-F-ctrls"></div>
    <div class="chart" id="vis-F-chart"></div>
  </div>

  <div class="ins-section" id="vis-G">
    <div class="ins-h">G. 80/20 Pareto — How concentrated is revenue?</div>
    <p class="ins-sub">Products ranked by revenue. Threshold markers at 50%, 80%, 90%.</p>
    <div class="ctrls" id="vis-G-ctrls"></div>
    <div class="chart" id="vis-G-chart"></div>
  </div>

  <div class="ins-section" id="vis-H">
    <div class="ins-h">H. Product × Channel Matrix</div>
    <p class="ins-sub">Which channel is best for each product? Sort by profitable channel count, EBITDA, or revenue.</p>
    <div class="ctrls" id="vis-H-ctrls"></div>
    <div class="tw" id="vis-H-table" style="max-height:480px;overflow-y:auto;border-radius:10px"></div>
  </div>

  <div class="ins-section" id="vis-I">
    <div class="ins-h">I. Product Action Distribution</div>
    <p class="ins-sub">What is the recommended action across the portfolio? Uses existing action classifications.</p>
    <div class="ctrls" id="vis-I-ctrls"></div>
    <div class="chart" id="vis-I-chart"></div>
  </div>

</div><!-- /.wrap -->
</div><!-- /#chan-insights -->
"""

# ── 4. JavaScript ─────────────────────────────────────────────────────────
JS = """
/* ================================================================
   INSIGHTS TAB — 9 visualizations
   Uses ONLY existing helpers: el, txt, bar, ticks, bind, R, Rs, P,
   esc, nf, QC, QN, ACTN, D, D_AMZ, D_FC, D_BL, tip,
   chartWaterfallC, amazonWfStages, firstcryWfStages, blinkitWfStages
   Zero changes to existing sections.
   ================================================================ */
(function(){

/* ── shared helpers ── */
function insEl(n,a){ return el(n,a||{}); }

function hbar(svg,bx,by,bw,bh,fill,op,tooltip){
  if(bw<0.5) return;
  var b=bar(bx,by,bw,bh,4,'right');
  b.setAttribute('fill',fill);
  if(op!=null) b.setAttribute('fill-opacity',op);
  if(tooltip) bind(b,tooltip);
  svg.appendChild(b);
}

function vline(svg,x1,y1,x2,y2,stroke,sw){
  svg.appendChild(el('line',{x1:x1,y1:y1,x2:x2,y2:y2,stroke:stroke||'var(--axis)','stroke-width':sw||1.5}));
}
function hline(svg,x1,y1,x2,y2,stroke,sw){
  svg.appendChild(el('line',{x1:x1,y1:y1,x2:x2,y2:y2,stroke:stroke||'var(--grid)','stroke-width':sw||1}));
}

function axTick(svg,x,y,label,anchor,fsize){
  svg.appendChild(txt(x,y,label,{'text-anchor':anchor||'end','font-size':fsize||10.5,fill:'var(--ink-3)'}));
}

function makeSegCtrl(id, buttons, onchange){
  var d=document.getElementById(id); if(!d) return;
  var html='<div class="seg" id="'+id+'-seg">';
  buttons.forEach(function(b,i){ html+='<button aria-pressed="'+(i===0)+'" data-v="'+b.v+'">'+b.t+'</button>'; });
  html+='</div>';
  d.innerHTML=html;
  document.getElementById(id+'-seg').addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    Array.from(e.currentTarget.children).forEach(function(x){ x.setAttribute('aria-pressed',x===b); });
    onchange(b.dataset.v);
  });
}

/* ── A. Channel Profitability Ranking ── */
function renderVisA(){
  var host=document.getElementById('vis-A-chart'); if(!host) return;
  var aprW=D.periods.apr.tot;
  var rows=[
    {name:'Website', rev:aprW.rev, ebitda:aprW.ebitda, ebpct:aprW.ebitdapct, gmpct:aprW.gm/aprW.netrev*100, mktpct:aprW.mktg/aprW.netrev*100, platform:null},
    {name:'Amazon',  rev:D_AMZ.tot.rev, ebitda:D_AMZ.tot.ebitda, ebpct:D_AMZ.tot.ebitdapct, gmpct:D_AMZ.tot.gmpct*100, mktpct:D_AMZ.tot.mktg/D_AMZ.tot.netrev*100, platform:null},
    {name:'FirstCry',rev:D_FC.tot.rev,  ebitda:D_FC.tot.ebitda,  ebpct:D_FC.tot.ebitdapct, gmpct:D_FC.tot.gmpct, mktpct:null, platform:D_FC.tot.fcm/D_FC.tot.netrev*100},
    {name:'Blinkit', rev:D_BL.tot.rev,  ebitda:D_BL.tot.ebitda,  ebpct:D_BL.tot.ebitdapct, gmpct:D_BL.tot.gmpct*100, mktpct:D_BL.tot.mktgpct, platform:D_BL.wf.blmargin_u/D_BL.tot.netrev*100},
  ];
  rows.sort(function(a,b){ return b.ebitda-a.ebitda; });

  var W=620, rh=48, m={t:14,r:130,b:20,l:84};
  var H=m.t+m.b+rows.length*rh;
  var iw=W-m.l-m.r;
  var lo=Math.min.apply(null,rows.map(function(r){ return r.ebitda; }))*1.1;
  var hi=Math.max.apply(null,rows.map(function(r){ return r.ebitda; }))*1.15;
  if(hi<0) hi=0;
  var range=hi-lo||1;
  var x=function(v){ return m.l+(v-lo)/range*iw; };
  var s=el('svg',{viewBox:'0 0 '+W+' '+H,'aria-label':'Channel EBITDA ranking'});

  for(var t2=0;t2<(ticks(lo,hi,4)||[]).length;t2++){
    var tv=ticks(lo,hi,4)[t2];
    hline(s,x(tv),m.t,x(tv),m.t+rows.length*rh,'var(--grid)',1);
    axTick(s,x(tv),m.t+rows.length*rh+14,Rs(tv),'middle',9.5);
  }
  vline(s,x(0),m.t,x(0),m.t+rows.length*rh,'var(--axis)',1.5);

  rows.forEach(function(r,i){
    var y=m.t+i*rh+8, bh=rh-18;
    var bx=Math.min(x(0),x(r.ebitda)), bw=Math.abs(x(r.ebitda)-x(0));
    var fill=r.ebitda>=0?'var(--good)':'var(--crit)';
    var tip2='<b>'+esc(r.name)+'</b><div>Revenue '+R(r.rev)+'</div><div>EBITDA '+R(r.ebitda)+' ('+P(r.ebpct)+')</div><div>Gross Margin '+P(r.gmpct)+'</div>'+(r.mktpct?'<div>Marketing '+P(r.mktpct)+' of net rev</div>':'')+(r.platform?'<div>Platform fee '+P(r.platform)+' of net rev</div>':'');
    hbar(s,bx,y,Math.max(bw,2),bh,fill,0.8,tip2);
    s.appendChild(txt(m.l-6,y+bh-3,r.name,{'text-anchor':'end','font-size':11.5,'font-weight':600,fill:'var(--ink-1)'}));
    s.appendChild(txt(W-4,y+bh-3,Rs(r.ebitda)+' · '+P(r.ebpct),{'text-anchor':'end','font-size':10,'font-weight':600,fill:r.ebitda>=0?'var(--good)':'var(--ink-2)'}));
  });
  host.appendChild(s);
}

/* ── B. Profitable SKU Rate ── */
function renderVisB(){
  var host=document.getElementById('vis-B-chart'); if(!host) return;
  var aprW=D.periods.apr;
  function qCount(quad, q){ var qd=(quad||{})[q]||{}; return qd.n||0; }
  var channels=[
    {name:'Website',  star:qCount(aprW.quad,'star'), oh:qCount(aprW.quad,'overhead'), loss:qCount(aprW.quad,'loss')},
    {name:'Amazon',   star:qCount(D_AMZ.quad,'star'), oh:qCount(D_AMZ.quad,'overhead'), loss:qCount(D_AMZ.quad,'loss')},
    {name:'FirstCry', star:qCount(D_FC.quad,'star'),  oh:qCount(D_FC.quad,'overhead'),  loss:qCount(D_FC.quad,'loss')},
    {name:'Blinkit',  star:qCount(D_BL.quad,'star'),  oh:qCount(D_BL.quad,'overhead'),  loss:qCount(D_BL.quad,'loss')},
  ];
  channels.forEach(function(c){ c.total=c.star+c.oh+c.loss; c.pct=c.total?c.star/c.total*100:0; });
  channels.sort(function(a,b){ return b.pct-a.pct; });

  var W=620, rh=52, m={t:14,r:140,b:20,l:84};
  var H=m.t+m.b+channels.length*rh;
  var iw=W-m.l-m.r;
  var x=function(v){ return m.l+v/100*iw; };
  var s=el('svg',{viewBox:'0 0 '+W+' '+H,'aria-label':'Profitable SKU rate by channel'});

  [0,25,50,75,100].forEach(function(t2){
    hline(s,x(t2),m.t,x(t2),m.t+channels.length*rh,'var(--grid)',1);
    axTick(s,x(t2),m.t+channels.length*rh+14,t2+'%','middle',9.5);
  });

  channels.forEach(function(ch,i){
    var y=m.t+i*rh+6, bh=rh-16;
    var bw=x(ch.pct)-m.l;
    var seg=ch.total?iw/ch.total:0;
    /* stacked: star (green) | overhead (warn) | loss (crit) */
    var bx=m.l;
    [[ch.star,'var(--good)','Star'],[ch.oh,'var(--warn)','Overhead-heavy'],[ch.loss,'var(--crit)','Loss-making']].forEach(function(seg_){
      var n=seg_[0], fill=seg_[1], label=seg_[2];
      var w=n*seg;
      if(w>0.5){
        var b=bar(bx,y,w,bh,2,'right'); b.setAttribute('fill',fill); b.setAttribute('fill-opacity',0.75);
        bind(b,'<b>'+esc(ch.name)+' · '+label+'</b><div>'+n+' of '+ch.total+' products</div><div>'+(ch.total?P(n/ch.total*100):'—')+'</div>');
        s.appendChild(b);
      }
      bx+=w;
    });
    s.appendChild(txt(m.l-6,y+bh-3,ch.name,{'text-anchor':'end','font-size':11.5,'font-weight':600,fill:'var(--ink-1)'}));
    s.appendChild(txt(W-4,y+bh-3,ch.star+'/'+ch.total+' profitable · '+P(ch.pct),{'text-anchor':'end','font-size':10,'font-weight':600,fill:ch.pct>30?'var(--good)':'var(--ink-2)'}));
  });
  /* legend */
  var lg=s.cloneNode?null:null;
  var legY=m.t+channels.length*rh+32;
  [['var(--good)','Star (profitable)'],['var(--warn)','Overhead-heavy'],['var(--crit)','Loss-making']].forEach(function(item,li){
    var lx=m.l+li*150;
    s.appendChild(el('rect',{x:lx,y:legY-8,width:10,height:10,rx:2,fill:item[0],'fill-opacity':0.75}));
    s.appendChild(txt(lx+14,legY,item[1],{'font-size':10.5,fill:'var(--ink-2)'}));
  });
  var H2=H+24;
  s.setAttribute('viewBox','0 0 '+W+' '+H2);
  host.appendChild(s);
}

/* ── C. Product Profitability Quadrant (CM2/u vs EBITDA/u) ── */
function renderVisC(chanKey){
  var host=document.getElementById('vis-C-chart'); if(!host) return;
  host.innerHTML='';
  var prods=[];
  if(chanKey==='website') prods=D.periods.apr.products.map(function(p){ return {key:p.key,cat:p.cat,cx:p.cm2_u,cy:p.ebitda_u,rev:p.rev,units:p.units,mktg:p.mktg_u,ebpct:p.ebitdapct,quad:p.quad}; });
  else if(chanKey==='amazon') prods=D_AMZ.products.map(function(p){ return {key:p.key,cat:p.cat,cx:p.cm2_u,cy:p.ebitda_u,rev:p.rev_t||p.netrev_t||0,units:p.units,mktg:p.mktg_u,ebpct:p.ebitdapct,quad:p.quad}; });
  else if(chanKey==='firstcry') prods=D_FC.products.map(function(p){ return {key:p.key,cat:p.cat,cx:p.cm2_u,cy:p.ebitda_u,rev:p.rev_t||0,units:p.units,mktg:0,ebpct:p.ebitdapct,quad:p.quad}; });
  else if(chanKey==='blinkit') prods=D_BL.products.map(function(p){ return {key:p.key,cat:p.cat,cx:p.cm2_u,cy:p.ebitda_u,rev:p.rev_t||0,units:p.units,mktg:(p.mktg_u||0)+(p.othmktg_u||0),ebpct:p.ebitdapct,quad:p.quad}; });

  var W=620,H=430,m={t:16,r:16,b:44,l:64};
  var iw=W-m.l-m.r, ih=H-m.t-m.b;
  var allX=prods.map(function(p){ return p.cx||0; }), allY=prods.map(function(p){ return p.cy||0; });
  var xlo=Math.min.apply(null,allX)*1.15, xhi=Math.max.apply(null,allX)*1.15;
  var ylo=Math.min.apply(null,allY)*1.15, yhi=Math.max.apply(null,allY)*1.15;
  xlo=Math.min(xlo,-50); xhi=Math.max(xhi,50); ylo=Math.min(ylo,-50); yhi=Math.max(yhi,50);
  var xr=xhi-xlo||1, yr=yhi-ylo||1;
  var px=function(v){ return m.l+(Math.max(xlo,Math.min(xhi,v))-xlo)/xr*iw; };
  var py=function(v){ return m.t+ih-(Math.max(ylo,Math.min(yhi,v))-ylo)/yr*ih; };
  var rmax=Math.max.apply(null,prods.map(function(p){ return p.rev||1; }));
  var rad=function(v){ return 4+Math.sqrt(Math.max(v,0)/rmax)*20; };
  var s=el('svg',{viewBox:'0 0 '+W+' '+H,'aria-label':'CM2/unit vs EBITDA/unit quadrant'});
  var x0=px(0), y0=py(0);
  /* quadrant shading */
  s.appendChild(el('rect',{x:x0,y:m.t,width:m.l+iw-x0,height:y0-m.t,fill:'var(--good)','fill-opacity':.06}));
  s.appendChild(el('rect',{x:x0,y:y0,width:m.l+iw-x0,height:m.t+ih-y0,fill:'var(--warn)','fill-opacity':.08}));
  s.appendChild(el('rect',{x:m.l,y:y0,width:x0-m.l,height:m.t+ih-y0,fill:'var(--crit)','fill-opacity':.07}));
  /* grid */
  ticks(xlo,xhi,5).forEach(function(t2){
    hline(s,px(t2),m.t,px(t2),m.t+ih,'var(--grid)',1);
    axTick(s,px(t2),H-6,R(t2),'middle',9.5);
  });
  ticks(ylo,yhi,5).forEach(function(t2){
    hline(s,m.l,py(t2),m.l+iw,py(t2),'var(--grid)',1);
    axTick(s,m.l-6,py(t2)+4,R(t2),'end',9.5);
  });
  vline(s,x0,m.t,x0,m.t+ih); hline(s,m.l,y0,m.l+iw,y0,'var(--axis)',1.5);
  /* axis labels */
  s.appendChild(txt(m.l+iw/2,H-1,'CM2 / unit →',{'text-anchor':'middle','font-size':11,fill:'var(--ink-2)'}));
  s.appendChild(txt(-(m.t+ih/2),13,'← EBITDA / unit',{'text-anchor':'middle','font-size':11,fill:'var(--ink-2)',transform:'rotate(-90)'}));
  /* quadrant labels */
  s.appendChild(txt(x0+6,m.t+12,'STAR (CM2+ / EBITDA+)',{'font-size':9.5,'font-weight':600,fill:'var(--good)'}));
  s.appendChild(txt(x0+6,m.t+ih-6,'OVERHEAD HEAVY',{'font-size':9.5,'font-weight':600,fill:'#8a6100'}));
  s.appendChild(txt(m.l+4,m.t+ih-6,'LOSS MAKING',{'font-size':9.5,'font-weight':600,fill:'var(--crit)'}));
  /* bubbles */
  var sorted=[].concat(prods).sort(function(a,b){ return (b.rev||0)-(a.rev||0); });
  sorted.forEach(function(p){
    var cx=px(p.cx||0), cy=py(p.cy||0), r=rad(p.rev||0);
    var c=el('circle',{cx:cx,cy:cy,r:r,fill:QC[p.quad]||'var(--ink-3)','fill-opacity':0.65,stroke:'var(--surface-1)','stroke-width':2});
    bind(c,'<b>'+esc(p.key)+'</b><div>'+esc(p.cat)+' · '+nf.format(p.units)+' units</div><div>Revenue '+R(p.rev)+'</div><div>CM2/unit '+R(p.cx)+'</div><div>EBITDA/unit '+R(p.cy)+' ('+P(p.ebpct)+')</div><div>Marketing/unit '+R(p.mktg)+'</div><div style="margin-top:4px;color:'+QC[p.quad]+';font-weight:600">'+(QN[p.quad]||p.quad)+'</div>');
    s.appendChild(c);
  });
  host.appendChild(s);
}

/* ── D. Revenue vs EBITDA scatter ── */
function renderVisD(chanKey){
  var host=document.getElementById('vis-D-chart'); if(!host) return;
  host.innerHTML='';
  var prods=[];
  if(chanKey==='website') prods=D.periods.apr.products.map(function(p){ return {key:p.key,cat:p.cat,rev:p.rev,ebitda:p.ebitda_t,units:p.units,cm2:p.cm2_t,ebpct:p.ebitdapct}; });
  else if(chanKey==='amazon') prods=D_AMZ.products.map(function(p){ return {key:p.key,cat:p.cat,rev:p.rev_t||p.netrev_t||0,ebitda:p.ebitda_t,units:p.units,cm2:p.cm2_t,ebpct:p.ebitdapct}; });
  else if(chanKey==='firstcry') prods=D_FC.products.map(function(p){ return {key:p.key,cat:p.cat,rev:p.rev_t||0,ebitda:p.ebitda_t,units:p.units,cm2:p.cm2_t||0,ebpct:p.ebitdapct}; });
  else if(chanKey==='blinkit') prods=D_BL.products.map(function(p){ return {key:p.key,cat:p.cat,rev:p.rev_t||0,ebitda:p.ebitda_t,units:p.units,cm2:p.cm2_t||0,ebpct:p.ebitdapct}; });

  var W=620,H=380,m={t:16,r:16,b:50,l:80};
  var iw=W-m.l-m.r, ih=H-m.t-m.b;
  var revs=prods.map(function(p){ return p.rev||0; });
  var ebitdas=prods.map(function(p){ return p.ebitda||0; });
  var maxR=Math.max.apply(null,revs)||1;
  var minE=Math.min.apply(null,ebitdas)*1.1, maxE=Math.max.apply(null,ebitdas)*1.1;
  if(maxE<0) maxE=0;
  var er=maxE-minE||1;
  var px2=function(v){ return m.l+v/maxR*iw; };
  var py2=function(v){ return m.t+ih-(v-minE)/er*ih; };
  var rad2=function(v){ return 4+Math.sqrt(Math.max(v,0)/Math.max.apply(null,prods.map(function(p){ return p.units||0; })))*18; };
  var s=el('svg',{viewBox:'0 0 '+W+' '+H,'aria-label':'Revenue vs EBITDA'});
  var y0=py2(0);
  s.appendChild(el('rect',{x:m.l,y:y0,width:iw,height:m.t+ih-y0,fill:'var(--crit)','fill-opacity':.05}));
  s.appendChild(el('rect',{x:m.l,y:m.t,width:iw,height:y0-m.t,fill:'var(--good)','fill-opacity':.05}));
  ticks(0,maxR,5).forEach(function(t2){ hline(s,px2(t2),m.t,px2(t2),m.t+ih,'var(--grid)',1); axTick(s,px2(t2),H-6,Rs(t2),'middle',9); });
  ticks(minE,maxE,5).forEach(function(t2){ hline(s,m.l,py2(t2),m.l+iw,py2(t2),'var(--grid)',1); axTick(s,m.l-6,py2(t2)+4,Rs(t2),'end',9); });
  hline(s,m.l,y0,m.l+iw,y0,'var(--axis)',1.5);
  s.appendChild(txt(m.l+iw/2,H-1,'Revenue →',{'text-anchor':'middle','font-size':11,fill:'var(--ink-2)'}));
  s.appendChild(txt(-(m.t+ih/2),12,'← EBITDA',{'text-anchor':'middle','font-size':11,fill:'var(--ink-2)',transform:'rotate(-90)'}));
  s.appendChild(txt(m.l+4,y0-5,'Profitable zone',{'font-size':9.5,'font-weight':600,fill:'var(--good)'}));
  s.appendChild(txt(m.l+4,y0+13,'Loss zone',{'font-size':9.5,'font-weight':600,fill:'var(--crit)'}));
  var sorted2=[].concat(prods).sort(function(a,b){ return (b.rev||0)-(a.rev||0); });
  sorted2.forEach(function(p){
    var cx=px2(p.rev||0), cy=py2(p.ebitda||0), r=rad2(p.units||1);
    var positive=(p.ebitda||0)>=0;
    var c=el('circle',{cx:cx,cy:cy,r:r,fill:positive?'var(--good)':'var(--crit)','fill-opacity':0.6,stroke:'var(--surface-1)','stroke-width':2});
    bind(c,'<b>'+esc(p.key)+'</b><div>'+esc(p.cat)+' · '+nf.format(p.units)+' units</div><div>Revenue '+R(p.rev)+'</div><div>CM2 '+R(p.cm2)+'</div><div>EBITDA '+R(p.ebitda)+' ('+P(p.ebpct)+')</div>');
    s.appendChild(c);
  });
  host.appendChild(s);
}

/* ── E. Top/Bottom EBITDA Products ── */
function renderVisE(metricKey, viewKey, chanKey){
  var host=document.getElementById('vis-E-chart'); if(!host) return;
  host.innerHTML='';
  var prods=[];
  if(chanKey==='website') prods=D.periods.apr.products.map(function(p){ return {key:p.key,cat:p.cat,rev:p.rev,cm2:p.cm2_t,ebitda:p.ebitda_t,cm2pct:p.cm2pct,ebpct:p.ebitdapct}; });
  else if(chanKey==='amazon') prods=D_AMZ.products.map(function(p){ return {key:p.key,cat:p.cat,rev:p.rev_t||0,cm2:p.cm2_t,ebitda:p.ebitda_t,cm2pct:p.cm2pct,ebpct:p.ebitdapct}; });
  else if(chanKey==='firstcry') prods=D_FC.products.map(function(p){ return {key:p.key,cat:p.cat,rev:p.rev_t||0,cm2:p.cm2_t||0,ebitda:p.ebitda_t,cm2pct:p.cm2pct,ebpct:p.ebitdapct}; });
  else if(chanKey==='blinkit') prods=D_BL.products.map(function(p){ return {key:p.key,cat:p.cat,rev:p.rev_t||0,cm2:p.cm2_t||0,ebitda:p.ebitda_t,cm2pct:p.cm2pct,ebpct:p.ebitdapct}; });

  var field=metricKey==='rev'?'rev':metricKey==='cm2'?'cm2':'ebitda';
  var sorted=[].concat(prods).sort(function(a,b){ return (b[field]||0)-(a[field]||0); });
  var rows=viewKey==='top10'?sorted.slice(0,10):viewKey==='bottom10'?sorted.slice(-10).reverse():sorted.slice(0,10);
  var lo=Math.min.apply(null,rows.map(function(r){ return r[field]||0; }))*1.08;
  var hi=Math.max.apply(null,rows.map(function(r){ return r[field]||0; }))*1.15;
  if(lo>0) lo=0; if(hi<0) hi=0;
  var range=hi-lo||1;
  var W=620,rh=22,m={t:8,r:110,b:28,l:130};
  var H=m.t+m.b+rows.length*rh;
  var x3=function(v){ return m.l+(v-lo)/range*(W-m.l-m.r); };
  var s=el('svg',{viewBox:'0 0 '+W+' '+H,'aria-label':'Top bottom products by '+field});
  ticks(lo,hi,5).forEach(function(t2){
    hline(s,x3(t2),m.t,x3(t2),m.t+rows.length*rh,'var(--grid)',1);
    axTick(s,x3(t2),H-8,Rs(t2),'middle',9.5);
  });
  hline(s,x3(0),m.t,x3(0),m.t+rows.length*rh,'var(--axis)',1.5);
  rows.forEach(function(r,i){
    var y=m.t+i*rh+2,bh=rh-6,v=r[field]||0;
    var bx=Math.min(x3(0),x3(v)),bw=Math.abs(x3(v)-x3(0));
    var fill=v>=0?'var(--pos)':'var(--neg)';
    var b=bar(bx,y,Math.max(bw,1.5),bh,3,v>=0?'right':'left');
    b.setAttribute('fill',fill); b.setAttribute('fill-opacity',0.7);
    bind(b,'<b>'+esc(r.key)+'</b><div>'+esc(r.cat)+'</div><div>Revenue '+R(r.rev)+'</div><div>CM2 '+R(r.cm2)+' ('+P(r.cm2pct)+')</div><div>EBITDA '+R(r.ebitda)+' ('+P(r.ebpct)+')</div>');
    s.appendChild(b);
    var lbl=r.key; if(lbl.length>18) lbl=lbl.slice(0,17)+'\u2026';
    s.appendChild(txt(m.l-5,y+bh-3,lbl,{'text-anchor':'end','font-size':10.5,fill:'var(--ink-1)'}));
    s.appendChild(txt(W-4,y+bh-3,Rs(v),{'text-anchor':'end','font-size':9.5,'font-weight':600,fill:v>=0?'var(--pos)':'var(--ink-2)'}));
  });
  host.appendChild(s);
}

/* ── F. Cost Structure waterfall ── */
function renderVisF(chanKey){
  var host=document.getElementById('vis-F-chart'); if(!host) return;
  host.innerHTML='';
  var D2=chanKey==='amazon'?D_AMZ:chanKey==='firstcry'?D_FC:chanKey==='blinkit'?D_BL:null;
  if(!D2){ host.innerHTML='<p class="note">Select a channel above.</p>'; return; }
  var stagesFn=chanKey==='amazon'?amazonWfStages:chanKey==='firstcry'?firstcryWfStages:blinkitWfStages;
  var stages=stagesFn(D2);
  var dom=[Math.min(D2.tot.ebitda,0)*1.06, D2.tot.rev*1.04];
  var breakMap={amazon:'Cost of Advertising',firstcry:'Firstcry Margin',blinkit:'Marketing + Blinkit Margin'};
  var breakLabel=breakMap[chanKey];
  var callout='';
  host.appendChild(chartWaterfallC(stages, D2.tot.rev, dom, callout));
}

/* ── G. Pareto with 50%/80%/90% thresholds ── */
function renderVisG(chanKey){
  var host=document.getElementById('vis-G-chart'); if(!host) return;
  host.innerHTML='';
  var prods=[];
  if(chanKey==='website') prods=D.periods.apr.products.map(function(p){ return {key:p.key,rev:p.rev||0}; });
  else if(chanKey==='amazon') prods=D_AMZ.products.map(function(p){ return {key:p.key,rev:p.rev_t||p.netrev_t||0}; });
  else if(chanKey==='firstcry') prods=D_FC.products.map(function(p){ return {key:p.key,rev:p.rev_t||0}; });
  else if(chanKey==='blinkit') prods=D_BL.products.map(function(p){ return {key:p.key,rev:p.rev_t||0}; });

  var sorted=[].concat(prods).sort(function(a,b){ return b.rev-a.rev; }).filter(function(p){ return p.rev>0; });
  var tot=sorted.reduce(function(s,p){ return s+p.rev; },0); if(!tot) return;
  var cum=0;
  sorted.forEach(function(p){ cum+=p.rev/tot*100; p.cum=cum; });

  var W=620,H=300,m={t:20,r:16,b:44,l:44};
  var iw=W-m.l-m.r, ih=H-m.t-m.b;
  var n=sorted.length, bw=iw/n;
  var x4=function(i){ return m.l+i*bw; };
  var y4=function(v){ return m.t+ih-v/100*ih; };
  var s=el('svg',{viewBox:'0 0 '+W+' '+H,'aria-label':'Pareto revenue'});
  [0,20,40,60,80,100].forEach(function(t2){
    hline(s,m.l,y4(t2),m.l+iw,y4(t2),'var(--grid)',1);
    axTick(s,m.l-6,y4(t2)+4,t2+'%','end',9.5);
  });
  /* threshold lines */
  [[50,'var(--s2)'],[80,'var(--warn)'],[90,'var(--crit)']].forEach(function(th){
    var ty=y4(th[0]);
    hline(s,m.l,ty,m.l+iw,ty,th[1],1.5);
    s.appendChild(el('path',{d:'M'+(m.l+iw)+','+ty,stroke:th[1],'stroke-width':1.5,'stroke-dasharray':'4 3',fill:'none'}));
    s.appendChild(txt(m.l+iw+2,ty+4,th[0]+'%',{'font-size':9,'font-weight':700,fill:th[1]}));
    /* label: how many products to reach */
    var cnt=0;
    for(var idx=0;idx<sorted.length;idx++){ if(sorted[idx].cum>=th[0]){ cnt=idx+1; break; } }
    s.appendChild(txt(m.l+4,ty-3,cnt+' SKUs',{'font-size':8.5,'font-weight':600,fill:th[1]}));
  });
  /* bars */
  sorted.forEach(function(p,i){
    var h=ih-(y4(p.rev/tot*100)-m.t);
    var b=bar(x4(i)+0.5,y4(p.rev/tot*100),Math.max(bw-1,1),h,Math.min(2,bw/2),'top');
    b.setAttribute('fill','var(--s1)'); b.setAttribute('fill-opacity',0.55);
    bind(b,'<b>'+esc(p.key)+'</b><div>Revenue '+R(p.rev)+'</div><div>Share '+P(p.rev/tot*100)+'</div><div>Cumulative '+P(p.cum)+'</div>');
    s.appendChild(b);
  });
  /* cumulative line */
  var linePts=sorted.map(function(p,i){ return (x4(i)+bw/2).toFixed(1)+','+y4(p.cum).toFixed(1); }).join(' L');
  s.appendChild(el('path',{d:'M'+linePts,fill:'none',stroke:'var(--s1)','stroke-width':2}));
  s.appendChild(txt(m.l+iw/2,H-2,'Products ranked by revenue (highest first) →',{'text-anchor':'middle','font-size':10.5,fill:'var(--ink-2)'}));
  host.appendChild(s);
}

/* ── H. Product × Channel Matrix ── */
function renderVisH(sortKey){
  var host=document.getElementById('vis-H-table'); if(!host) return;
  var chanOrder=['website','amazon','firstcry','blinkit'];
  var chanLabel=['Website','Amazon','FirstCry','Blinkit'];
  var allKeys={};
  function tagOf(q){ return q?('<span class="matrix-tag '+q+'">'+(q==='star'?'★ Star':q==='overhead'?'⬡ Overhead':'✗ Loss')+'</span>'):'<span class="matrix-tag notlisted">Not listed</span>'; }
  function getRevTotal(e){
    var t=0;
    if(e.w) t+=e.w.rev||0;
    if(e.a) t+=e.a.rev_t||e.a.netrev_t||0;
    if(e.f) t+=e.f.rev_t||0;
    if(e.b) t+=e.b.rev_t||0;
    return t;
  }
  function getProfitCount(e){
    var n=0;
    if(e.w&&e.w.quad==='star') n++;
    if(e.a&&e.a.quad==='star') n++;
    if(e.f&&e.f.quad==='star') n++;
    if(e.b&&e.b.quad==='star') n++;
    return n;
  }
  function getBestEbitda(e){
    var best=null;
    [e.w,e.a,e.f,e.b].forEach(function(p){ if(p&&(best===null||p.ebitda_t>best)) best=p.ebitda_t; });
    return best;
  }
  /* build index */
  D.periods.apr.products.forEach(function(p){ if(!allKeys[p.key]) allKeys[p.key]={k:p.key}; allKeys[p.key].w=p; });
  D_AMZ.products.forEach(function(p){ if(!allKeys[p.key]) allKeys[p.key]={k:p.key}; allKeys[p.key].a=p; });
  D_FC.products.forEach(function(p){ if(!allKeys[p.key]) allKeys[p.key]={k:p.key}; allKeys[p.key].f=p; });
  D_BL.products.forEach(function(p){ if(!allKeys[p.key]) allKeys[p.key]={k:p.key}; allKeys[p.key].b=p; });

  var entries=Object.values(allKeys);
  entries.sort(function(a,b){
    if(sortKey==='profitable') return getProfitCount(b)-getProfitCount(a);
    if(sortKey==='rev') return getRevTotal(b)-getRevTotal(a);
    if(sortKey==='ebitda') return (getBestEbitda(b)||0)-(getBestEbitda(a)||0);
    return getRevTotal(b)-getRevTotal(a);
  });

  var rows=entries.map(function(e){
    return '<tr><td style="min-width:140px"><b>'+esc(e.k)+'</b></td>'
      +chanOrder.map(function(c){ var p=e[c.charAt(0)]; return '<td class="matrix-cell">'+tagOf(p?p.quad:null)+'</td>'; }).join('')
      +'<td class="n" style="font-size:11px">'+getProfitCount(e)+'/4</td>'
      +'<td class="n" style="font-size:11px">'+Rs(getRevTotal(e))+'</td></tr>';
  }).join('');

  host.innerHTML='<table><thead><tr><th>Product</th>'+chanLabel.map(function(l){ return '<th>'+l+'</th>'; }).join('')+'<th>Stars</th><th>Total Rev</th></tr></thead><tbody>'+rows+'</tbody></table>';
}

/* ── I. Product Action Distribution ── */
function renderVisI(chanKey){
  var host=document.getElementById('vis-I-chart'); if(!host) return;
  host.innerHTML='';
  var prods=[];
  if(chanKey==='website') prods=D.periods.apr.products.filter(function(p){ return p.act; });
  else if(chanKey==='amazon') prods=D_AMZ.products.filter(function(p){ return p.act; });
  /* FC and BL don't have act fields — derive from quad */
  else if(chanKey==='firstcry') prods=D_FC.products.map(function(p){ return {act:p.quad==='star'?'scale':p.quad==='overhead'?'overhead':'cut'}; });
  else if(chanKey==='blinkit') prods=D_BL.products.map(function(p){ return {act:p.quad==='star'?'scale':p.quad==='overhead'?'overhead':'cut'}; });

  var counts={scale:0,overhead:0,page:0,cut:0,delist:0};
  prods.forEach(function(p){ if(counts[p.act]!=null) counts[p.act]++; });
  var rows=[
    {act:'scale',label:'Scale',n:counts.scale,color:'var(--good)'},
    {act:'overhead',label:'Hold / Monitor',n:counts.overhead,color:'var(--warn)'},
    {act:'page',label:'Fix Page First',n:counts.page,color:'var(--s1)'},
    {act:'cut',label:'Cut Spend / Discontinue',n:counts.cut,color:'var(--crit)'},
    {act:'delist',label:'Reprice or Delist',n:counts.delist,color:'var(--crit)'},
  ].filter(function(r){ return r.n>0; }).sort(function(a,b){ return b.n-a.n; });

  if(!rows.length){ host.innerHTML='<p class="note muted">No action data for this channel.</p>'; return; }
  var maxN=rows[0].n, W=520, rh=28, m={t:8,r:70,b:16,l:160};
  var H=m.t+m.b+rows.length*rh;
  var iw=W-m.l-m.r;
  var x5=function(v){ return m.l+v/maxN*iw; };
  var s=el('svg',{viewBox:'0 0 '+W+' '+H,'aria-label':'Action distribution'});
  rows.forEach(function(r,i){
    var y=m.t+i*rh+3, bh=rh-8;
    var bw=x5(r.n)-m.l;
    var b=bar(m.l,y,Math.max(bw,2),bh,3,'right'); b.setAttribute('fill',r.color); b.setAttribute('fill-opacity',0.7);
    bind(b,'<b>'+r.label+'</b><div>'+r.n+' products</div>');
    s.appendChild(b);
    s.appendChild(txt(m.l-6,y+bh-3,r.label,{'text-anchor':'end','font-size':10.5,'font-weight':600,fill:'var(--ink-1)'}));
    s.appendChild(txt(x5(r.n)+5,y+bh-3,r.n,{'font-size':10.5,'font-weight':700,fill:'var(--ink-1)'}));
  });
  host.appendChild(s);
}

/* ── Wire controls ── */
function setupInsightsControls(){
  /* C */
  var cChan='website';
  makeSegCtrl('vis-C-ctrls',[{v:'website',t:'Website'},{v:'amazon',t:'Amazon'},{v:'firstcry',t:'FirstCry'},{v:'blinkit',t:'Blinkit'}],function(v){ cChan=v; renderVisC(v); });
  /* D */
  var dChan='website';
  makeSegCtrl('vis-D-ctrls',[{v:'website',t:'Website'},{v:'amazon',t:'Amazon'},{v:'firstcry',t:'FirstCry'},{v:'blinkit',t:'Blinkit'}],function(v){ dChan=v; renderVisD(v); });
  /* E */
  var eMet='ebitda', eView='top10', eChan='website';
  var updateE=function(){ renderVisE(eMet,eView,eChan); };
  makeSegCtrl('vis-E-ctrls',[{v:'ebitda',t:'EBITDA'},{v:'rev',t:'Revenue'},{v:'cm2',t:'CM2'}],function(v){ eMet=v; updateE(); });
  /* F */
  makeSegCtrl('vis-F-ctrls',[{v:'amazon',t:'Amazon'},{v:'firstcry',t:'FirstCry'},{v:'blinkit',t:'Blinkit'}],function(v){ renderVisF(v); });
  /* G */
  var gChan='website';
  makeSegCtrl('vis-G-ctrls',[{v:'website',t:'Website'},{v:'amazon',t:'Amazon'},{v:'firstcry',t:'FirstCry'},{v:'blinkit',t:'Blinkit'}],function(v){ gChan=v; renderVisG(v); });
  /* H */
  makeSegCtrl('vis-H-ctrls',[{v:'rev',t:'By Revenue'},{v:'profitable',t:'By Stars'},{v:'ebitda',t:'By Best EBITDA'}],function(v){ renderVisH(v); });
  /* I */
  makeSegCtrl('vis-I-ctrls',[{v:'website',t:'Website'},{v:'amazon',t:'Amazon'},{v:'firstcry',t:'FirstCry'},{v:'blinkit',t:'Blinkit'}],function(v){ renderVisI(v); });
}

/* ── Main render (lazy, fires when tab first opened) ── */
function renderInsights(){
  renderVisA();
  renderVisB();
  renderVisC('website');
  renderVisD('website');
  renderVisE('ebitda','top10','website');
  renderVisF('amazon');
  renderVisG('website');
  renderVisH('rev');
  renderVisI('website');
  setupInsightsControls();
}

/* ── Wire the Insights chan-panel ── */
(function(){
  var panel=document.getElementById('chan-insights');
  if(!panel) return;
  var rendered=false;
  /* The main chan-switch handler already shows/hides .chan-panel — we just need to fire render on first open */
  var origSwitch=document.querySelector('.chan-switch');
  if(origSwitch){
    origSwitch.addEventListener('click',function(e){
      var b=e.target.closest('[data-chan="insights"]');
      if(b && !rendered){ renderInsights(); rendered=true; }
    });
  }
})();

})(); /* end IIFE */
"""

# ── Assemble injection script ─────────────────────────────────────────────
with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS before </style>
css_anchor = '</style>'
html = html.replace(css_anchor, CSS + '\n' + css_anchor, 1)
print('CSS injected')

# 2. Add nav button after analysis button
old_btn = '<button role="tab" aria-selected="false" data-chan="analysis">Channel Analysis</button>'
new_btn = old_btn + '\n    ' + NAV_BTN
html = html.replace(old_btn, new_btn, 1)
print('Nav button injected')

# 3. Add panel HTML before the tip div
tip_anchor = '<div class="tip" id="tip"></div>'
html = html.replace(tip_anchor, PANEL_HTML + '\n' + tip_anchor, 1)
print('Panel HTML injected')

# 4. Add JS before </script> (last one)
last_script_end = html.rfind('</script>')
html = html[:last_script_end] + '\n' + JS + '\n' + html[last_script_end:]
print('JS injected')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Written. Size:', len(html))
