#!/usr/bin/env python3
"""
Repo Summary Export -- Generate MD, PDF, and HTML from repo analysis data.

Usage:
    python3 repo_summary_export.py --input /tmp/repo_summary_export.json
    python3 repo_summary_export.py --input data.json --output-dir /custom/path/

Input: JSON payload from summary-synthesizer agent
Output: .html, .pdf, .md in {output_dir}/Repo_Summaries/ folder
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

TEAL = "#0F766E"
TEAL_RGB = (15, 118, 110)
TEAL_LIGHT = "#CCFBF1"
TEAL_DARK = "#134E4A"
AMBER = "#D97706"
AMBER_RGB = (217, 119, 6)
AMBER_LIGHT = "#FEF3C7"
AMBER_DARK = "#92400E"
LIGHT_BG = "#F8FAFC"
BORDER_COLOR = "#E2E8F0"

MATURITY_COLORS = {
    "MATURE": {"bg": "#059669", "text": "#FFFFFF", "label": "MATURE"},
    "DEVELOPING": {"bg": "#D97706", "text": "#FFFFFF", "label": "DEVELOPING"},
    "EARLY_STAGE": {"bg": "#3B82F6", "text": "#FFFFFF", "label": "EARLY STAGE"},
    "PROTOTYPE": {"bg": "#7C3AED", "text": "#FFFFFF", "label": "PROTOTYPE"},
}

STATUS_COLORS = {
    "complete": {"bg": "#D1FAE5", "text": "#065F46", "label": "Complete"},
    "partial": {"bg": "#FEF3C7", "text": "#92400E", "label": "Partial"},
    "stub": {"bg": "#FEE2E2", "text": "#991B1B", "label": "Stub"},
    "planned": {"bg": "#E0E7FF", "text": "#3730A3", "label": "Planned"},
}

SEVERITY_COLORS = {
    "CRITICAL": {"bg": "#FEE2E2", "text": "#991B1B", "header_bg": "#DC2626"},
    "HIGH": {"bg": "#FFF7ED", "text": "#9A3412", "header_bg": "#EA580C"},
    "MEDIUM": {"bg": "#FEFCE8", "text": "#854D0E", "header_bg": "#CA8A04"},
    "LOW": {"bg": "#F0FDF4", "text": "#166534", "header_bg": "#16A34A"},
}

INFRA_QUALITY_COLORS = {
    "complete": {"bg": "#D1FAE5", "text": "#065F46"},
    "partial": {"bg": "#FEF3C7", "text": "#92400E"},
    "missing": {"bg": "#FEE2E2", "text": "#991B1B"},
}

SCORE_COLORS = [
    (80, "#D1FAE5", "#065F46"),  # Mature
    (60, "#FEF3C7", "#854D0E"),  # Developing
    (40, "#DBEAFE", "#1E40AF"),  # Early Stage
    (0, "#EDE9FE", "#5B21B6"),   # Prototype
]

DIMENSION_NAMES = {
    "documentation": "Documentation",
    "feature_completeness": "Feature Completeness",
    "infrastructure": "Infrastructure",
    "test_presence": "Test Presence",
    "architecture_clarity": "Architecture Clarity",
}

INFRA_DISPLAY_NAMES = {
    "error_handling": "Error Handling",
    "logging": "Logging",
    "input_validation": "Input Validation",
    "rate_limiting": "Rate Limiting",
    "health_check": "Health Check",
    "cors": "CORS",
    "env_config": "Env Config",
    "ci_cd": "CI/CD",
    "migrations": "Migrations",
    "secrets": "Secrets",
}

RECENCY_COLORS = {
    "active": {"bg": "#D1FAE5", "text": "#065F46", "label": "Active"},
    "stable": {"bg": "#DBEAFE", "text": "#1E40AF", "label": "Stable"},
    "stale": {"bg": "#FEE2E2", "text": "#991B1B", "label": "Stale"},
}

CHAIN_ICONS = {
    "complete": "&#10003;",  # checkmark
    "broken": "&#10007;",    # x mark
    "not_traced": "-",
}

# Words that should always be uppercase in gap type labels
UPPERCASE_WORDS = {"ux", "ui", "api", "ci", "cd", "cors", "csrf", "sql", "xss", "jwt", "ssh", "ssl", "tls"}


def format_label(raw: str) -> str:
    """Convert underscore_case like 'ux_gap' or 'ui' to proper case: 'UX Gap', 'UI'."""
    words = raw.replace("_", " ").split()
    return " ".join(w.upper() if w.lower() in UPPERCASE_WORDS else w.title() for w in words)


# Backward compat alias
format_gap_type = format_label


# -- Helpers ------------------------------------------------------------------

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:60].strip("-") or "untitled"


def compute_paths(data: dict, output_dir: str):
    project = slugify(data.get("project_name", "project"))
    d = data.get("date", date.today().isoformat())
    stem = f"{d}_{project}_Repo_Summary"
    folder = os.path.join(output_dir, "Repo_Summaries")
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


def group_gaps_by_severity(gaps: list) -> dict:
    groups = {}
    order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    for gap in gaps:
        sev = gap.get("severity", "LOW").upper()
        if sev not in order:
            sev = "LOW"
        groups.setdefault(sev, []).append(gap)
    return {k: groups[k] for k in order if k in groups}


def _html_stack_deps(data: dict) -> str:
    """Build HTML tables for categorized stack dependencies."""
    stack_deps = data.get("stack_dependencies", {})
    if not stack_deps:
        return ""
    sections = []
    for cat, deps in stack_deps.items():
        if not deps:
            continue
        cat_label = escape_html(format_label(cat))
        rows = ""
        for dep in deps:
            if isinstance(dep, str):
                rows += f"<tr><td>{escape_html(dep)}</td><td>-</td><td>-</td></tr>"
            else:
                rows += (f"<tr><td style='font-weight:600'>{escape_html(dep.get('name', ''))}</td>"
                         f"<td style='font-size:12px;color:#64748B'>{escape_html(dep.get('version', ''))}</td>"
                         f"<td style='font-size:12px'>{escape_html(dep.get('purpose', ''))}</td></tr>")
        sections.append(f"""<h3>{cat_label}</h3>
        <table><tr><th>Package</th><th style="width:100px">Version</th><th>Purpose</th></tr>{rows}</table>""")
    return "\n".join(sections)


def _html_test_suite(data: dict) -> str:
    """Build HTML for test suite results section (v1.1)."""
    test_results = data.get("test_results")
    if not test_results:
        return ""
    runner = escape_html(test_results.get("runner", "none"))
    total = test_results.get("total_tests", 0)
    passed = test_results.get("passed_tests", 0)
    failed = test_results.get("failed_tests", 0)
    skipped = test_results.get("skipped_tests", 0)
    rate = test_results.get("pass_rate", 0)
    rate_pct = f"{rate * 100:.0f}%" if isinstance(rate, (int, float)) else "N/A"
    test_files = test_results.get("test_files_count", 0)
    error = test_results.get("error")

    if total == -1:
        status_html = '<span style="color:#991B1B;font-weight:600">Runner failed</span>'
        if error:
            status_html += f'<br><span style="font-size:12px;color:#64748B">{escape_html(error)}</span>'
    elif total == 0:
        status_html = '<span style="color:#64748B">No tests detected</span>'
    else:
        rate_color = "#065F46" if rate >= 0.9 else ("#92400E" if rate >= 0.7 else "#991B1B")
        status_html = f'<span style="color:{rate_color};font-weight:600">{rate_pct} pass rate</span>'

    return f"""
<div class="content">
  <h2>Test Suite</h2>
  <div style="display:flex;gap:20px;margin:16px 0">
    <div style="flex:1;background:#D1FAE5;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#065F46">{passed}</div>
      <div style="font-size:12px;color:#065F46">Passed</div>
    </div>
    <div style="flex:1;background:#FEE2E2;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#991B1B">{failed}</div>
      <div style="font-size:12px;color:#991B1B">Failed</div>
    </div>
    <div style="flex:1;background:#E0E7FF;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#3730A3">{skipped}</div>
      <div style="font-size:12px;color:#3730A3">Skipped</div>
    </div>
  </div>
  <p><strong>Runner:</strong> {runner} | <strong>Total Tests:</strong> {total} | <strong>Test Files:</strong> {test_files} | {status_html}</p>
