#!/usr/bin/env python3
"""
Business Analysis Export -- Generate MD, PDF, and HTML from business idea analysis data.

Usage:
    python3 business_analysis_export.py --input /tmp/business_analysis_export.json
    python3 business_analysis_export.py --input data.json --output-dir /custom/path/

Input: JSON payload from report-synthesizer agent
Output: .html, .pdf, .md in {output_dir}/Business_Analysis/ folder
"""

import argparse
import json
import os
import re
import sys
from datetime import date

# Use venv packages
VENV_SITE = os.path.expanduser("~/.claude/scripts/.venv/lib")
for d in os.listdir(VENV_SITE):
    sp = os.path.join(VENV_SITE, d, "site-packages")
    if os.path.isdir(sp) and sp not in sys.path:
        sys.path.insert(0, sp)

from fpdf import FPDF

# -- Constants ----------------------------------------------------------------

DEFAULT_OUTPUT_DIR = "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output"

TEAL = "#0D9488"
TEAL_RGB = (13, 148, 136)
TEAL_DARK = "#0F766E"
LIGHT_BG = "#F8FAFC"
BORDER_COLOR = "#E2E8F0"

VERDICT_COLORS = {
    "STRONG_GO": {"bg": "#059669", "text": "#FFFFFF", "label": "STRONG GO"},
    "GO":        {"bg": "#0D9488", "text": "#FFFFFF", "label": "GO"},
    "CONDITIONAL": {"bg": "#D97706", "text": "#FFFFFF", "label": "CONDITIONAL"},
    "NO_GO":     {"bg": "#DC2626", "text": "#FFFFFF", "label": "NO GO"},
    "BLOCKED":   {"bg": "#DC2626", "text": "#FFFFFF", "label": "BLOCKED"},
}

VERDICT_RGB = {
    "STRONG_GO": (5, 150, 105),
    "GO":        (13, 148, 136),
    "CONDITIONAL": (217, 119, 6),
    "NO_GO":     (220, 38, 38),
    "BLOCKED":   (220, 38, 38),
}

RISK_SEVERITY_COLORS = {
    "critical": {"bg": "#FEE2E2", "text": "#991B1B", "header_bg": "#DC2626"},
    "high":     {"bg": "#FFF7ED", "text": "#9A3412", "header_bg": "#EA580C"},
    "medium":   {"bg": "#FEFCE8", "text": "#854D0E", "header_bg": "#CA8A04"},
    "low":      {"bg": "#F0FDF4", "text": "#166534", "header_bg": "#16A34A"},
}

SCORE_COLORS = [
    (90, "#D1FAE5", "#065F46"),
    (80, "#E2EFDA", "#166534"),
    (70, "#FFF2CC", "#854D0E"),
    (60, "#FED7AA", "#9A3412"),
    (0,  "#FFC7CE", "#991B1B"),
]

DIMENSION_NAMES = {
    "market_demand": "Market Demand",
    "competitive_landscape": "Competitive Landscape",
    "financial_viability": "Financial Viability",
    "execution_feasibility": "Execution Feasibility",
    "risk_assessment": "Risk Assessment",
}


# -- Helpers ------------------------------------------------------------------

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:60].strip("-") or "untitled"


def compute_paths(data: dict, output_dir: str):
    idea = slugify(data.get("idea_description", "business-idea"))
    d = data.get("date", date.today().isoformat())
    depth = data.get("depth", "standard")
    stem = f"{d}_{idea}_{depth}_Analysis"
    folder = os.path.join(output_dir, "Business_Analysis")
    os.makedirs(folder, exist_ok=True)
    return {
        "folder": folder,
        "stem": stem,
        "html": os.path.join(folder, f"{stem}.html"),
        "pdf": os.path.join(folder, f"{stem}.pdf"),
        "md": os.path.join(folder, f"{stem}.md"),
    }


def escape_html(s: str) -> str:
    return (str(s).replace("&", "&amp;")
                  .replace("<", "&lt;")
                  .replace(">", "&gt;")
                  .replace('"', "&quot;"))


def latin_safe(s: str) -> str:
    replacements = {
        "\u2014": "--", "\u2013": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u2022": "*",
        "\u00a0": " ", "\u200b": "", "\u2713": "[x]", "\u2717": "[ ]",
    }
    for char, repl in replacements.items():
        s = s.replace(char, repl)
    return s.encode("latin-1", errors="replace").decode("latin-1")


def truncate(s: str, max_len: int = 60) -> str:
    s = latin_safe(str(s)) if s else ""
    return s[:max_len - 3] + "..." if len(s) > max_len else s


def score_color_bg(score: int) -> str:
    for threshold, bg, _ in SCORE_COLORS:
        if score >= threshold:
            return bg
    return SCORE_COLORS[-1][1]


def score_color_text(score: int) -> str:
    for threshold, _, text in SCORE_COLORS:
        if score >= threshold:
            return text
    return SCORE_COLORS[-1][2]


# -- HTML Generation ---------------------------------------------------------

