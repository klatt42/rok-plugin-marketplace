#!/usr/bin/env python3
"""
Business Idea Finder - Export Script
Generates HTML, PDF, and Markdown files from idea finder shortlist JSON.

Usage:
    python3 idea_finder_export.py --input shortlist.json
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

# Color scheme (teal-based)
TEAL = "#0D9488"
TEAL_DARK = "#0F766E"

TIER_COLORS = {
    "HOT": {"bg": "#059669", "text": "#FFFFFF"},
    "WARM": {"bg": "#0D9488", "text": "#FFFFFF"},
    "WATCH": {"bg": "#D97706", "text": "#FFFFFF"},
    "PASS": {"bg": "#DC2626", "text": "#FFFFFF"}
}

# Default output directory
DEFAULT_OUTPUT_DIR = "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Idea_Finder/"


def latin_safe(text):
    """Convert text to Latin-1 safe string for PDF output."""
    if text is None:
        return ""
    return str(text).encode('latin-1', 'ignore').decode('latin-1')


def slugify(text):
    """Convert text to URL-safe slug."""
    if not text:
        return "broad_scan"
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')


def score_color(score):
    """Return color based on score value."""
    if score >= 80:
        return "#059669"  # Green
    elif score >= 65:
        return "#0D9488"  # Teal
    elif score >= 50:
        return "#D97706"  # Amber
    else:
        return "#DC2626"  # Red


def generate_html(data, output_path):
    """Generate HTML report from shortlist data."""
    topic = data.get('topic') or "Broad Market Scan"
    depth = data.get('depth', 'explore').upper()
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    shortlist = data.get('shortlist', [])
    themes = data.get('themes', {})
    methodology = data.get('methodology', {})

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Idea Finder - {topic}</title>
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
            background: linear-gradient(135deg, #f0fdfa 0%, #ffffff 100%);
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
            background: linear-gradient(135deg, {TEAL} 0%, {TEAL_DARK} 100%);
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
            color: {TEAL_DARK};
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid {TEAL};
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
            background: {TEAL};
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
            background: #f0fdfa;
        }}

        .rank {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {TEAL};
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
            border-color: {TEAL};
            box-shadow: 0 8px 24px rgba(13,148,136,0.15);
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
            color: {TEAL_DARK};
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
            border-left: 4px solid {TEAL};
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

        .evidence {{
            background: #f0fdfa;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }}

        .evidence-title {{
            font-weight: 600;
            color: {TEAL_DARK};
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

        .modes-list {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}

        .mode-tag {{
            background: {TEAL};
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 500;
        }}

        .analyze-prompt {{
            background: #1f2937;
            color: #f9fafb;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 1rem;
            position: relative;
        }}

        .analyze-prompt-title {{
            font-weight: 600;
            margin-bottom: 0.8rem;
            color: #10b981;
        }}

        .analyze-prompt code {{
            display: block;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
        }}

        .themes-section {{
            background: linear-gradient(135deg, #f0fdfa 0%, #ecfdf5 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-top: 2rem;
        }}

        .theme-item {{
            margin-bottom: 1.5rem;
        }}

        .theme-label {{
            font-weight: 600;
            color: {TEAL_DARK};
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
            <h1>Business Idea Finder</h1>
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
                    <div class="meta-label">Total Discoveries</div>
                    <div class="meta-value">{data.get('total_raw_discoveries', 0)}</div>
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
                            <th>Idea Name</th>
                            <th style="width: 100px;">Tier</th>
                            <th style="width: 120px;">Score</th>
                            <th style="width: 120px;">Profile Fit</th>
                            <th style="width: 140px;">Opportunity</th>
                            <th style="width: 100px;">Type</th>
                            <th style="width: 120px;">Build Time</th>
                            <th style="width: 130px;">Window</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # Add shortlist table rows
    for idea in shortlist:
        rank = idea.get('rank', 0)
        name = idea.get('idea_name', 'Unnamed Idea')
        tier = idea.get('tier', 'WATCH')
        composite = idea.get('composite_score', 0)
        profile_fit = idea.get('profile_fit', 0)
        opportunity = idea.get('opportunity_signal', 0)
        opp_type = idea.get('opportunity_type', 'Unknown')
        build_time = idea.get('estimated_build_time', 'N/A')
        window = idea.get('arbitrage_window', 'N/A')

        tier_style = f"background: {TIER_COLORS.get(tier, TIER_COLORS['WATCH'])['bg']}; color: {TIER_COLORS.get(tier, TIER_COLORS['WATCH'])['text']};"

        html += f"""
                        <tr>
                            <td class="rank">#{rank}</td>
                            <td><strong>{name}</strong></td>
                            <td><span class="tier-badge" style="{tier_style}">{tier}</span></td>
                            <td>
                                <div class="score" style="color: {score_color(composite)};">{composite}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {composite}%; background: {score_color(composite)};"></div>
                                </div>
                            </td>
                            <td>
                                <div class="score" style="color: {score_color(profile_fit)};">{profile_fit}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {profile_fit}%; background: {score_color(profile_fit)};"></div>
                                </div>
                            </td>
                            <td>
                                <div class="score" style="color: {score_color(opportunity)};">{opportunity}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {opportunity}%; background: {score_color(opportunity)};"></div>
                                </div>
                            </td>
                            <td>{opp_type}</td>
                            <td>{build_time}</td>
                            <td>{window}</td>
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
        name = idea.get('idea_name', 'Unnamed Idea')
        tier = idea.get('tier', 'WATCH')
        one_liner = idea.get('one_liner', '')
        composite = idea.get('composite_score', 0)
        profile_fit = idea.get('profile_fit', 0)
        opportunity = idea.get('opportunity_signal', 0)
        opp_type = idea.get('opportunity_type', 'Unknown')
        build_time = idea.get('estimated_build_time', 'N/A')
        window = idea.get('arbitrage_window', 'N/A')
        evidence = idea.get('key_evidence', '')
        ai_advantage = idea.get('ai_advantage', '')
        modes = idea.get('discovery_modes', [])
        analyze_prompt = idea.get('analyze_prompt', '')
        intersection = idea.get('intersection_multiplier', 1.0)

        tier_style = f"background: {TIER_COLORS.get(tier, TIER_COLORS['WATCH'])['bg']}; color: {TIER_COLORS.get(tier, TIER_COLORS['WATCH'])['text']};"

        html += f"""
                <div class="idea-card">
                    <div class="idea-card-header">
                        <div class="idea-title">#{rank}. {name}</div>
                        <div class="idea-badges">
                            <span class="tier-badge" style="{tier_style}">{tier}</span>
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
                            <div class="detail-label">Profile Fit</div>
                            <div class="detail-value" style="color: {score_color(profile_fit)};">{profile_fit}</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {profile_fit}%; background: {score_color(profile_fit)};"></div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Opportunity Signal</div>
                            <div class="detail-value" style="color: {score_color(opportunity)};">{opportunity}</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {opportunity}%; background: {score_color(opportunity)};"></div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Opportunity Type</div>
                            <div class="detail-value">{opp_type}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Build Time</div>
                            <div class="detail-value">{build_time}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Arbitrage Window</div>
                            <div class="detail-value">{window}</div>
                        </div>
"""

        if intersection > 1.0:
            html += f"""
                        <div class="detail-item">
                            <div class="detail-label">Intersection Multiplier</div>
                            <div class="detail-value" style="color: {TEAL};">{intersection}x</div>
                        </div>
"""

        html += """
                    </div>
"""

        if evidence:
            html += f"""
                    <div class="evidence">
                        <div class="evidence-title">Key Evidence</div>
                        <div>{evidence}</div>
                    </div>
"""

        if ai_advantage:
            html += f"""
                    <div class="ai-advantage">
                        <div class="ai-advantage-title">AI Advantage</div>
                        <div>{ai_advantage}</div>
                    </div>
"""

        if modes:
            html += f"""
                    <div style="margin-bottom: 1rem;">
                        <div class="detail-label" style="margin-bottom: 0.5rem;">Discovery Modes</div>
                        <div class="modes-list">
"""
            for mode in modes:
                html += f'                            <span class="mode-tag">{mode}</span>\n'

            html += """
                        </div>
                    </div>
"""

        if analyze_prompt:
            html += f"""
                    <div class="analyze-prompt">
                        <div class="analyze-prompt-title">Ready-to-Paste Analyzer Prompt</div>
                        <code>{analyze_prompt}</code>
                    </div>
"""

        html += """
                </div>
"""

    html += """
            </div>
"""

    # Add themes section
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

        if themes.get('emerging_niche'):
            html += f"""
                    <div class="theme-item">
                        <div class="theme-label">Emerging Niche</div>
                        <div class="theme-value">{themes['emerging_niche']}</div>
                    </div>
"""

        if themes.get('strongest_arbitrage'):
            html += f"""
                    <div class="theme-item">
                        <div class="theme-label">Strongest Arbitrage Opportunity</div>
                        <div class="theme-value">{themes['strongest_arbitrage']}</div>
                    </div>
"""

        html += """
                </div>
            </div>
"""

    # Add methodology section
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

        html += """
                </div>
            </div>
"""

    html += f"""
            <div class="footer">
                Generated by Business Idea Finder on {generated_date}<br>
                ROK Plugin Marketplace - Business Idea Finder v{PLUGIN_VERSION}
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

    class IdeaFinderPDF(FPDF):
        def header(self):
            self.set_fill_color(13, 148, 136)  # TEAL
            self.rect(0, 0, 210, 40, 'F')
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 20)
            self.cell(0, 15, '', 0, 1)
            self.cell(0, 10, latin_safe('Business Idea Finder'), 0, 1, 'C')
            self.set_font('Arial', '', 12)
            topic = data.get('topic') or 'Broad Market Scan'
            self.cell(0, 8, latin_safe(topic), 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = IdeaFinderPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Summary stats
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(15, 118, 110)  # TEAL_DARK
    pdf.cell(0, 10, latin_safe('Summary'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)

    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    depth = data.get('depth', 'explore').upper()
    total_raw = data.get('total_raw_discoveries', 0)
    after_dedup = data.get('after_dedup', 0)
    shortlist_count = data.get('shortlist_count', 0)

    pdf.cell(90, 8, latin_safe(f'Generated: {generated_date}'), 0, 0)
    pdf.cell(90, 8, latin_safe(f'Depth: {depth}'), 0, 1)
    pdf.cell(90, 8, latin_safe(f'Raw Discoveries: {total_raw}'), 0, 0)
    pdf.cell(90, 8, latin_safe(f'After Dedup: {after_dedup}'), 0, 1)
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
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 10, latin_safe('Shortlist Overview'), 0, 1)
    pdf.ln(2)

    shortlist = data.get('shortlist', [])

    # Table header
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(13, 148, 136)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(12, 8, '#', 1, 0, 'C', True)
    pdf.cell(60, 8, 'Idea Name', 1, 0, 'C', True)
    pdf.cell(20, 8, 'Tier', 1, 0, 'C', True)
    pdf.cell(20, 8, 'Score', 1, 0, 'C', True)
    pdf.cell(30, 8, 'Build Time', 1, 0, 'C', True)
    pdf.cell(38, 8, 'Window', 1, 1, 'C', True)

    # Table rows
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(0, 0, 0)

    for idea in shortlist:
        rank = idea.get('rank', 0)
        name = idea.get('idea_name', 'Unnamed Idea')
        tier = idea.get('tier', 'WATCH')
        composite = idea.get('composite_score', 0)
        build_time = idea.get('estimated_build_time', 'N/A')
        window = idea.get('arbitrage_window', 'N/A')

        pdf.cell(12, 8, str(rank), 1, 0, 'C')
        pdf.cell(60, 8, latin_safe(name[:35]), 1, 0)
        pdf.cell(20, 8, tier, 1, 0, 'C')
        pdf.cell(20, 8, str(composite), 1, 0, 'C')
        pdf.cell(30, 8, latin_safe(build_time), 1, 0, 'C')
        pdf.cell(38, 8, latin_safe(window), 1, 1, 'C')

    pdf.ln(10)

    # Detailed sections
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 10, latin_safe('Detailed Analysis'), 0, 1)
    pdf.ln(5)

    for idx, idea in enumerate(shortlist):
        if idx > 0:
            pdf.ln(8)

        rank = idea.get('rank', 0)
        name = idea.get('idea_name', 'Unnamed Idea')
        tier = idea.get('tier', 'WATCH')
        one_liner = idea.get('one_liner', '')
        composite = idea.get('composite_score', 0)
        profile_fit = idea.get('profile_fit', 0)
        opportunity = idea.get('opportunity_signal', 0)
        opp_type = idea.get('opportunity_type', 'Unknown')
        build_time = idea.get('estimated_build_time', 'N/A')
        window = idea.get('arbitrage_window', 'N/A')
        evidence = idea.get('key_evidence', '')
        ai_advantage = idea.get('ai_advantage', '')
        modes = idea.get('discovery_modes', [])

        # Idea header
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 8, latin_safe(f'#{rank}. {name}'), 0, 1)

        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 6, latin_safe(one_liner))
        pdf.ln(2)

        # Scores
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(60, 6, latin_safe(f'Composite Score: {composite}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Profile Fit: {profile_fit}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Opportunity: {opportunity}'), 0, 1)

        pdf.cell(60, 6, latin_safe(f'Type: {opp_type}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Build Time: {build_time}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Window: {window}'), 0, 1)

        pdf.ln(3)

        # Evidence
        if evidence:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Key Evidence:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(0, 5, latin_safe(evidence))
            pdf.ln(2)

        # AI Advantage
        if ai_advantage:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('AI Advantage:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(0, 5, latin_safe(ai_advantage))
            pdf.ln(2)

        # Discovery modes
        if modes:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe(f'Discovery Modes: {", ".join(modes)}'), 0, 1)

        # Page break check
        if pdf.get_y() > 250 and idx < len(shortlist) - 1:
            pdf.add_page()

    # Themes section
    themes = data.get('themes', {})
    if themes:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(15, 118, 110)
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

        if themes.get('emerging_niche'):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Emerging Niche:'), 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, latin_safe(themes['emerging_niche']))
            pdf.ln(3)

        if themes.get('strongest_arbitrage'):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Strongest Arbitrage Opportunity:'), 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, latin_safe(themes['strongest_arbitrage']))

    pdf.output(output_path)


def generate_markdown(data, output_path):
    """Generate Markdown report from shortlist data."""
    topic = data.get('topic') or "Broad Market Scan"
    depth = data.get('depth', 'explore').upper()
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    shortlist = data.get('shortlist', [])
    themes = data.get('themes', {})
    methodology = data.get('methodology', {})

    md = f"""# Business Idea Finder

