#!/usr/bin/env python3
"""
Intel Briefing Export -- Generate MD, PDF, and HTML from intelligence briefing data.

Usage:
    python3 intel_briefing_export.py --input /tmp/intel_briefing_export.json
    python3 intel_briefing_export.py --input data.json --output-dir /custom/path/
    python3 intel_briefing_export.py --input data.json --type predictions

Input: JSON payload from briefing-synthesizer agent or command output
Output: .html, .pdf, .md in {output_dir}/Intel-Briefings/ folder

Supported types: briefing, predictions, accuracy
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

NAVY = "#1E3A5F"
NAVY_RGB = (30, 58, 95)
GOLD = "#D4AF37"
GOLD_RGB = (212, 175, 55)
NAVY_LIGHT = "#2C5282"
LIGHT_BG = "#F7F9FC"
BORDER_COLOR = "#CBD5E1"
TEXT_DARK = "#1A202C"
TEXT_MUTED = "#64748B"

CONFIDENCE_COLORS = {
    "high":   {"bg": "#D1FAE5", "text": "#065F46", "label": "HIGH"},
    "medium": {"bg": "#FEF3C7", "text": "#92400E", "label": "MEDIUM"},
    "low":    {"bg": "#FEE2E2", "text": "#991B1B", "label": "LOW"},
}

CONFIDENCE_RGB = {
    "high":   (5, 150, 105),
    "medium": (146, 64, 14),
    "low":    (153, 27, 27),
}

OUTLOOK_COLORS = {
    "bullish": {"bg": "#D1FAE5", "text": "#065F46"},
    "bearish": {"bg": "#FEE2E2", "text": "#991B1B"},
    "neutral": {"bg": "#F1F5F9", "text": "#475569"},
}

RISK_COLORS = {
    "high":   {"bg": "#FEE2E2", "text": "#991B1B", "border": "#DC2626"},
    "medium": {"bg": "#FEF3C7", "text": "#92400E", "border": "#D97706"},
    "low":    {"bg": "#D1FAE5", "text": "#065F46", "border": "#059669"},
}

OUTCOME_COLORS = {
    "correct":           {"bg": "#D1FAE5", "text": "#065F46"},
    "partially_correct": {"bg": "#FEF3C7", "text": "#92400E"},
    "incorrect":         {"bg": "#FEE2E2", "text": "#991B1B"},
    "pending":           {"bg": "#F1F5F9", "text": "#475569"},
    "indeterminate":     {"bg": "#E2E8F0", "text": "#64748B"},
}


# -- Helpers ------------------------------------------------------------------

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:60].strip("-") or "untitled"


def compute_paths(data: dict, output_dir: str):
    report_type = data.get("type", "briefing")
    d = data.get("date", date.today().isoformat())
    version = data.get("version", 1)

    if report_type == "briefing":
        stem = f"{d}_intel-briefing_v{version}"
    elif report_type == "predictions":
        stem = f"{d}_prediction-report"
    elif report_type == "accuracy":
        stem = f"{d}_accuracy-report"
    else:
        stem = f"{d}_{slugify(report_type)}"

    folder = os.path.join(output_dir, "Intel-Briefings")
    os.makedirs(folder, exist_ok=True)
    return {
        "folder": folder,
        "stem": stem,
        "html": os.path.join(folder, f"{stem}.html"),
        "pdf": os.path.join(folder, f"{stem}.pdf"),
        "md": os.path.join(folder, f"{stem}.md"),
    }


def escape_html(s) -> str:
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


def confidence_label(score):
    try:
        score = float(score)
    except (TypeError, ValueError):
        return "low"
    if score >= 0.70:
        return "high"
    elif score >= 0.40:
        return "medium"
    else:
        return "low"


def confidence_badge_html(score):
    label = confidence_label(score)
    c = CONFIDENCE_COLORS[label]
    pct = f"{float(score) * 100:.0f}%" if score else "N/A"
    return f'<span style="display:inline-block;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700;color:{c["text"]};background:{c["bg"]}">{pct}</span>'


# -- HTML Generation ---------------------------------------------------------

def generate_briefing_html(data: dict, output_path: str):
    version = data.get("version", 1)
    gen_date = escape_html(data.get("date", date.today().isoformat()))
    doc_count = data.get("document_count", 0)
    new_count = data.get("new_since_last", 0)
    pred_count = data.get("prediction_count", 0)
    exec_summary = escape_html(data.get("executive_summary", ""))
    key_devs = data.get("key_developments", [])
    financial = data.get("financial_section", {})
    geopolitical = data.get("geopolitical_section", {})
    cross_domain = data.get("cross_domain_themes", [])
    consensus = data.get("consensus_themes", {})
    contested = data.get("contested_topics", {})
    predictions = data.get("high_confidence_predictions", [])
    pred_tracking = data.get("prediction_tracking", {})
    alert_matches = data.get("alert_matches", [])
    watch_items = data.get("watch_items", [])

    # Key developments rows
    dev_rows = ""
    for dev in key_devs:
        impact = dev.get("impact", "medium").upper()
        ic = RISK_COLORS.get(dev.get("impact", "medium"), RISK_COLORS["medium"])
        dev_rows += f"""
        <div style="padding:10px 14px;border-left:4px solid {ic['border']};margin-bottom:8px;background:{ic['bg']}">
          <strong style="color:{ic['text']}">{escape_html(dev.get('development', ''))}</strong>
          <div style="font-size:12px;color:{TEXT_MUTED};margin-top:4px">
            Source: {escape_html(dev.get('source', 'N/A'))} | Impact: {impact}
          </div>
        </div>"""

    # Financial sector views
    sector_rows = ""
    for sv in financial.get("sector_views", []):
        oc = OUTLOOK_COLORS.get(sv.get("outlook", "neutral"), OUTLOOK_COLORS["neutral"])
        sector_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(sv.get('sector', ''))}</td>
          <td style="text-align:center"><span style="display:inline-block;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700;color:{oc['text']};background:{oc['bg']}">{escape_html(sv.get('outlook', '').upper())}</span></td>
          <td style="text-align:center">{confidence_badge_html(sv.get('confidence', 0))}</td>
          <td style="font-size:12px;color:{TEXT_MUTED}">{escape_html(sv.get('rationale', ''))}</td>
        </tr>"""

    # Financial predictions
    fin_pred_rows = ""
    for i, p in enumerate(financial.get("predictions", []), 1):
        fin_pred_rows += f"""
        <tr>
          <td style="text-align:center;font-weight:600">{i}</td>
          <td>{escape_html(p.get('prediction', ''))}</td>
          <td style="text-align:center">{escape_html(p.get('timeframe', ''))}</td>
          <td style="text-align:center">{confidence_badge_html(p.get('confidence', 0))}</td>
          <td style="font-size:12px;color:{TEXT_MUTED}">{escape_html(p.get('rationale', ''))}</td>
        </tr>"""

    # Risk matrix
    risk_rows = ""
    for r in geopolitical.get("risk_matrix", []):
        pc = RISK_COLORS.get(r.get("probability", "medium"), RISK_COLORS["medium"])
        ic = RISK_COLORS.get(r.get("impact", "medium"), RISK_COLORS["medium"])
        risk_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(r.get('risk', ''))}</td>
          <td style="text-align:center"><span style="display:inline-block;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;color:{pc['text']};background:{pc['bg']}">{escape_html(r.get('probability', '').upper())}</span></td>
          <td style="text-align:center"><span style="display:inline-block;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;color:{ic['text']};background:{ic['bg']}">{escape_html(r.get('impact', '').upper())}</span></td>
          <td style="text-align:center;font-size:12px">{escape_html(r.get('timeframe', ''))}</td>
        </tr>"""

    # Geopolitical predictions
    geo_pred_rows = ""
    for i, p in enumerate(geopolitical.get("predictions", []), 1):
        geo_pred_rows += f"""
        <tr>
          <td style="text-align:center;font-weight:600">{i}</td>
          <td>{escape_html(p.get('prediction', ''))}</td>
          <td style="text-align:center">{escape_html(p.get('timeframe', ''))}</td>
          <td style="text-align:center">{confidence_badge_html(p.get('confidence', 0))}</td>
          <td style="font-size:12px;color:{TEXT_MUTED}">{escape_html(p.get('rationale', ''))}</td>
        </tr>"""

    # Cross-domain themes
    cross_rows = ""
    for ct in cross_domain:
        cross_rows += f"""
        <div style="background:{LIGHT_BG};padding:14px;border-radius:8px;margin-bottom:10px;border:1px solid {BORDER_COLOR}">
          <div style="font-weight:700;color:{NAVY};margin-bottom:6px">{escape_html(ct.get('theme', ''))}</div>
          <div style="display:flex;gap:16px;flex-wrap:wrap">
            <div style="flex:1;min-width:200px">
              <div style="font-size:11px;color:{GOLD};font-weight:600;text-transform:uppercase">Financial Angle</div>
              <div style="font-size:13px;color:{TEXT_DARK}">{escape_html(ct.get('financial_angle', ''))}</div>
            </div>
            <div style="flex:1;min-width:200px">
              <div style="font-size:11px;color:{GOLD};font-weight:600;text-transform:uppercase">Geopolitical Angle</div>
              <div style="font-size:13px;color:{TEXT_DARK}">{escape_html(ct.get('geopolitical_angle', ''))}</div>
            </div>
          </div>
          <div style="text-align:right;margin-top:6px">{confidence_badge_html(ct.get('confidence', 0))}</div>
        </div>"""

    # Consensus themes
    consensus_rows = ""
    for theme_name, info in consensus.items():
        consensus_rows += f"""
        <div style="padding:8px 14px;background:#D1FAE5;border-radius:6px;margin-bottom:6px;border-left:4px solid #059669">
          <strong style="color:#065F46">{escape_html(theme_name)}</strong>:
          {escape_html(info.get('description', '') if isinstance(info, dict) else str(info))}
          <span style="float:right">{confidence_badge_html(info.get('confidence', 0) if isinstance(info, dict) else 0)}</span>
        </div>"""

    # Contested topics
    contested_rows = ""
    for topic_name, info in contested.items():
        contested_rows += f"""
        <div style="padding:12px 14px;background:#FFF7ED;border-radius:6px;margin-bottom:8px;border-left:4px solid #D97706">
          <div style="font-weight:700;color:#9A3412;margin-bottom:8px">{escape_html(topic_name)}</div>
          <div style="display:flex;gap:12px;flex-wrap:wrap">
            <div style="flex:1;min-width:200px;background:#FEF3C7;padding:8px;border-radius:4px">
              <div style="font-size:11px;font-weight:600;color:#92400E">VIEW A</div>
              <div style="font-size:13px">{escape_html(info.get('view_a', {}).get('position', '') if isinstance(info, dict) else '')}</div>
              <div style="font-size:11px;color:{TEXT_MUTED}">Sources: {escape_html(', '.join(info.get('view_a', {}).get('sources', [])) if isinstance(info, dict) else '')}</div>
            </div>
            <div style="flex:1;min-width:200px;background:#FEF3C7;padding:8px;border-radius:4px">
              <div style="font-size:11px;font-weight:600;color:#92400E">VIEW B</div>
              <div style="font-size:13px">{escape_html(info.get('view_b', {}).get('position', '') if isinstance(info, dict) else '')}</div>
              <div style="font-size:11px;color:{TEXT_MUTED}">Sources: {escape_html(', '.join(info.get('view_b', {}).get('sources', [])) if isinstance(info, dict) else '')}</div>
            </div>
          </div>
          <div style="font-size:12px;color:#64748B;margin-top:6px;font-style:italic">Assessment: {escape_html(info.get('assessment', '') if isinstance(info, dict) else '')}</div>
        </div>"""

    # Alert matches
    alert_rows = ""
    for am in alert_matches:
        alert_rows += f"""
        <div style="padding:8px 14px;background:#DBEAFE;border-radius:6px;margin-bottom:6px;border-left:4px solid #2563EB">
          <strong style="color:#1E40AF">{escape_html(am.get('alert_topic', ''))}</strong>:
          <span style="font-size:13px">{escape_html(am.get('significance', ''))}</span>
        </div>"""

    # Watch items
    watch_rows = "".join(f"<li style='margin-bottom:6px'>{escape_html(w)}</li>" for w in watch_items)

    # Prediction tracking
    due_rows = ""
    for p in pred_tracking.get("due_for_evaluation", []):
        due_rows += f"""
        <tr>
          <td>{escape_html(p.get('prediction', ''))}</td>
          <td style="text-align:center;font-size:12px">{escape_html(p.get('made', ''))}</td>
          <td style="text-align:center;font-size:12px">{escape_html(p.get('target_date', ''))}</td>
          <td style="font-size:12px">{escape_html(p.get('source', ''))}</td>
        </tr>"""

    outcome_rows = ""
    for p in pred_tracking.get("recent_outcomes", []):
        oc = OUTCOME_COLORS.get(p.get("outcome", "pending"), OUTCOME_COLORS["pending"])
        outcome_rows += f"""
        <tr>
          <td>{escape_html(p.get('prediction', ''))}</td>
          <td style="text-align:center"><span style="display:inline-block;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;color:{oc['text']};background:{oc['bg']}">{escape_html(p.get('outcome', '').upper().replace('_', ' '))}</span></td>
          <td style="font-size:12px">{escape_html(p.get('notes', ''))}</td>
        </tr>"""

    accuracy = pred_tracking.get("accuracy_summary", {})
    accuracy_html = ""
    if accuracy:
        accuracy_html = f"""
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin:12px 0">
          <div style="flex:1;min-width:120px;background:#EFF6FF;padding:12px;border-radius:8px;text-align:center">
            <div style="font-size:10px;color:{NAVY};font-weight:600;text-transform:uppercase">Financial</div>
            <div style="font-size:20px;font-weight:700;color:{NAVY}">{escape_html(accuracy.get('financial', 'N/A'))}</div>
          </div>
          <div style="flex:1;min-width:120px;background:#EFF6FF;padding:12px;border-radius:8px;text-align:center">
            <div style="font-size:10px;color:{NAVY};font-weight:600;text-transform:uppercase">Geopolitical</div>
            <div style="font-size:20px;font-weight:700;color:{NAVY}">{escape_html(accuracy.get('geopolitical', 'N/A'))}</div>
          </div>
          <div style="flex:1;min-width:120px;background:{GOLD};padding:12px;border-radius:8px;text-align:center">
            <div style="font-size:10px;color:{NAVY};font-weight:600;text-transform:uppercase">Overall</div>
            <div style="font-size:20px;font-weight:700;color:{NAVY}">{escape_html(accuracy.get('overall', 'N/A'))}</div>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Intelligence Briefing v{version}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color:{TEXT_DARK}; background:#FFFFFF; line-height:1.6; }}
  .container {{ max-width:900px; margin:0 auto; padding:32px 24px; }}
  .header {{ background: linear-gradient(135deg, {NAVY} 0%, {NAVY_LIGHT} 100%); color:white; padding:32px; border-radius:12px; margin-bottom:32px; }}
  .header h1 {{ font-size:28px; margin-bottom:8px; }}
  .header .meta {{ font-size:13px; opacity:0.85; }}
  .header .meta span {{ margin-right:16px; }}
  h2 {{ color:{NAVY}; font-size:20px; margin:28px 0 12px 0; padding-bottom:6px; border-bottom:2px solid {GOLD}; }}
  h3 {{ color:{NAVY_LIGHT}; font-size:16px; margin:20px 0 8px 0; }}
  table {{ width:100%; border-collapse:collapse; margin:12px 0; font-size:14px; }}
  th {{ background:{NAVY}; color:white; padding:10px 12px; text-align:left; font-size:12px; text-transform:uppercase; letter-spacing:0.5px; }}
  td {{ padding:8px 12px; border-bottom:1px solid {BORDER_COLOR}; }}
  tr:hover {{ background:{LIGHT_BG}; }}
  .section {{ margin-bottom:24px; }}
  .divider {{ border:none; border-top:2px solid {GOLD}; margin:32px 0; }}
  .footer {{ text-align:center; font-size:12px; color:{TEXT_MUTED}; margin-top:40px; padding-top:16px; border-top:1px solid {BORDER_COLOR}; }}
  p {{ margin-bottom:12px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>Intelligence Briefing v{version}</h1>
    <div class="meta">
      <span>Generated: {gen_date}</span>
      <span>Documents: {doc_count}</span>
      <span>New Since Last: {new_count}</span>
      <span>Active Predictions: {pred_count}</span>
    </div>
  </div>

  <div class="section">
    <h2>Executive Summary</h2>
    <p>{exec_summary}</p>
  </div>

  {"<div class='section'><h2>Key Developments Since Last Briefing</h2>" + dev_rows + "</div>" if dev_rows else ""}

  <hr class="divider">

  <div class="section">
    <h2>Financial Outlook</h2>
    <h3>Market Analysis</h3>
    <p><strong>Short-term (0-6mo):</strong> {escape_html(financial.get('market_outlook', {}).get('short_term', 'N/A'))}</p>
    <p><strong>Medium-term (6-24mo):</strong> {escape_html(financial.get('market_outlook', {}).get('medium_term', 'N/A'))}</p>

    {"<h3>Sector Views</h3><table><tr><th>Sector</th><th>Outlook</th><th>Confidence</th><th>Key Factor</th></tr>" + sector_rows + "</table>" if sector_rows else ""}

    {"<h3>Financial Predictions</h3><table><tr><th>#</th><th>Prediction</th><th>Timeframe</th><th>Confidence</th><th>Rationale</th></tr>" + fin_pred_rows + "</table>" if fin_pred_rows else ""}
  </div>

  <hr class="divider">

  <div class="section">
    <h2>Geopolitical Analysis</h2>
    <p>{escape_html(geopolitical.get('section_summary', ''))}</p>

    {"<h3>Risk Matrix</h3><table><tr><th>Risk</th><th>Probability</th><th>Impact</th><th>Timeframe</th></tr>" + risk_rows + "</table>" if risk_rows else ""}

    {"<h3>Geopolitical Predictions</h3><table><tr><th>#</th><th>Prediction</th><th>Timeframe</th><th>Confidence</th><th>Rationale</th></tr>" + geo_pred_rows + "</table>" if geo_pred_rows else ""}
  </div>

  {"<hr class='divider'><div class='section'><h2>Cross-Domain Themes</h2>" + cross_rows + "</div>" if cross_rows else ""}

  <hr class="divider">

  <div class="section">
    <h2>Consensus vs Contested</h2>
    {"<h3>High-Confidence Themes</h3>" + consensus_rows if consensus_rows else "<p>No consensus themes detected yet.</p>"}
    {"<h3>Contested Topics</h3>" + contested_rows if contested_rows else ""}
  </div>

  <hr class="divider">

  <div class="section">
    <h2>Prediction Tracking</h2>
    {accuracy_html}
    {"<h3>Due for Evaluation</h3><table><tr><th>Prediction</th><th>Made</th><th>Target Date</th><th>Source</th></tr>" + due_rows + "</table>" if due_rows else "<p>No predictions currently due for evaluation.</p>"}
    {"<h3>Recent Outcomes</h3><table><tr><th>Prediction</th><th>Outcome</th><th>Notes</th></tr>" + outcome_rows + "</table>" if outcome_rows else ""}
  </div>

  {"<hr class='divider'><div class='section'><h2>Alert Matches</h2>" + alert_rows + "</div>" if alert_rows else ""}

  {"<hr class='divider'><div class='section'><h2>Watch Items</h2><ul style='padding-left:20px'>" + watch_rows + "</ul></div>" if watch_rows else ""}

  <div class="footer">
    Intel-Briefing Plugin v1.0 | Generated {gen_date}
  </div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def generate_predictions_html(data: dict, output_path: str):
    gen_date = escape_html(data.get("date", date.today().isoformat()))
    predictions = data.get("predictions", [])
    accuracy = data.get("accuracy", {})

    pred_rows = ""
    for p in predictions:
        oc = OUTCOME_COLORS.get(p.get("outcome", "pending"), OUTCOME_COLORS["pending"])
        pred_rows += f"""
        <tr>
          <td>{escape_html(p.get('prediction_text', ''))}</td>
          <td style="text-align:center">{escape_html(p.get('category', ''))}</td>
          <td style="text-align:center">{confidence_badge_html(p.get('initial_confidence', 0))}</td>
          <td style="text-align:center">{escape_html(p.get('timeframe', ''))}</td>
          <td style="text-align:center">{escape_html(p.get('target_date', ''))}</td>
          <td style="text-align:center"><span style="display:inline-block;padding:2px 8px;border-radius:8px;font-size:11px;font-weight:600;color:{oc['text']};background:{oc['bg']}">{escape_html(p.get('outcome', 'PENDING').upper().replace('_', ' '))}</span></td>
          <td style="font-size:12px">{escape_html(p.get('source_author', ''))}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Prediction Tracking Report</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color:{TEXT_DARK}; background:#FFFFFF; line-height:1.6; }}
  .container {{ max-width:900px; margin:0 auto; padding:32px 24px; }}
  .header {{ background: linear-gradient(135deg, {NAVY} 0%, {NAVY_LIGHT} 100%); color:white; padding:32px; border-radius:12px; margin-bottom:32px; }}
  .header h1 {{ font-size:28px; margin-bottom:8px; }}
  h2 {{ color:{NAVY}; font-size:20px; margin:28px 0 12px 0; padding-bottom:6px; border-bottom:2px solid {GOLD}; }}
  table {{ width:100%; border-collapse:collapse; margin:12px 0; font-size:13px; }}
  th {{ background:{NAVY}; color:white; padding:10px 12px; text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:0.5px; }}
  td {{ padding:8px 12px; border-bottom:1px solid {BORDER_COLOR}; }}
  tr:hover {{ background:{LIGHT_BG}; }}
  .footer {{ text-align:center; font-size:12px; color:{TEXT_MUTED}; margin-top:40px; padding-top:16px; border-top:1px solid {BORDER_COLOR}; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>Prediction Tracking Report</h1>
    <div style="font-size:13px;opacity:0.85">Generated: {gen_date} | Total Predictions: {len(predictions)}</div>
  </div>

  <h2>All Predictions</h2>
  <table>
    <tr><th>Prediction</th><th>Category</th><th>Confidence</th><th>Timeframe</th><th>Target</th><th>Outcome</th><th>Source</th></tr>
    {pred_rows}
  </table>

  <div class="footer">Intel-Briefing Plugin v1.0 | Generated {gen_date}</div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def generate_accuracy_html(data: dict, output_path: str):
    gen_date = escape_html(data.get("date", date.today().isoformat()))
    overall = data.get("overall", {})
    by_category = data.get("by_category", [])
    by_source = data.get("by_source", [])

    cat_rows = ""
    for c in by_category:
        cat_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(c.get('category', ''))}</td>
          <td style="text-align:center">{c.get('evaluated', 0)}</td>
          <td style="text-align:center">{c.get('correct', 0)}</td>
          <td style="text-align:center">{c.get('partial', 0)}</td>
          <td style="text-align:center">{c.get('incorrect', 0)}</td>
          <td style="text-align:center;font-weight:700">{escape_html(c.get('accuracy', 'N/A'))}</td>
          <td style="text-align:center">{escape_html(c.get('brier', 'N/A'))}</td>
        </tr>"""

    src_rows = ""
    for s in by_source:
        src_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(s.get('source', ''))}</td>
          <td style="text-align:center">{s.get('predictions', 0)}</td>
          <td style="text-align:center">{s.get('correct', 0)}</td>
          <td style="text-align:center;font-weight:700">{escape_html(s.get('accuracy', 'N/A'))}</td>
          <td style="text-align:center">{escape_html(s.get('trust_tier', 'STANDARD'))}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Prediction Accuracy Report</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color:{TEXT_DARK}; background:#FFFFFF; line-height:1.6; }}
  .container {{ max-width:900px; margin:0 auto; padding:32px 24px; }}
  .header {{ background: linear-gradient(135deg, {NAVY} 0%, {NAVY_LIGHT} 100%); color:white; padding:32px; border-radius:12px; margin-bottom:32px; }}
  .header h1 {{ font-size:28px; margin-bottom:8px; }}
  h2 {{ color:{NAVY}; font-size:20px; margin:28px 0 12px 0; padding-bottom:6px; border-bottom:2px solid {GOLD}; }}
  table {{ width:100%; border-collapse:collapse; margin:12px 0; font-size:14px; }}
  th {{ background:{NAVY}; color:white; padding:10px 12px; text-align:left; font-size:12px; text-transform:uppercase; letter-spacing:0.5px; }}
  td {{ padding:8px 12px; border-bottom:1px solid {BORDER_COLOR}; }}
  tr:hover {{ background:{LIGHT_BG}; }}
  .stat-box {{ background:{LIGHT_BG}; padding:16px; border-radius:8px; text-align:center; border:1px solid {BORDER_COLOR}; }}
  .footer {{ text-align:center; font-size:12px; color:{TEXT_MUTED}; margin-top:40px; padding-top:16px; border-top:1px solid {BORDER_COLOR}; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>Prediction Accuracy Report</h1>
    <div style="font-size:13px;opacity:0.85">Generated: {gen_date}</div>
  </div>

  <h2>Overall Performance</h2>
  <div style="display:flex;gap:16px;flex-wrap:wrap;margin:16px 0">
    <div class="stat-box" style="flex:1;min-width:120px">
      <div style="font-size:10px;color:{NAVY};font-weight:600;text-transform:uppercase">Total</div>
      <div style="font-size:24px;font-weight:700;color:{NAVY}">{overall.get('total', 0)}</div>
    </div>
    <div class="stat-box" style="flex:1;min-width:120px">
      <div style="font-size:10px;color:{NAVY};font-weight:600;text-transform:uppercase">Evaluated</div>
      <div style="font-size:24px;font-weight:700;color:{NAVY}">{overall.get('evaluated', 0)}</div>
    </div>
    <div class="stat-box" style="flex:1;min-width:120px;background:#D1FAE5">
      <div style="font-size:10px;color:#065F46;font-weight:600;text-transform:uppercase">Correct</div>
      <div style="font-size:24px;font-weight:700;color:#065F46">{overall.get('correct', 0)}</div>
    </div>
    <div class="stat-box" style="flex:1;min-width:120px;background:{GOLD}">
      <div style="font-size:10px;color:{NAVY};font-weight:600;text-transform:uppercase">Accuracy</div>
      <div style="font-size:24px;font-weight:700;color:{NAVY}">{escape_html(overall.get('accuracy', 'N/A'))}</div>
    </div>
    <div class="stat-box" style="flex:1;min-width:120px">
      <div style="font-size:10px;color:{NAVY};font-weight:600;text-transform:uppercase">Brier Score</div>
      <div style="font-size:24px;font-weight:700;color:{NAVY}">{escape_html(overall.get('brier', 'N/A'))}</div>
    </div>
  </div>

  <h2>By Category</h2>
  <table>
    <tr><th>Category</th><th>Evaluated</th><th>Correct</th><th>Partial</th><th>Incorrect</th><th>Accuracy</th><th>Brier</th></tr>
    {cat_rows}
  </table>

  <h2>By Source</h2>
  <table>
    <tr><th>Source</th><th>Predictions</th><th>Correct</th><th>Accuracy</th><th>Trust Tier</th></tr>
    {src_rows}
  </table>

  <div class="footer">Intel-Briefing Plugin v1.0 | Generated {gen_date}</div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


# -- PDF Generation ----------------------------------------------------------

class IntelPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_fill_color(*NAVY_RGB)
        self.rect(0, 0, 210, 18, "F")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(255, 255, 255)
        self.set_y(4)
        self.cell(0, 10, "INTEL-BRIEFING", ln=True, align="L")
        self.set_text_color(*GOLD_RGB)
        self.set_font("Helvetica", "", 8)
        self.cell(0, 5, "Intelligence Analysis & Forecasting", ln=True, align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, f"Intel-Briefing v1.0 | Page {self.page_no()}", align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*NAVY_RGB)
        self.cell(0, 10, latin_safe(title), ln=True)
        self.set_draw_color(*GOLD_RGB)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_title(self, title: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(44, 82, 130)
        self.cell(0, 8, latin_safe(title), ln=True)
        self.ln(2)

    def body_text(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(26, 32, 44)
        self.multi_cell(0, 5, latin_safe(text))
        self.ln(3)

    def add_table(self, headers: list, rows: list, col_widths: list = None):
        if not col_widths:
            w = (self.w - 20) / len(headers)
            col_widths = [w] * len(headers)

        # Header
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(*NAVY_RGB)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, latin_safe(h), 1, 0, "C", fill=True)
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 8)
        self.set_text_color(26, 32, 44)
        fill = False
        for row in rows:
            if self.get_y() > 265:
                self.add_page()
            if fill:
                self.set_fill_color(247, 249, 252)
            else:
                self.set_fill_color(255, 255, 255)
            max_h = 7
            for i, cell_text in enumerate(row):
                safe = latin_safe(str(cell_text))[:int(col_widths[i] / 1.8)]
                self.cell(col_widths[i], max_h, safe, 1, 0, "L", fill=True)
            self.ln()
            fill = not fill
        self.ln(4)


def generate_briefing_pdf(data: dict, output_path: str):
    pdf = IntelPDF()
    pdf.add_page()

    version = data.get("version", 1)
    gen_date = data.get("date", date.today().isoformat())
    doc_count = data.get("document_count", 0)
    new_count = data.get("new_since_last", 0)

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*NAVY_RGB)
    pdf.cell(0, 12, f"Intelligence Briefing v{version}", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, f"Generated: {gen_date} | Documents: {doc_count} | New: {new_count}", ln=True)
    pdf.ln(8)

    # Executive Summary
    pdf.section_title("Executive Summary")
    pdf.body_text(data.get("executive_summary", "No summary available."))

    # Key Developments
    devs = data.get("key_developments", [])
    if devs:
        pdf.section_title("Key Developments")
        for dev in devs:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*NAVY_RGB)
            text = dev.get("development", "") if isinstance(dev, dict) else str(dev)
            pdf.multi_cell(0, 5, latin_safe(f"* {text}"))
            if isinstance(dev, dict) and dev.get("source"):
                pdf.set_font("Helvetica", "I", 8)
                pdf.set_text_color(100, 116, 139)
                pdf.cell(0, 5, latin_safe(f"  Source: {dev['source']} | Impact: {dev.get('impact', 'N/A').upper()}"), ln=True)
            pdf.ln(2)

    # Financial Outlook
    financial = data.get("financial_section", {})
    if financial:
        pdf.section_title("Financial Outlook")
        mo = financial.get("market_outlook", {})
        if mo:
            pdf.sub_title("Market Analysis")
            if mo.get("short_term"):
                pdf.body_text(f"Short-term (0-6mo): {mo['short_term']}")
            if mo.get("medium_term"):
                pdf.body_text(f"Medium-term (6-24mo): {mo['medium_term']}")

        svs = financial.get("sector_views", [])
        if svs:
            pdf.sub_title("Sector Views")
            rows = [[sv.get("sector", ""), sv.get("outlook", "").upper(),
                      f"{float(sv.get('confidence', 0))*100:.0f}%",
                      sv.get("rationale", "")[:60]] for sv in svs]
            pdf.add_table(["Sector", "Outlook", "Conf.", "Key Factor"], rows,
                         [35, 25, 20, 110])

        preds = financial.get("predictions", [])
        if preds:
            pdf.sub_title("Financial Predictions")
            rows = [[p.get("prediction", "")[:80], p.get("timeframe", ""),
                      f"{float(p.get('confidence', 0))*100:.0f}%"] for p in preds]
            pdf.add_table(["Prediction", "Timeframe", "Confidence"], rows,
                         [120, 30, 40])

    # Geopolitical Analysis
    geopolitical = data.get("geopolitical_section", {})
    if geopolitical:
        pdf.section_title("Geopolitical Analysis")
        if geopolitical.get("section_summary"):
            pdf.body_text(geopolitical["section_summary"])

        risks = geopolitical.get("risk_matrix", [])
        if risks:
            pdf.sub_title("Risk Matrix")
            rows = [[r.get("risk", "")[:60], r.get("probability", "").upper(),
                      r.get("impact", "").upper(), r.get("timeframe", "")] for r in risks]
            pdf.add_table(["Risk", "Probability", "Impact", "Timeframe"], rows,
                         [80, 30, 30, 50])

        preds = geopolitical.get("predictions", [])
        if preds:
            pdf.sub_title("Geopolitical Predictions")
            rows = [[p.get("prediction", "")[:80], p.get("timeframe", ""),
                      f"{float(p.get('confidence', 0))*100:.0f}%"] for p in preds]
            pdf.add_table(["Prediction", "Timeframe", "Confidence"], rows,
                         [120, 30, 40])

    # Watch Items
    watch = data.get("watch_items", [])
    if watch:
        pdf.section_title("Watch Items")
        for w in watch:
            pdf.body_text(f"* {w}")

    pdf.output(output_path)


def generate_predictions_pdf(data: dict, output_path: str):
    pdf = IntelPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*NAVY_RGB)
    pdf.cell(0, 12, "Prediction Tracking Report", ln=True)
    pdf.ln(8)

    predictions = data.get("predictions", [])
    if predictions:
        rows = [[p.get("prediction_text", "")[:60], p.get("category", ""),
                  f"{float(p.get('initial_confidence', 0))*100:.0f}%",
                  p.get("timeframe", ""), p.get("outcome", "pending").upper()]
                for p in predictions]
        pdf.add_table(["Prediction", "Category", "Conf.", "Timeframe", "Outcome"], rows,
                     [70, 30, 20, 25, 45])

    pdf.output(output_path)