</div>"""


def _html_integration_chains(data: dict) -> str:
    """Build HTML for integration chains section (v1.1)."""
    chains_data = data.get("integration_chains")
    if not chains_data:
        return ""
    total = chains_data.get("total_traced", 0)
    complete = chains_data.get("complete_chains", 0)
    broken = chains_data.get("broken_chains", 0)
    missing = escape_html(chains_data.get("common_missing_layer", ""))
    chains = chains_data.get("chains", [])

    rows = ""
    for ch in chains:
        area = escape_html(ch.get("feature_area", ""))
        is_complete = ch.get("chain_complete", False)
        layers = ch.get("chain")
        if isinstance(layers, list):
            layer_names = " -> ".join(escape_html(l.get("layer", "")) for l in layers)
        else:
            layer_names = ""
        missing_l = ", ".join(escape_html(m) for m in ch.get("missing_layers", []))
        icon = CHAIN_ICONS.get("complete" if is_complete else "broken", "-")
        color = "#065F46" if is_complete else "#991B1B"
        rows += f"""
        <tr>
          <td style="font-weight:600">{area}</td>
          <td style="font-size:12px">{layer_names}</td>
          <td style="text-align:center;color:{color}">{icon}</td>
          <td style="font-size:12px;color:#64748B">{missing_l or '-'}</td>
        </tr>"""

    summary = f"{complete} of {total} feature chains are complete"
    if missing:
        summary += f" (most common missing layer: {missing})"

    return f"""
  <h3>Integration Chains</h3>
  <p style="font-size:14px;color:#475569">{escape_html(summary)}</p>
  <table>
    <tr>
      <th>Feature Area</th>
      <th>Chain</th>
      <th style="width:60px;text-align:center">Status</th>
      <th style="width:140px">Missing</th>
    </tr>
    {rows}
  </table>"""


def _html_recency(data: dict) -> str:
    """Build HTML for recency data section (v1.1)."""
    recency = data.get("recency_data")
    if not recency:
        return ""
    total_commits = recency.get("total_recent_commits", 0)
    window = escape_html(recency.get("recency_window", "30 days"))
    files = recency.get("recently_active_files", [])[:10]
    dirs = recency.get("recently_active_dirs", [])[:10]

    file_rows = ""
    for f in files:
        fname = escape_html(f.get("file", ""))
        count = f.get("change_count", 0)
        file_rows += f"<tr><td><code style='font-size:12px;background:#F1F5F9;padding:1px 5px;border-radius:3px'>{fname}</code></td><td style='text-align:center'>{count}</td></tr>"

    return f"""
  <h3>Recent Activity ({window})</h3>
  <p><strong>{total_commits}</strong> commits in the last {window}</p>
  {"<h4>Most Active Files</h4><table><tr><th>File</th><th style='width:80px;text-align:center'>Changes</th></tr>" + file_rows + "</table>" if file_rows else ""}"""


# -- HTML Generation ---------------------------------------------------------

def generate_html(data: dict, output_path: str):
    project = escape_html(data.get("project_name", "Project"))
    d = escape_html(data.get("date", ""))
    maturity_level = data.get("maturity_level", "PROTOTYPE")
    score = data.get("maturity_score", 0)
    dim_scores = data.get("dimension_scores", {})
    purpose = data.get("purpose", {})
    features = data.get("features", [])
    feature_summary = data.get("feature_summary", {})
    stack = data.get("stack", {})
    gaps = data.get("gaps", [])
    gap_summary = data.get("gap_summary", {})
    architecture = data.get("architecture", {})
    infra_checklist = data.get("infrastructure_checklist", {})
    recommendations = data.get("recommendations", [])
    exec_summary = escape_html(data.get("executive_summary", ""))
    handoff_brief = data.get("handoff_brief", "")
    suite_ctx = data.get("suite_context")
    git_stats = data.get("git_stats", {})

    mc = MATURITY_COLORS.get(maturity_level, MATURITY_COLORS["PROTOTYPE"])

    # Dimension score bars (Fix 9: handle 0-value scores)
    dim_rows = ""
    for key, info in dim_scores.items():
        ds = info.get("score", 0)
        weight = info.get("weight", 0)
        dn = escape_html(DIMENSION_NAMES.get(key, key))
        bg = score_color_bg(ds)
        tc = score_color_text(ds)
        if ds == 0:
            bar_html = f'''<div style="background:#F1F5F9;border-radius:4px;height:24px;position:relative;display:flex;align-items:center;padding-left:8px">
                <span style="font-size:12px;font-weight:700;color:{tc}">0</span>
              </div>'''
        else:
            pct = max(8, ds)
            bar_html = f'''<div style="background:#F1F5F9;border-radius:4px;height:24px;position:relative;overflow:hidden">
              <div style="background:{bg};height:100%;width:{pct}%;border-radius:4px;display:flex;align-items:center;padding-left:8px">
                <span style="font-size:12px;font-weight:700;color:{tc}">{ds}</span>
              </div>
            </div>'''
        dim_rows += f"""
        <tr>
          <td style="font-weight:600">{dn}</td>
          <td>{bar_html}</td>
          <td style="text-align:center">{int(weight * 100)}%</td>
        </tr>"""

    # Feature inventory table -- detect v1.1 features
    is_v11 = data.get("version", "1.0") >= "1.1"
    feature_rows = ""
    for feat in features:
        st = feat.get("status", "planned")
        sc_info = STATUS_COLORS.get(st, STATUS_COLORS["planned"])
        tests = "Yes" if feat.get("has_tests") else "No"
        ui = "Yes" if feat.get("has_ui") else "No"
        api = "Yes" if feat.get("has_api") else "No"
        compl = feat.get("completeness", 0)
        feat_desc = feat.get("description", "")
        feat_files = feat.get("key_files", [])

        # v1.1 columns
        depth_html = ""
        test_cov_html = ""
        recency_html = ""
        chain_html = ""
        if is_v11:
            depth = feat.get("implementation_depth", {})
            loc = depth.get("avg_handler_loc", 0)
            loc_color = "#065F46" if loc >= 20 else ("#92400E" if loc >= 6 else "#991B1B")
            depth_html = f'<td style="text-align:center"><span style="font-size:11px;font-weight:600;color:{loc_color}">{loc} LOC</span></td>'

            tc = feat.get("test_coverage", {})
            tc_count = tc.get("test_case_count", 0)
            test_cov_html = f'<td style="text-align:center">{tc_count}</td>'

            rs = feat.get("recency_signal", "")
            if rs and rs in RECENCY_COLORS:
                rc = RECENCY_COLORS[rs]
                recency_html = f'<td style="text-align:center"><span style="display:inline-block;background:{rc["bg"]};color:{rc["text"]};font-size:10px;font-weight:600;padding:1px 6px;border-radius:8px">{rc["label"]}</span></td>'
            else:
                recency_html = '<td style="text-align:center">-</td>'

            cs = feat.get("chain_status", "not_traced")
            chain_icon = CHAIN_ICONS.get(cs, "-")
            chain_color = "#065F46" if cs == "complete" else ("#991B1B" if cs == "broken" else "#64748B")
            chain_html = f'<td style="text-align:center;color:{chain_color}">{chain_icon}</td>'

        feature_rows += f"""
        <tr>
          <td style="font-weight:600">{escape_html(feat.get('name', ''))}</td>
          <td>{escape_html(feat.get('category', ''))}</td>
          <td><span style="display:inline-block;background:{sc_info['bg']};color:{sc_info['text']};font-size:11px;font-weight:600;padding:2px 8px;border-radius:10px">{sc_info['label']}</span></td>
          <td style="text-align:center">{compl}%</td>
          <td style="text-align:center">{tests}</td>
          {depth_html}{test_cov_html}{recency_html}{chain_html}
          <td style="text-align:center">{ui}</td>
          <td style="text-align:center">{api}</td>
        </tr>"""
        # Detail row: description + key files
        detail_colspan = 11 if is_v11 else 7
        if feat_desc or feat_files:
            detail_parts = []
            if feat_desc:
                detail_parts.append(f"<span style='color:#475569'>{escape_html(feat_desc)}</span>")
            if feat_files:
                files_html = " ".join(
                    f"<code style='font-size:11px;background:#F1F5F9;padding:1px 5px;border-radius:3px;margin-right:4px'>{escape_html(fp)}</code>"
                    for fp in feat_files[:5]
                )
                detail_parts.append(f"<span style='color:#64748B;font-size:12px'>Files: {files_html}</span>")
            feature_rows += f"""
        <tr>
          <td colspan="{detail_colspan}" style="background:#F8FAFC;padding:4px 12px 8px 24px;border-bottom:1px solid #E2E8F0;font-size:13px">
            {"<br>".join(detail_parts)}
          </td>
        </tr>"""

    # Stack dependencies
    stack_deps = ""
    key_deps = stack.get("key_dependencies", [])
    if key_deps:
        dep_items = ", ".join(escape_html(d) for d in key_deps)
        stack_deps = f"<p><strong>Key Dependencies:</strong> {dep_items}</p>"

    # Architecture key files
    key_files_rows = ""
    arch_key_files = architecture.get("key_files", [])
    for kf in arch_key_files[:20]:
        imp = kf.get("importance", "medium")
        imp_color = {"critical": "#DC2626", "high": "#EA580C", "medium": "#CA8A04", "low": "#16A34A"}.get(imp, "#CA8A04")
        key_files_rows += f"""
        <tr>
          <td><code style="font-size:12px;background:#F1F5F9;padding:2px 6px;border-radius:3px">{escape_html(kf.get('path', ''))}</code></td>
          <td>{escape_html(kf.get('role', ''))}</td>
          <td><span style="color:{imp_color};font-weight:600;font-size:12px">{imp.upper()}</span></td>
        </tr>"""

    # Infrastructure checklist
    infra_rows = ""
    infra_detail = data.get("infrastructure_detail", {})
    for item_key, quality in infra_checklist.items():
        item_name = INFRA_DISPLAY_NAMES.get(item_key, item_key.replace("_", " ").title())
        if isinstance(quality, dict):
            q_val = quality.get("quality", quality.get("status", "missing"))
            notes = quality.get("notes", "")
        else:
            q_val = quality
            notes = infra_detail.get(item_key, {}).get("notes", "")
        qi = INFRA_QUALITY_COLORS.get(q_val, INFRA_QUALITY_COLORS["missing"])
        notes_cell = f'<td style="font-size:12px;color:#64748B">{escape_html(notes)}</td>' if notes else '<td style="font-size:12px;color:#64748B">-</td>'
        infra_rows += f"""
        <tr>
          <td>{escape_html(item_name)}</td>
          <td><span style="display:inline-block;background:{qi['bg']};color:{qi['text']};font-size:11px;font-weight:600;padding:2px 8px;border-radius:10px">{escape_html(q_val.title())}</span></td>
          {notes_cell}
        </tr>"""

    # Gaps table
    grouped_gaps = group_gaps_by_severity(gaps)
    gap_sections = ""
    for sev, sev_gaps in grouped_gaps.items():
        gc = SEVERITY_COLORS.get(sev, SEVERITY_COLORS["LOW"])
        rows = ""
        for g in sev_gaps:
            effort = g.get("effort_estimate", "")
            rows += f"""
            <tr>
              <td style="font-weight:600">{escape_html(g.get('id', ''))}</td>
              <td>{escape_html(g.get('title', ''))}</td>
              <td style="font-size:12px">{escape_html(format_gap_type(g.get('type', '')))}</td>
              <td style="font-size:12px">{escape_html(effort)}</td>
            </tr>
            <tr>
              <td colspan="4" style="background:{gc['bg']};padding:8px 12px;font-size:13px">
                <strong>Fix:</strong> {escape_html(g.get('recommendation', ''))}
              </td>
            </tr>"""
        gap_sections += f"""
        <h3 style="color:{gc['header_bg']}">{sev} ({len(sev_gaps)})</h3>
        <table>
          <tr>
            <th style="background:{gc['header_bg']};width:70px">ID</th>
            <th style="background:{gc['header_bg']}">Gap</th>
            <th style="background:{gc['header_bg']};width:140px">Type</th>
            <th style="background:{gc['header_bg']};width:80px">Effort</th>
          </tr>
          {rows}
        </table>"""

    # Recommendations
    rec_items = "\n".join(f"<li>{escape_html(r)}</li>" for r in recommendations)

    # Navigation tips
    nav_tips = ""
    tips = architecture.get("navigation_tips", [])
    if tips:
        tip_items = "\n".join(f"<li>{escape_html(t)}</li>" for t in tips)
        nav_tips = f"<h3>Navigation Tips</h3><ul>{tip_items}</ul>"

    # Suite context
    suite_html = ""
    if suite_ctx:
        mismatches = suite_ctx.get("version_mismatches", [])
        integration_gaps = suite_ctx.get("integration_gaps", [])
        cross_recs = suite_ctx.get("cross_repo_recommendations", [])

        mm_rows = ""
        for mm in mismatches:
            dep = mm.get("dep", "")
            repos = {k: v for k, v in mm.items() if k != "dep"}
            versions = ", ".join(f"{k}: {v}" for k, v in repos.items())
            mm_rows += f"<tr><td>{escape_html(dep)}</td><td>{escape_html(versions)}</td></tr>"

        ig_items = "\n".join(f"<li>{escape_html(g)}</li>" for g in integration_gaps)
        cr_items = "\n".join(f"<li>{escape_html(r)}</li>" for r in cross_recs)

        suite_html = f"""
