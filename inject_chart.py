"""
Replaces the Per-Product Breakdown static table with a bar chart + scatter + collapsible table.
"""
import json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# locate table boundaries
h2_start = html.find('<h2>Per-Product Breakdown</h2>')
table_div_start = html.find('<div class="tw"><table>', h2_start)
table_div_end   = html.find('</table></div>', table_div_start) + len('</table></div>')
original_table  = html[table_div_start:table_div_end]
print('Table span:', table_div_start, '-', table_div_end, '(%d chars)' % (table_div_end - table_div_start))

PRODS = [
  {"name":"magic paint dust","units":279,"rev":228058,"cm2u":-333},
  {"name":"Playdough","units":270,"rev":224974,"cm2u":-393},
  {"name":"FP8+CB","units":144,"rev":172949,"cm2u":72},
  {"name":"SFP","units":231,"rev":127623,"cm2u":-161},
  {"name":"SFP+CB","units":112,"rev":106738,"cm2u":49},
  {"name":"SFP+JB","units":98,"rev":98611,"cm2u":224},
  {"name":"FP8+AR+CB","units":53,"rev":95282,"cm2u":270},
  {"name":"FP8,B8,CB","units":57,"rev":89346,"cm2u":182},
  {"name":"FP3","units":140,"rev":81603,"cm2u":-94},
  {"name":"B3","units":145,"rev":74752,"cm2u":-469},
  {"name":"FP8","units":73,"rev":61630,"cm2u":21},
  {"name":"AR","units":93,"rev":59084,"cm2u":-13},
  {"name":"MPD+JB","units":42,"rev":52670,"cm2u":-57},
  {"name":"Apron","units":69,"rev":48589,"cm2u":-27},
  {"name":"MPD+AR","units":33,"rev":46749,"cm2u":-62},
  {"name":"ABC Kit","units":81,"rev":46506,"cm2u":193},
  {"name":"Canvas Kit","units":76,"rev":45846,"cm2u":-607},
  {"name":"Stamp kit","units":46,"rev":42022,"cm2u":49},
  {"name":"T&F","units":45,"rev":37339,"cm2u":-64},
  {"name":"Preschool kit","units":68,"rev":36114,"cm2u":-287},
  {"name":"SJ+B8","units":41,"rev":34809,"cm2u":-187},
  {"name":"SJ+SFP+CB","units":24,"rev":32541,"cm2u":320},
  {"name":"DP","units":93,"rev":31190,"cm2u":-132},
  {"name":"SR+Playdough","units":20,"rev":28525,"cm2u":85},
  {"name":"B8","units":66,"rev":27680,"cm2u":-193},
]
prods_json = json.dumps(PRODS)

# ── HTML wrapper (no curly braces that could confuse anything) ─────────────
CHARTS_HTML = (
'<!-- Per-Product Breakdown: charts + collapsible table -->\n'
'<div style="margin-bottom:10px">\n'
'  <div class="ctrls" style="margin-bottom:10px">\n'
'    <div class="seg" id="ppb-toggle">\n'
'      <button aria-pressed="true"  data-view="bar">Bar chart</button>\n'
'      <button aria-pressed="false" data-view="scatter">Scatter</button>\n'
'    </div>\n'
'    <span class="muted" style="font-size:12px;margin-left:8px">'
'Top 25 products &middot; sorted by Rev w/ GST &darr; &middot; '
'<span style="display:inline-block;width:60px;height:9px;border-radius:2px;vertical-align:middle;'
'background:linear-gradient(to right,rgb(253,53,16),rgb(140,163,26),rgb(0,200,50))"></span>'
' colour = CM2/unit (red = negative, green = positive)</span>\n'
'  </div>\n'
'  <div class="chart" id="ppb-bar-wrap"></div>\n'
'  <div class="chart" id="ppb-scat-wrap" hidden></div>\n'
'</div>\n'
'<details id="ppb-details" style="margin-top:8px">\n'
'  <summary style="cursor:pointer;font-size:13px;color:var(--ink-2);padding:6px 2px;'
'user-select:none;list-style:none">&#9658; Show full table (all products)</summary>\n'
'  <p class="note" style="margin-top:6px">All products sorted by 3-month revenue with GST descending.</p>\n'
+ original_table +
'\n</details>\n'
)