def generate_accuracy_pdf(data: dict, output_path: str):
    pdf = IntelPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*NAVY_RGB)
    pdf.cell(0, 12, "Prediction Accuracy Report", ln=True)
    pdf.ln(8)

    overall = data.get("overall", {})
    if overall:
        pdf.section_title("Overall Performance")
        pdf.body_text(f"Total: {overall.get('total', 0)} | Evaluated: {overall.get('evaluated', 0)} | "
                      f"Correct: {overall.get('correct', 0)} | Accuracy: {overall.get('accuracy', 'N/A')} | "
                      f"Brier Score: {overall.get('brier', 'N/A')}")

    by_cat = data.get("by_category", [])
    if by_cat:
        pdf.section_title("By Category")
        rows = [[c.get("category", ""), c.get("evaluated", 0), c.get("correct", 0),
                  c.get("accuracy", "N/A"), c.get("brier", "N/A")] for c in by_cat]
        pdf.add_table(["Category", "Evaluated", "Correct", "Accuracy", "Brier"], rows,
                     [40, 30, 30, 40, 50])

    by_src = data.get("by_source", [])
    if by_src:
        pdf.section_title("By Source")
        rows = [[s.get("source", ""), s.get("predictions", 0),
                  s.get("accuracy", "N/A"), s.get("trust_tier", "STANDARD")] for s in by_src]
        pdf.add_table(["Source", "Predictions", "Accuracy", "Trust Tier"], rows,
                     [50, 35, 50, 55])

    pdf.output(output_path)


