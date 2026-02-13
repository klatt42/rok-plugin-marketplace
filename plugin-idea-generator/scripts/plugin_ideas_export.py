#!/usr/bin/env python3
"""
Plugin Idea Generator - Export Script
Generates HTML, PDF, and Markdown files from plugin idea shortlist JSON.

Usage:
    python3 plugin_ideas_export.py --input shortlist.json
"""

import sys
import os
import json
import argparse
from datetime import datetime
import re

# Add virtual environment to Python path
VENV_SITE = os.path.expanduser("~/.claude/scripts/.venv/lib")
for d in os.listdir(VENV_SITE):
    sp = os.path.join(VENV_SITE, d, "site-packages")
    if os.path.isdir(sp) and sp not in sys.path:
        sys.path.insert(0, sp)

from fpdf import FPDF

# Load plugin version from plugin.json (single source of truth)
_PLUGIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, ".claude-plugin", "plugin.json")
try:
    with open(_PLUGIN_DIR, 'r') as _f:
        PLUGIN_VERSION = json.load(_f)["version"]
except (FileNotFoundError, KeyError, json.JSONDecodeError):
    PLUGIN_VERSION = "unknown"

# Color scheme (indigo-based for plugin ideas — distinct from business-idea-finder's teal)
PRIMARY = "#6366F1"
PRIMARY_DARK = "#4F46E5"

TIER_COLORS = {
    "BUILD_NOW": {"bg": "#059669", "text": "#FFFFFF"},
    "STRONG": {"bg": "#6366F1", "text": "#FFFFFF"},
    "BACKLOG": {"bg": "#D97706", "text": "#FFFFFF"},
    "PASS": {"bg": "#DC2626", "text": "#FFFFFF"}
}

PATHWAY_COLORS = {
    "saas_app": "#6366F1",
    "chrome_extension": "#8B5CF6",
    "api_service": "#0EA5E9",
    "marketplace_plugin": "#059669",
    "mobile_app": "#F59E0B",
    "hybrid": "#EC4899"
}

# Default output directory
DEFAULT_OUTPUT_DIR = "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Plugin_Ideas/"


def latin_safe(text):
    """Convert text to Latin-1 safe string for PDF output."""
    if text is None:
        return ""
    return str(text).encode('latin-1', 'ignore').decode('latin-1')


def slugify(text):
    """Convert text to URL-safe slug."""
    if not text:
        return "open_discovery"
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')


def score_color(score):
    """Return color based on score value."""
    if score >= 80:
        return "#059669"
    elif score >= 65:
        return "#6366F1"
    elif score >= 50:
        return "#D97706"
    else:
        return "#DC2626"


def pathway_display(pathway):
    """Format pathway for display."""
    return pathway.replace('_', ' ').title() if pathway else 'Unknown'


