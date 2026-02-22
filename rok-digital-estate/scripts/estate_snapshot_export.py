#!/usr/bin/env python3
"""
Estate Snapshot Export -- Generate MD, PDF, and HTML from digital estate data.

Usage:
    python3 estate_snapshot_export.py --input /tmp/estate_snapshot_export.json
    python3 estate_snapshot_export.py --input data.json --output-dir /custom/path/
    python3 estate_snapshot_export.py --input data.json --formats html,pdf

Input: JSON payload from estate-synthesizer agent or command output
Output: .html, .pdf, .md in {output_dir}/ folder

Supported types: estate_snapshot
"""

import argparse
import json
import os
import re
import sys
from datetime import date

# Use venv packages
VENV_SITE = os.path.expanduser("~/.claude/scripts/.venv/lib")
if os.path.isdir(VENV_SITE):
    for d in os.listdir(VENV_SITE):
        sp = os.path.join(VENV_SITE, d, "site-packages")
        if os.path.isdir(sp) and sp not in sys.path:
            sys.path.insert(0, sp)

from fpdf import FPDF

# -- Constants ----------------------------------------------------------------

DEFAULT_OUTPUT_DIR = os.path.expanduser("~/projects/rok-copilot/estate-snapshots")

# Color palette: Slate + Amber
SLATE = "#1E293B"
SLATE_RGB = (30, 41, 59)
AMBER = "#D97706"
AMBER_RGB = (217, 119, 6)
SLATE_LIGHT = "#334155"
SLATE_LIGHT_RGB = (51, 65, 85)
LIGHT_BG = "#FFFBEB"
BORDER_COLOR = "#FDE68A"
TEXT_DARK = "#1A202C"
TEXT_MUTED = "#64748B"
GREEN = "#059669"
GREEN_RGB = (5, 150, 105)

# Urgency tier colors
TIER_COLORS = {
    "CRITICAL":  {"bg": "#FEE2E2", "text": "#991B1B", "border": "#DC2626", "rgb": (220, 38, 38)},
    "ATTENTION": {"bg": "#FEF3C7", "text": "#92400E", "border": "#D97706", "rgb": (217, 119, 6)},
    "MONITOR":   {"bg": "#FEF9C3", "text": "#854D0E", "border": "#EAB308", "rgb": (234, 179, 8)},
    "STABLE":    {"bg": "#D1FAE5", "text": "#065F46", "border": "#059669", "rgb": (5, 150, 105)},
}

STATUS_COLORS = {
    "active":    {"bg": "#D1FAE5", "text": "#065F46"},
    "recent":    {"bg": "#DBEAFE", "text": "#1E40AF"},
    "dormant":   {"bg": "#FEF9C3", "text": "#854D0E"},
    "abandoned": {"bg": "#F3F4F6", "text": "#6B7280"},
}

HEALTH_COLORS = {
    "HEALTHY":          {"bg": "#D1FAE5", "text": "#065F46"},
    "NEEDS ATTENTION":  {"bg": "#FEF3C7", "text": "#92400E"},
    "CRITICAL ITEMS":   {"bg": "#FEE2E2", "text": "#991B1B"},
}


# -- Helpers ------------------------------------------------------------------

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:60].strip("-") or "untitled"