<div class="content">
  <h2>Suite Integration Analysis</h2>
  <p><strong>Repos Analyzed:</strong> {', '.join(escape_html(r) for r in suite_ctx.get('repos_analyzed', []))}</p>

  {"<h3>Version Mismatches</h3><table><tr><th>Dependency</th><th>Versions</th></tr>" + mm_rows + "</table>" if mm_rows else ""}
  {"<h3>Integration Gaps</h3><ul>" + ig_items + "</ul>" if ig_items else ""}
  {"<h3>Cross-Repo Recommendations</h3><ol>" + cr_items + "</ol>" if cr_items else ""}
</div>"""

    # Purpose section
    purpose_html = ""
    if purpose:
        target_users = ""
        for tu in purpose.get("target_users", []):
            target_users += f"<li><strong>{escape_html(tu.get('persona', ''))}:</strong> {escape_html(tu.get('description', ''))}</li>"
        deploy = purpose.get("deployment_model", {})
        purpose_html = f"""
  <h2>Purpose</h2>
  <p class="text-block" style="font-size:16px;font-weight:600;color:{TEAL}">{escape_html(purpose.get('statement', ''))}</p>
  <p class="text-block">{escape_html(purpose.get('extended', ''))}</p>
  <p><strong>Type:</strong> {escape_html(purpose.get('project_type', ''))}</p>
  <p><strong>Deploy:</strong> {escape_html(deploy.get('type', ''))} on {escape_html(deploy.get('platform', ''))}</p>
  {"<h3>Target Users</h3><ul>" + target_users + "</ul>" if target_users else ""}"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{project} - Repo Summary</title>
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
  .maturity-badge {{
    display: inline-block;
    padding: 4px 14px;
    border-radius: 14px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: {mc['text']};
    background: {mc['bg']};
  }}
  .score-big {{
    font-size: 48px;
    font-weight: 800;
    color: {TEAL};
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
    color: {TEAL};
    font-size: 18px;
    font-weight: 700;
    margin: 24px 0 12px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid #E2E8F0;
  }}
  h2:first-child {{ margin-top: 0; }}
  h3 {{
    color: {TEAL_DARK};
    font-size: 15px;
    font-weight: 600;
    margin: 16px 0 8px 0;
  }}
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
  ul {{ margin: 8px 0 16px 24px; }}
  ol {{ margin: 8px 0 16px 24px; }}
  li {{ margin-bottom: 6px; }}
  .text-block {{ margin: 8px 0 16px 0; line-height: 1.7; }}
  code {{ font-family: 'Fira Code', 'Consolas', monospace; }}
  .handoff {{
    background: {TEAL_LIGHT};
    border: 2px solid {TEAL};
    border-radius: 8px;
    padding: 24px 32px;
    white-space: pre-wrap;
    font-family: 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
    line-height: 1.6;
    color: {TEAL_DARK};
  }}
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
  <div class="subtitle">Repository Summary &amp; Handoff Document</div>
