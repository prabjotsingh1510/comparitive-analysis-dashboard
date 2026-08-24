"""Generate the scatter plot HTML snippet and inject it into index.html."""
import json, re

with open('scatter_data.json', encoding='utf-8') as f:
    skus = json.load(f)

# Serialize the data compactly for embedding
sku_js = json.dumps(skus, ensure_ascii=False, separators=(',',':'))

# CSS for collapsible details
COLLAPSIBLE_CSS = """
  /* Collapsible DC sections */
  .dc-collapsible { margin-bottom: 12px; }
  .dc-collapsible > details { }
  .dc-collapsible > details > summary {
    list-style: none; cursor: pointer; user-select: none;
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; border-radius: 8px;
    background: var(--wash); border: 1px solid var(--border);
    font-size: 13px; font-weight: 600; color: var(--ink-2);
    transition: background .15s;
  }
  .dc-collapsible > details > summary:hover { background: var(--grid); color: var(--ink-1); }
  .dc-collapsible > details > summary::-webkit-details-marker { display: none; }
  .dc-collapsible > details[open] > summary { color: var(--ink-1); }
  .dc-chevron { display: inline-block; width: 14px; height: 14px; flex: none;
    transition: transform .2s; background: var(--ink-3);
    mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 6l4 4 4-4'/%3E%3C/svg%3E") center/14px no-repeat;
    -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 6l4 4 4-4'/%3E%3C/svg%3E") center/14px no-repeat; }
  .dc-collapsible > details[open] .dc-chevron { transform: rotate(180deg); }
  .dc-collapsible > details > .qa { margin-top: 8px; border-radius: 0 0 10px 10px; margin-bottom: 0; }
"""