# ── JavaScript (no Python f-string — written as raw string, __PRODS__ substituted) ──
JS = r"""<script>
(function(){
  var PRODS=__PRODS__;
  var NS='http://www.w3.org/2000/svg';

  /* diverging colour: red at -600, neutral grey-green at 0, green at +600 */
  function cm2col(v){
    var c=600,t=Math.max(-c,Math.min(c,v))/c;
    var r,g,b;
    if(t>=0){ r=Math.round(140-140*t);g=Math.round(163+92*t);b=30; }
    else     { var tt=-t;r=Math.round(140+113*tt);g=Math.round(163-110*tt);b=30; }
    return 'rgb('+r+','+g+','+b+')';
  }
  function se(tag,a){ var e=document.createElementNS(NS,tag); for(var k in a) e.setAttribute(k,a[k]); return e; }
  function st(x,y,s,anchor,sz,fill,bold){
    var e=se('text',{x:x,y:y,'text-anchor':anchor||'middle','font-size':sz||10,fill:fill||'var(--ink-3)'});
    if(bold)e.setAttribute('font-weight','600'); e.textContent=s; return e;
  }
  function sl(x1,y1,x2,y2,stroke,sw){ return se('line',{x1:x1,y1:y1,x2:x2,y2:y2,stroke:stroke||'var(--grid)','stroke-width':sw||1}); }
  function tip(el,html){
    el.addEventListener('mousemove',function(e){
      var t=document.getElementById('tip'); if(!t)return;
      t.innerHTML=html; t.style.opacity=1;
      var bx=e.clientX+14,by=e.clientY+14;
      if(bx+(t.offsetWidth||220)>window.innerWidth-8) bx=e.clientX-(t.offsetWidth||220)-14;
      if(by+(t.offsetHeight||100)>window.innerHeight-8) by=e.clientY-(t.offsetHeight||100)-14;
      t.style.left=bx+'px';t.style.top=by+'px';
    });
    el.addEventListener('mouseleave',function(){var t=document.getElementById('tip');if(t)t.style.opacity=0;});
  }
  function fmtRev(v){ return '\u20b9'+v.toLocaleString('en-IN'); }
  function fmtCm2(v){ return (v>=0?'+':'')+v+'/u'; }

  /* =========== BAR CHART =========== */
  function drawBar(){
    var host=document.getElementById('ppb-bar-wrap');
    if(!host)return; host.innerHTML='';
    var W=680,rh=28,m={t:10,r:120,b:30,l:116};
    var H=m.t+m.b+PRODS.length*rh;
    var maxRev=PRODS[0].rev, iw=W-m.l-m.r;
    var xS=function(v){return m.l+v/maxRev*iw;};
    var svg=se('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':'Product revenue bar chart'});

    /* vertical grid + x-axis tick labels */
    for(var g=50000;g<=maxRev;g+=50000){
      svg.appendChild(sl(xS(g),m.t,xS(g),m.t+PRODS.length*rh));
      svg.appendChild(st(xS(g),H-7,'\u20b9'+(g/1000)+'k','middle',9.5));
    }

    PRODS.forEach(function(p,i){
      var y=m.t+i*rh+4, bh=rh-9;
      var bw=Math.max(xS(p.rev)-m.l,2);
      var fill=cm2col(p.cm2u);

      /* bar */
      var rect=se('rect',{x:m.l,y:y,width:bw,height:bh,rx:3,fill:fill,'fill-opacity':0.84});
      var th='<b>'+p.name+'</b>'
        +'<div>Revenue '+fmtRev(p.rev)+'</div>'
        +'<div>Units '+p.units+'</div>'
        +'<div>CM2/unit '+fmtCm2(p.cm2u)+'</div>'
        +'<div style="margin-top:4px;color:'+(p.cm2u>=0?'var(--good)':'var(--crit)')+';font-weight:600">'
        +(p.cm2u>=0?'\u2714 CM2 positive':'\u26a0 CM2 negative')+'</div>';
      tip(rect,th); svg.appendChild(rect);

      /* product name label */
      var nm=p.name.length>16?p.name.slice(0,15)+'\u2026':p.name;
      svg.appendChild(st(m.l-5,y+bh-2,nm,'end',10.5,'var(--ink-1)',true));

      /* CM2/unit data label at bar end */
      var lx=xS(p.rev)+5;
      var dlbl=se('text',{x:lx,y:y+bh-2,'font-size':9.5,'font-weight':'700',
        fill:p.cm2u>=0?'var(--good)':'var(--crit)'});
      dlbl.textContent=fmtCm2(p.cm2u);
      svg.appendChild(dlbl);
    });

    /* colour scale legend */
    var defs=se('defs',{});
    var grad=se('linearGradient',{id:'ppbcgrad',x1:'0',x2:'1',y1:'0',y2:'0'});
    [['0%','rgb(253,53,16)'],['50%','rgb(140,163,30)'],['100%','rgb(0,200,50)']].forEach(function(s){
      grad.appendChild(se('stop',{offset:s[0],'stop-color':s[1]}));
    });
    defs.appendChild(grad); svg.appendChild(defs);
    var lx=m.l, ly=H-14, lw=190;
    svg.appendChild(se('rect',{x:lx,y:ly-9,width:lw,height:7,rx:2,fill:'url(#ppbcgrad)'}));
    [[lx,'\u2212600'],[(lx+lw/2),'0'],[(lx+lw),'+600']].forEach(function(p2){
      svg.appendChild(st(p2[0],ly+4,p2[1],'middle',8.5));
    });
    svg.appendChild(st(lx+lw+7,ly+1,'CM2/unit','start',8.5,'var(--ink-2)'));

    host.appendChild(svg);
  }

  /* =========== SCATTER CHART =========== */
  function drawScatter(){
    var host=document.getElementById('ppb-scat-wrap');
    if(!host)return; host.innerHTML='';
    var W=680,H=390,m={t:20,r:24,b:50,l:68};
    var iw=W-m.l-m.r, ih=H-m.t-m.b;
    var maxRev=PRODS[0].rev;
    var ylo=-720, yhi=380;
    var px=function(v){return m.l+v/maxRev*iw;};
    var py=function(v){return m.t+ih-(Math.max(ylo,Math.min(yhi,v))-ylo)/(yhi-ylo)*ih;};
    var maxU=Math.max.apply(null,PRODS.map(function(p){return p.units;}));
    var rad=function(u){return 4+Math.sqrt(u/maxU)*22;};
    var svg=se('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':'Revenue vs CM2/unit scatter'});

    /* background zones */
    var y0=py(0);
    svg.appendChild(se('rect',{x:m.l,y:m.t,width:iw,height:y0-m.t,fill:'var(--good)','fill-opacity':0.05}));
    svg.appendChild(se('rect',{x:m.l,y:y0,width:iw,height:m.t+ih-y0,fill:'var(--crit)','fill-opacity':0.06}));

    /* grid */
    for(var xg=0;xg<=maxRev;xg+=50000){
      svg.appendChild(sl(px(xg),m.t,px(xg),m.t+ih));
      svg.appendChild(st(px(xg),H-5,'\u20b9'+(xg/1000)+'k','middle',9));
    }
    [-600,-400,-200,-100,0,100,200,300].forEach(function(yv){
      if(yv>=ylo&&yv<=yhi){
        svg.appendChild(sl(m.l,py(yv),m.l+iw,py(yv)));
        svg.appendChild(st(m.l-5,py(yv)+4,(yv>0?'+':'')+yv,'end',9));
      }
    });
    svg.appendChild(sl(m.l,y0,m.l+iw,y0,'var(--axis)',1.5));
    svg.appendChild(st(m.l+iw/2,H-1,'Revenue (w/ GST) \u2192','middle',11,'var(--ink-2)'));
    var yl=st(11,m.t+ih/2,'CM2 / unit','middle',11,'var(--ink-2)');
    yl.setAttribute('transform','rotate(-90,11,'+(m.t+ih/2)+')'); svg.appendChild(yl);
    svg.appendChild(st(m.l+5,m.t+14,'\u25b2 CM2 positive','start',9.5,'var(--good)',true));
    svg.appendChild(st(m.l+5,y0+14,'\u25bc CM2 negative','start',9.5,'var(--crit)',true));

    /* bubbles — negatives first so positives sit on top */
    var sorted=[].concat(PRODS).sort(function(a,b){return a.cm2u-b.cm2u;});
    sorted.forEach(function(p){
      var cx=px(p.rev), cy=py(p.cm2u), r=rad(p.units);
      var c=se('circle',{cx:cx,cy:cy,r:r,fill:cm2col(p.cm2u),'fill-opacity':0.72,
        stroke:'var(--surface-1)','stroke-width':1.5});
      var isOutlier=p.cm2u<0&&p.rev>50000;
      var th='<b>'+p.name+'</b>'
        +'<div>Revenue '+fmtRev(p.rev)+'</div>'
        +'<div>Units '+p.units+'</div>'
        +'<div>CM2/unit '+fmtCm2(p.cm2u)+'</div>'
        +(isOutlier?'<div style="margin-top:4px;color:var(--crit);font-weight:600">\u26a0 High-rev / negative-margin outlier</div>':'');
      tip(c,th); svg.appendChild(c);

      /* label notable products */
      var flag=['magic paint dust','Playdough','B3','Canvas Kit','Activity Pack',
                'SFP+JB','FP8+AR+CB','SJ+SFP+CB','ABC Kit','SFP'];
      if(flag.indexOf(p.name)!==-1){
        var s2=p.name.length>13?p.name.slice(0,12)+'\u2026':p.name;
        svg.appendChild(st(cx+r+3,cy+4,s2,'start',9.5,'var(--ink-1)',true));
      }
    });

    /* bubble size legend */
    [[maxU,'max ('+maxU+'u)'],[Math.round(maxU/2),'mid'],[20,'20u']].forEach(function(leg,li){
      var lr=rad(leg[0]), lx=W-54, ly=m.t+20+li*44;
      svg.appendChild(se('circle',{cx:lx,cy:ly,r:lr,fill:'none',stroke:'var(--ink-3)','stroke-width':1}));
      svg.appendChild(st(lx+lr+4,ly+4,leg[1],'start',8.5));
    });
    svg.appendChild(st(W-54,m.t+8,'size=units','middle',8.5,'var(--ink-3)'));

    host.appendChild(svg);
  }

  /* initial render */
  drawBar();

  /* toggle */
  var seg=document.getElementById('ppb-toggle');
  if(seg){
    seg.addEventListener('click',function(e){
      var b=e.target.closest('button'); if(!b)return;
      Array.from(seg.children).forEach(function(x){x.setAttribute('aria-pressed',x===b);});
      var v=b.dataset.view;
      document.getElementById('ppb-bar-wrap').hidden=(v!=='bar');
      document.getElementById('ppb-scat-wrap').hidden=(v!=='scatter');
      if(v==='scatter') drawScatter();
    });
  }

  /* details toggle label */
  var det=document.getElementById('ppb-details');
  if(det){
    det.addEventListener('toggle',function(){
      det.querySelector('summary').textContent=
        det.open?'\u25be Hide full table (all products)':'\u25b8 Show full table (all products)';
    });
  }
})();
</script>
"""

JS = JS.replace('__PRODS__', prods_json)

REPLACEMENT = CHARTS_HTML + JS

new_html = html[:table_div_start] + REPLACEMENT + html[table_div_end:]
print('Replaced %d chars with %d chars' % (table_div_end - table_div_start, len(REPLACEMENT)))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print('Written. Size:', len(new_html))