</div>
<div class="meta-bar">
  <div class="meta-item"><strong>Date:</strong> {d}</div>
  <div class="meta-item"><strong>Stack:</strong> {escape_html(stack.get('framework', ''))} + {escape_html(stack.get('database', ''))}</div>
  <div class="meta-item"><strong>Language:</strong> {escape_html(stack.get('primary_language', ''))}</div>
  <div class="meta-item"><strong>Deploy:</strong> {escape_html(stack.get('deployment', ''))}</div>
  {"<div class='meta-item'><strong>Commits:</strong> " + escape_html(str(git_stats.get('commit_count', ''))) + "</div>" if git_stats.get('commit_count') else ""}
  {"<div class='meta-item'><strong>Last Commit:</strong> " + escape_html(str(git_stats.get('last_commit', ''))) + "</div>" if git_stats.get('last_commit') else ""}
  {"<div class='meta-item'><strong>Contributors:</strong> " + escape_html(', '.join(git_stats.get('contributors', [])[:3])) + "</div>" if git_stats.get('contributors') else ""}
  <div class="maturity-badge">{mc['label']}</div>
</div>

<!-- Maturity Score Card -->
<div class="content">
  <div class="score-big">{score}/100</div>
  <p style="text-align:center;color:#64748B;margin-bottom:16px">Repo Maturity Score</p>

  <h2>Score Breakdown</h2>
  <table>
    <tr>
      <th style="width:180px">Dimension</th>
      <th>Score</th>
      <th style="width:70px;text-align:center">Weight</th>
    </tr>
    {dim_rows}
  </table>

  <h2>Executive Summary</h2>
  <p class="text-block">{exec_summary}</p>

  <!-- Feature/Gap summary cards -->
  <div style="display:flex;gap:20px;margin:16px 0">
    <div style="flex:1;background:#D1FAE5;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#065F46">{feature_summary.get('complete', 0)}</div>
      <div style="font-size:12px;color:#065F46">Complete</div>
    </div>
    <div style="flex:1;background:#FEF3C7;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#92400E">{feature_summary.get('partial', 0)}</div>
      <div style="font-size:12px;color:#92400E">Partial</div>
    </div>
    <div style="flex:1;background:#FEE2E2;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#991B1B">{feature_summary.get('stub', 0)}</div>
      <div style="font-size:12px;color:#991B1B">Stubs</div>
    </div>
    <div style="flex:1;background:#E0E7FF;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#3730A3">{feature_summary.get('planned', 0)}</div>
      <div style="font-size:12px;color:#3730A3">Planned</div>
    </div>
  </div>
</div>

<!-- Purpose -->
<div class="content">
  {purpose_html}
</div>

<!-- Architecture Overview -->
<div class="content">
  <h2>Architecture Overview</h2>
  <p><strong>Style:</strong> {escape_html(architecture.get('style', ''))}</p>
  <p><strong>Pattern:</strong> {escape_html(architecture.get('pattern', ''))}</p>
  <p><strong>Data Flow:</strong> {escape_html(architecture.get('data_flow', ''))}</p>
  {nav_tips}

  {_html_integration_chains(data)}

  <h3>Key Files</h3>
  <table>
    <tr>
      <th>File</th>
      <th>Role</th>
      <th style="width:80px">Importance</th>
    </tr>
    {key_files_rows}
  </table>
</div>

<!-- Tech Stack -->
<div class="content">
  <h2>Tech Stack</h2>
  <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px">
    <div class="meta-item"><strong>Language:</strong> {escape_html(stack.get('primary_language', 'N/A'))}</div>
    <div class="meta-item"><strong>Framework:</strong> {escape_html(stack.get('framework', 'N/A'))}</div>
    <div class="meta-item"><strong>Database:</strong> {escape_html(stack.get('database', 'N/A'))}</div>
    <div class="meta-item"><strong>Runtime:</strong> {escape_html(stack.get('runtime', 'N/A'))}</div>
    <div class="meta-item"><strong>Deploy:</strong> {escape_html(stack.get('deployment', 'N/A'))}</div>
  </div>
  {_html_stack_deps(data)}
  {stack_deps}
</div>

<!-- Feature Inventory -->
<div class="content">
  <h2>Feature Inventory ({feature_summary.get('total', 0)} features)</h2>
  <table>
    <tr>
      <th>Feature</th>
      <th style="width:90px">Category</th>
      <th style="width:75px">Status</th>
      <th style="width:50px;text-align:center">Done</th>
      <th style="width:45px;text-align:center">Tests</th>
      {"<th style='width:55px;text-align:center'>Depth</th><th style='width:50px;text-align:center'>TCov</th><th style='width:55px;text-align:center'>Recent</th><th style='width:45px;text-align:center'>Chain</th>" if is_v11 else ""}
      <th style="width:35px;text-align:center">UI</th>
      <th style="width:35px;text-align:center">API</th>
    </tr>
    {feature_rows}
  </table>
</div>

<!-- Infrastructure Checklist -->
<div class="content">
  <h2>Infrastructure Checklist</h2>
  <table>
    <tr>
      <th style="width:140px">Item</th>
      <th style="width:90px">Status</th>
      <th>Notes</th>
    </tr>
    {infra_rows}
  </table>
</div>

{_html_test_suite(data)}

<!-- Gaps & Recency -->
<div class="content">
  {_html_recency(data)}
  <h2>Gaps Analysis ({gap_summary.get('total', 0)} gaps)</h2>
  <div style="display:flex;gap:20px;margin:16px 0">
    <div style="flex:1;background:#FEE2E2;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#991B1B">{gap_summary.get('critical', 0)}</div>
      <div style="font-size:12px;color:#991B1B">Critical</div>
    </div>
    <div style="flex:1;background:#FFF7ED;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#9A3412">{gap_summary.get('high', 0)}</div>
      <div style="font-size:12px;color:#9A3412">High</div>
    </div>
    <div style="flex:1;background:#FEFCE8;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#854D0E">{gap_summary.get('medium', 0)}</div>
      <div style="font-size:12px;color:#854D0E">Medium</div>
    </div>
    <div style="flex:1;background:#F0FDF4;padding:12px 16px;border-radius:6px;text-align:center">
      <div style="font-size:24px;font-weight:700;color:#166534">{gap_summary.get('low', 0)}</div>
      <div style="font-size:12px;color:#166534">Low</div>
    </div>
  </div>
  {gap_sections}
</div>

<!-- Recommendations -->
<div class="content">
  <h2>Recommendations</h2>
  <ol style="margin:8px 0 16px 24px">
    {rec_items}
  </ol>
</div>

{suite_html}

<!-- Handoff Brief -->
<div class="content" style="border:2px solid {TEAL}">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <h2 style="margin-bottom:0;border-bottom:none;padding-bottom:0">Handoff Brief</h2>
    <button onclick="copyDoc('handoff-content', this)" style="background:{TEAL};color:white;border:none;padding:6px 16px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer">Copy to Clipboard</button>
  </div>
  <p style="font-size:12px;color:#64748B;margin:4px 0 12px 0">Evergreen orientation document for another Claude Code session</p>
  <div class="handoff" id="handoff-content">{escape_html(handoff_brief)}</div>
</div>

{"" if not data.get("gap_analysis") else f'''
<!-- Gap Analysis -->
<div class="content" style="border:2px solid {AMBER}">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <h2 style="margin-bottom:0;border-bottom:none;padding-bottom:0;color:{AMBER}">Gap Analysis</h2>
    <button onclick="copyDoc('gap-content', this)" style="background:{AMBER};color:white;border:none;padding:6px 16px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer">Copy to Clipboard</button>
  </div>
  <p style="font-size:12px;color:#64748B;margin:4px 0 12px 0">Point-in-time assessment -- goes stale in ~2 weeks</p>
  <div style="background:{AMBER_LIGHT};border:2px solid {AMBER};border-radius:8px;padding:24px 32px;white-space:pre-wrap;font-family:Fira Code,Consolas,monospace;font-size:13px;line-height:1.6;color:{AMBER_DARK}" id="gap-content">{escape_html(data.get("gap_analysis", ""))}</div>
</div>
'''}

<script>
function copyDoc(elementId, btn) {{
  const text = document.getElementById(elementId).innerText;
  const origBg = btn.style.background;
  navigator.clipboard.writeText(text).then(() => {{
    btn.textContent = 'Copied!';
    btn.style.background = '#059669';
    setTimeout(() => {{ btn.textContent = 'Copy to Clipboard'; btn.style.background = origBg; }}, 2000);
  }});
}}
</script>