SCATTER_HTML = r"""
<!-- ===== SCATTER PLOT: SKU Quadrant Map ===== -->
<div class="chart" style="margin-bottom:16px;padding:20px 18px 16px">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:14px">
    <div>
      <div style="font-size:15px;font-weight:700;letter-spacing:-0.01em;color:var(--ink-1)">SKU Quadrant Map — CM2/unit vs EBITDA/unit</div>
      <div style="font-size:12px;color:var(--ink-2);margin-top:3px">192 SKUs across all channels · dot size = units sold · hover for details · outliers shown at axis boundary (&#9650;)</div>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:8px 14px;font-size:11.5px;color:var(--ink-2);align-items:center">
      <span><svg width="10" height="10" style="vertical-align:-1px;margin-right:4px"><circle cx="5" cy="5" r="5" fill="#2a78d6"/></svg>Website</span>
      <span><svg width="10" height="10" style="vertical-align:-1px;margin-right:4px"><circle cx="5" cy="5" r="5" fill="#f59e0b"/></svg>Amazon</span>
      <span><svg width="10" height="10" style="vertical-align:-1px;margin-right:4px"><circle cx="5" cy="5" r="5" fill="#1baf7a"/></svg>FirstCry</span>
      <span><svg width="10" height="10" style="vertical-align:-1px;margin-right:4px"><circle cx="5" cy="5" r="5" fill="#e34948"/></svg>Blinkit</span>
      <span style="border-left:1px solid var(--border);padding-left:14px">
        <label style="display:flex;align-items:center;gap:5px;cursor:pointer;font-size:11.5px">
          <input type="checkbox" id="scatter-filter-stars" checked style="margin:0">
          Stars only
        </label>
      </span>
    </div>
  </div>
  <canvas id="scatter-chart" style="width:100%;display:block;cursor:crosshair"></canvas>
</div>
<div id="scatter-tip" class="tip" style="max-width:220px;line-height:1.5"></div>
""" + f"""
<script>
(function(){{
  var SKU_DATA = {sku_js};
  var canvas = document.getElementById('scatter-chart');
  var tip    = document.getElementById('scatter-tip');
  var chkStars = document.getElementById('scatter-filter-stars');
  if (!canvas) return;

  var CH_COLORS = {{
    'Website':  '#2a78d6',
    'Amazon':   '#f59e0b',
    'FirstCry': '#1baf7a',
    'Blinkit':  '#e34948'
  }};

  // Axis clamp — outliers shown at boundary with triangle marker
  var AXIS_CM2   = [-800, 800];
  var AXIS_EBITDA= [-800, 800];

  var hovIdx = -1;
  var dots = [];  // computed dot positions for hit-testing

  function clamp(v, lo, hi) {{ return v < lo ? lo : v > hi ? hi : v; }}
  function isClipped(s) {{ return Math.abs(s.cm2_u) > 800 || Math.abs(s.ebitda_u) > 800; }}

  // Dot radius based on units (sqrt scaling)
  function dotR(units) {{
    var r = 3.5 + Math.sqrt(units) * 0.055;
    return Math.min(r, 16);
  }}

  function isDark() {{
    return document.documentElement.getAttribute('data-theme')==='dark' ||
      (window.matchMedia && window.matchMedia('(prefers-color-scheme:dark)').matches &&
       !document.documentElement.getAttribute('data-theme'));
  }}

  var starsOnly = false;
  if (chkStars) chkStars.addEventListener('change', function(){{ starsOnly = chkStars.checked; draw(); }});
  // Start unchecked (show all)
  starsOnly = false;

  function draw() {{
    var dark = isDark();
    var ink1 = dark?'#ffffff':'#0b0b0b';
    var ink2 = dark?'#c3c2b7':'#52514e';
    var ink3 = dark?'#898781':'#898781';
    var grid = dark?'rgba(255,255,255,0.07)':'rgba(0,0,0,0.06)';
    var axisC= dark?'rgba(255,255,255,0.20)':'rgba(0,0,0,0.18)';
    var quadBg= dark?'rgba(255,255,255,0.02)':'rgba(0,0,0,0.015)';

    var dpr = window.devicePixelRatio||1;
    var cssW = canvas.parentElement.clientWidth - 36;
    if (cssW < 320) cssW = 320;
    var cssH = Math.max(420, Math.round(cssW * 0.55));
    canvas.style.width  = cssW+'px';
    canvas.style.height = cssH+'px';
    canvas.width  = cssW*dpr;
    canvas.height = cssH*dpr;
    var ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    ctx.clearRect(0,0,cssW,cssH);

    var padL=60, padR=28, padT=28, padB=52;
    var cW = cssW-padL-padR, cH = cssH-padT-padB;

    // Data → pixel
    var xMin=AXIS_CM2[0],    xMax=AXIS_CM2[1];
    var yMin=AXIS_EBITDA[0], yMax=AXIS_EBITDA[1];
    function px(v)  {{ return padL + (clamp(v,xMin,xMax)-xMin)/(xMax-xMin)*cW; }}
    function py(v)  {{ return padT + cH - (clamp(v,yMin,yMax)-yMin)/(yMax-yMin)*cH; }}
    var x0 = px(0), y0 = py(0);  // origin pixel positions

    // Background quadrant shading
    // Q1 top-right: star (green tint)
    ctx.fillStyle = dark?'rgba(22,163,74,0.05)':'rgba(22,163,74,0.04)';
    ctx.fillRect(x0, padT, padL+cW-x0, y0-padT);
    // Q3 bottom-left: loss (red tint)
    ctx.fillStyle = dark?'rgba(239,68,68,0.06)':'rgba(239,68,68,0.04)';
    ctx.fillRect(padL, y0, x0-padL, padT+cH-y0);
    // Q4 bottom-right: overhead (amber tint)
    ctx.fillStyle = dark?'rgba(245,158,11,0.05)':'rgba(245,158,11,0.03)';
    ctx.fillRect(x0, y0, padL+cW-x0, padT+cH-y0);

    // Grid lines
    ctx.font = '10px system-ui,sans-serif';
    ctx.textAlign='right'; ctx.textBaseline='middle';
    ctx.fillStyle = ink3;
    var yTicks = [-600,-400,-200,0,200,400,600];
    yTicks.forEach(function(v) {{
      var yp = py(v);
      ctx.beginPath(); ctx.strokeStyle=grid; ctx.lineWidth=1;
      ctx.moveTo(padL,yp); ctx.lineTo(padL+cW,yp); ctx.stroke();
      ctx.fillText(v==0?'0':'₹'+v, padL-5, yp);
    }});
    ctx.textAlign='center'; ctx.textBaseline='top';
    var xTicks = [-600,-400,-200,0,200,400,600];
    xTicks.forEach(function(v) {{
      var xp = px(v);
      ctx.beginPath(); ctx.strokeStyle=grid; ctx.lineWidth=1;
      ctx.moveTo(xp,padT); ctx.lineTo(xp,padT+cH); ctx.stroke();
      ctx.fillText(v==0?'0':'₹'+v, xp, padT+cH+5);
    }});

    // Zero axes (thicker)
    ctx.beginPath(); ctx.strokeStyle=axisC; ctx.lineWidth=1.5;
    ctx.moveTo(padL,y0); ctx.lineTo(padL+cW,y0); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x0,padT); ctx.lineTo(x0,padT+cH); ctx.stroke();

    // Axis labels
    ctx.font='bold 10.5px system-ui,sans-serif';
    ctx.fillStyle=ink2;
    ctx.textAlign='center'; ctx.textBaseline='bottom';
    ctx.fillText('CM2 / unit (₹)', padL+cW/2, cssH-3);
    ctx.save(); ctx.translate(13, padT+cH/2); ctx.rotate(-Math.PI/2);
    ctx.textBaseline='top'; ctx.fillText('EBITDA / unit (₹)', 0, 0);
    ctx.restore();

    // Quadrant labels
    ctx.font='bold 10px system-ui,sans-serif';
    var qlPad = 7;
    // Top-right: Star
    ctx.fillStyle='rgba(22,163,74,0.75)';
    ctx.textAlign='right'; ctx.textBaseline='top';
    ctx.fillText('★ Star (CM2+ / EBITDA+)', padL+cW-qlPad, padT+qlPad);
    // Bottom-right: Overhead-heavy
    ctx.fillStyle='rgba(180,120,0,0.70)';
    ctx.textAlign='right'; ctx.textBaseline='bottom';
    ctx.fillText('◐ Overhead-heavy (CM2+ / EBITDA−)', padL+cW-qlPad, padT+cH-qlPad);
    // Bottom-left: Loss-making
    ctx.fillStyle='rgba(200,50,50,0.75)';
    ctx.textAlign='left'; ctx.textBaseline='bottom';
    ctx.fillText('✕ Loss-making (CM2− / EBITDA−)', padL+qlPad, padT+cH-qlPad);
    // Top-left: edge case
    ctx.fillStyle='rgba(120,120,120,0.55)';
    ctx.textAlign='left'; ctx.textBaseline='top';
    ctx.fillText('(CM2− / EBITDA+) rare', padL+qlPad, padT+qlPad);

    // Draw dots
    dots = [];
    var visible = SKU_DATA.filter(function(s) {{
      if (starsOnly && s.quad !== 'star') return false;
      return true;
    }});

    // Draw non-hovered first, hovered on top
    function drawDot(s, idx, isHov) {{
      var cx = px(s.cm2_u), cy = py(s.ebitda_u);
      var r  = dotR(s.units) * (isHov ? 1.35 : 1);
      var col = CH_COLORS[s.channel] || '#888';
      var clipped = isClipped(s);

      if (clipped) {{
        // Triangle marker for clipped outliers
        ctx.save();
        ctx.translate(cx, cy);
        var tr = 7;
        // Determine direction (which axis is clipped)
        var cx_real = px(s.cm2_u), cy_real = py(s.ebitda_u);
        ctx.beginPath();
        ctx.moveTo(0,-tr); ctx.lineTo(tr,tr); ctx.lineTo(-tr,tr); ctx.closePath();
        ctx.fillStyle = col;
        ctx.globalAlpha = 0.7;
        ctx.fill();
        ctx.globalAlpha=1;
        ctx.restore();
      }} else {{
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI*2);
        ctx.fillStyle = col;
        ctx.globalAlpha = isHov ? 1.0 : 0.72;
        ctx.fill();
        ctx.globalAlpha = 1;
        if (isHov) {{
          ctx.beginPath();
          ctx.arc(cx, cy, r+2.5, 0, Math.PI*2);
          ctx.strokeStyle = col;
          ctx.lineWidth = 1.5;
          ctx.globalAlpha = 0.4;
          ctx.stroke();
          ctx.globalAlpha = 1;
        }}
      }}
      dots[idx] = {{cx:cx, cy:cy, r:Math.max(r,7), s:s, idx:idx}};
    }}

    visible.forEach(function(s,i) {{
      if (i !== hovIdx) drawDot(s, i, false);
    }});
    if (hovIdx >= 0 && hovIdx < visible.length) drawDot(visible[hovIdx], hovIdx, true);
  }}

  // Tooltip & hover
  canvas.addEventListener('mousemove', function(e) {{
    var rect = canvas.getBoundingClientRect();
    var mx = e.clientX-rect.left, my = e.clientY-rect.top;
    var found = -1;
    for (var i=dots.length-1;i>=0;i--) {{
      var d=dots[i];
      if (!d) continue;
      var dx=mx-d.cx, dy=my-d.cy;
      if (dx*dx+dy*dy <= (d.r+3)*(d.r+3)) {{ found=i; break; }}
    }}
    if (found>=0) {{
      var s=dots[found].s;
      hovIdx=found;
      var html='<b style="font-size:12.5px">'+s.name+'</b>'+
        '<div style="color:var(--ink-3);font-size:11px;margin:2px 0 4px">'+s.channel+'</div>'+
        '<div>CM2/unit: <b style="color:'+((s.cm2_u>=0)?'#16a34a':'#dc2626')+'">&#8377;'+s.cm2_u.toFixed(0)+'</b></div>'+
        '<div>EBITDA/unit: <b style="color:'+((s.ebitda_u>=0)?'#16a34a':'#dc2626')+'">&#8377;'+s.ebitda_u.toFixed(0)+'</b></div>'+
        '<div>Units sold: <b>'+s.units.toLocaleString()+'</b></div>'+
        '<div style="margin-top:4px;font-size:10.5px;color:var(--ink-3)">Quadrant: '+s.quad+'</div>'+
        (isClipped(s)?'<div style="font-size:10px;color:#f59e0b;margin-top:3px">&#9650; Plotted at axis boundary</div>':'');
      tip.innerHTML=html;
      tip.style.opacity='1';
      tip.style.left=(e.clientX+14)+'px';
      tip.style.top=(e.clientY-10)+'px';
      draw();
    }} else {{
      if (hovIdx>=0) {{ hovIdx=-1; draw(); }}
      tip.style.opacity='0';
    }}
  }});
  canvas.addEventListener('mouseleave', function(){{
    tip.style.opacity='0'; hovIdx=-1; draw();
  }});

  // Click to filter by channel
  canvas.addEventListener('click', function(e) {{
    var rect=canvas.getBoundingClientRect();
    var mx=e.clientX-rect.left, my=e.clientY-rect.top;
    for (var i=dots.length-1;i>=0;i--) {{
      var d=dots[i];
      if (!d) continue;
      var dx=mx-d.cx, dy=my-d.cy;
      if (dx*dx+dy*dy<=(d.r+3)*(d.r+3)) {{
        // no filter, just ensure tip stays
        return;
      }}
    }}
  }});

  draw();
  window.addEventListener('resize', function(){{ setTimeout(draw,60); }});
}})();
</script>
"""