def generate_html(data: dict, output_path: str):
    idea = escape_html(data.get("idea_description", "Business Idea"))
    d = escape_html(data.get("date", ""))
    depth = escape_html(data.get("depth", "standard"))
    profile = escape_html(data.get("operator_profile", "solopreneur"))
    exec_summary = escape_html(data.get("executive_summary", ""))
    opportunities = data.get("opportunities", [])
    market = data.get("market_research", {})
    competitive = data.get("competitive_analysis", {})
    risk_register = data.get("risk_register", [])
    methodology = data.get("methodology", {})

    # Opportunity ranking rows
    opp_rows = ""
    for opp in opportunities:
        v = opp.get("verdict", "NO_GO")
        vc = VERDICT_COLORS.get(v, VERDICT_COLORS["NO_GO"])
        solo = "Yes" if opp.get("solopreneur_viable") else "No"
        opp_rows += f"""
        <tr>
          <td style="font-weight:700;text-align:center">{opp.get('rank', '')}</td>
          <td style="font-weight:600">{escape_html(opp.get('name', ''))}</td>
          <td style="text-align:center;font-size:20px;font-weight:800;color:{vc['bg']}">{opp.get('composite_score', 0)}</td>
          <td style="text-align:center"><span style="display:inline-block;padding:3px 12px;border-radius:12px;font-size:11px;font-weight:700;color:{vc['text']};background:{vc['bg']}">{vc['label']}</span></td>
          <td style="text-align:center">{solo}</td>
          <td style="font-size:12px;color:#64748B">{escape_html(opp.get('recommended_pricing', ''))}</td>
        </tr>"""

    # Top opportunity detail
    top_detail = ""
    if opportunities:
        top = opportunities[0]
        tv = top.get("verdict", "NO_GO")
        tvc = VERDICT_COLORS.get(tv, VERDICT_COLORS["NO_GO"])

        # Dimension score bars
        dim_rows = ""
        for dim in top.get("dimensions", []):
            ds = dim.get("score", 0)
            dn = escape_html(dim.get("name", ""))
            bg = score_color_bg(ds)
            tc = score_color_text(ds)
            pct = max(5, ds)
            findings = "".join(f"<li>{escape_html(f)}</li>" for f in dim.get("key_findings", []))
            dim_rows += f"""
            <tr>
              <td style="font-weight:600;width:160px">{dn}</td>
              <td>
                <div style="background:#F1F5F9;border-radius:4px;height:24px;position:relative;overflow:hidden;margin-bottom:4px">
                  <div style="background:{bg};height:100%;width:{pct}%;border-radius:4px;display:flex;align-items:center;padding-left:8px">
                    <span style="font-size:12px;font-weight:700;color:{tc}">{ds}</span>
                  </div>
                </div>
                {"<ul style='margin:4px 0 0 16px;font-size:12px;color:#64748B'>" + findings + "</ul>" if findings else ""}
              </td>
            </tr>"""

        # TAM info
        tam = top.get("tam", {})
        tam_html = ""
        if tam:
            tam_html = f"""
            <div style="display:flex;gap:12px;margin:12px 0;flex-wrap:wrap">
              <div style="flex:1;min-width:120px;background:#F0FDFA;padding:10px;border-radius:6px;text-align:center">
                <div style="font-size:10px;color:{TEAL_DARK};text-transform:uppercase;letter-spacing:0.5px">TAM</div>
                <div style="font-size:16px;font-weight:700;color:{TEAL_DARK}">{escape_html(tam.get('total_addressable', 'N/A'))}</div>
              </div>
              <div style="flex:1;min-width:120px;background:#F0FDFA;padding:10px;border-radius:6px;text-align:center">
                <div style="font-size:10px;color:{TEAL_DARK};text-transform:uppercase;letter-spacing:0.5px">SAM</div>
                <div style="font-size:16px;font-weight:700;color:{TEAL_DARK}">{escape_html(tam.get('serviceable_addressable', 'N/A'))}</div>
              </div>
              <div style="flex:1;min-width:120px;background:#F0FDFA;padding:10px;border-radius:6px;text-align:center">
                <div style="font-size:10px;color:{TEAL_DARK};text-transform:uppercase;letter-spacing:0.5px">SOM Y1</div>
                <div style="font-size:16px;font-weight:700;color:{TEAL_DARK}">{escape_html(tam.get('obtainable_y1', 'N/A'))}</div>
              </div>
              <div style="flex:1;min-width:120px;background:#F0FDFA;padding:10px;border-radius:6px;text-align:center">
                <div style="font-size:10px;color:{TEAL_DARK};text-transform:uppercase;letter-spacing:0.5px">SOM Y3</div>
                <div style="font-size:16px;font-weight:700;color:{TEAL_DARK}">{escape_html(tam.get('obtainable_y3', 'N/A'))}</div>
              </div>
            </div>"""

        # Risks
        risk_items = ""
        for r in top.get("top_risks", []):
            sev = r.get("severity", "medium").lower()
            sc = RISK_SEVERITY_COLORS.get(sev, RISK_SEVERITY_COLORS["medium"])
            risk_items += f"""
            <div style="background:{sc['bg']};padding:10px 14px;border-radius:6px;margin-bottom:8px;border-left:4px solid {sc['header_bg']}">
              <strong style="color:{sc['text']}">[{sev.upper()}]</strong> <span style="color:{sc['text']}">{escape_html(r.get('risk', ''))}</span>
              <div style="font-size:12px;color:#64748B;margin-top:4px">Mitigation: {escape_html(r.get('mitigation', ''))}</div>
            </div>"""

        # Kill criteria
        kill_items = ""
        for kc in top.get("kill_criteria", []):
            status = kc.get("status", "unverified")
            icon = "[ ]" if status == "unverified" else "[x]"
            kill_items += f"<li><code>{icon}</code> {escape_html(kc.get('assumption', ''))} -- Kill if: {escape_html(kc.get('kill_condition', ''))}</li>"

        # Next steps
        step_items = "".join(f"<li>{escape_html(s)}</li>" for s in top.get("next_steps", []))

        top_detail = f"""
        <h2>Top Opportunity: {escape_html(top.get('name', ''))} (Score: {top.get('composite_score', 0)})</h2>
        <p>{escape_html(top.get('description', ''))}</p>
        <div style="display:flex;gap:16px;margin:12px 0;flex-wrap:wrap">
          <span style="display:inline-block;padding:4px 14px;border-radius:14px;font-size:12px;font-weight:700;color:{tvc['text']};background:{tvc['bg']}">{tvc['label']}</span>
          <span style="font-size:13px;color:#64748B">MVP: {escape_html(top.get('mvp_timeline', 'TBD'))}</span>
          <span style="font-size:13px;color:#64748B">Pricing: {escape_html(top.get('recommended_pricing', 'TBD'))}</span>
          <span style="font-size:13px;color:#64748B">Solo: {"Yes" if top.get('solopreneur_viable') else "No"}</span>
        </div>
        {tam_html}
        <h3 style="color:{TEAL};margin-top:20px">Dimension Scores</h3>
        <table>{dim_rows}</table>
        {"<h3 style='color:" + TEAL + "'>Top Risks</h3>" + risk_items if risk_items else ""}
        {"<h3 style='color:" + TEAL + "'>Kill Criteria</h3><ul>" + kill_items + "</ul>" if kill_items else ""}
        {"<h3 style='color:" + TEAL + "'>Next Steps</h3><ol>" + step_items + "</ol>" if step_items else ""}
        """

    # Pain points
    pain_rows = ""
    for pp in market.get("pain_points", []):
        pain_rows += f"""
        <tr>
          <td>{escape_html(pp.get('description', ''))}</td>
          <td style="text-align:center;font-weight:700">{pp.get('severity', 0)}</td>
          <td style="text-align:center">{escape_html(pp.get('frequency', ''))}</td>
          <td>{escape_html(pp.get('affected_segment', ''))}</td>
          <td style="font-size:12px">{escape_html(pp.get('economic_impact', ''))}</td>
        </tr>"""

    # Competitors
    comp_rows = ""
    for comp in competitive.get("competitors", []):
        strengths = ", ".join(comp.get("strengths", []))
        weaknesses = ", ".join(comp.get("weaknesses", []))
        comp_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(comp.get('name', ''))}</td>
          <td>{escape_html(comp.get('pricing', ''))}</td>
          <td style="font-size:12px">{escape_html(strengths)}</td>
          <td style="font-size:12px">{escape_html(weaknesses)}</td>
        </tr>"""

    # Feature matrix
    fm = competitive.get("feature_matrix", {})
    fm_html = ""
    if fm and fm.get("features"):
        features = fm["features"]
        competitors = fm.get("competitors", {})
        fm_headers = "".join(f"<th style='background:{TEAL};color:white'>{escape_html(c)}</th>" for c in competitors.keys())
        fm_body = ""
        for i, feat in enumerate(features):
            cells = ""
            for comp_name, vals in competitors.items():
                val = vals[i] if i < len(vals) else False
                cells += f"<td style='text-align:center'>{'[x]' if val else '[ ]'}</td>"
            fm_body += f"<tr><td style='font-weight:600'>{escape_html(feat)}</td>{cells}</tr>"
        fm_html = f"""
        <h3 style="color:{TEAL}">Feature Matrix</h3>
        <table>
          <tr><th style="background:{TEAL};color:white">Feature</th>{fm_headers}</tr>
          {fm_body}
        </table>"""

    # Risk register
    risk_reg_rows = ""
    for risk in risk_register:
        sev = risk.get("severity", "medium").lower()
        sc = RISK_SEVERITY_COLORS.get(sev, RISK_SEVERITY_COLORS["medium"])
        risk_reg_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(risk.get('id', ''))}</td>
          <td>{escape_html(risk.get('category', ''))}</td>
          <td><span style="background:{sc['bg']};color:{sc['text']};padding:2px 8px;border-radius:8px;font-size:11px;font-weight:700">{sev.upper()}</span></td>
          <td>{escape_html(risk.get('description', ''))}</td>
          <td style="font-size:12px">{escape_html(risk.get('mitigation', ''))}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Business Idea Analysis: {idea}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #1E293B;
    background: #F8FAFC;
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }}
  .header {{
    background: {TEAL};
    color: white;
    padding: 24px 32px;
    border-radius: 8px 8px 0 0;
  }}
  .header h1 {{ font-size: 22px; font-weight: 700; margin-bottom: 4px; }}
  .header .subtitle {{ font-size: 13px; opacity: 0.85; }}
  .meta-bar {{
    background: white;
    border: 1px solid {BORDER_COLOR};
    border-top: none;
    padding: 16px 32px;
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    align-items: center;
    border-radius: 0 0 8px 8px;
    margin-bottom: 24px;
  }}
  .meta-item {{ font-size: 13px; color: #64748B; }}
  .meta-item strong {{ color: #1E293B; }}
  .content {{
    background: white;
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 32px;
    margin-bottom: 24px;
  }}
  h2 {{
    color: {TEAL};
    font-size: 18px;
    font-weight: 700;
    margin: 24px 0 12px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid #E2E8F0;
  }}
  h2:first-child {{ margin-top: 0; }}
  h3 {{ font-size: 15px; margin: 16px 0 8px 0; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 20px 0;
    font-size: 14px;
  }}
  th {{
    background: {TEAL};
    color: white;
    padding: 10px 12px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
  }}
  td {{
    padding: 8px 12px;
    border-bottom: 1px solid #E2E8F0;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{ background: #F8FAFC; }}
  ul, ol {{ margin: 8px 0 16px 24px; }}
  li {{ margin-bottom: 6px; }}
  .text-block {{ margin: 8px 0 16px 0; line-height: 1.7; }}
  .footer {{
    text-align: center;
    font-size: 12px;
    color: #94A3B8;
    padding: 16px;
  }}
  @media print {{
    body {{ background: white; padding: 0; }}
    .header {{ border-radius: 0; }}
    .content {{ border: none; }}
  }}
</style>
</head>
<body>
<div class="header">
  <h1>Business Idea Analysis</h1>
  <div class="subtitle">{idea}</div>
</div>
<div class="meta-bar">
  <div class="meta-item"><strong>Date:</strong> {d}</div>
  <div class="meta-item"><strong>Depth:</strong> {depth}</div>
  <div class="meta-item"><strong>Profile:</strong> {profile}</div>
  <div class="meta-item"><strong>Searches:</strong> {methodology.get('web_searches_performed', 0)}</div>
  <div class="meta-item"><strong>Agents:</strong> {methodology.get('agents_dispatched', 0)}</div>
</div>

<div class="content">
  <h2>Executive Summary</h2>
  <p class="text-block">{exec_summary}</p>
</div>

<div class="content">
  <h2>Opportunity Rankings</h2>
  <table>
    <tr>
      <th style="width:40px">#</th>
      <th>Opportunity</th>
      <th style="width:70px;text-align:center">Score</th>
      <th style="width:120px;text-align:center">Verdict</th>
      <th style="width:50px;text-align:center">Solo</th>
      <th>Pricing</th>
    </tr>
    {opp_rows}
  </table>
</div>

<div class="content">
  {top_detail}
</div>

{"<div class='content'><h2>Pain Points</h2><table><tr><th>Pain Point</th><th style='width:70px;text-align:center'>Severity</th><th style='width:90px;text-align:center'>Frequency</th><th>Segment</th><th>Impact</th></tr>" + pain_rows + "</table></div>" if pain_rows else ""}

{"<div class='content'><h2>Competitive Landscape</h2><table><tr><th>Competitor</th><th style='width:100px'>Pricing</th><th>Strengths</th><th>Weaknesses</th></tr>" + comp_rows + "</table>" + fm_html + "<p class='text-block'><strong>Gap Summary:</strong> " + escape_html(competitive.get('gap_summary', '')) + "</p></div>" if comp_rows else ""}

{"<div class='content'><h2>Risk Register</h2><table><tr><th style='width:80px'>ID</th><th style='width:90px'>Category</th><th style='width:80px'>Severity</th><th>Description</th><th>Mitigation</th></tr>" + risk_reg_rows + "</table></div>" if risk_reg_rows else ""}

<div class="footer">
  Generated by Claude Code | Business Idea Analyzer Plugin | {d}
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


# -- PDF Generation -----------------------------------------------------------

class BusinessAnalysisPDF(FPDF):
    def __init__(self, data: dict):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.data = data
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*TEAL_RGB)
        self.cell(0, 8, "BUSINESS IDEA ANALYSIS", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(120, 120, 120)
        idea = latin_safe(self.data.get("idea_description", ""))
        self.cell(0, 6, truncate(idea, 80), new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        d = self.data.get("date", "")
        depth = self.data.get("depth", "standard")
        profile = self.data.get("operator_profile", "solopreneur")
        self.cell(0, 5, f"{d}  |  Depth: {depth}  |  Profile: {profile}", new_x="LMARGIN", new_y="NEXT")
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Generated by Claude Code  |  Business Idea Analyzer  |  Page {self.page_no()}/{{nb}}", align="C")


def _pdf_section_header(pdf, title):
    pdf.set_text_color(*TEAL_RGB)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, latin_safe(title), new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(226, 232, 240)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(3)


def _pdf_table_header(pdf, headers, widths):
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*TEAL_RGB)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(widths[i], 6, latin_safe(h), border=1, fill=True, align="C")
    pdf.ln()


def _pdf_verdict_badge(pdf, verdict, x=None):
    """Draw a colored verdict badge at current position or specified x."""
    vrgb = VERDICT_RGB.get(verdict, VERDICT_RGB["NO_GO"])
    vc = VERDICT_COLORS.get(verdict, VERDICT_COLORS["NO_GO"])
    label = vc["label"]
    pdf.set_font("Helvetica", "B", 8)
    w = pdf.get_string_width(label) + 10
    if x is not None:
        pdf.set_x(x)
    pdf.set_fill_color(*vrgb)
    pdf.set_text_color(255, 255, 255)
    y = pdf.get_y()
    pdf.rect(pdf.get_x(), y, w, 5, style="F")
    pdf.cell(w, 5, label, align="C")
    pdf.set_text_color(60, 60, 60)
    return w


def _pdf_score_bar(pdf, score, x, y, bar_width=60, bar_height=4):
    """Draw a colored score bar at (x, y)."""
    # Background track
    pdf.set_fill_color(241, 245, 249)
    pdf.rect(x, y, bar_width, bar_height, style="F")
    # Score fill
    if score >= 80:
        r, g, b = 5, 150, 105
    elif score >= 65:
        r, g, b = 13, 148, 136
    elif score >= 50:
        r, g, b = 217, 119, 6
    else:
        r, g, b = 220, 38, 38
    fill_width = max(2, bar_width * score / 100)
    pdf.set_fill_color(r, g, b)
    pdf.rect(x, y, fill_width, bar_height, style="F")


def _pdf_risk_severity_cell(pdf, severity, width):
    """Draw a severity cell with colored background."""
    sev = severity.lower()
    colors = {
        "critical": (254, 226, 226, 153, 27, 27),
        "high": (255, 247, 237, 154, 52, 18),
        "medium": (254, 252, 232, 133, 77, 14),
        "low": (240, 253, 244, 22, 101, 52),
    }
    bg_r, bg_g, bg_b, t_r, t_g, t_b = colors.get(sev, colors["medium"])
    pdf.set_fill_color(bg_r, bg_g, bg_b)
    pdf.set_text_color(t_r, t_g, t_b)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.cell(width, 5.5, sev.upper(), border=1, fill=True, align="C")
    pdf.set_text_color(60, 60, 60)
    pdf.set_font("Helvetica", "", 7.5)


def _pdf_tam_cards(pdf, tam):
    """Draw TAM/SAM/SOM as side-by-side cards."""
    labels = [("TAM", "total_addressable"), ("SAM", "serviceable_addressable"),
              ("SOM Y1", "obtainable_y1"), ("SOM Y3", "obtainable_y3")]
    card_w = (pdf.w - pdf.l_margin - pdf.r_margin - 9) / 4  # 3mm gaps
    start_x = pdf.l_margin
    y = pdf.get_y()
    for i, (label, key) in enumerate(labels):
        x = start_x + i * (card_w + 3)
        # Card background
        pdf.set_fill_color(240, 253, 250)
        pdf.rect(x, y, card_w, 14, style="F")
        # Label
        pdf.set_xy(x, y + 1)
        pdf.set_font("Helvetica", "", 6)
        pdf.set_text_color(*TEAL_RGB)
        pdf.cell(card_w, 4, label, align="C")
        # Value
        pdf.set_xy(x, y + 5)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(15, 118, 110)
        val = latin_safe(tam.get(key, "N/A"))
        pdf.cell(card_w, 8, val, align="C")
    pdf.set_y(y + 17)
    pdf.set_text_color(60, 60, 60)


def generate_pdf(data: dict, output_path: str):
    pdf = BusinessAnalysisPDF(data)
    pdf.alias_nb_pages()
    pdf.add_page()

    opportunities = data.get("opportunities", [])

    # -- Big score + verdict for top opportunity --
    if opportunities:
        top = opportunities[0]
        score = top.get("composite_score", 0)
        verdict = top.get("verdict", "NO_GO")

        # Large centered score
        pdf.set_font("Helvetica", "B", 36)
        vrgb = VERDICT_RGB.get(verdict, VERDICT_RGB["NO_GO"])
        pdf.set_text_color(*vrgb)
        pdf.cell(0, 18, f"{score}/100", align="C", new_x="LMARGIN", new_y="NEXT")

        # Verdict badge centered
        vc = VERDICT_COLORS.get(verdict, VERDICT_COLORS["NO_GO"])
        label = vc["label"]
        pdf.set_font("Helvetica", "B", 11)
        badge_w = pdf.get_string_width(label) + 16
        badge_x = (pdf.w - badge_w) / 2
        pdf.set_fill_color(*vrgb)
        pdf.set_text_color(255, 255, 255)
        pdf.set_x(badge_x)
        pdf.cell(badge_w, 8, label, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Subtitle
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 5, latin_safe(f"Top Opportunity: {top.get('name', '')}  |  MVP: {top.get('mvp_timeline', 'TBD')}  |  Pricing: {top.get('recommended_pricing', 'TBD')}"), align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)

    # -- Opportunity Rankings Table --
    if opportunities:
        _pdf_section_header(pdf, "Opportunity Rankings")
        headers = ["#", "Opportunity", "Score", "Verdict", "Solo", "Pricing"]
        widths = [10, 55, 18, 28, 14, 45]
        _pdf_table_header(pdf, headers, widths)

        pdf.set_font("Helvetica", "", 8)
        for idx, opp in enumerate(opportunities):
            if idx % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)

            v = opp.get("verdict", "NO_GO")
            pdf.set_text_color(60, 60, 60)
            pdf.cell(widths[0], 6, str(opp.get("rank", "")), border=1, fill=True, align="C")
            pdf.cell(widths[1], 6, truncate(opp.get("name", ""), 35), border=1, fill=True)

            # Score with color
            s = opp.get("composite_score", 0)
            vrgb = VERDICT_RGB.get(v, VERDICT_RGB["NO_GO"])
            pdf.set_text_color(*vrgb)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(widths[2], 6, str(s), border=1, fill=True, align="C")

            # Verdict badge in cell
            vc = VERDICT_COLORS.get(v, VERDICT_COLORS["NO_GO"])
            pdf.set_fill_color(*vrgb)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 7)
            pdf.cell(widths[3], 6, vc["label"], border=1, fill=True, align="C")

            # Reset for remaining cells
            if idx % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(60, 60, 60)
            pdf.set_font("Helvetica", "", 8)
            solo = "Yes" if opp.get("solopreneur_viable") else "No"
            pdf.cell(widths[4], 6, solo, border=1, fill=True, align="C")
            pdf.cell(widths[5], 6, truncate(opp.get("recommended_pricing", ""), 28), border=1, fill=True)
            pdf.ln()
        pdf.ln(4)

    # -- Top Opportunity Dimension Scores with Bars --
    if opportunities:
        top = opportunities[0]
        _pdf_section_header(pdf, f"Score Breakdown: {truncate(top.get('name', ''), 45)}")

        label_w = 50
        bar_w = 80
        score_w = 20
        wt_w = 20
        total_w = label_w + bar_w + score_w + wt_w

        # Header
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_fill_color(*TEAL_RGB)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(label_w, 6, "Dimension", border=1, fill=True)
        pdf.cell(bar_w, 6, "Score", border=1, fill=True, align="C")
        pdf.cell(score_w, 6, "Value", border=1, fill=True, align="C")
        pdf.cell(wt_w, 6, "Weight", border=1, fill=True, align="C")
        pdf.ln()

        for idx, dim in enumerate(top.get("dimensions", [])):
            ds = dim.get("score", 0)
            dn = latin_safe(dim.get("name", ""))
            wt = dim.get("weight", 0)

            if idx % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)

            row_y = pdf.get_y()
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(label_w, 7, f"  {dn}", border=1, fill=True)

            # Score bar cell
            bar_x = pdf.get_x()
            pdf.cell(bar_w, 7, "", border=1, fill=True)
            _pdf_score_bar(pdf, ds, bar_x + 4, row_y + 1.5, bar_w - 8, 4)

            # Score value with color
            if ds >= 80:
                pdf.set_text_color(6, 95, 70)
            elif ds >= 65:
                pdf.set_text_color(133, 77, 14)
            else:
                pdf.set_text_color(153, 27, 27)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(score_w, 7, str(ds), border=1, fill=True, align="C")

            pdf.set_text_color(100, 116, 139)
            pdf.set_font("Helvetica", "", 8)
            pdf.cell(wt_w, 7, f"{int(wt * 100)}%", border=1, fill=True, align="C")
            pdf.ln()

        pdf.ln(4)

        # TAM cards
        tam = top.get("tam", {})
        if tam:
            pdf.set_text_color(*TEAL_RGB)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 6, "Market Sizing", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            _pdf_tam_cards(pdf, tam)
            pdf.ln(2)

        # Key findings per dimension
        for dim in top.get("dimensions", []):
            findings = dim.get("key_findings", [])
            if findings:
                pdf.set_text_color(*TEAL_RGB)
                pdf.set_font("Helvetica", "B", 9)
                pdf.cell(0, 5, latin_safe(dim.get("name", "")), new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", "", 8)
                pdf.set_text_color(60, 60, 60)
                for f in findings:
                    pdf.set_x(pdf.l_margin + 4)
                    pdf.multi_cell(0, 4, latin_safe(f"- {f}"))
                pdf.ln(1)
        pdf.ln(2)

        # Top risks with severity coloring
        risks = top.get("top_risks", [])
        if risks:
            _pdf_section_header(pdf, "Top Risks")
            for r in risks:
                sev = r.get("severity", "medium").lower()
                colors = {
                    "critical": (254, 226, 226, 153, 27, 27),
                    "high": (255, 247, 237, 154, 52, 18),
                    "medium": (254, 252, 232, 133, 77, 14),
                    "low": (240, 253, 244, 22, 101, 52),
                }
                bg_r, bg_g, bg_b, t_r, t_g, t_b = colors.get(sev, colors["medium"])

                # Severity tag
                pdf.set_fill_color(bg_r, bg_g, bg_b)
                pdf.set_text_color(t_r, t_g, t_b)
                pdf.set_font("Helvetica", "B", 7)
                tag_w = pdf.get_string_width(sev.upper()) + 6
                pdf.cell(tag_w, 5, sev.upper(), fill=True)
                pdf.set_font("Helvetica", "", 8)
                pdf.set_text_color(60, 60, 60)
                pdf.cell(3, 5, "")
                pdf.multi_cell(0, 5, latin_safe(r.get("risk", "")))
                if r.get("mitigation"):
                    pdf.set_font("Helvetica", "I", 7)
                    pdf.set_text_color(100, 116, 139)
                    pdf.set_x(pdf.l_margin + tag_w + 3)
                    pdf.multi_cell(0, 4, latin_safe(f"Mitigation: {r.get('mitigation', '')}"))
                pdf.set_text_color(60, 60, 60)
                pdf.ln(2)
            pdf.ln(2)

        # Kill criteria
        kcs = top.get("kill_criteria", [])
        if kcs:
            pdf.set_text_color(*TEAL_RGB)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 6, "Kill Criteria", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(60, 60, 60)
            for kc in kcs:
                status = kc.get("status", "unverified")
                icon = "[x]" if status != "unverified" else "[ ]"
                pdf.multi_cell(0, 4.5, latin_safe(f"  {icon} {kc.get('assumption', '')} -- Kill if: {kc.get('kill_condition', '')}"))
                pdf.ln(1)
            pdf.ln(2)

        # Next steps
        steps = top.get("next_steps", [])
        if steps:
            _pdf_section_header(pdf, "Next Steps")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(40, 40, 40)
            for i, step in enumerate(steps, 1):
                pdf.multi_cell(0, 5, latin_safe(f"  {i}. {step}"))
                pdf.ln(1)
            pdf.ln(2)

    # -- Executive Summary --
    _pdf_section_header(pdf, "Executive Summary")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 5, latin_safe(data.get("executive_summary", "")))
    pdf.ln(4)

    # -- Competitors --
    competitors = data.get("competitive_analysis", {}).get("competitors", [])
    if competitors:
        _pdf_section_header(pdf, "Competitive Landscape")
        c_headers = ["Competitor", "Pricing", "Strengths", "Weaknesses"]
        c_widths = [35, 25, 55, 55]
        _pdf_table_header(pdf, c_headers, c_widths)

        pdf.set_font("Helvetica", "", 7.5)
        for idx, comp in enumerate(competitors):
            if idx % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(c_widths[0], 5.5, truncate(comp.get("name", ""), 22), border=1, fill=True)
            pdf.cell(c_widths[1], 5.5, truncate(comp.get("pricing", ""), 16), border=1, fill=True)
            pdf.cell(c_widths[2], 5.5, truncate(", ".join(comp.get("strengths", [])), 38), border=1, fill=True)
            pdf.cell(c_widths[3], 5.5, truncate(", ".join(comp.get("weaknesses", [])), 38), border=1, fill=True)
            pdf.ln()
        pdf.ln(4)

    # -- Pain Points --
    pain_points = data.get("market_research", {}).get("pain_points", [])
    if pain_points:
        _pdf_section_header(pdf, "Pain Points")
        p_headers = ["Pain Point", "Severity", "Frequency", "Segment"]
        p_widths = [65, 20, 25, 60]
        _pdf_table_header(pdf, p_headers, p_widths)

        pdf.set_font("Helvetica", "", 7.5)
        for idx, pp in enumerate(pain_points):
            if idx % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)

            pdf.set_text_color(60, 60, 60)
            pdf.cell(p_widths[0], 5.5, truncate(pp.get("description", ""), 44), border=1, fill=True)

            # Severity with color
            sev_val = pp.get("severity", 0)
            if sev_val >= 80:
                pdf.set_text_color(153, 27, 27)
            elif sev_val >= 60:
                pdf.set_text_color(154, 52, 18)
            else:
                pdf.set_text_color(133, 77, 14)
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(p_widths[1], 5.5, str(sev_val), border=1, fill=True, align="C")

            pdf.set_text_color(60, 60, 60)
            pdf.set_font("Helvetica", "", 7.5)
            pdf.cell(p_widths[2], 5.5, truncate(pp.get("frequency", ""), 16), border=1, fill=True, align="C")
            pdf.cell(p_widths[3], 5.5, truncate(pp.get("affected_segment", ""), 40), border=1, fill=True)
            pdf.ln()
        pdf.ln(4)

    # -- Risk Register --
    if risk_register := data.get("risk_register", []):
        _pdf_section_header(pdf, "Risk Register")
        r_headers = ["ID", "Category", "Severity", "Description"]
        r_widths = [20, 25, 20, 105]
        _pdf_table_header(pdf, r_headers, r_widths)

        pdf.set_font("Helvetica", "", 7.5)
        for idx, risk in enumerate(risk_register):
            if idx % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(r_widths[0], 5.5, risk.get("id", ""), border=1, fill=True)
            pdf.cell(r_widths[1], 5.5, truncate(risk.get("category", ""), 16), border=1, fill=True)
            _pdf_risk_severity_cell(pdf, risk.get("severity", "medium"), r_widths[2])
            pdf.cell(r_widths[3], 5.5, truncate(risk.get("description", ""), 70), border=1, fill=True)
            pdf.ln()
        pdf.ln(4)

    # -- Methodology footer --
    methodology = data.get("methodology", {})
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(130, 130, 130)
    searches = methodology.get("web_searches_performed", 0)
    agents = methodology.get("agents_dispatched", 0)
    confidence = methodology.get("confidence_threshold", 70)
    pdf.cell(0, 5, latin_safe(f"Web Searches: {searches}  |  Agents: {agents}  |  Confidence Threshold: {confidence}"), new_x="LMARGIN", new_y="NEXT")

    pdf.output(output_path)


# -- Markdown Generation ------------------------------------------------------

def generate_md(data: dict, output_path: str):
    idea = data.get("idea_description", "Business Idea")
    d = data.get("date", "")
    depth = data.get("depth", "standard")
    profile = data.get("operator_profile", "solopreneur")
    exec_summary = data.get("executive_summary", "")
    opportunities = data.get("opportunities", [])
    market = data.get("market_research", {})
    competitive = data.get("competitive_analysis", {})
    risk_register = data.get("risk_register", [])
    methodology = data.get("methodology", {})

    lines = []

    # YAML frontmatter
    lines.append("---")
    lines.append(f"idea: \"{idea}\"")
    lines.append(f"date: {d}")
    lines.append(f"depth: {depth}")
    lines.append(f"profile: {profile}")
    if opportunities:
        lines.append(f"top_score: {opportunities[0].get('composite_score', 0)}")
        lines.append(f"top_verdict: {opportunities[0].get('verdict', '')}")
    lines.append("---")
    lines.append("")

    # Title
    lines.append(f"# Business Idea Analysis: {idea}")
    lines.append("")
    lines.append(f"**Date**: {d}  |  **Depth**: {depth}  |  **Profile**: {profile}")
    lines.append(f"**Searches**: {methodology.get('web_searches_performed', 0)}  |  **Agents**: {methodology.get('agents_dispatched', 0)}")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(exec_summary)
    lines.append("")

    # Opportunity Rankings
    if opportunities:
        lines.append("## Opportunity Rankings")
        lines.append("")
        lines.append("| # | Opportunity | Score | Verdict | Solo | Pricing |")
        lines.append("|---|-------------|-------|---------|------|---------|")
        for opp in opportunities:
            v = VERDICT_COLORS.get(opp.get("verdict", ""), {}).get("label", opp.get("verdict", ""))
            solo = "Yes" if opp.get("solopreneur_viable") else "No"
            lines.append(f"| {opp.get('rank', '')} | {opp.get('name', '')} | {opp.get('composite_score', 0)} | {v} | {solo} | {opp.get('recommended_pricing', '')} |")
        lines.append("")

    # Top Opportunity Detail
    if opportunities:
        top = opportunities[0]
        tv = VERDICT_COLORS.get(top.get("verdict", ""), {}).get("label", top.get("verdict", ""))
        lines.append(f"## Top Opportunity: {top.get('name', '')} ({tv})")
        lines.append("")
        lines.append(f"> {top.get('description', '')}")
        lines.append("")

        # Dimensions
        lines.append("### Dimension Scores")
        lines.append("")
        lines.append("| Dimension | Score | Weight |")
        lines.append("|-----------|-------|--------|")
        for dim in top.get("dimensions", []):
            wt = int(dim.get("weight", 0) * 100)
            lines.append(f"| {dim.get('name', '')} | {dim.get('score', 0)}/100 | {wt}% |")
        lines.append("")

        # Key findings per dimension
        for dim in top.get("dimensions", []):
            findings = dim.get("key_findings", [])
            if findings:
                lines.append(f"**{dim.get('name', '')}**: {dim.get('summary', '')}")
                for f in findings:
                    lines.append(f"- {f}")
                lines.append("")

        # TAM
        tam = top.get("tam", {})
        if tam:
            lines.append("### Market Sizing")
            lines.append("")
            lines.append(f"- **TAM**: {tam.get('total_addressable', 'N/A')}")
            lines.append(f"- **SAM**: {tam.get('serviceable_addressable', 'N/A')}")
            lines.append(f"- **SOM Year 1**: {tam.get('obtainable_y1', 'N/A')}")
            lines.append(f"- **SOM Year 3**: {tam.get('obtainable_y3', 'N/A')}")
            lines.append("")

        # Risks
        risks = top.get("top_risks", [])
        if risks:
            lines.append("### Top Risks")
            lines.append("")
            for r in risks:
                lines.append(f"- **[{r.get('severity', 'medium').upper()}]** {r.get('risk', '')} -- Mitigation: {r.get('mitigation', '')}")
            lines.append("")

        # Kill Criteria
        kcs = top.get("kill_criteria", [])
        if kcs:
            lines.append("### Kill Criteria")
            lines.append("")
            for kc in kcs:
                status = kc.get("status", "unverified")
                check = "x" if status != "unverified" else " "
                lines.append(f"- [{check}] {kc.get('assumption', '')} -- Kill if: {kc.get('kill_condition', '')}")
            lines.append("")

        # Next Steps
        steps = top.get("next_steps", [])
        if steps:
            lines.append("### Next Steps")
            lines.append("")
            for i, step in enumerate(steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

    # Pain Points
    pain_points = market.get("pain_points", [])
    if pain_points:
        lines.append("## Pain Points")
        lines.append("")
        lines.append("| Pain Point | Severity | Frequency | Segment |")
        lines.append("|-----------|----------|-----------|---------|")
        for pp in pain_points:
            lines.append(f"| {pp.get('description', '')} | {pp.get('severity', 0)} | {pp.get('frequency', '')} | {pp.get('affected_segment', '')} |")
        lines.append("")

    # Competitors
    competitors = competitive.get("competitors", [])
    if competitors:
        lines.append("## Competitive Landscape")
        lines.append("")
        lines.append("| Competitor | Pricing | Strengths | Weaknesses |")
        lines.append("|-----------|---------|-----------|------------|")
        for comp in competitors:
            s = ", ".join(comp.get("strengths", []))
            w = ", ".join(comp.get("weaknesses", []))
            lines.append(f"| {comp.get('name', '')} | {comp.get('pricing', '')} | {s} | {w} |")
        lines.append("")
        if competitive.get("gap_summary"):
            lines.append(f"**Gap Summary**: {competitive['gap_summary']}")
            lines.append("")

    # Risk Register
    if risk_register:
        lines.append("## Risk Register")
        lines.append("")
        lines.append("| ID | Category | Severity | Description | Mitigation |")
        lines.append("|----|----------|----------|-------------|------------|")
        for risk in risk_register:
            lines.append(f"| {risk.get('id', '')} | {risk.get('category', '')} | {risk.get('severity', '')} | {risk.get('description', '')} | {risk.get('mitigation', '')} |")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*Generated by Claude Code | Business Idea Analyzer Plugin | {d}*")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# -- Main --------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Export business idea analysis to MD, PDF, and HTML")
    parser.add_argument("--input", required=True, help="Path to JSON input file")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Base output directory")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = json.load(f)

    paths = compute_paths(data, args.output_dir)

    generate_html(data, paths["html"])
    generate_pdf(data, paths["pdf"])
    generate_md(data, paths["md"])

    result = {
        "html": paths["html"],
        "pdf": paths["pdf"],
        "md": paths["md"],
        "output_folder": paths["folder"],
        "top_opportunity": opportunities[0].get("name", "") if (opportunities := data.get("opportunities", [])) else "",
        "top_score": opportunities[0].get("composite_score", 0) if opportunities else 0,
        "top_verdict": opportunities[0].get("verdict", "") if opportunities else "",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