<!-- Methodology -->
<div class="content">
  <details>
    <summary style="cursor:pointer;font-weight:600;color:{TEAL};font-size:15px;padding:4px 0">Methodology &amp; Scoring</summary>
    <div style="margin-top:12px;font-size:13px;color:#475569;line-height:1.7">
      <p><strong>Maturity Score</strong> is a weighted composite of 5 dimensions:</p>
      <table style="font-size:12px;margin:8px 0">
        <tr><th>Dimension</th><th style="width:80px">Weight</th><th>What It Measures</th></tr>
        <tr><td>Documentation</td><td>15%</td><td>README quality, inline docs, API documentation</td></tr>
        <tr><td>Feature Completeness</td><td>30%</td><td>Ratio of complete vs partial/stub features</td></tr>
        <tr><td>Infrastructure</td><td>20%</td><td>Error handling, logging, validation, CI/CD, config management</td></tr>
        <tr><td>Test Presence</td><td>15%</td><td>Test coverage across features, test framework setup</td></tr>
        <tr><td>Architecture Clarity</td><td>20%</td><td>Code organization, separation of concerns, navigability</td></tr>
      </table>
      <p><strong>Maturity Levels:</strong> MATURE (80+), DEVELOPING (60-79), EARLY STAGE (40-59), PROTOTYPE (&lt;40)</p>
      <p><strong>Gap Severity:</strong> CRITICAL = blocking production use, HIGH = significant limitation, MEDIUM = should fix before scaling, LOW = nice to have</p>
      <p><strong>Analysis Agents:</strong> 5 specialized agents (Purpose, Features, Stack, Gaps, Architecture) run in parallel, then a synthesizer merges findings and calculates scores.</p>
    </div>
  </details>
</div>

<div class="footer">
  Generated by Claude Code | Repo Summarizer Plugin | {d}
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


# -- PDF Generation -----------------------------------------------------------