# Now read index.html and make all the edits
with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Add collapsible CSS before </style>
html = html.replace('</style>', COLLAPSIBLE_CSS + '\n</style>', 1)

# 2. Insert scatter plot before Q1
Q1_MARKER = '<!-- ===== Q1 ===== -->'
html = html.replace(Q1_MARKER, SCATTER_HTML + '\n<!-- ===== Q1 ===== -->', 1)

# 3. Wrap DC1 in collapsible details
DC1_START = '<!-- ===== Q1 ===== -->\n<div class="qa" style="--qac:var(--good);margin-bottom:12px">'
DC1_END   = '  </div>\n</div>\n\n<!-- ===== Q2 ===== -->'
DC1_SUMMARY = '<summary><span class="dc-chevron"></span>Decision Criteria 1 — Star products (CM2+ &amp; EBITDA+) · <span style="color:var(--ink-3);font-weight:400">Show channel breakdown table</span></summary>'

OLD_DC1 = '<!-- ===== Q1 ===== -->\n<div class="qa" style="--qac:var(--good);margin-bottom:12px">'
NEW_DC1 = '<!-- ===== Q1 ===== -->\n<div class="dc-collapsible"><details>\n' + DC1_SUMMARY + '\n<div class="qa" style="--qac:var(--good);margin-bottom:12px">'
html = html.replace(OLD_DC1, NEW_DC1, 1)

