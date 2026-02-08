#!/usr/bin/env python3
"""
Code Review Export -- Generate MD, PDF, and HTML from production code review data.

Usage:
    python3 code_review_export.py --input /tmp/code_review_export.json
    python3 code_review_export.py --input data.json --output-dir /custom/path/

Input: JSON payload from report-generator agent
Output: .html, .pdf, .md in {output_dir}/Code_Reviews/ folder
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

# ── Constants ──────────────────────────────────────────────────────────────────

DEFAULT_OUTPUT_DIR = "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output"

INDIGO = "#312E81"
INDIGO_RGB = (49, 46, 129)
LIGHT_BG = "#F8FAFC"
BORDER_COLOR = "#E2E8F0"

VERDICT_COLORS = {
    "PASS": {"bg": "#059669", "text": "#FFFFFF", "label": "PASS"},
    "PASS_WITH_WARNINGS": {"bg": "#D97706", "text": "#FFFFFF", "label": "PASS WITH WARNINGS"},
    "FAIL": {"bg": "#DC2626", "text": "#FFFFFF", "label": "FAIL"},
}

SEVERITY_COLORS = {
    "CRITICAL": {"bg": "#FEE2E2", "text": "#991B1B", "header_bg": "#DC2626"},
    "HIGH": {"bg": "#FFF7ED", "text": "#9A3412", "header_bg": "#EA580C"},
    "MEDIUM": {"bg": "#FEFCE8", "text": "#854D0E", "header_bg": "#CA8A04"},
    "LOW": {"bg": "#F0FDF4", "text": "#166534", "header_bg": "#16A34A"},
}

SCORE_COLORS = [
    (90, "#D1FAE5", "#065F46"),   # Excellent
    (80, "#E2EFDA", "#166534"),   # Good
    (70, "#FFF2CC", "#854D0E"),   # Needs Work
    (60, "#FED7AA", "#9A3412"),   # Poor
    (0,  "#FFC7CE", "#991B1B"),   # Critical
]

DIMENSION_NAMES = {
    "code_quality": "Code Quality",
    "testing": "Testing",
    "ui_ux": "UI/UX",
    "responsive_design": "Responsive",
    "security": "Security",
    "performance": "Performance",
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:60].strip("-") or "untitled"


def compute_paths(data: dict, output_dir: str):
    project = slugify(data.get("project_name", "project"))
    d = data.get("date", date.today().isoformat())
    stem = f"{d}_{project}_Code_Review"
    folder = os.path.join(output_dir, "Code_Reviews")
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


def group_issues_by_severity(issues: list) -> dict:
    groups = {}
    order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    for issue in issues:
        sev = issue.get("severity", "LOW").upper()
        if sev not in order:
            sev = "LOW"
        groups.setdefault(sev, []).append(issue)
    return {k: groups[k] for k in order if k in groups}


# ── HTML Generation ────────────────────────────────────────────────────────────

def generate_html(data: dict, output_path: str):
    project = escape_html(data.get("project_name", "Project"))
    d = escape_html(data.get("date", ""))
    verdict = data.get("verdict", "FAIL")
    score = data.get("production_readiness_score", 0)
    dimensions = data.get("dimensions", [])
    issues = data.get("issues", [])
    issue_summary = data.get("issue_summary", {})
    exec_summary = escape_html(data.get("executive_summary", ""))
    recommendations = data.get("recommendations", [])
    tech_stack = escape_html(data.get("tech_stack", ""))
    files_total = data.get("files_reviewed_total", 0)

    vc = VERDICT_COLORS.get(verdict, VERDICT_COLORS["FAIL"])

    # Build dimension score bars
    dim_rows = ""
    for dim in dimensions:
        ds = dim.get("score", 0)
        dn = escape_html(dim.get("name", ""))
        dic = dim.get("issue_count", 0)
        bg = score_color_bg(ds)
        tc = score_color_text(ds)
        pct = max(5, ds)
        dim_rows += f"""
        <tr>
          <td style="font-weight:600">{dn}</td>
          <td>
            <div style="background:#F1F5F9;border-radius:4px;height:24px;position:relative;overflow:hidden">
              <div style="background:{bg};height:100%;width:{pct}%;border-radius:4px;display:flex;align-items:center;padding-left:8px">
                <span style="font-size:12px;font-weight:700;color:{tc}">{ds}</span>
              </div>
            </div>
          </td>
          <td style="text-align:center">{dic}</td>
        </tr>"""

    # Build issue tables
    grouped = group_issues_by_severity(issues)
    issue_sections = ""
    for sev, sev_issues in grouped.items():
        sc = SEVERITY_COLORS.get(sev, SEVERITY_COLORS["LOW"])
        rows = ""
        for iss in sev_issues:
            fls = ", ".join(f"{f.get('path','')}:{f.get('line','')}" for f in iss.get("files", []))
            rows += f"""
            <tr>
              <td style="font-weight:600">{escape_html(iss.get('id',''))}</td>
              <td>{escape_html(iss.get('title',''))}</td>
              <td style="font-size:12px;color:#64748B">{escape_html(fls)}</td>
              <td style="font-size:12px">{escape_html(DIMENSION_NAMES.get(iss.get('dimension',''), iss.get('dimension','')))}</td>
              <td style="font-size:12px">{iss.get('confidence', '')}</td>
            </tr>
            <tr>
              <td colspan="5" style="background:{sc['bg']};padding:8px 12px;font-size:13px">
                <strong>Issue:</strong> {escape_html(iss.get('description',''))}<br>
                <strong>Fix:</strong> {escape_html(iss.get('recommendation',''))}
              </td>
            </tr>"""

        issue_sections += f"""
        <h2 style="color:{sc['header_bg']}">{sev} Issues ({len(sev_issues)})</h2>
        <table>
          <tr>
            <th style="background:{sc['header_bg']};width:70px">ID</th>
            <th style="background:{sc['header_bg']}">Issue</th>
            <th style="background:{sc['header_bg']};width:200px">Location</th>
            <th style="background:{sc['header_bg']};width:100px">Dimension</th>
            <th style="background:{sc['header_bg']};width:60px">Conf.</th>
          </tr>
          {rows}
        </table>"""

    # Build recommendations
    rec_items = "\n".join(f"<li>{escape_html(r)}</li>" for r in recommendations)

    # Build positive findings
    positive_html = ""
    for dim in dimensions:
        pf = dim.get("positive_findings", [])
        if pf:
            dn = escape_html(dim.get("name", ""))
            items = ", ".join(escape_html(p) for p in pf)
            positive_html += f"<li><strong>{dn}:</strong> {items}</li>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{project} - Production Code Review</title>
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
    background: {INDIGO};
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
  .verdict-badge {{
    display: inline-block;
    padding: 4px 14px;
    border-radius: 14px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: {vc['text']};
    background: {vc['bg']};
  }}
  .score-big {{
    font-size: 48px;
    font-weight: 800;
    color: {INDIGO};
    text-align: center;
    padding: 16px 0;
  }}
  .content {{
    background: white;
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 32px;
    margin-bottom: 24px;
  }}
  h2 {{
    color: {INDIGO};
    font-size: 18px;
    font-weight: 700;
    margin: 24px 0 12px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid #E2E8F0;
  }}
  h2:first-child {{ margin-top: 0; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 20px 0;
    font-size: 14px;
  }}
  th {{
    background: {INDIGO};
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
  ul {{ margin: 8px 0 16px 24px; }}
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
  <h1>{project}</h1>
  <div class="subtitle">Production Code Review Report</div>
</div>
<div class="meta-bar">
  <div class="meta-item"><strong>Date:</strong> {d}</div>
  <div class="meta-item"><strong>Stack:</strong> {tech_stack}</div>
  <div class="meta-item"><strong>Files Reviewed:</strong> {files_total}</div>
  <div class="verdict-badge">{vc['label']}</div>
</div>

<div class="content">
  <div class="score-big">{score}/100</div>
  <p style="text-align:center;color:#64748B;margin-bottom:16px">Production Readiness Score</p>

  <h2>Score Breakdown</h2>
  <table>
    <tr>
      <th style="width:140px">Dimension</th>
      <th>Score</th>
      <th style="width:70px;text-align:center">Issues</th>
    </tr>
    {dim_rows}
  </table>

  <h2>Executive Summary</h2>
  <p class="text-block">{exec_summary}</p>

  <div style="display:flex;gap:20px;margin:16px 0">
    <div style="flex:1;background:#FEE2E2;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#991B1B">{issue_summary.get('critical', 0)}</div>
      <div style="font-size:12px;color:#991B1B">Critical</div>
    </div>
    <div style="flex:1;background:#FFF7ED;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#9A3412">{issue_summary.get('high', 0)}</div>
      <div style="font-size:12px;color:#9A3412">High</div>
    </div>
    <div style="flex:1;background:#FEFCE8;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#854D0E">{issue_summary.get('medium', 0)}</div>
      <div style="font-size:12px;color:#854D0E">Medium</div>
    </div>
    <div style="flex:1;background:#F0FDF4;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#166534">{issue_summary.get('low', 0)}</div>
      <div style="font-size:12px;color:#166534">Low</div>
    </div>
  </div>
</div>

<div class="content">
  {issue_sections}
</div>

<div class="content">
  <h2>Recommendations</h2>
  <ol style="margin:8px 0 16px 24px">
    {rec_items}
  </ol>

  {"<h2>Positive Findings</h2><ul>" + positive_html + "</ul>" if positive_html else ""}
</div>

<div class="footer">
  Generated by Claude Code | Production Code Review Plugin | {d}
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


# ── PDF Generation ─────────────────────────────────────────────────────────────

class CodeReviewPDF(FPDF):
    def __init__(self, data: dict):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.data = data
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*INDIGO_RGB)
        self.cell(0, 8, "PRODUCTION CODE REVIEW", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(120, 120, 120)
        project = latin_safe(self.data.get("project_name", ""))
        self.cell(0, 6, project, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        d = self.data.get("date", "")
        stack = latin_safe(self.data.get("tech_stack", ""))
        self.cell(0, 5, f"{d}  |  {stack}", new_x="LMARGIN", new_y="NEXT")
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Generated by Claude Code  |  Production Code Review  |  Confidential  |  Page {self.page_no()}/{{nb}}", align="C")


def generate_pdf(data: dict, output_path: str):
    pdf = CodeReviewPDF(data)
    pdf.alias_nb_pages()
    pdf.add_page()

    verdict = data.get("verdict", "FAIL")
    score = data.get("production_readiness_score", 0)
    dimensions = data.get("dimensions", [])
    issues = data.get("issues", [])
    issue_summary = data.get("issue_summary", {})

    # ── Verdict + Score ──
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*INDIGO_RGB)
    pdf.cell(0, 14, f"Score: {score}/100", align="C", new_x="LMARGIN", new_y="NEXT")

    # Verdict badge
    pdf.set_font("Helvetica", "B", 12)
    if verdict == "PASS":
        pdf.set_fill_color(5, 150, 105)
    elif verdict == "PASS_WITH_WARNINGS":
        pdf.set_fill_color(217, 119, 6)
    else:
        pdf.set_fill_color(220, 38, 38)
    pdf.set_text_color(255, 255, 255)
    label = VERDICT_COLORS.get(verdict, VERDICT_COLORS["FAIL"])["label"]
    w = pdf.get_string_width(label) + 16
    x = (pdf.w - w) / 2
    pdf.set_x(x)
    pdf.cell(w, 8, label, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ── Issue Summary ──
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    c = issue_summary.get("critical", 0)
    h = issue_summary.get("high", 0)
    m = issue_summary.get("medium", 0)
    lo = issue_summary.get("low", 0)
    t = issue_summary.get("total", 0)
    pdf.cell(0, 6, latin_safe(f"Total Issues: {t}  |  Critical: {c}  |  High: {h}  |  Medium: {m}  |  Low: {lo}"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # ── Dimension Scores Table ──
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*INDIGO_RGB)
    pdf.cell(0, 8, "Score Breakdown", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    dim_headers = ["Dimension", "Score", "Issues"]
    dim_widths = [60, 80, 30]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*INDIGO_RGB)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(dim_headers):
        pdf.cell(dim_widths[i], 6, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for idx, dim in enumerate(dimensions):
        ds = dim.get("score", 0)
        dn = latin_safe(dim.get("name", ""))
        dic = dim.get("issue_count", 0)

        if idx % 2 == 0:
            pdf.set_fill_color(248, 250, 252)
        else:
            pdf.set_fill_color(255, 255, 255)

        # Score color
        if ds >= 85:
            pdf.set_text_color(6, 95, 70)
        elif ds >= 70:
            pdf.set_text_color(133, 77, 14)
        else:
            pdf.set_text_color(153, 27, 27)

        pdf.cell(dim_widths[0], 6, f"  {dn}", border=1, fill=True)
        pdf.cell(dim_widths[1], 6, str(ds), border=1, fill=True, align="C")
        pdf.set_text_color(60, 60, 60)
        pdf.cell(dim_widths[2], 6, str(dic), border=1, fill=True, align="C")
        pdf.ln()
    pdf.ln(4)

    # ── Executive Summary ──
    pdf.set_text_color(*INDIGO_RGB)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 5, latin_safe(data.get("executive_summary", "")))
    pdf.ln(4)

    # ── Issues by Severity ──
    grouped = group_issues_by_severity(issues)
    issue_headers = ["ID", "Issue", "Location", "Dim."]
    issue_widths = [18, 72, 55, 25]

    for sev, sev_issues in grouped.items():
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*INDIGO_RGB)
        pdf.cell(0, 8, f"{sev} Issues ({len(sev_issues)})", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        # Header
        sc = SEVERITY_COLORS.get(sev, SEVERITY_COLORS["LOW"])
        r, g, b = int(sc["header_bg"][1:3], 16), int(sc["header_bg"][3:5], 16), int(sc["header_bg"][5:7], 16)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        for i, h in enumerate(issue_headers):
            pdf.cell(issue_widths[i], 6, h, border=1, fill=True, align="C")
        pdf.ln()

        pdf.set_font("Helvetica", "", 7.5)
        for iss_idx, iss in enumerate(sev_issues):
            if iss_idx % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(60, 60, 60)

            fls = ", ".join(f"{f.get('path','')}:{f.get('line','')}" for f in iss.get("files", []))
            dim_label = DIMENSION_NAMES.get(iss.get("dimension", ""), iss.get("dimension", ""))

            row_data = [
                iss.get("id", ""),
                truncate(iss.get("title", ""), 50),
                truncate(fls, 38),
                truncate(dim_label, 16),
            ]
            for i, val in enumerate(row_data):
                pdf.cell(issue_widths[i], 5.5, val, border=1, fill=True)
            pdf.ln()

            # Recommendation row
            rec = iss.get("recommendation", "")
            if rec:
                pdf.set_font("Helvetica", "I", 7)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(issue_widths[0], 4, "", border=0)
                pdf.multi_cell(sum(issue_widths[1:]), 4, truncate(latin_safe(f"Fix: {rec}"), 120))
                pdf.set_font("Helvetica", "", 7.5)

        pdf.ln(4)

    # ── Recommendations ──
    pdf.set_text_color(*INDIGO_RGB)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Recommendations", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    for i, rec in enumerate(data.get("recommendations", []), 1):
        pdf.multi_cell(0, 5, latin_safe(f"  {i}. {rec}"))
        pdf.ln(1)

    # ── Footer metadata ──
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(130, 130, 130)
    files_total = data.get("files_reviewed_total", 0)
    pdf.cell(0, 5, latin_safe(f"Files Reviewed: {files_total}  |  Stack: {data.get('tech_stack', '')}"), new_x="LMARGIN", new_y="NEXT")

    pdf.output(output_path)


# ── Markdown Generation ────────────────────────────────────────────────────────

def generate_md(data: dict, output_path: str):
    project = data.get("project_name", "Project")
    d = data.get("date", "")
    verdict = data.get("verdict", "FAIL")
    score = data.get("production_readiness_score", 0)
    dimensions = data.get("dimensions", [])
    issues = data.get("issues", [])
    issue_summary = data.get("issue_summary", {})
    exec_summary = data.get("executive_summary", "")
    recommendations = data.get("recommendations", [])
    tech_stack = data.get("tech_stack", "")
    files_total = data.get("files_reviewed_total", 0)

    lines = []

    # YAML frontmatter
    lines.append("---")
    lines.append(f"project: {project}")
    lines.append(f"date: {d}")
    lines.append(f"verdict: {verdict}")
    lines.append(f"score: {score}")
    lines.append(f"stack: {tech_stack}")
    lines.append(f"files_reviewed: {files_total}")
    lines.append("---")
    lines.append("")

    # Title
    lines.append(f"# Production Code Review: {project}")
    lines.append("")
    lines.append(f"**Date**: {d}  |  **Verdict**: {verdict}  |  **Score**: {score}/100")
    lines.append(f"**Stack**: {tech_stack}  |  **Files Reviewed**: {files_total}")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(exec_summary)
    lines.append("")

    # Issue Summary
    c = issue_summary.get("critical", 0)
    h = issue_summary.get("high", 0)
    m = issue_summary.get("medium", 0)
    lo = issue_summary.get("low", 0)
    t = issue_summary.get("total", 0)
    lines.append(f"**Total Issues**: {t} (Critical: {c}, High: {h}, Medium: {m}, Low: {lo})")
    lines.append("")

    # Score Breakdown
    lines.append("## Score Breakdown")
    lines.append("")
    lines.append("| Dimension | Score | Issues |")
    lines.append("|-----------|-------|--------|")
    for dim in dimensions:
        dn = dim.get("name", "")
        ds = dim.get("score", 0)
        dic = dim.get("issue_count", 0)
        lines.append(f"| {dn} | {ds}/100 | {dic} |")
    lines.append("")

    # Issues by Severity
    grouped = group_issues_by_severity(issues)
    for sev, sev_issues in grouped.items():
        lines.append(f"## {sev} Issues ({len(sev_issues)})")
        lines.append("")
        for iss in sev_issues:
            fls = ", ".join(f"`{f.get('path','')}:{f.get('line','')}`" for f in iss.get("files", []))
            dim_label = DIMENSION_NAMES.get(iss.get("dimension", ""), iss.get("dimension", ""))
            lines.append(f"### {iss.get('id', '')} - {iss.get('title', '')}")
            lines.append("")
            lines.append(f"- **Dimension**: {dim_label}")
            lines.append(f"- **Confidence**: {iss.get('confidence', '')}")
            lines.append(f"- **Location**: {fls}")
            lines.append(f"- **Description**: {iss.get('description', '')}")
            lines.append(f"- **Recommendation**: {iss.get('recommendation', '')}")
            lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    for i, rec in enumerate(recommendations, 1):
        lines.append(f"{i}. {rec}")
    lines.append("")

    # Positive Findings
    has_positive = any(dim.get("positive_findings") for dim in dimensions)
    if has_positive:
        lines.append("## Positive Findings")
        lines.append("")
        for dim in dimensions:
            pf = dim.get("positive_findings", [])
            if pf:
                dn = dim.get("name", "")
                lines.append(f"**{dn}**: {', '.join(pf)}")
                lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*Generated by Claude Code | Production Code Review Plugin | {d}*")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Export production code review to MD, PDF, and HTML")
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
        "verdict": data.get("verdict", ""),
        "score": data.get("production_readiness_score", 0),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