def generate_html(data, output_path):
    """Generate HTML report from shortlist data."""
    topic = data.get('topic') or "Open Discovery"
    depth = data.get('depth', 'standard').upper()
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    shortlist = data.get('shortlist', [])
    themes = data.get('themes', {})
    methodology = data.get('methodology', {})
    portfolio_analysis = data.get('portfolio_analysis', {})

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plugin Idea Generator - {topic}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: linear-gradient(135deg, #eef2ff 0%, #ffffff 100%);
            padding: 2rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }}

        .header .subtitle {{
            font-size: 1.2rem;
            opacity: 0.95;
            margin-bottom: 1.5rem;
        }}

        .header .meta {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
            font-size: 0.95rem;
        }}

        .meta-item {{
            background: rgba(255,255,255,0.15);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }}

        .meta-label {{
            opacity: 0.8;
            font-size: 0.85rem;
        }}

        .meta-value {{
            font-weight: 600;
            font-size: 1.1rem;
        }}

        .content {{
            padding: 2rem;
        }}

        .section {{
            margin-bottom: 3rem;
        }}

        .section-title {{
            font-size: 1.8rem;
            color: {PRIMARY_DARK};
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid {PRIMARY};
        }}

        .shortlist-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 2rem;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .shortlist-table th {{
            background: {PRIMARY};
            color: white;
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .shortlist-table td {{
            padding: 1rem;
            border-bottom: 1px solid #e5e7eb;
        }}

        .shortlist-table tr:last-child td {{
            border-bottom: none;
        }}

        .shortlist-table tr:hover {{
            background: #eef2ff;
        }}

        .rank {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {PRIMARY};
            text-align: center;
        }}

        .tier-badge {{
            display: inline-block;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .pathway-badge {{
            display: inline-block;
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            font-weight: 500;
            font-size: 0.8rem;
            color: white;
        }}

        .score {{
            font-weight: 600;
            font-size: 1.1rem;
        }}

        .score-bar {{
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.3rem;
        }}

        .score-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }}

        .idea-card {{
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        }}

        .idea-card:hover {{
            border-color: {PRIMARY};
            box-shadow: 0 8px 24px rgba(99,102,241,0.15);
        }}

        .idea-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .idea-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {PRIMARY_DARK};
            flex: 1;
        }}

        .idea-badges {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}

        .one-liner {{
            font-size: 1.1rem;
            color: #4b5563;
            font-style: italic;
            margin-bottom: 1.5rem;
            padding-left: 1rem;
            border-left: 4px solid {PRIMARY};
        }}

        .detail-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .detail-item {{
            background: #f9fafb;
            padding: 1rem;
            border-radius: 8px;
        }}

        .detail-label {{
            font-size: 0.85rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.3rem;
        }}

        .detail-value {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #1f2937;
        }}

        .market-signal {{
            background: #eef2ff;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }}

        .market-signal-title {{
            font-weight: 600;
            color: {PRIMARY_DARK};
            margin-bottom: 0.5rem;
        }}

        .ai-advantage {{
            background: #fef3c7;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border-left: 4px solid #d97706;
        }}

        .ai-advantage-title {{
            font-weight: 600;
            color: #92400e;
            margin-bottom: 0.5rem;
        }}

        .create-prompt {{
            background: #1f2937;
            color: #f9fafb;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 1rem;
            position: relative;
        }}

        .create-prompt-title {{
            font-weight: 600;
            margin-bottom: 0.8rem;
            color: #818cf8;
        }}

        .create-prompt code {{
            display: block;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
        }}

        .portfolio-section {{
            background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-top: 2rem;
        }}

        .themes-section {{
            background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-top: 2rem;
        }}

        .theme-item {{
            margin-bottom: 1.5rem;
        }}

        .theme-label {{
            font-weight: 600;
            color: {PRIMARY_DARK};
            margin-bottom: 0.3rem;
            font-size: 1.1rem;
        }}

        .theme-value {{
            color: #1f2937;
            font-size: 1rem;
        }}

        .methodology {{
            background: #f9fafb;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 2rem;
        }}

        .methodology-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}

        .footer {{
            text-align: center;
            padding: 2rem;
            color: #6b7280;
            font-size: 0.9rem;
            border-top: 1px solid #e5e7eb;
            margin-top: 2rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Plugin Idea Generator</h1>
            <div class="subtitle">{topic}</div>
            <div class="meta">
                <div class="meta-item">
                    <div class="meta-label">Generated</div>
                    <div class="meta-value">{generated_date}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Depth</div>
                    <div class="meta-value">{depth}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Shortlist</div>
                    <div class="meta-value">{len(shortlist)} Ideas</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Plugins Scanned</div>
                    <div class="meta-value">{data.get('plugins_scanned', 0)}</div>
                </div>
            </div>
        </div>

        <div class="content">
            <div class="section">
                <h2 class="section-title">Shortlist Overview</h2>
                <table class="shortlist-table">
                    <thead>
                        <tr>
                            <th style="width: 60px;">Rank</th>
                            <th>Plugin Idea</th>
                            <th style="width: 100px;">Tier</th>
                            <th style="width: 80px;">Score</th>
                            <th style="width: 80px;">Utility</th>
                            <th style="width: 80px;">Market</th>
                            <th style="width: 80px;">Novelty</th>
                            <th style="width: 110px;">Pathway</th>
                            <th style="width: 110px;">Extends</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # Add shortlist table rows
    for idea in shortlist:
        rank = idea.get('rank', 0)
        name = idea.get('display_name', idea.get('plugin_name', 'Unnamed'))
        tier = idea.get('tier', 'BACKLOG')
        composite = idea.get('composite_score', 0)
        utility = idea.get('personal_utility', 0)
        market = idea.get('marketization_score', 0)
        novelty = idea.get('novelty_score', 0)
        pathway = idea.get('product_pathway', 'unknown')
        extends = idea.get('extends_plugin') or '--'

        tier_style = f"background: {TIER_COLORS.get(tier, TIER_COLORS['BACKLOG'])['bg']}; color: {TIER_COLORS.get(tier, TIER_COLORS['BACKLOG'])['text']};"
        pw_color = PATHWAY_COLORS.get(pathway, '#6b7280')

        html += f"""
                        <tr>
                            <td class="rank">#{rank}</td>
                            <td><strong>{name}</strong></td>
                            <td><span class="tier-badge" style="{tier_style}">{tier.replace('_', ' ')}</span></td>
                            <td>
                                <div class="score" style="color: {score_color(composite)};">{composite}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {composite}%; background: {score_color(composite)};"></div>
                                </div>
                            </td>
                            <td>
                                <div class="score" style="color: {score_color(utility)};">{utility}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {utility}%; background: {score_color(utility)};"></div>
                                </div>
                            </td>
                            <td>
                                <div class="score" style="color: {score_color(market)};">{market}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {market}%; background: {score_color(market)};"></div>
                                </div>
                            </td>
                            <td>
                                <div class="score" style="color: {score_color(novelty)};">{novelty}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {novelty}%; background: {score_color(novelty)};"></div>
                                </div>
                            </td>
                            <td><span class="pathway-badge" style="background: {pw_color};">{pathway_display(pathway)}</span></td>
                            <td>{extends}</td>
                        </tr>
"""

    html += """
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2 class="section-title">Detailed Analysis</h2>
"""

    # Add detailed idea cards
    for idea in shortlist:
        rank = idea.get('rank', 0)
        name = idea.get('display_name', idea.get('plugin_name', 'Unnamed'))
        tier = idea.get('tier', 'BACKLOG')
        one_liner = idea.get('one_liner', '')
        composite = idea.get('composite_score', 0)
        utility = idea.get('personal_utility', 0)
        market = idea.get('marketization_score', 0)
        novelty = idea.get('novelty_score', 0)
        pathway = idea.get('product_pathway', 'unknown')
        pathway_note = idea.get('pathway_note', '')
        extends = idea.get('extends_plugin') or 'Standalone'
        target_user = idea.get('target_user', '')
        why_it_fits = idea.get('why_it_fits', '')
        market_signal = idea.get('market_signal', '')
        ai_advantage = idea.get('ai_native_advantage', idea.get('ai_advantage', ''))
        key_risk = idea.get('key_risk', '')
        build_estimate = idea.get('build_estimate', {})
        plugin_mvp = build_estimate.get('plugin_mvp', 'N/A')
        product_mvp = build_estimate.get('product_mvp', 'N/A')
        structure = idea.get('proposed_structure', {})
        agents = structure.get('agents', 0)
        commands = structure.get('commands', 0)
        skills = structure.get('skills', 0)
        agent_roles = structure.get('agent_roles', [])
        create_prompt = idea.get('create_prompt', '')
        strategy = idea.get('generation_strategy', '')
        architecture = idea.get('architecture_sketch')

        tier_style = f"background: {TIER_COLORS.get(tier, TIER_COLORS['BACKLOG'])['bg']}; color: {TIER_COLORS.get(tier, TIER_COLORS['BACKLOG'])['text']};"
        pw_color = PATHWAY_COLORS.get(pathway, '#6b7280')

        html += f"""
                <div class="idea-card">
                    <div class="idea-card-header">
                        <div class="idea-title">#{rank}. {name}</div>
                        <div class="idea-badges">
                            <span class="tier-badge" style="{tier_style}">{tier.replace('_', ' ')}</span>
                            <span class="pathway-badge" style="background: {pw_color};">{pathway_display(pathway)}</span>
                        </div>
                    </div>

                    <div class="one-liner">{one_liner}</div>

                    <div class="detail-grid">
                        <div class="detail-item">
                            <div class="detail-label">Composite Score</div>
                            <div class="detail-value" style="color: {score_color(composite)};">{composite}</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {composite}%; background: {score_color(composite)};"></div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Personal Utility</div>
                            <div class="detail-value" style="color: {score_color(utility)};">{utility}</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {utility}%; background: {score_color(utility)};"></div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Marketization</div>
                            <div class="detail-value" style="color: {score_color(market)};">{market}</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {market}%; background: {score_color(market)};"></div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Novelty</div>
                            <div class="detail-value" style="color: {score_color(novelty)};">{novelty}</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {novelty}%; background: {score_color(novelty)};"></div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Product Pathway</div>
                            <div class="detail-value">{pathway_display(pathway)}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Extends</div>
                            <div class="detail-value">{extends}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Target User</div>
                            <div class="detail-value" style="font-size:0.95rem;">{target_user}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Generation Strategy</div>
                            <div class="detail-value">{strategy.replace('-', ' ').title() if strategy else 'N/A'}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Build Estimate</div>
                            <div class="detail-value">Plugin: {plugin_mvp} / Product: {product_mvp}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Structure</div>
                            <div class="detail-value">{agents} agents, {commands} cmds, {skills} skills</div>
                        </div>
                    </div>
"""

        if why_it_fits:
            html += f"""
                    <div class="market-signal">
                        <div class="market-signal-title">Why It Fits You</div>
                        <div>{why_it_fits}</div>
                    </div>
"""

        if market_signal:
            html += f"""
                    <div class="market-signal">
                        <div class="market-signal-title">Market Signal</div>
                        <div>{market_signal}</div>
                    </div>
"""

        if ai_advantage:
            html += f"""
                    <div class="ai-advantage">
                        <div class="ai-advantage-title">AI-Native Advantage</div>
                        <div>{ai_advantage}</div>
                    </div>
"""

        if pathway_note:
            html += f"""
                    <div style="background:#eef2ff; padding:1rem; border-radius:8px; margin-bottom:1rem;">
                        <div style="font-weight:600; color:{PRIMARY_DARK}; margin-bottom:0.3rem;">Monetization Pathway</div>
                        <div>{pathway_note}</div>
                    </div>
"""

        if key_risk:
            html += f"""
                    <div style="background:#fef2f2; padding:1rem; border-radius:8px; margin-bottom:1rem; border-left:4px solid #dc2626;">
                        <div style="font-weight:600; color:#991b1b; margin-bottom:0.3rem;">Key Risk</div>
                        <div>{key_risk}</div>
                    </div>
"""

        if architecture:
            arch_agents = architecture.get('agents', [])
            arch_commands = architecture.get('commands', [])
            arch_flow = architecture.get('data_flow', '')
            arch_connect = architecture.get('interconnections', '')

            html += """
                    <div style="background:#f5f3ff; padding:1.5rem; border-radius:8px; margin-bottom:1rem;">
                        <div style="font-weight:600; color:#4F46E5; margin-bottom:0.8rem; font-size:1.1rem;">Architecture Sketch</div>
"""
            if arch_agents:
                html += '                        <div style="margin-bottom:0.8rem;"><strong>Agents:</strong><ul style="margin-top:0.3rem;">'
                for a in arch_agents:
                    html += f'<li><code>{a.get("name", "")}</code> ({a.get("model", "")}) — {a.get("purpose", "")}</li>'
                html += '</ul></div>'

            if arch_commands:
                html += '                        <div style="margin-bottom:0.8rem;"><strong>Commands:</strong><ul style="margin-top:0.3rem;">'
                for c in arch_commands:
                    html += f'<li><code>{c.get("name", "")}</code> — {c.get("description", "")}</li>'
                html += '</ul></div>'

            if arch_flow:
                html += f'                        <div style="margin-bottom:0.5rem;"><strong>Data Flow:</strong> {arch_flow}</div>'

            if arch_connect:
                html += f'                        <div><strong>Interconnections:</strong> {arch_connect}</div>'

            html += """
                    </div>
"""

        if create_prompt:
            html += f"""
                    <div class="create-prompt">
                        <div class="create-prompt-title">Build This Plugin</div>
                        <code>{create_prompt}</code>
                    </div>
"""

        html += """
                </div>
"""

    html += """
            </div>
"""

    # Portfolio Analysis section
    if portfolio_analysis:
        covered = portfolio_analysis.get('covered_domains', [])
        gaps = portfolio_analysis.get('gap_domains', [])
        extensions = portfolio_analysis.get('extension_opportunities', [])

        html += f"""
            <div class="section">
                <h2 class="section-title">Portfolio Gap Analysis</h2>
                <div class="portfolio-section">
                    <div class="detail-grid">
                        <div class="detail-item">
                            <div class="detail-label">Total Plugins</div>
                            <div class="detail-value">{portfolio_analysis.get('total_plugins', 0)}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Covered Domains ({len(covered)})</div>
                            <div class="detail-value" style="font-size:0.95rem;">{', '.join(covered)}</div>
                        </div>
                        <div class="detail-item" style="grid-column: 1 / -1;">
                            <div class="detail-label">Gap Domains ({len(gaps)})</div>
                            <div class="detail-value" style="color:#dc2626; font-size:0.95rem;">{', '.join(gaps)}</div>
                        </div>
                    </div>
"""

        if extensions:
            html += """
                    <div style="margin-top:1rem;">
                        <div class="detail-label">Extension Opportunities</div>
                        <ul style="margin-top:0.5rem;">
"""
            for ext in extensions:
                existing = ext.get('existing', '')
                extension = ext.get('extension', '')
                html += f'                            <li><strong>{existing}</strong> → {extension}</li>\n'

            html += """
                        </ul>
                    </div>
"""

        html += """
                </div>
            </div>
"""

    # Themes section
    if themes:
        html += """
            <div class="section">
                <h2 class="section-title">Emerging Themes</h2>
                <div class="themes-section">
"""

        if themes.get('dominant_theme'):
            html += f"""
                    <div class="theme-item">
                        <div class="theme-label">Dominant Theme</div>
                        <div class="theme-value">{themes['dominant_theme']}</div>
                    </div>
"""

        if themes.get('emerging_capability'):
            html += f"""
                    <div class="theme-item">
                        <div class="theme-label">Emerging Capability</div>
                        <div class="theme-value">{themes['emerging_capability']}</div>
                    </div>
"""

        if themes.get('strongest_market_signal'):
            html += f"""
                    <div class="theme-item">
                        <div class="theme-label">Strongest Market Signal</div>
                        <div class="theme-value">{themes['strongest_market_signal']}</div>
                    </div>
"""

        html += """
                </div>
            </div>
"""

    # Methodology section
    if methodology:
        html += """
            <div class="methodology">
                <h3 style="margin-bottom: 1rem; color: #1f2937;">Methodology</h3>
                <div class="methodology-grid">
"""

        if methodology.get('agents_dispatched'):
            html += f"""
                    <div class="detail-item">
                        <div class="detail-label">Agents Dispatched</div>
                        <div class="detail-value">{methodology['agents_dispatched']}</div>
                    </div>
"""

        if methodology.get('total_searches'):
            html += f"""
                    <div class="detail-item">
                        <div class="detail-label">Total Searches</div>
                        <div class="detail-value">{methodology['total_searches']}</div>
                    </div>
"""

        if methodology.get('dedup_merges'):
            html += f"""
                    <div class="detail-item">
                        <div class="detail-label">Duplicates Merged</div>
                        <div class="detail-value">{methodology['dedup_merges']}</div>
                    </div>
"""

        if methodology.get('sources_covered'):
            sources = ', '.join(methodology['sources_covered'])
            html += f"""
                    <div class="detail-item" style="grid-column: 1 / -1;">
                        <div class="detail-label">Sources Covered</div>
                        <div class="detail-value">{sources}</div>
                    </div>
"""

        strategies = methodology.get('strategies_used', {})
        if strategies:
            strategy_str = ', '.join([f'{k}: {v}' for k, v in strategies.items()])
            html += f"""
                    <div class="detail-item" style="grid-column: 1 / -1;">
                        <div class="detail-label">Idea Generation Strategies</div>
                        <div class="detail-value">{strategy_str}</div>
                    </div>
"""

        html += """
                </div>
            </div>
"""

    html += f"""
            <div class="footer">
                Generated by Plugin Idea Generator on {generated_date}<br>
                ROK Plugin Marketplace - Plugin Idea Generator v{PLUGIN_VERSION}
            </div>
        </div>
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_pdf(data, output_path):
    """Generate PDF report from shortlist data."""

    class PluginIdeaPDF(FPDF):
        def header(self):
            self.set_fill_color(99, 102, 241)  # PRIMARY (indigo)
            self.rect(0, 0, 210, 40, 'F')
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 20)
            self.cell(0, 15, '', 0, 1)
            self.cell(0, 10, latin_safe('Plugin Idea Generator'), 0, 1, 'C')
            self.set_font('Arial', '', 12)
            topic = data.get('topic') or 'Open Discovery'
            self.cell(0, 8, latin_safe(topic), 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PluginIdeaPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Summary stats
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(79, 70, 229)  # PRIMARY_DARK
    pdf.cell(0, 10, latin_safe('Summary'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)

    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    depth = data.get('depth', 'standard').upper()
    plugins_scanned = data.get('plugins_scanned', 0)
    ideas_generated = data.get('ideas_generated', 0)
    shortlist_count = data.get('shortlist_count', 0)

    pdf.cell(90, 8, latin_safe(f'Generated: {generated_date}'), 0, 0)
    pdf.cell(90, 8, latin_safe(f'Depth: {depth}'), 0, 1)
    pdf.cell(90, 8, latin_safe(f'Plugins Scanned: {plugins_scanned}'), 0, 0)
    pdf.cell(90, 8, latin_safe(f'Ideas Generated: {ideas_generated}'), 0, 1)
    pdf.cell(90, 8, latin_safe(f'Shortlist Count: {shortlist_count}'), 0, 1)
    pdf.ln(5)

    # Methodology
    methodology = data.get('methodology', {})
    if methodology:
        agents = methodology.get('agents_dispatched', 0)
        searches = methodology.get('total_searches', 0)
        sources = methodology.get('sources_covered', [])

        pdf.cell(90, 8, latin_safe(f'Agents Dispatched: {agents}'), 0, 0)
        pdf.cell(90, 8, latin_safe(f'Total Searches: {searches}'), 0, 1)
        if sources:
            pdf.cell(0, 8, latin_safe(f'Sources: {", ".join(sources)}'), 0, 1)

    pdf.ln(10)

    # Shortlist table
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 10, latin_safe('Shortlist Overview'), 0, 1)
    pdf.ln(2)

    shortlist = data.get('shortlist', [])

    # Table header
    pdf.set_font('Arial', 'B', 8)
    pdf.set_fill_color(99, 102, 241)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(10, 8, '#', 1, 0, 'C', True)
    pdf.cell(45, 8, 'Plugin Idea', 1, 0, 'C', True)
    pdf.cell(22, 8, 'Tier', 1, 0, 'C', True)
    pdf.cell(16, 8, 'Score', 1, 0, 'C', True)
    pdf.cell(18, 8, 'Utility', 1, 0, 'C', True)
    pdf.cell(18, 8, 'Market', 1, 0, 'C', True)
    pdf.cell(18, 8, 'Novelty', 1, 0, 'C', True)
    pdf.cell(28, 8, 'Pathway', 1, 1, 'C', True)

    # Table rows
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(0, 0, 0)

    for idea in shortlist:
        rank = idea.get('rank', 0)
        name = idea.get('display_name', idea.get('plugin_name', 'Unnamed'))
        tier = idea.get('tier', 'BACKLOG')
        composite = idea.get('composite_score', 0)
        utility = idea.get('personal_utility', 0)
        market = idea.get('marketization_score', 0)
        novelty = idea.get('novelty_score', 0)
        pathway = idea.get('product_pathway', 'unknown')

        pdf.cell(10, 8, str(rank), 1, 0, 'C')
        pdf.cell(45, 8, latin_safe(name[:28]), 1, 0)
        pdf.cell(22, 8, tier.replace('_', ' '), 1, 0, 'C')
        pdf.cell(16, 8, str(composite), 1, 0, 'C')
        pdf.cell(18, 8, str(utility), 1, 0, 'C')
        pdf.cell(18, 8, str(market), 1, 0, 'C')
        pdf.cell(18, 8, str(novelty), 1, 0, 'C')
        pdf.cell(28, 8, latin_safe(pathway_display(pathway)[:16]), 1, 1, 'C')

    pdf.ln(10)

    # Detailed sections
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 10, latin_safe('Detailed Analysis'), 0, 1)
    pdf.ln(5)

    for idx, idea in enumerate(shortlist):
        if idx > 0:
            pdf.ln(8)

        rank = idea.get('rank', 0)
        name = idea.get('display_name', idea.get('plugin_name', 'Unnamed'))
        tier = idea.get('tier', 'BACKLOG')
        one_liner = idea.get('one_liner', '')
        composite = idea.get('composite_score', 0)
        utility = idea.get('personal_utility', 0)
        market = idea.get('marketization_score', 0)
        novelty = idea.get('novelty_score', 0)
        pathway = idea.get('product_pathway', 'unknown')
        pathway_note = idea.get('pathway_note', '')
        extends = idea.get('extends_plugin') or 'Standalone'
        why_it_fits = idea.get('why_it_fits', '')
        market_signal = idea.get('market_signal', '')
        ai_advantage = idea.get('ai_native_advantage', idea.get('ai_advantage', ''))
        key_risk = idea.get('key_risk', '')
        build_estimate = idea.get('build_estimate', {})
        plugin_mvp = build_estimate.get('plugin_mvp', 'N/A')
        product_mvp = build_estimate.get('product_mvp', 'N/A')
        create_prompt = idea.get('create_prompt', '')

        # Idea header
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(79, 70, 229)
        pdf.cell(0, 8, latin_safe(f'#{rank}. {name}'), 0, 1)

        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 6, latin_safe(one_liner))
        pdf.ln(2)

        # Scores
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(60, 6, latin_safe(f'Composite: {composite}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Utility: {utility}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Market: {market}'), 0, 1)

        pdf.cell(60, 6, latin_safe(f'Novelty: {novelty}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Pathway: {pathway_display(pathway)}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Extends: {extends}'), 0, 1)

        pdf.cell(0, 6, latin_safe(f'Build: Plugin {plugin_mvp} / Product {product_mvp}'), 0, 1)
        pdf.ln(3)

        if why_it_fits:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Why It Fits:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(0, 5, latin_safe(why_it_fits))
            pdf.ln(2)

        if market_signal:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Market Signal:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(0, 5, latin_safe(market_signal))
            pdf.ln(2)

        if ai_advantage:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('AI Advantage:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(0, 5, latin_safe(ai_advantage))
            pdf.ln(2)

        if pathway_note:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Monetization:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(0, 5, latin_safe(pathway_note))
            pdf.ln(2)

        if key_risk:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Key Risk:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(0, 5, latin_safe(key_risk))
            pdf.ln(2)

        if create_prompt:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe(f'Build: {create_prompt}'), 0, 1)

        # Page break check
        if pdf.get_y() > 250 and idx < len(shortlist) - 1:
            pdf.add_page()

    # Themes section
    themes = data.get('themes', {})
    if themes:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(79, 70, 229)
        pdf.cell(0, 10, latin_safe('Emerging Themes'), 0, 1)
        pdf.ln(5)

        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)

        if themes.get('dominant_theme'):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Dominant Theme:'), 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, latin_safe(themes['dominant_theme']))
            pdf.ln(3)

        if themes.get('emerging_capability'):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Emerging Capability:'), 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, latin_safe(themes['emerging_capability']))
            pdf.ln(3)

        if themes.get('strongest_market_signal'):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Strongest Market Signal:'), 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, latin_safe(themes['strongest_market_signal']))

    # Portfolio Analysis
    portfolio_analysis = data.get('portfolio_analysis', {})
    if portfolio_analysis:
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(79, 70, 229)
        pdf.cell(0, 10, latin_safe('Portfolio Gap Analysis'), 0, 1)
        pdf.ln(3)

        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)

        total = portfolio_analysis.get('total_plugins', 0)
        covered = portfolio_analysis.get('covered_domains', [])
        gaps = portfolio_analysis.get('gap_domains', [])

        pdf.cell(0, 6, latin_safe(f'Total Plugins: {total}'), 0, 1)
        pdf.cell(0, 6, latin_safe(f'Covered ({len(covered)}): {", ".join(covered)}'), 0, 1)
        pdf.cell(0, 6, latin_safe(f'Gaps ({len(gaps)}): {", ".join(gaps)}'), 0, 1)

        extensions = portfolio_analysis.get('extension_opportunities', [])
        if extensions:
            pdf.ln(3)
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Extension Opportunities:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            for ext in extensions:
                existing = ext.get('existing', '')
                extension = ext.get('extension', '')
                pdf.cell(0, 5, latin_safe(f'  - {existing} -> {extension}'), 0, 1)

    pdf.output(output_path)


def generate_markdown(data, output_path):
    """Generate Markdown report from shortlist data."""
    topic = data.get('topic') or "Open Discovery"
    depth = data.get('depth', 'standard').upper()
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    shortlist = data.get('shortlist', [])
    themes = data.get('themes', {})
    methodology = data.get('methodology', {})
    portfolio_analysis = data.get('portfolio_analysis', {})

    md = f"""# Plugin Idea Generator

## {topic}

**Generated:** {generated_date}
**Depth:** {depth}
**Plugins Scanned:** {data.get('plugins_scanned', 0)}
**Ideas Generated:** {data.get('ideas_generated', 0)}
**Shortlist Count:** {data.get('shortlist_count', 0)}

---

## Methodology

"""

    if methodology:
        md += f"""- **Agents Dispatched:** {methodology.get('agents_dispatched', 0)}
- **Total Searches:** {methodology.get('total_searches', 0)}
- **Duplicates Merged:** {methodology.get('dedup_merges', 0)}
- **Sources Covered:** {', '.join(methodology.get('sources_covered', []))}
"""
        strategies = methodology.get('strategies_used', {})
        if strategies:
            strategy_str = ', '.join([f'{k}: {v}' for k, v in strategies.items()])
            md += f"- **Strategies Used:** {strategy_str}\n"

        md += "\n"

    md += """---

## Shortlist Overview

| Rank | Plugin Idea | Tier | Score | Utility | Market | Novelty | Pathway | Extends |
|------|-------------|------|-------|---------|--------|---------|---------|---------|
"""

    for idea in shortlist:
        rank = idea.get('rank', 0)
        name = idea.get('display_name', idea.get('plugin_name', 'Unnamed'))
        tier = idea.get('tier', 'BACKLOG')
        composite = idea.get('composite_score', 0)
        utility = idea.get('personal_utility', 0)
        market = idea.get('marketization_score', 0)
        novelty = idea.get('novelty_score', 0)
        pathway = idea.get('product_pathway', 'unknown')
        extends = idea.get('extends_plugin') or '--'

        md += f"| {rank} | {name} | {tier.replace('_', ' ')} | {composite} | {utility} | {market} | {novelty} | {pathway_display(pathway)} | {extends} |\n"

    md += "\n---\n\n## Detailed Analysis\n\n"

    for idea in shortlist:
        rank = idea.get('rank', 0)
        name = idea.get('display_name', idea.get('plugin_name', 'Unnamed'))
        tier = idea.get('tier', 'BACKLOG')
        one_liner = idea.get('one_liner', '')
        composite = idea.get('composite_score', 0)
        utility = idea.get('personal_utility', 0)
        market = idea.get('marketization_score', 0)
        novelty = idea.get('novelty_score', 0)
        pathway = idea.get('product_pathway', 'unknown')
        pathway_note = idea.get('pathway_note', '')
        extends = idea.get('extends_plugin') or 'Standalone'
        target_user = idea.get('target_user', '')
        why_it_fits = idea.get('why_it_fits', '')
        market_signal = idea.get('market_signal', '')
        ai_advantage = idea.get('ai_native_advantage', idea.get('ai_advantage', ''))
        key_risk = idea.get('key_risk', '')
        build_estimate = idea.get('build_estimate', {})
        plugin_mvp = build_estimate.get('plugin_mvp', 'N/A')
        product_mvp = build_estimate.get('product_mvp', 'N/A')
        structure = idea.get('proposed_structure', {})
        agents = structure.get('agents', 0)
        commands = structure.get('commands', 0)
        skills = structure.get('skills', 0)
        strategy = idea.get('generation_strategy', '')
        create_prompt = idea.get('create_prompt', '')
        architecture = idea.get('architecture_sketch')

        md += f"""### #{rank}. {name}

**Tier:** {tier.replace('_', ' ')}
**One-liner:** {one_liner}

**Scores:**
- Composite: {composite}
- Personal Utility: {utility}
- Marketization: {market}
- Novelty: {novelty}

**Details:**
- Product Pathway: {pathway_display(pathway)}
- Extends: {extends}
- Target User: {target_user}
- Generation Strategy: {strategy.replace('-', ' ').title() if strategy else 'N/A'}
- Build: Plugin {plugin_mvp} / Product {product_mvp}
- Structure: {agents} agents, {commands} commands, {skills} skills

"""

        if why_it_fits:
            md += f"**Why It Fits You:**\n{why_it_fits}\n\n"

        if market_signal:
            md += f"**Market Signal:**\n{market_signal}\n\n"

        if ai_advantage:
            md += f"**AI-Native Advantage:**\n{ai_advantage}\n\n"

        if pathway_note:
            md += f"**Monetization Pathway:**\n{pathway_note}\n\n"

        if key_risk:
            md += f"**Key Risk:**\n{key_risk}\n\n"

        if architecture:
            md += "**Architecture Sketch:**\n\n"
            arch_agents = architecture.get('agents', [])
            if arch_agents:
                md += "Agents:\n"
                for a in arch_agents:
                    md += f"- `{a.get('name', '')}` ({a.get('model', '')}) — {a.get('purpose', '')}\n"
                md += "\n"

            arch_commands = architecture.get('commands', [])
            if arch_commands:
                md += "Commands:\n"
                for c in arch_commands:
                    md += f"- `{c.get('name', '')}` — {c.get('description', '')}\n"
                md += "\n"

            arch_flow = architecture.get('data_flow', '')
            if arch_flow:
                md += f"Data Flow: {arch_flow}\n\n"

            arch_connect = architecture.get('interconnections', '')
            if arch_connect:
                md += f"Interconnections: {arch_connect}\n\n"

        if create_prompt:
            md += f"**Build This Plugin:**\n\n```\n{create_prompt}\n```\n\n"

        md += "---\n\n"

    # Themes
    if themes:
        md += "## Emerging Themes\n\n"

        if themes.get('dominant_theme'):
            md += f"**Dominant Theme:**  \n{themes['dominant_theme']}\n\n"

        if themes.get('emerging_capability'):
            md += f"**Emerging Capability:**  \n{themes['emerging_capability']}\n\n"

        if themes.get('strongest_market_signal'):
            md += f"**Strongest Market Signal:**  \n{themes['strongest_market_signal']}\n\n"

    # Portfolio Analysis
    if portfolio_analysis:
        md += "## Portfolio Gap Analysis\n\n"
        total = portfolio_analysis.get('total_plugins', 0)
        covered = portfolio_analysis.get('covered_domains', [])
        gaps = portfolio_analysis.get('gap_domains', [])

        md += f"- **Total Plugins:** {total}\n"
        md += f"- **Covered Domains ({len(covered)}):** {', '.join(covered)}\n"
        md += f"- **Gap Domains ({len(gaps)}):** {', '.join(gaps)}\n\n"

        extensions = portfolio_analysis.get('extension_opportunities', [])
        if extensions:
            md += "**Extension Opportunities:**\n\n"
            for ext in extensions:
                existing = ext.get('existing', '')
                extension = ext.get('extension', '')
                md += f"- **{existing}** -> {extension}\n"
            md += "\n"

    md += f"""---

*Generated by Plugin Idea Generator on {generated_date}*
*ROK Plugin Marketplace - Plugin Idea Generator v{PLUGIN_VERSION}*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)


def main():
    parser = argparse.ArgumentParser(description='Export Plugin Idea Generator shortlist to HTML, PDF, and Markdown')
    parser.add_argument('--input', required=True, help='Path to shortlist JSON file')
    parser.add_argument('--output-dir', default=DEFAULT_OUTPUT_DIR, help='Output directory')

    args = parser.parse_args()

    # Read input JSON
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate data type
    if data.get('type') != 'plugin_idea_shortlist':
        print(f"Warning: Expected type 'plugin_idea_shortlist', got '{data.get('type')}'", file=sys.stderr)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate filename base
    topic = data.get('topic')
    topic_slug = slugify(topic) if topic else "open_discovery"
    date_str = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    base_filename = f"plugin_ideas_{topic_slug}_{date_str}"

    # Generate outputs
    try:
        html_path = os.path.join(args.output_dir, f"{base_filename}.html")
        print(f"Generating HTML: {html_path}")
        generate_html(data, html_path)
        print(f"  HTML generated successfully")

        pdf_path = os.path.join(args.output_dir, f"{base_filename}.pdf")
        print(f"Generating PDF: {pdf_path}")
        generate_pdf(data, pdf_path)
        print(f"  PDF generated successfully")

        md_path = os.path.join(args.output_dir, f"{base_filename}.md")
        print(f"Generating Markdown: {md_path}")
        generate_markdown(data, md_path)
        print(f"  Markdown generated successfully")

        print("\nExport complete!")
        print(f"\nOutput files:")
        print(f"  - {html_path}")
        print(f"  - {pdf_path}")
        print(f"  - {md_path}")

    except Exception as e:
        print(f"Error during export: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