def compute_paths(data: dict, output_dir: str):
    d = data.get("date", data.get("snapshot_date", date.today().isoformat()))
    version = data.get("version", 1)
    stem = f"{d}_estate-snapshot_v{version}"

    os.makedirs(output_dir, exist_ok=True)
    return {
        "folder": output_dir,
        "stem": stem,
        "html": os.path.join(output_dir, f"{stem}.html"),
        "pdf": os.path.join(output_dir, f"{stem}.pdf"),
        "md": os.path.join(output_dir, f"{stem}.md"),
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


def format_cost(amount):
    try:
        return f"${float(amount):,.2f}"
    except (TypeError, ValueError):
        return "$0.00"


def tier_badge_html(tier):
    tier = tier.upper() if tier else "STABLE"
    c = TIER_COLORS.get(tier, TIER_COLORS["STABLE"])
    return f'<span style="display:inline-block;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700;color:{c["text"]};background:{c["bg"]}">{tier}</span>'


def status_badge_html(status):
    status = status.lower() if status else "abandoned"
    c = STATUS_COLORS.get(status, STATUS_COLORS["abandoned"])
    return f'<span style="display:inline-block;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700;color:{c["text"]};background:{c["bg"]}">{status.upper()}</span>'


# -- HTML Generation ---------------------------------------------------------

def generate_estate_html(data: dict, output_path: str):
    version = data.get("version", 1)
    gen_date = escape_html(data.get("snapshot_date", data.get("date", date.today().isoformat())))
    estate_health = data.get("estate_health", "UNKNOWN")
    exec_summary = escape_html(data.get("executive_summary", ""))
    projects = data.get("unified_projects", [])
    bus_factor = data.get("bus_factor_dashboard", {})
    deployment_map = data.get("deployment_map", {})
    cost_summary = data.get("cost_summary", {})
    access_guide = data.get("access_guide", [])
    memory = data.get("memory_highlights", {})
    contacts = data.get("contacts", [])
    emergency_steps = data.get("emergency_steps", [])
    cross_ref = data.get("cross_reference_notes", {})
    completeness = data.get("completeness_score", 0)

    # Health badge
    hc = HEALTH_COLORS.get(estate_health, HEALTH_COLORS["NEEDS ATTENTION"])
    health_badge = f'<span style="display:inline-block;padding:4px 16px;border-radius:12px;font-size:14px;font-weight:700;color:{hc["text"]};background:{hc["bg"]}">{escape_html(estate_health)}</span>'

    # Bus Factor rows by tier
    def bus_factor_rows(tier_key):
        items = bus_factor.get(tier_key, [])
        rows = ""
        for item in items:
            tc = TIER_COLORS.get(tier_key.upper(), TIER_COLORS["STABLE"])
            rows += f"""
            <tr>
              <td style="font-weight:600">{escape_html(item.get('item', ''))}</td>
              <td>{escape_html(item.get('type', ''))}</td>
              <td style="text-align:center;font-weight:700;color:{tc['text']}">{item.get('days_left', 'N/A')}</td>
              <td style="font-size:12px">{escape_html(item.get('risk', ''))}</td>
              <td style="font-size:12px;color:{AMBER}">{escape_html(item.get('action', ''))}</td>
            </tr>"""
        return rows

    # Project inventory rows
    proj_rows = ""
    for i, p in enumerate(projects, 1):
        proj_rows += f"""
        <tr>
          <td style="text-align:center">{i}</td>
          <td style="font-weight:600">{escape_html(p.get('name', ''))}</td>
          <td style="text-align:center">{status_badge_html(p.get('status', ''))}</td>
          <td style="font-size:11px">{escape_html(', '.join(p.get('tech_stack', [])))}</td>
          <td style="font-size:11px;font-family:monospace">{escape_html(p.get('local_path', ''))}</td>
          <td style="font-size:11px">{escape_html(p.get('deployment_url', '') or 'none')}</td>
          <td style="font-size:11px">{escape_html(p.get('last_activity', ''))}</td>
        </tr>"""

    # Deployment rows
    deploy_rows = ""
    for site in deployment_map.get("netlify_sites", []) + deployment_map.get("vercel_projects", []):
        provider = "Netlify" if site in deployment_map.get("netlify_sites", []) else "Vercel"
        deploy_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(site.get('name', ''))}</td>
          <td>{provider}</td>
          <td style="font-size:11px">{escape_html(site.get('url', ''))}</td>
          <td style="font-size:11px">{escape_html(', '.join(site.get('custom_domains', [])) or 'none')}</td>
          <td>{escape_html(site.get('ssl_status', site.get('deploy_status', '')))}</td>
          <td style="font-size:11px">{escape_html(site.get('last_deploy', ''))}</td>
        </tr>"""

    # Subscription rows
    sub_rows = ""
    for sub in cost_summary.get("subscriptions", []):
        sub_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(sub.get('service', ''))}</td>
          <td style="text-align:right">{format_cost(sub.get('monthly_cost', 0))}</td>
          <td style="text-align:center">{escape_html(sub.get('renewal_date', ''))}</td>
          <td style="text-align:center">{escape_html('Yes' if sub.get('auto_renew') else 'NO')}</td>
          <td style="font-size:11px">{escape_html(sub.get('payment_method', ''))}</td>
        </tr>"""

    # Access guide rows
    access_rows = ""
    for svc in access_guide:
        access_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(svc.get('service', ''))}</td>
          <td style="font-size:11px">{escape_html(svc.get('url', ''))}</td>
          <td style="font-size:11px">{escape_html(svc.get('login_method', ''))}</td>
          <td style="font-size:11px">{escape_html(svc.get('credential_location', ''))}</td>
        </tr>"""

    # Contact rows
    contact_rows = ""
    for c in contacts:
        contact_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(c.get('name', ''))}</td>
          <td>{escape_html(c.get('role', ''))}</td>
          <td>{escape_html(c.get('email', ''))}</td>
          <td>{escape_html(c.get('phone', ''))}</td>
          <td style="font-size:11px">{escape_html(', '.join(c.get('projects', [])) if isinstance(c.get('projects'), list) else c.get('projects', ''))}</td>
        </tr>"""

    # Memory highlights
    decisions_html = ""
    for d in memory.get("key_decisions", []):
        if isinstance(d, str):
            decisions_html += f"""
        <tr>
          <td style="font-weight:600" colspan="3">{escape_html(d)}</td>
        </tr>"""
        else:
            decisions_html += f"""
        <tr>
          <td style="font-weight:600">{escape_html(d.get('key', d.get('decision', '')))}</td>
          <td style="font-size:12px">{escape_html(d.get('value', d.get('context', '')))}</td>
          <td style="font-size:11px">{escape_html(d.get('created_at', d.get('date', '')))}</td>
        </tr>"""

    gotchas_html = ""
    for g in memory.get("known_gotchas", []):
        if isinstance(g, str):
            gotchas_html += f"""
        <tr>
          <td style="font-weight:600" colspan="3">{escape_html(g)}</td>
        </tr>"""
        else:
            gotchas_html += f"""
        <tr>
          <td style="font-weight:600">{escape_html(g.get('key', g.get('gotcha', '')))}</td>
          <td style="font-size:12px">{escape_html(g.get('impact', ''))}</td>
          <td style="font-size:12px">{escape_html(g.get('workaround', ''))}</td>
        </tr>"""

    # Emergency steps
    steps_html = ""
    for i, step in enumerate(emergency_steps, 1):
        step_text = step if isinstance(step, str) else step.get("step", str(step))
        steps_html += f"""
        <div style="padding:12px 16px;border-left:4px solid {AMBER};margin-bottom:8px;background:{LIGHT_BG}">
          <strong style="color:{SLATE};font-size:16px">{i}.</strong>
          <span style="color:{TEXT_DARK};margin-left:8px">{escape_html(step_text)}</span>
        </div>"""

    # Plugin Portfolio section
    plugin_portfolio = data.get("plugin_portfolio", {})
    plugin_section_html = ""
    if plugin_portfolio:
        categories = plugin_portfolio.get("categories", {})
        cat_html = ""
        for cat_name, plugins in categories.items():
            plugin_rows = ""
            for pl in plugins:
                plugin_rows += f"""
                <tr>
                  <td style="font-weight:600;white-space:nowrap">{escape_html(pl.get('name', ''))}</td>
                  <td style="font-size:12px">{escape_html(pl.get('description', ''))}</td>
                </tr>"""
            cat_html += f"""
            <h3 style="margin-top:16px">{escape_html(cat_name)} ({len(plugins)})</h3>
            <table><tr><th style="width:200px">Plugin</th><th>Description</th></tr>
            {plugin_rows}
            </table>"""
        plugin_section_html = f"""
<div class="section">
  <h2>11. Plugin Portfolio</h2>
  <p style="color:{TEXT_MUTED};font-size:13px;margin-bottom:12px">
    {plugin_portfolio.get('total_plugins', 0)} custom Claude Code plugins in
    <a href="{escape_html(plugin_portfolio.get('repository', ''))}" style="color:{AMBER}">rok-plugin-marketplace</a>
  </p>
  <div class="summary-grid">
    <div class="summary-card"><div class="label">Total Plugins</div><div class="value">{plugin_portfolio.get('total_plugins', 0)}</div></div>
    <div class="summary-card"><div class="label">Categories</div><div class="value">{len(categories)}</div></div>
  </div>
  {cat_html}
</div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Digital Estate Snapshot v{version}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:#F8FAFC; color:{TEXT_DARK}; line-height:1.6; }}
  .container {{ max-width:1100px; margin:0 auto; padding:24px; }}
  .header {{ background:linear-gradient(135deg,{SLATE},{SLATE_LIGHT}); color:white; padding:32px; border-radius:12px; margin-bottom:24px; }}
  .header h1 {{ font-size:28px; margin-bottom:8px; }}
  .header .meta {{ font-size:13px; opacity:0.85; }}
  .confidential {{ background:#DC2626; color:white; display:inline-block; padding:2px 12px; border-radius:4px; font-size:11px; font-weight:700; letter-spacing:1px; margin-top:8px; }}
  .section {{ background:white; border-radius:10px; padding:24px; margin-bottom:20px; box-shadow:0 1px 3px rgba(0,0,0,0.08); }}
  .section h2 {{ color:{SLATE}; font-size:20px; border-bottom:2px solid {AMBER}; padding-bottom:8px; margin-bottom:16px; }}
  .section h3 {{ color:{SLATE_LIGHT}; font-size:15px; margin:16px 0 8px; }}
  table {{ width:100%; border-collapse:collapse; margin:12px 0; }}
  th {{ background:{SLATE}; color:white; padding:8px 12px; text-align:left; font-size:12px; font-weight:600; }}
  td {{ padding:8px 12px; border-bottom:1px solid #E2E8F0; font-size:13px; }}
  tr:nth-child(even) {{ background:#F8FAFC; }}
  .summary-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; margin:16px 0; }}
  .summary-card {{ background:{LIGHT_BG}; border:1px solid {BORDER_COLOR}; border-radius:8px; padding:16px; text-align:center; }}
  .summary-card .label {{ font-size:12px; color:{TEXT_MUTED}; text-transform:uppercase; font-weight:600; }}
  .summary-card .value {{ font-size:24px; font-weight:700; color:{SLATE}; margin-top:4px; }}
  .tier-section {{ margin:16px 0; }}
  .tier-header {{ padding:8px 16px; border-radius:8px 8px 0 0; font-weight:700; font-size:14px; }}
  @media print {{ .container {{ max-width:100%; padding:0; }} .section {{ break-inside:avoid; box-shadow:none; border:1px solid #E2E8F0; }} }}
</style>
</head>
<body>
<div class="container">

<div class="header">
  <h1>Digital Estate Snapshot v{version}</h1>
  <div class="meta">Generated: {gen_date} | Projects: {len(projects)} | Monthly Burn: {format_cost(cost_summary.get('monthly_burn', 0))} | Completeness: {completeness}%</div>
  <div style="margin-top:8px">{health_badge}</div>
  <div class="confidential">CONFIDENTIAL</div>
</div>

<!-- 1. Executive Summary -->
<div class="section">
  <h2>1. Executive Summary</h2>
  <p>{exec_summary.replace(chr(10), '<br>')}</p>
  <div class="summary-grid">
    <div class="summary-card"><div class="label">Total Projects</div><div class="value">{len(projects)}</div></div>
    <div class="summary-card"><div class="label">Monthly Burn</div><div class="value">{format_cost(cost_summary.get('monthly_burn', 0))}</div></div>
    <div class="summary-card"><div class="label">Critical Items</div><div class="value" style="color:#DC2626">{len(bus_factor.get('critical', []))}</div></div>
    <div class="summary-card"><div class="label">Completeness</div><div class="value">{completeness}%</div></div>
  </div>
</div>

<!-- 2. Bus Factor Dashboard -->
<div class="section">
  <h2>2. Bus Factor Dashboard</h2>
  <p style="color:{TEXT_MUTED};font-size:13px;margin-bottom:16px">Items sorted by urgency. This is the "what breaks first" view.</p>

  <div class="tier-section">
    <div class="tier-header" style="background:#FEE2E2;color:#991B1B">CRITICAL -- Action Required Within 30 Days ({len(bus_factor.get('critical', []))} items)</div>
    <table><tr><th>Item</th><th>Type</th><th>Days Left</th><th>Risk</th><th>Action Needed</th></tr>
    {bus_factor_rows('critical')}
    </table>
  </div>

  <div class="tier-section">
    <div class="tier-header" style="background:#FEF3C7;color:#92400E">ATTENTION -- Review Within 60 Days ({len(bus_factor.get('attention', []))} items)</div>
    <table><tr><th>Item</th><th>Type</th><th>Days Left</th><th>Risk</th><th>Action Needed</th></tr>
    {bus_factor_rows('attention')}
    </table>
  </div>

  <div class="tier-section">
    <div class="tier-header" style="background:#FEF9C3;color:#854D0E">MONITOR -- Check Within 90 Days ({len(bus_factor.get('monitor', []))} items)</div>
    <table><tr><th>Item</th><th>Type</th><th>Days Left</th><th>Risk</th><th>Action Needed</th></tr>
    {bus_factor_rows('monitor')}
    </table>
  </div>

  <div style="padding:12px;background:#D1FAE5;border-radius:8px;color:#065F46;font-weight:600">
    STABLE -- {bus_factor.get('stable_count', 0)} items are auto-renewing and stable.
  </div>
</div>

<!-- 3. Project Inventory -->
<div class="section">
  <h2>3. Project Inventory</h2>
  <table>
    <tr><th>#</th><th>Project</th><th>Status</th><th>Tech Stack</th><th>Local Path</th><th>Deployment</th><th>Last Activity</th></tr>
    {proj_rows}
  </table>
  <h3>Cross-Reference Notes</h3>
  <ul style="font-size:13px;color:{TEXT_MUTED};padding-left:20px">
    <li><strong>Orphan repos</strong> (GitHub only): {', '.join((r if isinstance(r, str) else r.get('name', '')) for r in cross_ref.get('orphan_repos', [])) or 'None'}</li>
    <li><strong>Local only</strong> (no GitHub): {', '.join((p if isinstance(p, str) else p.get('name', '')) for p in cross_ref.get('local_only', [])) or 'None'}</li>
    <li><strong>Dirty repos</strong> (unpushed): {', '.join((d if isinstance(d, str) else d.get('name', '')) for d in cross_ref.get('dirty_repos', [])) or 'None'}</li>
  </ul>
</div>

<!-- 4. Deployment Map -->
<div class="section">
  <h2>4. Deployment Map</h2>
  <table>
    <tr><th>Site</th><th>Provider</th><th>URL</th><th>Custom Domain</th><th>Status</th><th>Last Deploy</th></tr>
    {deploy_rows}
  </table>
</div>

<!-- 5. Infrastructure & Hosting (rendered from exec summary data) -->
<div class="section">
  <h2>5. Infrastructure & Hosting</h2>
  <p style="font-size:13px;color:{TEXT_MUTED}">See estate-config.json for full infrastructure details.</p>
</div>

<!-- 6. Subscriptions & Costs -->
<div class="section">
  <h2>6. Subscriptions & Costs</h2>
  <div class="summary-grid">
    <div class="summary-card"><div class="label">Monthly Burn</div><div class="value">{format_cost(cost_summary.get('monthly_burn', 0))}</div></div>
    <div class="summary-card"><div class="label">Annual Burn</div><div class="value">{format_cost(cost_summary.get('annual_burn', 0))}</div></div>
  </div>
  <table>
    <tr><th>Service</th><th>Cost/mo</th><th>Renewal</th><th>Auto-Renew</th><th>Payment</th></tr>
    {sub_rows}
  </table>
</div>

<!-- 7. Access Guide -->
<div class="section">
  <h2>7. Access Guide</h2>
  <div style="background:#FEF3C7;padding:8px 16px;border-radius:8px;margin-bottom:12px;font-size:13px;color:#92400E">
    This section does NOT contain actual passwords. See credential master location for all passwords and recovery codes.
  </div>
  <table>
    <tr><th>Service</th><th>URL</th><th>Login Method</th><th>Credential Location</th></tr>
    {access_rows}
  </table>
</div>

<!-- 8. ROK Memory Highlights -->
<div class="section">
  <h2>8. ROK Memory Highlights</h2>
  <h3>Key Architectural Decisions</h3>
  <table>
    <tr><th>Decision</th><th>Context</th><th>Date</th></tr>
    {decisions_html}
  </table>
  <h3>Known Gotchas</h3>
  <table>
    <tr><th>Gotcha</th><th>Impact</th><th>Workaround</th></tr>
    {gotchas_html}
  </table>
</div>

<!-- 9. Contact List -->
<div class="section">
  <h2>9. Contact List</h2>
  <table>
    <tr><th>Name</th><th>Role</th><th>Email</th><th>Phone</th><th>Projects</th></tr>
    {contact_rows}
  </table>
</div>

<!-- 10. Quick Start -->
<div class="section">
  <h2>10. "If Something Happens" Quick Start</h2>
  <p style="color:{TEXT_MUTED};font-size:13px;margin-bottom:16px">For Ron's sons -- numbered steps in priority order:</p>
  {steps_html}
</div>

<!-- 11. Plugin Portfolio -->
{plugin_section_html}

<div style="text-align:center;padding:16px;color:{TEXT_MUTED};font-size:12px">
  Digital Estate Snapshot v{version} | Generated {gen_date} | rok-digital-estate plugin
</div>

</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


# -- PDF Generation ----------------------------------------------------------

class EstatePDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*SLATE_LIGHT_RGB)
        self.cell(0, 6, "CONFIDENTIAL - Digital Estate Snapshot", align="C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, f"Digital Estate Snapshot | Page {self.page_no()}", align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*SLATE_RGB)
        self.cell(0, 10, latin_safe(title), ln=True)
        self.set_draw_color(*AMBER_RGB)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_title(self, title: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*SLATE_LIGHT_RGB)
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
        self.set_fill_color(*SLATE_RGB)
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
            for i, cell_text in enumerate(row):
                safe = latin_safe(str(cell_text))[:int(col_widths[i] / 1.8)]
                self.cell(col_widths[i], 7, safe, 1, 0, "L", fill=True)
            self.ln()
            fill = not fill
        self.ln(4)


def generate_estate_pdf(data: dict, output_path: str):
    pdf = EstatePDF()
    pdf.add_page()

    version = data.get("version", 1)
    gen_date = data.get("snapshot_date", data.get("date", date.today().isoformat()))
    projects = data.get("unified_projects", [])
    bus_factor = data.get("bus_factor_dashboard", {})
    cost_summary = data.get("cost_summary", {})
    access_guide = data.get("access_guide", [])
    contacts = data.get("contacts", [])
    emergency_steps = data.get("emergency_steps", [])

    # Title page
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*SLATE_RGB)
    pdf.cell(0, 14, f"Digital Estate Snapshot v{version}", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, f"Generated: {gen_date} | Projects: {len(projects)} | Monthly Burn: {format_cost(cost_summary.get('monthly_burn', 0))}", ln=True)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(220, 38, 38)
    pdf.cell(0, 8, "CONFIDENTIAL", ln=True)
    pdf.ln(8)

    # 1. Executive Summary
    pdf.section_title("1. Executive Summary")
    pdf.body_text(data.get("executive_summary", "No summary available."))

    # 2. Bus Factor Dashboard
    pdf.section_title("2. Bus Factor Dashboard")
    for tier_key, tier_label in [("critical", "CRITICAL"), ("attention", "ATTENTION"), ("monitor", "MONITOR")]:
        items = bus_factor.get(tier_key, [])
        if items:
            tc = TIER_COLORS[tier_label]
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(*tc["rgb"])
            pdf.cell(0, 7, f"{tier_label} ({len(items)} items)", ln=True)
            rows = [[it.get("item", "")[:40], it.get("type", ""),
                      str(it.get("days_left", "")), it.get("action", "")[:50]] for it in items]
            pdf.add_table(["Item", "Type", "Days", "Action"], rows, [60, 30, 20, 80])

    stable_count = bus_factor.get("stable_count", 0)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GREEN_RGB)
    pdf.cell(0, 7, f"STABLE: {stable_count} items auto-renewing and stable.", ln=True)
    pdf.ln(4)

    # 3. Project Inventory
    pdf.section_title("3. Project Inventory")
    if projects:
        rows = [[p.get("name", "")[:30], p.get("status", "").upper(),
                  ", ".join(p.get("tech_stack", []))[:30],
                  (p.get("deployment_url") or "none")[:40],
                  p.get("last_activity", "") or ""] for p in projects]
        pdf.add_table(["Project", "Status", "Stack", "Deployment", "Last Activity"], rows,
                     [40, 22, 40, 55, 33])

    # 6. Subscriptions & Costs
    subs = cost_summary.get("subscriptions", [])
    if subs:
        pdf.section_title("6. Subscriptions & Costs")
        pdf.body_text(f"Monthly Burn: {format_cost(cost_summary.get('monthly_burn', 0))} | Annual: {format_cost(cost_summary.get('annual_burn', 0))}")
        rows = [[s.get("service", "")[:30], format_cost(s.get("monthly_cost", 0)),
                  s.get("renewal_date", ""),
                  "Yes" if s.get("auto_renew") else "NO"] for s in subs]
        pdf.add_table(["Service", "Cost/mo", "Renewal", "Auto-Renew"], rows,
                     [50, 30, 40, 30])

    # 7. Access Guide
    if access_guide:
        pdf.section_title("7. Access Guide")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(146, 64, 14)
        pdf.cell(0, 6, "NO actual passwords in this document. See credential master location.", ln=True)
        pdf.ln(2)
        rows = [[s.get("service", ""), s.get("login_method", "")[:40],
                  s.get("credential_location", "")[:40]] for s in access_guide]
        pdf.add_table(["Service", "Login Method", "Credential Location"], rows,
                     [40, 75, 75])

    # 9. Contact List
    if contacts:
        pdf.section_title("9. Contact List")
        rows = [[c.get("name", ""), c.get("role", "")[:30],
                  c.get("email", ""), c.get("phone", "")] for c in contacts]
        pdf.add_table(["Name", "Role", "Email", "Phone"], rows,
                     [40, 40, 55, 55])

    # 10. Quick Start
    if emergency_steps:
        pdf.section_title("10. Quick Start")
        for i, step in enumerate(emergency_steps, 1):
            step_text = step if isinstance(step, str) else step.get("step", str(step))
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(*AMBER_RGB)
            pdf.cell(8, 6, f"{i}.")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(26, 32, 44)
            pdf.multi_cell(0, 5, latin_safe(step_text))
            pdf.ln(2)

    # 11. Plugin Portfolio
    plugin_portfolio = data.get("plugin_portfolio", {})
    if plugin_portfolio:
        pdf.section_title(f"11. Plugin Portfolio ({plugin_portfolio.get('total_plugins', 0)} plugins)")
        categories = plugin_portfolio.get("categories", {})
        for cat_name, plugins in categories.items():
            pdf.sub_title(f"{cat_name} ({len(plugins)})")
            rows = [[pl.get("name", ""), pl.get("description", "")[:80]] for pl in plugins]
            pdf.add_table(["Plugin", "Description"], rows, [50, 140])

    pdf.output(output_path)


# -- Markdown Generation -----------------------------------------------------

def generate_estate_md(data: dict, output_path: str):
    # Use pre-rendered full_estate_md if available
    if data.get("full_estate_md"):
        md = data["full_estate_md"]
    else:
        version = data.get("version", 1)
        gen_date = data.get("snapshot_date", data.get("date", date.today().isoformat()))
        projects = data.get("unified_projects", [])
        cost_summary = data.get("cost_summary", {})
        bus_factor = data.get("bus_factor_dashboard", {})

        lines = [
            f"# Digital Estate Snapshot v{version}",
            f"**Generated:** {gen_date} | **Projects:** {len(projects)} | **Monthly Burn:** {format_cost(cost_summary.get('monthly_burn', 0))}",
            "",
            "**CONFIDENTIAL**",
            "",
            "---",
            "",
            "## 1. Executive Summary",
            data.get("executive_summary", "No summary available."),
            "",
            "---",
            "",
            "## 2. Bus Factor Dashboard",
            "",
        ]

        for tier_key, tier_label in [("critical", "CRITICAL"), ("attention", "ATTENTION"), ("monitor", "MONITOR")]:
            items = bus_factor.get(tier_key, [])
            lines.append(f"### {tier_label} ({len(items)} items)")
            if items:
                lines.append("| Item | Type | Days Left | Risk | Action |")
                lines.append("|------|------|-----------|------|--------|")
                for it in items:
                    lines.append(f"| {it.get('item', '')} | {it.get('type', '')} | {it.get('days_left', '')} | {it.get('risk', '')} | {it.get('action', '')} |")
            else:
                lines.append("No items in this tier.")
            lines.append("")

        lines.append(f"**STABLE:** {bus_factor.get('stable_count', 0)} items auto-renewing and stable.")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 3. Project Inventory
        lines.append("## 3. Project Inventory")
        lines.append("| # | Project | Status | Tech Stack | Deployment | Last Activity |")
        lines.append("|---|---------|--------|------------|------------|---------------|")
        for i, p in enumerate(projects, 1):
            lines.append(f"| {i} | {p.get('name', '')} | {p.get('status', '').upper()} | {', '.join(p.get('tech_stack', []))} | {p.get('deployment_url', 'none')} | {p.get('last_activity', '')} |")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 6. Subscriptions
        lines.append("## 6. Subscriptions & Costs")
        lines.append(f"**Monthly Burn:** {format_cost(cost_summary.get('monthly_burn', 0))} | **Annual:** {format_cost(cost_summary.get('annual_burn', 0))}")
        lines.append("")
        subs = cost_summary.get("subscriptions", [])
        if subs:
            lines.append("| Service | Cost/mo | Renewal | Auto-Renew |")
            lines.append("|---------|---------|---------|------------|")
            for s in subs:
                lines.append(f"| {s.get('service', '')} | {format_cost(s.get('monthly_cost', 0))} | {s.get('renewal_date', '')} | {'Yes' if s.get('auto_renew') else 'NO'} |")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 10. Quick Start
        lines.append("## 10. Quick Start")
        for i, step in enumerate(data.get("emergency_steps", []), 1):
            step_text = step if isinstance(step, str) else step.get("step", str(step))
            lines.append(f"{i}. {step_text}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 11. Plugin Portfolio
        plugin_portfolio = data.get("plugin_portfolio", {})
        if plugin_portfolio:
            lines.append(f"## 11. Plugin Portfolio ({plugin_portfolio.get('total_plugins', 0)} plugins)")
            lines.append(f"**Repository:** {plugin_portfolio.get('repository', '')}")
            lines.append("")
            for cat_name, plugins in plugin_portfolio.get("categories", {}).items():
                lines.append(f"### {cat_name} ({len(plugins)})")
                lines.append("| Plugin | Description |")
                lines.append("|--------|-------------|")
                for pl in plugins:
                    lines.append(f"| {pl.get('name', '')} | {pl.get('description', '')} |")
                lines.append("")
            lines.append("---")
            lines.append("")

        lines.append(f"*Digital Estate Snapshot v{version} | Generated {gen_date} | rok-digital-estate plugin*")

        md = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)


# -- Dispatch ----------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Estate Snapshot Export")
    parser.add_argument("--input", required=True, help="Path to JSON input file")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Output directory")
    parser.add_argument("--formats", default="all", help="Export formats: all, html, pdf, md (comma-separated)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    paths = compute_paths(data, args.output_dir)
    formats = args.formats.split(",") if args.formats != "all" else ["html", "pdf", "md"]

    results = {}

    if "html" in formats:
        generate_estate_html(data, paths["html"])
        results["html"] = paths["html"]

    if "pdf" in formats:
        generate_estate_pdf(data, paths["pdf"])
        results["pdf"] = paths["pdf"]

    if "md" in formats:
        generate_estate_md(data, paths["md"])
        results["md"] = paths["md"]

    results["output_folder"] = paths["folder"]
    results["type"] = "estate_snapshot"
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