# -- Markdown Generation -----------------------------------------------------

def generate_briefing_md(data: dict, output_path: str):
    version = data.get("version", 1)
    gen_date = data.get("date", date.today().isoformat())
    doc_count = data.get("document_count", 0)
    new_count = data.get("new_since_last", 0)
    pred_count = data.get("prediction_count", 0)

    # Use pre-rendered full_briefing_md if available
    if data.get("full_briefing_md"):
        md = data["full_briefing_md"]
    else:
        lines = [
            f"# Intelligence Briefing v{version}",
            f"**Generated:** {gen_date} | **Documents:** {doc_count} | **New Since Last:** {new_count} | **Active Predictions:** {pred_count}",
            "",
            "---",
            "",
            "## Executive Summary",
            data.get("executive_summary", "No summary available."),
            "",
        ]

        devs = data.get("key_developments", [])
        if devs:
            lines.append("## Key Developments Since Last Briefing")
            for dev in devs:
                if isinstance(dev, dict):
                    lines.append(f"- **{dev.get('development', '')}** -- {dev.get('source', 'N/A')} | Impact: {dev.get('impact', 'N/A').upper()}")
                else:
                    lines.append(f"- {dev}")
            lines.append("")

        financial = data.get("financial_section", {})
        if financial:
            lines.append("---")
            lines.append("")
            lines.append("## Financial Outlook")
            mo = financial.get("market_outlook", {})
            if mo:
                lines.append("### Market Analysis")
                if mo.get("short_term"):
                    lines.append(f"**Short-term (0-6mo):** {mo['short_term']}")
                if mo.get("medium_term"):
                    lines.append(f"\n**Medium-term (6-24mo):** {mo['medium_term']}")
                lines.append("")

            svs = financial.get("sector_views", [])
            if svs:
                lines.append("### Sector Views")
                lines.append("| Sector | Outlook | Confidence | Key Factor |")
                lines.append("|--------|---------|------------|------------|")
                for sv in svs:
                    conf = f"{float(sv.get('confidence', 0))*100:.0f}%"
                    lines.append(f"| {sv.get('sector', '')} | {sv.get('outlook', '').upper()} | {conf} | {sv.get('rationale', '')} |")
                lines.append("")

            preds = financial.get("predictions", [])
            if preds:
                lines.append("### Financial Predictions")
                lines.append("| # | Prediction | Timeframe | Confidence | Rationale |")
                lines.append("|---|-----------|-----------|------------|-----------|")
                for i, p in enumerate(preds, 1):
                    conf = f"{float(p.get('confidence', 0))*100:.0f}%"
                    lines.append(f"| {i} | {p.get('prediction', '')} | {p.get('timeframe', '')} | {conf} | {p.get('rationale', '')} |")
                lines.append("")

        geopolitical = data.get("geopolitical_section", {})
        if geopolitical:
            lines.append("---")
            lines.append("")
            lines.append("## Geopolitical Analysis")
            if geopolitical.get("section_summary"):
                lines.append(geopolitical["section_summary"])
                lines.append("")

            risks = geopolitical.get("risk_matrix", [])
            if risks:
                lines.append("### Risk Matrix")
                lines.append("| Risk | Probability | Impact | Timeframe |")
                lines.append("|------|------------|--------|-----------|")
                for r in risks:
                    lines.append(f"| {r.get('risk', '')} | {r.get('probability', '').upper()} | {r.get('impact', '').upper()} | {r.get('timeframe', '')} |")
                lines.append("")

        consensus = data.get("consensus_themes", {})
        if consensus:
            lines.append("---")
            lines.append("")
            lines.append("## High-Confidence Themes")
            for name, info in consensus.items():
                desc = info.get("description", "") if isinstance(info, dict) else str(info)
                lines.append(f"- **{name}**: {desc}")
            lines.append("")

        contested = data.get("contested_topics", {})
        if contested:
            lines.append("## Contested Topics")
            for name, info in contested.items():
                if isinstance(info, dict):
                    lines.append(f"- **{name}**")
                    lines.append(f"  - View A: {info.get('view_a', {}).get('position', '')}")
                    lines.append(f"  - View B: {info.get('view_b', {}).get('position', '')}")
                    lines.append(f"  - Assessment: {info.get('assessment', '')}")
            lines.append("")

        watch = data.get("watch_items", [])
        if watch:
            lines.append("---")
            lines.append("")
            lines.append("## Watch Items")
            for w in watch:
                lines.append(f"- {w}")
            lines.append("")

        lines.append("---")
        lines.append(f"*Intel-Briefing Plugin v1.0 | Generated {gen_date}*")
        md = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)