class RepoSummaryPDF(FPDF):
    def __init__(self, data: dict):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.data = data
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*TEAL_RGB)
        self.cell(0, 8, "REPOSITORY SUMMARY", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 11)
        self.set_text_color(120, 120, 120)
        project = latin_safe(self.data.get("project_name", ""))
        self.cell(0, 6, project, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        d = self.data.get("date", "")
        stack_info = latin_safe(self.data.get("stack", {}).get("framework", ""))
        self.cell(0, 5, f"{d}  |  {stack_info}", new_x="LMARGIN", new_y="NEXT")
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Generated by Claude Code  |  Repo Summarizer  |  Confidential  |  Page {self.page_no()}/{{nb}}", align="C")


def generate_pdf(data: dict, output_path: str):
    pdf = RepoSummaryPDF(data)
    pdf.alias_nb_pages()
    pdf.add_page()

    # Available width for content (page width minus margins)
    avail_w = pdf.w - pdf.l_margin - pdf.r_margin

    maturity_level = data.get("maturity_level", "PROTOTYPE")
    score = data.get("maturity_score", 0)
    dim_scores = data.get("dimension_scores", {})
    purpose = data.get("purpose", {})
    features = data.get("features", [])
    feature_summary = data.get("feature_summary", {})
    stack = data.get("stack", {})
    gaps = data.get("gaps", [])
    gap_summary = data.get("gap_summary", {})
    architecture = data.get("architecture", {})
    infra_checklist = data.get("infrastructure_checklist", {})
    recommendations = data.get("recommendations", [])
    handoff_brief = data.get("handoff_brief", "")
    git_stats = data.get("git_stats", {})

    # -- Maturity Score + Badge --
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*TEAL_RGB)
    pdf.cell(0, 14, f"Score: {score}/100", align="C", new_x="LMARGIN", new_y="NEXT")

    mc = MATURITY_COLORS.get(maturity_level, MATURITY_COLORS["PROTOTYPE"])
    r, g, b = int(mc["bg"][1:3], 16), int(mc["bg"][3:5], 16), int(mc["bg"][5:7], 16)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(r, g, b)
    pdf.set_text_color(255, 255, 255)
    label = mc["label"]
    w = pdf.get_string_width(label) + 16
    x = (pdf.w - w) / 2
    pdf.set_x(x)
    pdf.cell(w, 8, label, fill=True, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # -- Feature/Gap summary --
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    fs = feature_summary
    gs = gap_summary
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(avail_w, 6, latin_safe(
        f"Features: {fs.get('complete', 0)} complete, {fs.get('partial', 0)} partial, "
        f"{fs.get('stub', 0)} stubs, {fs.get('planned', 0)} planned  |  "
        f"Gaps: {gs.get('critical', 0)} crit, {gs.get('high', 0)} high, {gs.get('medium', 0)} med, {gs.get('low', 0)} low"
    ), align="C")
    pdf.ln(4)

    # -- Git Stats --
    if git_stats:
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(100, 100, 100)
        parts = []
        if git_stats.get("last_commit"):
            parts.append(f"Last commit: {git_stats['last_commit']}")
        if git_stats.get("commit_count"):
            parts.append(f"{git_stats['commit_count']} commits")
        if git_stats.get("contributors"):
            parts.append(f"Contributors: {', '.join(git_stats['contributors'][:3])}")
        if parts:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(avail_w, 4, latin_safe("  |  ".join(parts)), align="C")
    pdf.ln(4)

    # -- Dimension Scores --
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*TEAL_RGB)
    pdf.cell(0, 8, "Score Breakdown", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    headers = ["Dimension", "Score", "Weight"]
    widths = [avail_w * 0.40, avail_w * 0.35, avail_w * 0.25]
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*TEAL_RGB)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(headers):
        pdf.cell(widths[i], 6, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for idx, (key, info) in enumerate(dim_scores.items()):
        ds = info.get("score", 0)
        weight = info.get("weight", 0)
        dn = latin_safe(DIMENSION_NAMES.get(key, key))

        if idx % 2 == 0:
            pdf.set_fill_color(248, 250, 252)
        else:
            pdf.set_fill_color(255, 255, 255)

        if ds >= 80:
            pdf.set_text_color(6, 95, 70)
        elif ds >= 60:
            pdf.set_text_color(133, 77, 14)
        elif ds >= 40:
            pdf.set_text_color(30, 64, 175)
        else:
            pdf.set_text_color(91, 33, 182)

        pdf.cell(widths[0], 6, f"  {dn}", border=1, fill=True)
        pdf.cell(widths[1], 6, str(ds), border=1, fill=True, align="C")
        pdf.set_text_color(60, 60, 60)
        pdf.cell(widths[2], 6, f"{int(weight * 100)}%", border=1, fill=True, align="C",
                 new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # -- Purpose --
    if purpose.get("statement"):
        pdf.set_text_color(*TEAL_RGB)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Purpose", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*TEAL_RGB)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(avail_w, 5, latin_safe(purpose.get("statement", "")))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(40, 40, 40)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(avail_w, 5, latin_safe(purpose.get("extended", "")))
        pdf.ln(4)

    # -- Executive Summary --
    pdf.set_text_color(*TEAL_RGB)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(avail_w, 5, latin_safe(data.get("executive_summary", "")))
    pdf.ln(4)

    # -- Architecture --
    pdf.set_text_color(*TEAL_RGB)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Architecture", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    arch_text = (
        f"Style: {architecture.get('style', 'N/A')}\n"
        f"Pattern: {architecture.get('pattern', 'N/A')}\n"
        f"Data Flow: {architecture.get('data_flow', 'N/A')}"
    )
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(avail_w, 5, latin_safe(arch_text))
    pdf.ln(2)

    # Key files table -- proportional widths
    key_files = architecture.get("key_files", [])
    if key_files:
        kf_widths = [avail_w * 0.38, avail_w * 0.50, avail_w * 0.12]
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_fill_color(*TEAL_RGB)
        pdf.set_text_color(255, 255, 255)
        for i, h in enumerate(["File", "Role", "Imp."]):
            pdf.cell(kf_widths[i], 6, h, border=1, fill=True, align="C")
        pdf.ln()

        pdf.set_font("Helvetica", "", 7)
        for ki, kf in enumerate(key_files[:15]):
            if ki % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(60, 60, 60)
            path_trunc = int(kf_widths[0] / 1.6)
            role_trunc = int(kf_widths[1] / 1.6)
            pdf.cell(kf_widths[0], 5.5, truncate(kf.get("path", ""), path_trunc), border=1, fill=True)
            pdf.cell(kf_widths[1], 5.5, truncate(kf.get("role", ""), role_trunc), border=1, fill=True)
            pdf.cell(kf_widths[2], 5.5, truncate(kf.get("importance", ""), 10), border=1, fill=True, align="C",
                     new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # -- Tech Stack --
    stack_deps = data.get("stack_dependencies", {})
    if stack_deps or stack.get("key_dependencies"):
        pdf.set_text_color(*TEAL_RGB)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Tech Stack", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(40, 40, 40)
        stack_meta = []
        if stack.get("primary_language"):
            stack_meta.append(f"Language: {stack['primary_language']}")
        if stack.get("framework"):
            stack_meta.append(f"Framework: {stack['framework']}")
        if stack.get("database"):
            stack_meta.append(f"Database: {stack['database']}")
        if stack.get("deployment"):
            stack_meta.append(f"Deploy: {stack['deployment']}")
        if stack_meta:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(avail_w, 5, latin_safe("  |  ".join(stack_meta)))
            pdf.ln(2)

        if stack_deps:
            sd_widths = [avail_w * 0.22, avail_w * 0.35, avail_w * 0.43]
            for cat, deps in stack_deps.items():
                if not deps:
                    continue
                pdf.set_font("Helvetica", "B", 8)
                pdf.set_text_color(*TEAL_RGB)
                pdf.cell(0, 5, format_label(cat), new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", "", 7)
                pdf.set_text_color(60, 60, 60)
                for dep in deps[:8]:
                    name = dep if isinstance(dep, str) else dep.get("name", "")
                    ver = "" if isinstance(dep, str) else dep.get("version", "")
                    purp = "" if isinstance(dep, str) else dep.get("purpose", "")
                    pdf.set_fill_color(248, 250, 252)
                    pdf.cell(sd_widths[0], 4.5, truncate(latin_safe(name), 20), border=0, fill=True)
                    pdf.cell(sd_widths[1], 4.5, truncate(latin_safe(ver), 28), border=0, fill=True)
                    pdf.cell(sd_widths[2], 4.5, truncate(latin_safe(purp), 40), border=0, fill=True,
                             new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif stack.get("key_dependencies"):
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(avail_w, 5, latin_safe("Key deps: " + ", ".join(stack["key_dependencies"])))
        pdf.ln(4)

    # -- Feature Inventory --
    pdf.set_text_color(*TEAL_RGB)
    pdf.set_font("Helvetica", "B", 12)
    total_feat = feature_summary.get("total", 0)
    pdf.cell(0, 8, f"Feature Inventory ({total_feat} features)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    feat_headers = ["Feature", "Category", "Status", "Tests"]
    feat_widths = [avail_w * 0.42, avail_w * 0.20, avail_w * 0.20, avail_w * 0.18]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*TEAL_RGB)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(feat_headers):
        pdf.cell(feat_widths[i], 6, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 7)
    for fi, feat in enumerate(features):
        if fi % 2 == 0:
            pdf.set_fill_color(248, 250, 252)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(60, 60, 60)
        name_trunc = int(feat_widths[0] / 1.5)
        pdf.cell(feat_widths[0], 5.5, truncate(feat.get("name", ""), name_trunc), border=1, fill=True)
        pdf.cell(feat_widths[1], 5.5, truncate(feat.get("category", ""), 16), border=1, fill=True, align="C")
        pdf.cell(feat_widths[2], 5.5, truncate(feat.get("status", ""), 12), border=1, fill=True, align="C")
        tests = "Yes" if feat.get("has_tests") else "No"
        pdf.cell(feat_widths[3], 5.5, tests, border=1, fill=True, align="C",
                 new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # -- Infrastructure Checklist --
    pdf.set_text_color(*TEAL_RGB)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Infrastructure Checklist", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    ic_widths = [avail_w * 0.25, avail_w * 0.18, avail_w * 0.57]
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*TEAL_RGB)
    pdf.set_text_color(255, 255, 255)
    for i, h in enumerate(["Item", "Status", "Notes"]):
        pdf.cell(ic_widths[i], 6, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 7.5)
    infra_detail = data.get("infrastructure_detail", {})
    for ii, (ik, quality) in enumerate(infra_checklist.items()):
        item_name = INFRA_DISPLAY_NAMES.get(ik, ik.replace("_", " ").title())
        if isinstance(quality, dict):
            q_val = quality.get("quality", quality.get("status", "missing"))
            notes = quality.get("notes", "")
        else:
            q_val = quality
            notes = infra_detail.get(ik, {}).get("notes", "")
        if ii % 2 == 0:
            pdf.set_fill_color(248, 250, 252)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(60, 60, 60)
        notes_trunc = int(ic_widths[2] / 1.5)
        pdf.cell(ic_widths[0], 5.5, latin_safe(f"  {item_name}"), border=1, fill=True)
        pdf.cell(ic_widths[1], 5.5, latin_safe(q_val.title()), border=1, fill=True, align="C")
        pdf.cell(ic_widths[2], 5.5, truncate(latin_safe(notes), notes_trunc), border=1, fill=True,
                 new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # -- Test Suite (v1.1) --
    test_results = data.get("test_results")
    if test_results and test_results.get("total_tests", 0) != 0:
        pdf.set_text_color(*TEAL_RGB)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Test Suite", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(40, 40, 40)
        runner = test_results.get("runner", "unknown")
        total_t = test_results.get("total_tests", 0)
        passed_t = test_results.get("passed_tests", 0)
        failed_t = test_results.get("failed_tests", 0)
        rate_t = test_results.get("pass_rate", 0)
        rate_pct = f"{rate_t * 100:.0f}%" if isinstance(rate_t, (int, float)) else "N/A"
        test_files_t = test_results.get("test_files_count", 0)
        test_line = f"Runner: {runner} | Total: {total_t} | Passed: {passed_t} | Failed: {failed_t} | Rate: {rate_pct} | Files: {test_files_t}"
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(avail_w, 5, latin_safe(test_line))
        pdf.ln(4)

    # -- Gaps --
    grouped_gaps = group_gaps_by_severity(gaps)
    gap_widths = [avail_w * 0.10, avail_w * 0.42, avail_w * 0.28, avail_w * 0.20]

    for sev, sev_gaps in grouped_gaps.items():
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*TEAL_RGB)
        pdf.cell(0, 8, f"{sev} Gaps ({len(sev_gaps)})", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        gc = SEVERITY_COLORS.get(sev, SEVERITY_COLORS["LOW"])
        gr, gg, gb = int(gc["header_bg"][1:3], 16), int(gc["header_bg"][3:5], 16), int(gc["header_bg"][5:7], 16)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_fill_color(gr, gg, gb)
        pdf.set_text_color(255, 255, 255)
        for i, h in enumerate(["ID", "Gap", "Type", "Effort"]):
            pdf.cell(gap_widths[i], 6, h, border=1, fill=True, align="C")
        pdf.ln()

        pdf.set_font("Helvetica", "", 7)
        for gi, gap in enumerate(sev_gaps):
            if gi % 2 == 0:
                pdf.set_fill_color(248, 250, 252)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(60, 60, 60)
            gap_type = format_gap_type(gap.get("type", ""))
            title_trunc = int(gap_widths[1] / 1.5)
            type_trunc = int(gap_widths[2] / 1.6)
            pdf.cell(gap_widths[0], 5.5, gap.get("id", ""), border=1, fill=True)
            pdf.cell(gap_widths[1], 5.5, truncate(gap.get("title", ""), title_trunc), border=1, fill=True)
            pdf.cell(gap_widths[2], 5.5, truncate(gap_type, type_trunc), border=1, fill=True)
            pdf.cell(gap_widths[3], 5.5, truncate(gap.get("effort_estimate", ""), 14), border=1, fill=True, align="C",
                     new_x="LMARGIN", new_y="NEXT")

            rec = gap.get("recommendation", "")
            if rec:
                pdf.set_font("Helvetica", "I", 7)
                pdf.set_text_color(100, 100, 100)
                pdf.set_x(pdf.l_margin + gap_widths[0])
                rec_width = avail_w - gap_widths[0]
                pdf.multi_cell(rec_width, 4, latin_safe(f"Fix: {rec}"))
                pdf.set_font("Helvetica", "", 7)
        pdf.ln(4)

    # -- Recommendations --
    pdf.set_text_color(*TEAL_RGB)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Recommendations", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    for i, rec in enumerate(recommendations, 1):
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(avail_w, 5, latin_safe(f"  {i}. {rec}"))
        pdf.ln(1)

    # -- Handoff Brief --
    pdf.add_page()
    pdf.set_text_color(*TEAL_RGB)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Handoff Brief", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Courier", "", 7.5)
    pdf.set_text_color(40, 40, 40)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(avail_w, 3.8, latin_safe(handoff_brief))

    # -- Gap Analysis (v1.1) --
    gap_analysis_md = data.get("gap_analysis", "")
    if gap_analysis_md:
        pdf.add_page()
        pdf.set_text_color(*AMBER_RGB)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Gap Analysis", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, "Point-in-time assessment -- goes stale in ~2 weeks", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font("Courier", "", 7.5)
        pdf.set_text_color(40, 40, 40)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(avail_w, 3.8, latin_safe(gap_analysis_md))

    pdf.output(output_path)


# -- Markdown Generation ------------------------------------------------------

def generate_md(data: dict, output_path: str):
    project = data.get("project_name", "Project")
    d = data.get("date", "")
    maturity_level = data.get("maturity_level", "PROTOTYPE")
    score = data.get("maturity_score", 0)
    dim_scores = data.get("dimension_scores", {})
    purpose = data.get("purpose", {})
    features = data.get("features", [])
    feature_summary = data.get("feature_summary", {})
    stack = data.get("stack", {})
    gaps = data.get("gaps", [])
    gap_summary = data.get("gap_summary", {})
    architecture = data.get("architecture", {})
    infra_checklist = data.get("infrastructure_checklist", {})
    recommendations = data.get("recommendations", [])
    exec_summary = data.get("executive_summary", "")
    handoff_brief = data.get("handoff_brief", "")
    suite_ctx = data.get("suite_context")
    git_stats = data.get("git_stats", {})

    lines = []

    # YAML frontmatter
    lines.append("---")
    lines.append(f"project: {project}")
    lines.append(f"date: {d}")
    lines.append(f"maturity_level: {maturity_level}")
    lines.append(f"maturity_score: {score}")
    lines.append(f"stack: {stack.get('framework', '')} + {stack.get('database', '')}")
    lines.append(f"language: {stack.get('primary_language', '')}")
    lines.append(f"deployment: {stack.get('deployment', '')}")
    if git_stats.get("commit_count"):
        lines.append(f"commits: {git_stats['commit_count']}")
    if git_stats.get("contributors"):
        lines.append(f"contributors: {', '.join(git_stats['contributors'][:5])}")
    lines.append("---")
    lines.append("")

    # Title
    lines.append(f"# Repository Summary: {project}")
    lines.append("")
    lines.append(f"**Date**: {d}  |  **Maturity**: {maturity_level}  |  **Score**: {score}/100")
    lines.append(f"**Stack**: {stack.get('framework', '')} + {stack.get('database', '')}  |  **Deploy**: {stack.get('deployment', '')}")
    if git_stats:
        git_parts = []
        if git_stats.get("commit_count"):
            git_parts.append(f"**Commits**: {git_stats['commit_count']}")
        if git_stats.get("last_commit"):
            git_parts.append(f"**Last Commit**: {git_stats['last_commit']}")
        if git_stats.get("contributors"):
            git_parts.append(f"**Contributors**: {', '.join(git_stats['contributors'][:5])}")
        if git_parts:
            lines.append("  |  ".join(git_parts))
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(exec_summary)
    lines.append("")

    # Feature/Gap counts
    fs = feature_summary
    gs = gap_summary
    lines.append(f"**Features**: {fs.get('total', 0)} total ({fs.get('complete', 0)} complete, {fs.get('partial', 0)} partial, {fs.get('stub', 0)} stubs, {fs.get('planned', 0)} planned)")
    lines.append(f"**Gaps**: {gs.get('total', 0)} total (Critical: {gs.get('critical', 0)}, High: {gs.get('high', 0)}, Medium: {gs.get('medium', 0)}, Low: {gs.get('low', 0)})")
    lines.append("")

    # Score Breakdown
    lines.append("## Score Breakdown")
    lines.append("")
    lines.append("| Dimension | Score | Weight |")
    lines.append("|-----------|-------|--------|")
    for key, info in dim_scores.items():
        dn = DIMENSION_NAMES.get(key, key)
        ds = info.get("score", 0)
        weight = info.get("weight", 0)
        lines.append(f"| {dn} | {ds}/100 | {int(weight * 100)}% |")
    lines.append("")

    # Purpose
    if purpose.get("statement"):
        lines.append("## Purpose")
        lines.append("")
        lines.append(f"**{purpose.get('statement', '')}**")
        lines.append("")
        lines.append(purpose.get("extended", ""))
        lines.append("")
        lines.append(f"**Type**: {purpose.get('project_type', '')}  |  **Deploy**: {purpose.get('deployment_model', {}).get('type', '')} on {purpose.get('deployment_model', {}).get('platform', '')}")
        lines.append("")
        tus = purpose.get("target_users", [])
        if tus:
            lines.append("**Target Users**:")
            for tu in tus:
                lines.append(f"- **{tu.get('persona', '')}**: {tu.get('description', '')}")
            lines.append("")

    # Architecture
    lines.append("## Architecture")
    lines.append("")
    lines.append(f"- **Style**: {architecture.get('style', '')}")
    lines.append(f"- **Pattern**: {architecture.get('pattern', '')}")
    lines.append(f"- **Data Flow**: {architecture.get('data_flow', '')}")
    lines.append("")

    key_files = architecture.get("key_files", [])
    if key_files:
        lines.append("### Key Files")
        lines.append("")
        lines.append("| File | Role | Importance |")
        lines.append("|------|------|-----------|")
        for kf in key_files[:20]:
            lines.append(f"| `{kf.get('path', '')}` | {kf.get('role', '')} | {kf.get('importance', '')} |")
        lines.append("")

    tips = architecture.get("navigation_tips", [])
    if tips:
        lines.append("### Navigation Tips")
        lines.append("")
        for t in tips:
            lines.append(f"- {t}")
        lines.append("")

    # Tech Stack
    stack_deps_data = data.get("stack_dependencies", {})
    if stack_deps_data or stack.get("key_dependencies"):
        lines.append("## Tech Stack")
        lines.append("")
        lines.append(f"- **Language**: {stack.get('primary_language', 'N/A')}")
        lines.append(f"- **Framework**: {stack.get('framework', 'N/A')}")
        lines.append(f"- **Database**: {stack.get('database', 'N/A')}")
        lines.append(f"- **Runtime**: {stack.get('runtime', 'N/A')}")
        lines.append(f"- **Deploy**: {stack.get('deployment', 'N/A')}")
        lines.append("")
        if stack_deps_data:
            for cat, deps in stack_deps_data.items():
                if not deps:
                    continue
                lines.append(f"### {format_label(cat)}")
                lines.append("")
                lines.append("| Package | Version | Purpose |")
                lines.append("|---------|---------|---------|")
                for dep in deps:
                    if isinstance(dep, str):
                        lines.append(f"| {dep} | - | - |")
                    else:
                        lines.append(f"| {dep.get('name', '')} | {dep.get('version', '')} | {dep.get('purpose', '')} |")
                lines.append("")
        elif stack.get("key_dependencies"):
            lines.append(f"**Key Dependencies**: {', '.join(stack['key_dependencies'])}")
            lines.append("")

    # Feature Inventory
    is_v11 = data.get("version", "1.0") >= "1.1"
    lines.append(f"## Feature Inventory ({feature_summary.get('total', 0)} features)")
    lines.append("")
    if is_v11:
        lines.append("| Feature | Category | Status | Done | Tests | Depth | TCov | Recent | Chain | UI | API |")
        lines.append("|---------|----------|--------|------|-------|-------|------|--------|-------|----|-----|")
    else:
        lines.append("| Feature | Category | Status | Done | Tests | UI | API |")
        lines.append("|---------|----------|--------|------|-------|----|-----|")
    for feat in features:
        tests = "Yes" if feat.get("has_tests") else "No"
        ui = "Yes" if feat.get("has_ui") else "No"
        api = "Yes" if feat.get("has_api") else "No"
        compl = feat.get("completeness", 0)
        if is_v11:
            depth = feat.get("implementation_depth", {})
            loc = depth.get("avg_handler_loc", 0)
            tc = feat.get("test_coverage", {})
            tc_count = tc.get("test_case_count", 0)
            rs = feat.get("recency_signal", "-")
            cs = feat.get("chain_status", "-")
            lines.append(f"| {feat.get('name', '')} | {feat.get('category', '')} | {feat.get('status', '')} | {compl}% | {tests} | {loc} LOC | {tc_count} | {rs} | {cs} | {ui} | {api} |")
        else:
            lines.append(f"| {feat.get('name', '')} | {feat.get('category', '')} | {feat.get('status', '')} | {compl}% | {tests} | {ui} | {api} |")
    lines.append("")

    # Feature details (descriptions + key files)
    has_details = any(feat.get("description") or feat.get("key_files") for feat in features)
    if has_details:
        lines.append("### Feature Details")
        lines.append("")
        for feat in features:
            feat_desc = feat.get("description", "")
            feat_files = feat.get("key_files", [])
            if feat_desc or feat_files:
                lines.append(f"**{feat.get('name', '')}**")
                if feat_desc:
                    lines.append(f"> {feat_desc}")
                if feat_files:
                    lines.append(f"> Files: {', '.join(f'`{f}`' for f in feat_files[:5])}")
                lines.append("")

    # Infrastructure Checklist
    infra_detail = data.get("infrastructure_detail", {})
    lines.append("## Infrastructure Checklist")
    lines.append("")
    lines.append("| Item | Status | Notes |")
    lines.append("|------|--------|-------|")
    for ik, quality in infra_checklist.items():
        item_name = INFRA_DISPLAY_NAMES.get(ik, ik.replace("_", " ").title())
        if isinstance(quality, dict):
            q_val = quality.get("quality", quality.get("status", "missing"))
            notes = quality.get("notes", "")
        else:
            q_val = quality
            notes = infra_detail.get(ik, {}).get("notes", "")
        lines.append(f"| {item_name} | {q_val.title()} | {notes or '-'} |")
    lines.append("")

    # Test Suite (v1.1)
    test_results = data.get("test_results")
    if test_results:
        total_t = test_results.get("total_tests", 0)
        passed_t = test_results.get("passed_tests", 0)
        failed_t = test_results.get("failed_tests", 0)
        skipped_t = test_results.get("skipped_tests", 0)
        rate_t = test_results.get("pass_rate", 0)
        rate_pct = f"{rate_t * 100:.0f}%" if isinstance(rate_t, (int, float)) else "N/A"
        runner = test_results.get("runner", "none")
        test_files_t = test_results.get("test_files_count", 0)
        lines.append("## Test Suite")
        lines.append("")
        lines.append(f"- **Runner**: {runner}")
        lines.append(f"- **Total**: {total_t} | **Passed**: {passed_t} | **Failed**: {failed_t} | **Skipped**: {skipped_t}")
        lines.append(f"- **Pass Rate**: {rate_pct}")
        lines.append(f"- **Test Files**: {test_files_t}")
        error = test_results.get("error")
        if error:
            lines.append(f"- **Error**: {error}")
        lines.append("")

    # Integration Chains (v1.1)
    chains_data = data.get("integration_chains")
    if chains_data:
        total_ch = chains_data.get("total_traced", 0)
        complete_ch = chains_data.get("complete_chains", 0)
        broken_ch = chains_data.get("broken_chains", 0)
        lines.append("## Integration Chains")
        lines.append("")
        lines.append(f"**{complete_ch} of {total_ch}** feature chains are complete ({broken_ch} broken)")
        lines.append("")
        chains_list = chains_data.get("chains", [])
        if chains_list:
            lines.append("| Feature Area | Chain | Status | Missing |")
            lines.append("|-------------|-------|--------|---------|")
            for ch in chains_list:
                area = ch.get("feature_area", "")
                layers = ch.get("chain", [])
                layer_str = " -> ".join(l.get("layer", "") for l in layers) if isinstance(layers, list) else ""
                status = "Complete" if ch.get("chain_complete") else "Broken"
                missing = ", ".join(ch.get("missing_layers", [])) or "-"
                lines.append(f"| {area} | {layer_str} | {status} | {missing} |")
            lines.append("")

    # Recency (v1.1)
    recency_data = data.get("recency_data")
    if recency_data:
        total_commits = recency_data.get("total_recent_commits", 0)
        window = recency_data.get("recency_window", "30 days")
        lines.append(f"## Recent Activity ({window})")
        lines.append("")
        lines.append(f"**{total_commits}** commits in the last {window}")
        lines.append("")
        active_files = recency_data.get("recently_active_files", [])[:10]
        if active_files:
            lines.append("| File | Changes |")
            lines.append("|------|---------|")
            for af in active_files:
                lines.append(f"| `{af.get('file', '')}` | {af.get('change_count', 0)} |")
            lines.append("")

    # Gaps
    grouped_gaps = group_gaps_by_severity(gaps)
    for sev, sev_gaps in grouped_gaps.items():
        lines.append(f"## {sev} Gaps ({len(sev_gaps)})")
        lines.append("")
        for g in sev_gaps:
            gap_type = format_gap_type(g.get("type", ""))
            lines.append(f"### {g.get('id', '')} - {g.get('title', '')}")
            lines.append("")
            lines.append(f"- **Type**: {gap_type}")
            lines.append(f"- **Effort**: {g.get('effort_estimate', '')}")
            lines.append(f"- **Recommendation**: {g.get('recommendation', '')}")
            lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    for i, rec in enumerate(recommendations, 1):
        lines.append(f"{i}. {rec}")
    lines.append("")

    # Suite context
    if suite_ctx:
        lines.append("## Suite Integration Analysis")
        lines.append("")
        lines.append(f"**Repos Analyzed**: {', '.join(suite_ctx.get('repos_analyzed', []))}")
        lines.append("")

        mismatches = suite_ctx.get("version_mismatches", [])
        if mismatches:
            lines.append("### Version Mismatches")
            lines.append("")
            for mm in mismatches:
                dep = mm.get("dep", "")
                repos = {k: v for k, v in mm.items() if k != "dep"}
                versions = ", ".join(f"{k}: {v}" for k, v in repos.items())
                lines.append(f"- **{dep}**: {versions}")
            lines.append("")

        ig = suite_ctx.get("integration_gaps", [])
        if ig:
            lines.append("### Integration Gaps")
            lines.append("")
            for g in ig:
                lines.append(f"- {g}")
            lines.append("")

        cr = suite_ctx.get("cross_repo_recommendations", [])
        if cr:
            lines.append("### Cross-Repo Recommendations")
            lines.append("")
            for i, r in enumerate(cr, 1):
                lines.append(f"{i}. {r}")
            lines.append("")

    # Handoff Brief
    lines.append("## Handoff Brief")
    lines.append("")
    lines.append("```markdown")
    lines.append(handoff_brief)
    lines.append("```")
    lines.append("")

    # Gap Analysis (v1.1)
    gap_analysis_md = data.get("gap_analysis", "")
    if gap_analysis_md:
        lines.append("## Gap Analysis")
        lines.append("")
        lines.append("```markdown")
        lines.append(gap_analysis_md)
        lines.append("```")
        lines.append("")

    # Methodology
    lines.append("## Methodology & Scoring")
    lines.append("")
    lines.append("**Maturity Score** is a weighted composite of 5 dimensions:")
    lines.append("")
    lines.append("| Dimension | Weight | What It Measures |")
    lines.append("|-----------|--------|------------------|")
    lines.append("| Documentation | 15% | README quality, inline docs, API documentation |")
    lines.append("| Feature Completeness | 30% | Ratio of complete vs partial/stub features |")
    lines.append("| Infrastructure | 20% | Error handling, logging, validation, CI/CD, config management |")
    lines.append("| Test Presence | 15% | Test coverage across features, test framework setup |")
    lines.append("| Architecture Clarity | 20% | Code organization, separation of concerns, navigability |")
    lines.append("")
    lines.append("**Levels**: MATURE (80+) | DEVELOPING (60-79) | EARLY STAGE (40-59) | PROTOTYPE (<40)")
    lines.append("")
    lines.append("**Gap Severity**: CRITICAL = blocking production | HIGH = significant limitation | MEDIUM = fix before scaling | LOW = nice to have")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*Generated by Claude Code | Repo Summarizer Plugin | {d}*")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# -- Main --------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Export repo summary to MD, PDF, and HTML")
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
        "maturity_level": data.get("maturity_level", ""),
        "maturity_score": data.get("maturity_score", 0),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