OLD_DC1_END = '  </div>\n</div>\n\n<!-- ===== Q2 ===== -->'
NEW_DC1_END = '  </div>\n</div></details></div>\n\n<!-- ===== Q2 ===== -->'
html = html.replace(OLD_DC1_END, NEW_DC1_END, 1)

# 4. Wrap DC2 in collapsible
OLD_DC2 = '<!-- ===== Q2 ===== -->\n<div class="qa" style="--qac:var(--warn);margin-bottom:12px">'
DC2_SUMMARY = '<summary><span class="dc-chevron"></span>Decision Criteria 2 — Overhead-heavy products (CM2+ / EBITDA−) · <span style="color:var(--ink-3);font-weight:400">Show nearest-to-breakeven table</span></summary>'
NEW_DC2 = '<!-- ===== Q2 ===== -->\n<div class="dc-collapsible"><details>\n' + DC2_SUMMARY + '\n<div class="qa" style="--qac:var(--warn);margin-bottom:12px">'
html = html.replace(OLD_DC2, NEW_DC2, 1)

OLD_DC2_END = '  </div>\n</div>\n\n<!-- ===== Q3 ===== -->'
NEW_DC2_END = '  </div>\n</div></details></div>\n\n<!-- ===== Q3 ===== -->'
html = html.replace(OLD_DC2_END, NEW_DC2_END, 1)

# 5. Wrap DC3 in collapsible
OLD_DC3 = '<!-- ===== Q3 ===== -->\n<div class="qa" style="--qac:var(--crit);margin-bottom:12px">'
DC3_SUMMARY = '<summary><span class="dc-chevron"></span>Decision Criteria 3 — Loss-making / discontinue candidates · <span style="color:var(--ink-3);font-weight:400">Show highest-burn-rate table</span></summary>'
NEW_DC3 = '<!-- ===== Q3 ===== -->\n<div class="dc-collapsible"><details>\n' + DC3_SUMMARY + '\n<div class="qa" style="--qac:var(--crit);margin-bottom:12px">'
html = html.replace(OLD_DC3, NEW_DC3, 1)

OLD_DC3_END = '  </div>\n</div>\n\n<!-- ===== Q4 ===== -->'
NEW_DC3_END = '  </div>\n</div></details></div>\n\n<!-- ===== Q4 ===== -->'
html = html.replace(OLD_DC3_END, NEW_DC3_END, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done! Changes:')
print(' - Added scatter CSS')
print(' - Inserted SKU scatter plot before DC1')
print(' - Wrapped DC1, DC2, DC3 in collapsible <details>')
print(' - Total file size:', len(html), 'chars')