def generate_predictions_md(data: dict, output_path: str):
    gen_date = data.get("date", date.today().isoformat())
    predictions = data.get("predictions", [])

    lines = [
        "# Prediction Tracking Report",
        f"**Generated:** {gen_date} | **Total Predictions:** {len(predictions)}",
        "",
        "| Prediction | Category | Confidence | Timeframe | Target | Outcome | Source |",
        "|-----------|----------|------------|-----------|--------|---------|--------|",
    ]
    for p in predictions:
        conf = f"{float(p.get('initial_confidence', 0))*100:.0f}%"
        lines.append(f"| {p.get('prediction_text', '')} | {p.get('category', '')} | {conf} | {p.get('timeframe', '')} | {p.get('target_date', '')} | {p.get('outcome', 'pending').upper()} | {p.get('source_author', '')} |")

    lines.append("")
    lines.append(f"*Intel-Briefing Plugin v1.0 | Generated {gen_date}*")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_accuracy_md(data: dict, output_path: str):
    gen_date = data.get("date", date.today().isoformat())
    overall = data.get("overall", {})

    lines = [
        "# Prediction Accuracy Report",
        f"**Generated:** {gen_date}",
        "",
        "## Overall Performance",
        f"- **Total:** {overall.get('total', 0)}",
        f"- **Evaluated:** {overall.get('evaluated', 0)}",
        f"- **Correct:** {overall.get('correct', 0)}",
        f"- **Accuracy:** {overall.get('accuracy', 'N/A')}",
        f"- **Brier Score:** {overall.get('brier', 'N/A')}",
        "",
    ]

    by_cat = data.get("by_category", [])
    if by_cat:
        lines.append("## By Category")
        lines.append("| Category | Evaluated | Correct | Partial | Incorrect | Accuracy | Brier |")
        lines.append("|----------|-----------|---------|---------|-----------|----------|-------|")
        for c in by_cat:
            lines.append(f"| {c.get('category', '')} | {c.get('evaluated', 0)} | {c.get('correct', 0)} | {c.get('partial', 0)} | {c.get('incorrect', 0)} | {c.get('accuracy', 'N/A')} | {c.get('brier', 'N/A')} |")
        lines.append("")

    by_src = data.get("by_source", [])
    if by_src:
        lines.append("## By Source")
        lines.append("| Source | Predictions | Correct | Accuracy | Trust Tier |")
        lines.append("|--------|------------|---------|----------|------------|")
        for s in by_src:
            lines.append(f"| {s.get('source', '')} | {s.get('predictions', 0)} | {s.get('correct', 0)} | {s.get('accuracy', 'N/A')} | {s.get('trust_tier', 'STANDARD')} |")
        lines.append("")

    lines.append(f"*Intel-Briefing Plugin v1.0 | Generated {gen_date}*")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# -- Dispatch ----------------------------------------------------------------