## {topic}

**Generated:** {generated_date}
**Depth:** {depth}
**Shortlist Count:** {len(shortlist)}
**Total Raw Discoveries:** {data.get('total_raw_discoveries', 0)}
**After Deduplication:** {data.get('after_dedup', 0)}

---

## Methodology

"""

    if methodology:
        md += f"""- **Agents Dispatched:** {methodology.get('agents_dispatched', 0)}
- **Total Searches:** {methodology.get('total_searches', 0)}
- **Duplicates Merged:** {methodology.get('dedup_merges', 0)}
- **Sources Covered:** {', '.join(methodology.get('sources_covered', []))}

"""

    md += """---

## Shortlist Overview

| Rank | Idea Name | Tier | Score | Profile Fit | Opportunity | Type | Build Time | Window |
|------|-----------|------|-------|-------------|-------------|------|------------|--------|
"""

    for idea in shortlist:
        rank = idea.get('rank', 0)
        name = idea.get('idea_name', 'Unnamed Idea')
        tier = idea.get('tier', 'WATCH')
        composite = idea.get('composite_score', 0)
        profile_fit = idea.get('profile_fit', 0)
        opportunity = idea.get('opportunity_signal', 0)
        opp_type = idea.get('opportunity_type', 'Unknown')
        build_time = idea.get('estimated_build_time', 'N/A')
        window = idea.get('arbitrage_window', 'N/A')

        md += f"| {rank} | {name} | {tier} | {composite} | {profile_fit} | {opportunity} | {opp_type} | {build_time} | {window} |\n"

    md += "\n---\n\n## Detailed Analysis\n\n"

    for idea in shortlist:
        rank = idea.get('rank', 0)
        name = idea.get('idea_name', 'Unnamed Idea')
        tier = idea.get('tier', 'WATCH')
        one_liner = idea.get('one_liner', '')
        composite = idea.get('composite_score', 0)
        profile_fit = idea.get('profile_fit', 0)
        opportunity = idea.get('opportunity_signal', 0)
        opp_type = idea.get('opportunity_type', 'Unknown')
        build_time = idea.get('estimated_build_time', 'N/A')
        window = idea.get('arbitrage_window', 'N/A')
        evidence = idea.get('key_evidence', '')
        ai_advantage = idea.get('ai_advantage', '')
        modes = idea.get('discovery_modes', [])
        intersection = idea.get('intersection_multiplier', 1.0)
        analyze_prompt = idea.get('analyze_prompt', '')

        md += f"""### #{rank}. {name}

