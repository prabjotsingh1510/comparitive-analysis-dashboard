import json
import openpyxl

def num(v, default=None):
    if v is None or v == '':
        return default
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if s in ('NA', '#N/A', '#VALUE!', '#DIV/0!', ''):
        return default
    try:
        return float(s)
    except ValueError:
        return default

def rows_of(wb, sheet):
    rows = list(wb[sheet].iter_rows(values_only=True))
    header = rows[0]
    return header, rows[1:]

def bad(v):
    return v is None or (isinstance(v, str) and v.strip() in ('#N/A', '#DIV/0!', '#VALUE!', ''))

# ---------- 1) OLD FORMAT: Final sheets (unchanged source), reproduce D.periods[pk].products ----------
def load_old_final(path, sheet='Final'):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    h, rows = rows_of(wb, sheet)
    def c(name):
        # header has duplicate 'Product Name' - use positional index for col0/1
        return h.index(name)
    out = []
    total_rows = 0
    excluded = 0
    for r in rows:
        if not r or r[0] in (None, ''):
            continue
        total_rows += 1
        key = r[0]
        disp = r[1]
        rev = num(r[c('3 month revenue')], 0)
        units = num(r[c('Units sold')])
        ebitda_u = num(r[c('EBIDTA')])
        cm2_u = num(r[c('CM 2')])
        mktg_u = num(r[c('Marketing Cost')])
        if key == 'Digital Playbook' or rev in (0, None) or bad(r[c('CM 2')]) or bad(r[c('EBIDTA')]) or units in (None, 0):
            excluded += 1
            continue
        out.append({
            'key': str(key).strip(), 'disp': str(disp).strip(), 'rev': rev, 'units': units,
            'cm2_u': cm2_u, 'ebitda_u': ebitda_u, 'mktg_u': mktg_u,
        })
    return out, total_rows, excluded

jan_old, jan_total_rows, jan_excluded = load_old_final("Unit Economics For Website(1st Jan to 31st March)_JG (1).xlsx")
apr_old, apr_total_rows, apr_excluded = load_old_final("Unit Cost Economics - Website - Apr 2026-June 2026.xlsx")

print("JAN old: n=", len(jan_old), "sum_rev=", sum(p['rev'] for p in jan_old), "sum_units=", sum(p['units'] for p in jan_old),
      "total_rows=", jan_total_rows, "excluded=", jan_excluded)
print("APR old: n=", len(apr_old), "sum_rev=", sum(p['rev'] for p in apr_old), "sum_units=", sum(p['units'] for p in apr_old),
      "total_rows=", apr_total_rows, "excluded=", apr_excluded)