HTML_GENERATORS = {
    "briefing": generate_briefing_html,
    "predictions": generate_predictions_html,
    "accuracy": generate_accuracy_html,
}

PDF_GENERATORS = {
    "briefing": generate_briefing_pdf,
    "predictions": generate_predictions_pdf,
    "accuracy": generate_accuracy_pdf,
}

MD_GENERATORS = {
    "briefing": generate_briefing_md,
    "predictions": generate_predictions_md,
    "accuracy": generate_accuracy_md,
}


def main():
    parser = argparse.ArgumentParser(description="Intel Briefing Export")
    parser.add_argument("--input", required=True, help="Path to JSON input file")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Base output directory")
    parser.add_argument("--type", default=None, help="Report type override: briefing, predictions, accuracy")
    parser.add_argument("--formats", default="all", help="Export formats: all, html, pdf, md (comma-separated)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    report_type = args.type or data.get("type", "briefing")
    data["type"] = report_type

    paths = compute_paths(data, args.output_dir)
    formats = args.formats.split(",") if args.formats != "all" else ["html", "pdf", "md"]

    results = {}

    if "html" in formats and report_type in HTML_GENERATORS:
        HTML_GENERATORS[report_type](data, paths["html"])
        results["html"] = paths["html"]

    if "pdf" in formats and report_type in PDF_GENERATORS:
        PDF_GENERATORS[report_type](data, paths["pdf"])
        results["pdf"] = paths["pdf"]

    if "md" in formats and report_type in MD_GENERATORS:
        MD_GENERATORS[report_type](data, paths["md"])
        results["md"] = paths["md"]

    results["output_folder"] = paths["folder"]
    results["type"] = report_type
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