**Tier:** {tier}
**One-liner:** {one_liner}

**Scores:**
- Composite Score: {composite}
- Profile Fit: {profile_fit}
- Opportunity Signal: {opportunity}

**Details:**
- Opportunity Type: {opp_type}
- Estimated Build Time: {build_time}
- Arbitrage Window: {window}
"""

        if intersection > 1.0:
            md += f"- Intersection Multiplier: {intersection}x\n"

        md += "\n"

        if evidence:
            md += f"""**Key Evidence:**
{evidence}

"""

        if ai_advantage:
            md += f"""**AI Advantage:**
{ai_advantage}

"""

        if modes:
            md += f"**Discovery Modes:** {', '.join(modes)}\n\n"

        if analyze_prompt:
            md += f"""**Ready-to-Paste Analyzer Prompt:**

```
{analyze_prompt}
```

"""

        md += "---\n\n"

    if themes:
        md += "## Emerging Themes\n\n"

        if themes.get('dominant_theme'):
            md += f"**Dominant Theme:**  \n{themes['dominant_theme']}\n\n"

        if themes.get('emerging_niche'):
            md += f"**Emerging Niche:**  \n{themes['emerging_niche']}\n\n"

        if themes.get('strongest_arbitrage'):
            md += f"**Strongest Arbitrage Opportunity:**  \n{themes['strongest_arbitrage']}\n\n"

    md += f"""---

*Generated by Business Idea Finder on {generated_date}*
*ROK Plugin Marketplace - Business Idea Finder v{PLUGIN_VERSION}*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)


def main():
    parser = argparse.ArgumentParser(description='Export Business Idea Finder shortlist to HTML, PDF, and Markdown')
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
    if data.get('type') != 'idea_finder_shortlist':
        print(f"Warning: Expected type 'idea_finder_shortlist', got '{data.get('type')}'", file=sys.stderr)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate filename base
    topic = data.get('topic')
    topic_slug = slugify(topic) if topic else "broad_scan"
    date_str = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    base_filename = f"idea_finder_{topic_slug}_{date_str}"

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
