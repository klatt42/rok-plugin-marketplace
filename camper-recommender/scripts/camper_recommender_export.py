#!/usr/bin/env python3
"""
Camper Recommender - Export Script
Generates HTML, PDF, and Markdown files from camper/RV recommendations JSON.

Usage:
    python3 camper_recommender_export.py --input recommendations.json
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

# Color scheme (purple-based)
PURPLE = "#8B5CF6"
PURPLE_DARK = "#7C3AED"

TIER_COLORS = {
    "TOP_PICK": {"bg": "#059669", "text": "#FFFFFF"},
    "RECOMMENDED": {"bg": "#2563EB", "text": "#FFFFFF"},
    "CONSIDER": {"bg": "#D97706", "text": "#FFFFFF"},
    "PASS": {"bg": "#DC2626", "text": "#FFFFFF"}
}

# Default output directory
DEFAULT_OUTPUT_DIR = "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Camper_Recommendations/"


def latin_safe(text):
    """Convert text to Latin-1 safe string for PDF output."""
    if text is None:
        return ""
    return str(text).encode('latin-1', 'ignore').decode('latin-1')


def slugify(text):
    """Convert text to URL-safe slug."""
    if not text:
        return "general"
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')


def score_color(score):
    """Return color based on score value."""
    if score >= 85:
        return "#059669"  # Green
    elif score >= 70:
        return "#2563EB"  # Blue
    elif score >= 55:
        return "#D97706"  # Amber
    else:
        return "#DC2626"  # Red


def generate_html(data, output_path):
    """Generate HTML report from camper/RV recommendations data."""
    profile = data.get('requirements_profile', {})
    camper_type = profile.get('camper_type', 'Camper/RV')
    rv_type = profile.get('rv_type', '')
    budget = profile.get('budget_range', 'Not specified')
    tow_vehicle = profile.get('tow_vehicle', 'Not specified')
    depth = data.get('depth', 'standard').upper()
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    recommendations = data.get('recommendations', [])
    themes = data.get('themes', {})
    methodology = data.get('methodology', {})

    must_haves = ', '.join(profile.get('must_haves', []))
    priorities = ', '.join(profile.get('priorities', []))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Camper/RV Recommendations - {camper_type}</title>
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
            background: linear-gradient(135deg, #F5F3FF 0%, #FFFFFF 100%);
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
            background: linear-gradient(135deg, {PURPLE} 0%, {PURPLE_DARK} 100%);
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
            color: {PURPLE_DARK};
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid {PURPLE};
        }}

        .requirements-box {{
            background: #F5F3FF;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border-left: 4px solid {PURPLE};
        }}

        .requirements-box h3 {{
            color: {PURPLE_DARK};
            margin-bottom: 0.8rem;
        }}

        .req-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}

        .req-item {{
            font-size: 0.95rem;
        }}

        .req-label {{
            font-weight: 600;
            color: #374151;
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
            background: {PURPLE};
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
            background: #F5F3FF;
        }}

        .rank {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {PURPLE};
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

        .camper-card {{
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        }}

        .camper-card:hover {{
            border-color: {PURPLE};
            box-shadow: 0 8px 24px rgba(139,92,246,0.15);
        }}

        .camper-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .camper-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {PURPLE_DARK};
            flex: 1;
        }}

        .camper-badges {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}

        .floorplan-rec {{
            font-size: 1.05rem;
            color: #4b5563;
            font-style: italic;
            margin-bottom: 1.5rem;
            padding-left: 1rem;
            border-left: 4px solid {PURPLE};
        }}

        .detail-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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

        .weight-towing-box {{
            background: #FDF4FF;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border: 2px solid #E9D5FF;
        }}

        .weight-towing-box h4 {{
            color: {PURPLE_DARK};
            margin-bottom: 0.8rem;
            font-size: 1.1rem;
        }}

        .weight-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }}

        .weight-item {{
            text-align: center;
            padding: 0.5rem;
        }}

        .weight-value {{
            font-size: 1.3rem;
            font-weight: 700;
            color: {PURPLE_DARK};
        }}

        .weight-label {{
            font-size: 0.8rem;
            color: #6b7280;
            text-transform: uppercase;
        }}

        .tank-info {{
            background: #F0FDF4;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            border-left: 4px solid #059669;
        }}

        .tank-info h4 {{
            color: #059669;
            margin-bottom: 0.5rem;
        }}

        .tank-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 0.5rem;
        }}

        .pros-cons {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .pros {{
            background: #ecfdf5;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #059669;
        }}

        .cons {{
            background: #fef2f2;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #DC2626;
        }}

        .pros h4 {{
            color: #059669;
            margin-bottom: 0.5rem;
        }}

        .cons h4 {{
            color: #DC2626;
            margin-bottom: 0.5rem;
        }}

        .pros ul, .cons ul {{
            list-style: none;
            padding: 0;
        }}

        .pros li::before {{
            content: "+  ";
            color: #059669;
            font-weight: 700;
        }}

        .cons li::before {{
            content: "-  ";
            color: #DC2626;
            font-weight: 700;
        }}

        .finder-prompt {{
            background: #1f2937;
            color: #f9fafb;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 1rem;
            position: relative;
        }}

        .finder-prompt-title {{
            font-weight: 600;
            margin-bottom: 0.8rem;
            color: #C4B5FD;
        }}

        .finder-prompt code {{
            display: block;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.5;
        }}

        .themes-section {{
            background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-top: 2rem;
        }}

        .theme-item {{
            margin-bottom: 1.5rem;
        }}

        .theme-label {{
            font-weight: 600;
            color: {PURPLE_DARK};
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
            <h1>Camper/RV Recommendations</h1>
            <div class="subtitle">{camper_type} &mdash; {budget}</div>
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
                    <div class="meta-value">{len(recommendations)} Campers</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Analyzed</div>
                    <div class="meta-value">{data.get('campers_analyzed', 0)} Total</div>
                </div>
            </div>
        </div>

        <div class="content">
            <div class="section">
                <div class="requirements-box">
                    <h3>Your Requirements</h3>
                    <div class="req-grid">
                        <div class="req-item">
                            <div class="req-label">RV Type</div>
                            <div>{rv_type or camper_type}</div>
                        </div>
                        <div class="req-item">
                            <div class="req-label">Budget</div>
                            <div>{budget} ({profile.get('buying_preference', '')})</div>
                        </div>
                        <div class="req-item">
                            <div class="req-label">Must-Haves</div>
                            <div>{must_haves or 'None specified'}</div>
                        </div>
                        <div class="req-item">
                            <div class="req-label">Priorities</div>
                            <div>{priorities or 'None specified'}</div>
                        </div>
                        <div class="req-item">
                            <div class="req-label">Tow Vehicle</div>
                            <div>{tow_vehicle}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Recommendation Overview</h2>
                <table class="shortlist-table">
                    <thead>
                        <tr>
                            <th style="width: 60px;">Rank</th>
                            <th>Camper</th>
                            <th style="width: 100px;">RV Type</th>
                            <th style="width: 120px;">Tier</th>
                            <th style="width: 100px;">Score</th>
                            <th style="width: 100px;">Fit</th>
                            <th style="width: 80px;">Year</th>
                            <th style="width: 130px;">MSRP</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # Add table rows
    for rec in recommendations:
        rank = rec.get('rank', 0)
        make_model = rec.get('make_model', 'Unknown')
        floorplan = rec.get('floorplan', '')
        name = f"{make_model} {floorplan}".strip()
        rv_type_rec = rec.get('rv_type', 'N/A')
        tier = rec.get('tier', 'CONSIDER')
        composite = rec.get('composite_score', 0)
        fit = rec.get('fit_score', 0)
        market = rec.get('market_score', 0)
        year = rec.get('year', 'N/A')
        msrp = rec.get('msrp_range', 'N/A')

        tier_style = f"background: {TIER_COLORS.get(tier, TIER_COLORS['CONSIDER'])['bg']}; color: {TIER_COLORS.get(tier, TIER_COLORS['CONSIDER'])['text']};"

        html += f"""
                        <tr>
                            <td class="rank">#{rank}</td>
                            <td><strong>{name}</strong></td>
                            <td>{rv_type_rec}</td>
                            <td><span class="tier-badge" style="{tier_style}">{tier}</span></td>
                            <td>
                                <div class="score" style="color: {score_color(composite)};">{composite}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {composite}%; background: {score_color(composite)};"></div>
                                </div>
                            </td>
                            <td>
                                <div class="score" style="color: {score_color(fit)};">{fit}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {fit}%; background: {score_color(fit)};"></div>
                                </div>
                            </td>
                            <td>{year}</td>
                            <td>{msrp}</td>
                        </tr>
"""

    html += """
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2 class="section-title">Detailed Analysis</h2>
"""

    # Add detailed camper cards
    for rec in recommendations:
        rank = rec.get('rank', 0)
        make_model = rec.get('make_model', 'Unknown')
        floorplan = rec.get('floorplan', '')
        name = f"{make_model} {floorplan}".strip()
        rv_type_rec = rec.get('rv_type', 'N/A')
        tier = rec.get('tier', 'CONSIDER')
        composite = rec.get('composite_score', 0)
        fit = rec.get('fit_score', 0)
        market = rec.get('market_score', 0)
        year = rec.get('year', 'N/A')
        msrp = rec.get('msrp_range', 'N/A')
        build_quality = rec.get('build_quality_rating', 'N/A')
        length_ft = rec.get('length_ft', 'N/A')
        dry_weight = rec.get('dry_weight_lbs', 'N/A')
        gvwr = rec.get('gvwr_lbs', 'N/A')
        slides = rec.get('slides', 'N/A')
        sleeping_capacity = rec.get('sleeping_capacity', 'N/A')
        tco = rec.get('tco_5year', 'N/A')
        resale = rec.get('resale_3year', 'N/A')
        floorplan_rec = rec.get('best_floorplan_recommendation', '')
        pros = rec.get('pros', [])
        cons = rec.get('cons', [])
        sources = rec.get('key_sources', [])
        finder_prompt = rec.get('finder_prompt', '')
        tank_capacities = rec.get('tank_capacities', {})

        tier_style = f"background: {TIER_COLORS.get(tier, TIER_COLORS['CONSIDER'])['bg']}; color: {TIER_COLORS.get(tier, TIER_COLORS['CONSIDER'])['text']};"

        html += f"""
                <div class="camper-card">
                    <div class="camper-card-header">
                        <div class="camper-title">#{rank}. {name}</div>
                        <div class="camper-badges">
                            <span class="tier-badge" style="{tier_style}">{tier}</span>
                        </div>
                    </div>
"""

        if floorplan_rec:
            html += f"""
                    <div class="floorplan-rec">{floorplan_rec}</div>
"""

        html += f"""
                    <div class="detail-grid">
                        <div class="detail-item">
                            <div class="detail-label">Composite Score</div>
                            <div class="detail-value" style="color: {score_color(composite)};">{composite}</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {composite}%; background: {score_color(composite)};"></div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Fit Score</div>
                            <div class="detail-value" style="color: {score_color(fit)};">{fit}</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {fit}%; background: {score_color(fit)};"></div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Market Score</div>
                            <div class="detail-value" style="color: {score_color(market)};">{market}</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {market}%; background: {score_color(market)};"></div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">RV Type</div>
                            <div class="detail-value">{rv_type_rec}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Year</div>
                            <div class="detail-value">{year}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">MSRP Range</div>
                            <div class="detail-value">{msrp}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Build Quality</div>
                            <div class="detail-value">{build_quality}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Sleeping Capacity</div>
                            <div class="detail-value">{sleeping_capacity}</div>
                        </div>
                    </div>
"""

        # Weight and towing compatibility section
        if dry_weight != 'N/A' or gvwr != 'N/A' or length_ft != 'N/A' or slides != 'N/A':
            html += f"""
                    <div class="weight-towing-box">
                        <h4>Weight &amp; Dimensions</h4>
                        <div class="weight-grid">
                            <div class="weight-item">
                                <div class="weight-value">{length_ft}</div>
                                <div class="weight-label">Length (ft)</div>
                            </div>
                            <div class="weight-item">
                                <div class="weight-value">{dry_weight}</div>
                                <div class="weight-label">Dry Weight (lbs)</div>
                            </div>
                            <div class="weight-item">
                                <div class="weight-value">{gvwr}</div>
                                <div class="weight-label">GVWR (lbs)</div>
                            </div>
                            <div class="weight-item">
                                <div class="weight-value">{slides}</div>
                                <div class="weight-label">Slides</div>
                            </div>
                        </div>
                    </div>
"""

        # Tank capacities section (if available)
        if tank_capacities:
            fresh = tank_capacities.get('fresh_water', 'N/A')
            gray = tank_capacities.get('gray_water', 'N/A')
            black = tank_capacities.get('black_water', 'N/A')
            propane = tank_capacities.get('propane', 'N/A')

            html += f"""
                    <div class="tank-info">
                        <h4>Tank Capacities</h4>
                        <div class="tank-grid">
                            <div>
                                <div class="detail-label">Fresh Water</div>
                                <div class="detail-value">{fresh}</div>
                            </div>
                            <div>
                                <div class="detail-label">Gray Water</div>
                                <div class="detail-value">{gray}</div>
                            </div>
                            <div>
                                <div class="detail-label">Black Water</div>
                                <div class="detail-value">{black}</div>
                            </div>
                            <div>
                                <div class="detail-label">Propane</div>
                                <div class="detail-value">{propane}</div>
                            </div>
                        </div>
                    </div>
"""

        if tco != 'N/A' or resale != 'N/A':
            html += f"""
                    <div class="detail-grid">
                        <div class="detail-item">
                            <div class="detail-label">TCO (5yr)</div>
                            <div class="detail-value">{tco}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Resale (3yr)</div>
                            <div class="detail-value">{resale}</div>
                        </div>
                    </div>
"""

        if pros or cons:
            html += """
                    <div class="pros-cons">
"""
            if pros:
                html += """
                        <div class="pros">
                            <h4>Strengths</h4>
                            <ul>
"""
                for p in pros:
                    html += f"                                <li>{p}</li>\n"
                html += """
                            </ul>
                        </div>
"""
            if cons:
                html += """
                        <div class="cons">
                            <h4>Weaknesses</h4>
                            <ul>
"""
                for c in cons:
                    html += f"                                <li>{c}</li>\n"
                html += """
                            </ul>
                        </div>
"""
            html += """
                    </div>
"""

        if sources:
            sources_str = ', '.join(sources)
            html += f"""
                    <div style="margin-bottom: 1rem;">
                        <div class="detail-label" style="margin-bottom: 0.3rem;">Key Sources</div>
                        <div style="color: #6b7280; font-size: 0.9rem;">{sources_str}</div>
                    </div>
"""

        if finder_prompt:
            html += f"""
                    <div class="finder-prompt">
                        <div class="finder-prompt-title">Ready-to-Paste Finder Prompt</div>
                        <code>{finder_prompt}</code>
                    </div>
"""

        html += """
                </div>
"""

    html += """
            </div>
"""

    # Themes section
    if themes:
        html += """
            <div class="section">
                <h2 class="section-title">Segment Insights</h2>
                <div class="themes-section">
"""

        if themes.get('segment_insight'):
            html += f"""
                    <div class="theme-item">
                        <div class="theme-label">Segment Insight</div>
                        <div class="theme-value">{themes['segment_insight']}</div>
                    </div>
"""

        if themes.get('best_value'):
            html += f"""
                    <div class="theme-item">
                        <div class="theme-label">Best Value</div>
                        <div class="theme-value">{themes['best_value']}</div>
                    </div>
"""

        if themes.get('quality_leader'):
            html += f"""
                    <div class="theme-item">
                        <div class="theme-label">Quality Leader</div>
                        <div class="theme-value">{themes['quality_leader']}</div>
                    </div>
"""

        if themes.get('rising_star'):
            html += f"""
                    <div class="theme-item">
                        <div class="theme-label">Rising Star</div>
                        <div class="theme-value">{themes['rising_star']}</div>
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

        if methodology.get('depth'):
            html += f"""
                    <div class="detail-item">
                        <div class="detail-label">Research Depth</div>
                        <div class="detail-value">{methodology['depth'].upper()}</div>
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
                Generated by Camper Recommender on {generated_date}<br>
                ROK Plugin Marketplace - Camper Recommender v1.0
            </div>
        </div>
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_pdf(data, output_path):
    """Generate PDF report from camper/RV recommendations data."""

    class CamperPDF(FPDF):
        def header(self):
            self.set_fill_color(139, 92, 246)  # PURPLE #8B5CF6
            self.rect(0, 0, 210, 40, 'F')
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 20)
            self.cell(0, 15, '', 0, 1)
            self.cell(0, 10, latin_safe('Camper/RV Recommendations'), 0, 1, 'C')
            self.set_font('Arial', '', 12)
            profile = data.get('requirements_profile', {})
            subtitle = f"{profile.get('camper_type', 'Camper/RV')} - {profile.get('budget_range', '')}"
            self.cell(0, 8, latin_safe(subtitle), 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = CamperPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    profile = data.get('requirements_profile', {})

    # Requirements summary
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(124, 58, 237)  # PURPLE_DARK
    pdf.cell(0, 10, latin_safe('Requirements'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0, 0, 0)

    rv_type = profile.get('rv_type', '')
    camper_type = profile.get('camper_type', 'N/A')
    pdf.cell(90, 7, latin_safe(f'RV Type: {rv_type or camper_type}'), 0, 0)
    pdf.cell(90, 7, latin_safe(f'Budget: {profile.get("budget_range", "N/A")}'), 0, 1)
    pdf.cell(90, 7, latin_safe(f'Preference: {profile.get("buying_preference", "N/A")}'), 0, 0)
    tow_vehicle = profile.get('tow_vehicle', 'N/A')
    pdf.cell(90, 7, latin_safe(f'Tow Vehicle: {tow_vehicle}'), 0, 1)
    must_haves = ', '.join(profile.get('must_haves', []))
    pdf.cell(90, 7, latin_safe(f'Must-Haves: {must_haves}'), 0, 0)
    priorities = ', '.join(profile.get('priorities', []))
    pdf.cell(90, 7, latin_safe(f'Priorities: {priorities}'), 0, 1)
    pdf.ln(5)

    # Summary stats
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 10, latin_safe('Summary'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)

    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    depth = data.get('depth', 'standard').upper()

    pdf.cell(90, 8, latin_safe(f'Generated: {generated_date}'), 0, 0)
    pdf.cell(90, 8, latin_safe(f'Depth: {depth}'), 0, 1)
    pdf.cell(90, 8, latin_safe(f'Campers Analyzed: {data.get("campers_analyzed", 0)}'), 0, 0)
    pdf.cell(90, 8, latin_safe(f'Shortlist: {data.get("shortlist_count", 0)}'), 0, 1)

    methodology = data.get('methodology', {})
    if methodology:
        pdf.cell(90, 8, latin_safe(f'Agents: {methodology.get("agents_dispatched", 0)}'), 0, 0)
        pdf.cell(90, 8, latin_safe(f'Searches: {methodology.get("total_searches", 0)}'), 0, 1)

    pdf.ln(10)

    # Recommendations table
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 10, latin_safe('Recommendations'), 0, 1)
    pdf.ln(2)

    recommendations = data.get('recommendations', [])

    # Table header
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(139, 92, 246)  # PURPLE
    pdf.set_text_color(255, 255, 255)
    pdf.cell(10, 8, '#', 1, 0, 'C', True)
    pdf.cell(45, 8, 'Camper', 1, 0, 'C', True)
    pdf.cell(25, 8, 'RV Type', 1, 0, 'C', True)
    pdf.cell(22, 8, 'Tier', 1, 0, 'C', True)
    pdf.cell(16, 8, 'Score', 1, 0, 'C', True)
    pdf.cell(14, 8, 'Fit', 1, 0, 'C', True)
    pdf.cell(14, 8, 'Year', 1, 0, 'C', True)
    pdf.cell(35, 8, 'MSRP', 1, 1, 'C', True)

    # Table rows
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(0, 0, 0)

    for rec in recommendations:
        rank = rec.get('rank', 0)
        make_model = rec.get('make_model', 'Unknown')
        floorplan = rec.get('floorplan', '')
        name = f"{make_model} {floorplan}".strip()
        rv_type_rec = rec.get('rv_type', 'N/A')
        tier = rec.get('tier', 'CONSIDER')
        composite = rec.get('composite_score', 0)
        fit = rec.get('fit_score', 0)
        year = rec.get('year', 'N/A')
        msrp = rec.get('msrp_range', 'N/A')

        pdf.cell(10, 8, str(rank), 1, 0, 'C')
        pdf.cell(45, 8, latin_safe(name[:26]), 1, 0)
        pdf.cell(25, 8, latin_safe(str(rv_type_rec)[:14]), 1, 0, 'C')
        pdf.cell(22, 8, tier, 1, 0, 'C')
        pdf.cell(16, 8, str(composite), 1, 0, 'C')
        pdf.cell(14, 8, str(fit), 1, 0, 'C')
        pdf.cell(14, 8, str(year), 1, 0, 'C')
        pdf.cell(35, 8, latin_safe(str(msrp)[:20]), 1, 1, 'C')

    pdf.ln(10)

    # Detailed sections
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 10, latin_safe('Detailed Analysis'), 0, 1)
    pdf.ln(5)

    for idx, rec in enumerate(recommendations):
        if idx > 0:
            pdf.ln(8)

        rank = rec.get('rank', 0)
        make_model = rec.get('make_model', 'Unknown')
        floorplan = rec.get('floorplan', '')
        name = f"{make_model} {floorplan}".strip()
        rv_type_rec = rec.get('rv_type', 'N/A')
        tier = rec.get('tier', 'CONSIDER')
        composite = rec.get('composite_score', 0)
        fit = rec.get('fit_score', 0)
        market = rec.get('market_score', 0)
        year = rec.get('year', 'N/A')
        msrp = rec.get('msrp_range', 'N/A')
        build_quality = rec.get('build_quality_rating', 'N/A')
        length_ft = rec.get('length_ft', 'N/A')
        dry_weight = rec.get('dry_weight_lbs', 'N/A')
        gvwr = rec.get('gvwr_lbs', 'N/A')
        slides = rec.get('slides', 'N/A')
        sleeping_capacity = rec.get('sleeping_capacity', 'N/A')
        tco = rec.get('tco_5year', 'N/A')
        resale = rec.get('resale_3year', 'N/A')
        floorplan_rec = rec.get('best_floorplan_recommendation', '')
        pros = rec.get('pros', [])
        cons = rec.get('cons', [])
        tank_capacities = rec.get('tank_capacities', {})

        # Camper header
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(124, 58, 237)
        pdf.cell(0, 8, latin_safe(f'#{rank}. {name} ({tier} - {composite})'), 0, 1)

        if floorplan_rec:
            pdf.set_font('Arial', 'I', 10)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 6, latin_safe(floorplan_rec))
            pdf.ln(2)

        # Scores and specs
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(60, 6, latin_safe(f'Composite: {composite}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Fit Score: {fit}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Market Score: {market}'), 0, 1)
        pdf.cell(60, 6, latin_safe(f'Year: {year}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'MSRP: {msrp}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'RV Type: {rv_type_rec}'), 0, 1)
        pdf.cell(60, 6, latin_safe(f'Build Quality: {build_quality}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Sleeping Capacity: {sleeping_capacity}'), 0, 1)
        pdf.ln(2)

        # Weight and towing info
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(124, 58, 237)
        pdf.cell(0, 6, latin_safe('Weight & Dimensions:'), 0, 1)
        pdf.set_font('Arial', '', 9)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(45, 6, latin_safe(f'Length: {length_ft} ft'), 0, 0)
        pdf.cell(50, 6, latin_safe(f'Dry Weight: {dry_weight} lbs'), 0, 0)
        pdf.cell(45, 6, latin_safe(f'GVWR: {gvwr} lbs'), 0, 0)
        pdf.cell(40, 6, latin_safe(f'Slides: {slides}'), 0, 1)

        # Tank capacities (if available)
        if tank_capacities:
            fresh = tank_capacities.get('fresh_water', 'N/A')
            gray = tank_capacities.get('gray_water', 'N/A')
            black = tank_capacities.get('black_water', 'N/A')
            propane = tank_capacities.get('propane', 'N/A')
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(5, 150, 105)
            pdf.cell(0, 6, latin_safe('Tank Capacities:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(45, 6, latin_safe(f'Fresh: {fresh}'), 0, 0)
            pdf.cell(45, 6, latin_safe(f'Gray: {gray}'), 0, 0)
            pdf.cell(45, 6, latin_safe(f'Black: {black}'), 0, 0)
            pdf.cell(45, 6, latin_safe(f'Propane: {propane}'), 0, 1)

        if tco != 'N/A' or resale != 'N/A':
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(60, 6, latin_safe(f'TCO (5yr): {tco}'), 0, 0)
            pdf.cell(60, 6, latin_safe(f'Resale (3yr): {resale}'), 0, 1)

        pdf.ln(3)

        # Pros
        if pros:
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 6, latin_safe('Strengths:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            for p in pros:
                pdf.cell(5, 5, '', 0, 0)
                pdf.cell(0, 5, latin_safe(f'+ {p}'), 0, 1)
            pdf.ln(2)

        # Cons
        if cons:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Weaknesses:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            for c in cons:
                pdf.cell(5, 5, '', 0, 0)
                pdf.cell(0, 5, latin_safe(f'- {c}'), 0, 1)
            pdf.ln(2)

        # Page break check
        if pdf.get_y() > 250 and idx < len(recommendations) - 1:
            pdf.add_page()

    # Themes section
    themes = data.get('themes', {})
    if themes:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(124, 58, 237)
        pdf.cell(0, 10, latin_safe('Segment Insights'), 0, 1)
        pdf.ln(5)

        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)

        if themes.get('segment_insight'):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Segment Insight:'), 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, latin_safe(themes['segment_insight']))
            pdf.ln(3)

        if themes.get('best_value'):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Best Value:'), 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, latin_safe(themes['best_value']))
            pdf.ln(3)

        if themes.get('quality_leader'):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Quality Leader:'), 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, latin_safe(themes['quality_leader']))
            pdf.ln(3)

        if themes.get('rising_star'):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Rising Star:'), 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, latin_safe(themes['rising_star']))

    pdf.output(output_path)


def generate_markdown(data, output_path):
    """Generate Markdown report from camper/RV recommendations data."""
    profile = data.get('requirements_profile', {})
    camper_type = profile.get('camper_type', 'Camper/RV')
    rv_type = profile.get('rv_type', '')
    budget = profile.get('budget_range', 'Not specified')
    tow_vehicle = profile.get('tow_vehicle', 'Not specified')
    depth = data.get('depth', 'standard').upper()
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    recommendations = data.get('recommendations', [])
    themes = data.get('themes', {})
    methodology = data.get('methodology', {})

    must_haves = ', '.join(profile.get('must_haves', []))
    priorities = ', '.join(profile.get('priorities', []))

    md = f"""# Camper/RV Recommendations

## {camper_type} — {budget}

**Generated:** {generated_date}
**Depth:** {depth}
**Campers Analyzed:** {data.get('campers_analyzed', 0)}
**Shortlist:** {data.get('shortlist_count', 0)}

---

## Your Requirements

- **RV Type:** {rv_type or camper_type}
- **Budget:** {budget} ({profile.get('buying_preference', '')})
- **Must-Haves:** {must_haves or 'None specified'}
- **Priorities:** {priorities or 'None specified'}
- **Tow Vehicle:** {tow_vehicle}

---

## Methodology

"""

    if methodology:
        md += f"""- **Agents Dispatched:** {methodology.get('agents_dispatched', 0)}
- **Total Searches:** {methodology.get('total_searches', 0)}
- **Sources Covered:** {', '.join(methodology.get('sources_covered', []))}
- **Depth:** {methodology.get('depth', 'standard')}

"""

    md += """---

## Recommendation Overview

| Rank | Camper | RV Type | Tier | Score | Fit | Market | Year | MSRP |
|------|--------|---------|------|-------|-----|--------|------|------|
"""

    for rec in recommendations:
        rank = rec.get('rank', 0)
        make_model = rec.get('make_model', 'Unknown')
        floorplan = rec.get('floorplan', '')
        name = f"{make_model} {floorplan}".strip()
        rv_type_rec = rec.get('rv_type', 'N/A')
        tier = rec.get('tier', 'CONSIDER')
        composite = rec.get('composite_score', 0)
        fit = rec.get('fit_score', 0)
        market = rec.get('market_score', 0)
        year = rec.get('year', 'N/A')
        msrp = rec.get('msrp_range', 'N/A')

        md += f"| {rank} | {name} | {rv_type_rec} | {tier} | {composite} | {fit} | {market} | {year} | {msrp} |\n"

    md += "\n---\n\n## Detailed Analysis\n\n"

    for rec in recommendations:
        rank = rec.get('rank', 0)
        make_model = rec.get('make_model', 'Unknown')
        floorplan = rec.get('floorplan', '')
        name = f"{make_model} {floorplan}".strip()
        rv_type_rec = rec.get('rv_type', 'N/A')
        tier = rec.get('tier', 'CONSIDER')
        composite = rec.get('composite_score', 0)
        fit = rec.get('fit_score', 0)
        market = rec.get('market_score', 0)
        year = rec.get('year', 'N/A')
        msrp = rec.get('msrp_range', 'N/A')
        build_quality = rec.get('build_quality_rating', 'N/A')
        length_ft = rec.get('length_ft', 'N/A')
        dry_weight = rec.get('dry_weight_lbs', 'N/A')
        gvwr = rec.get('gvwr_lbs', 'N/A')
        slides = rec.get('slides', 'N/A')
        sleeping_capacity = rec.get('sleeping_capacity', 'N/A')
        tco = rec.get('tco_5year', 'N/A')
        resale = rec.get('resale_3year', 'N/A')
        floorplan_rec = rec.get('best_floorplan_recommendation', '')
        pros = rec.get('pros', [])
        cons = rec.get('cons', [])
        sources = rec.get('key_sources', [])
        finder_prompt = rec.get('finder_prompt', '')
        tank_capacities = rec.get('tank_capacities', {})

        md += f"""### #{rank}. {name}

**Tier:** {tier} | **Score:** {composite} | **Fit:** {fit} | **Market:** {market}

**Details:**
- RV Type: {rv_type_rec}
- Year: {year}
- MSRP Range: {msrp}
- Build Quality: {build_quality}
- Sleeping Capacity: {sleeping_capacity}

**Weight & Dimensions:**
- Length: {length_ft} ft
- Dry Weight: {dry_weight} lbs
- GVWR: {gvwr} lbs
- Slides: {slides}

"""

        # Tank capacities
        if tank_capacities:
            fresh = tank_capacities.get('fresh_water', 'N/A')
            gray = tank_capacities.get('gray_water', 'N/A')
            black = tank_capacities.get('black_water', 'N/A')
            propane = tank_capacities.get('propane', 'N/A')
            md += f"""**Tank Capacities:**
- Fresh Water: {fresh}
- Gray Water: {gray}
- Black Water: {black}
- Propane: {propane}

"""

        if tco != 'N/A' or resale != 'N/A':
            md += f"""**Cost of Ownership:**
- TCO (5yr): {tco}
- Resale (3yr): {resale}

"""

        if floorplan_rec:
            md += f"**Best Floorplan:** {floorplan_rec}\n\n"

        if pros:
            md += "**Strengths:**\n"
            for p in pros:
                md += f"- {p}\n"
            md += "\n"

        if cons:
            md += "**Weaknesses:**\n"
            for c in cons:
                md += f"- {c}\n"
            md += "\n"

        if sources:
            md += f"**Sources:** {', '.join(sources)}\n\n"

        if finder_prompt:
            md += f"""**Finder Prompt:**

```
{finder_prompt}
```

"""

        md += "---\n\n"

    if themes:
        md += "## Segment Insights\n\n"

        if themes.get('segment_insight'):
            md += f"**Segment Insight:**  \n{themes['segment_insight']}\n\n"

        if themes.get('best_value'):
            md += f"**Best Value:**  \n{themes['best_value']}\n\n"

        if themes.get('quality_leader'):
            md += f"**Quality Leader:**  \n{themes['quality_leader']}\n\n"

        if themes.get('rising_star'):
            md += f"**Rising Star:**  \n{themes['rising_star']}\n\n"

    md += f"""---

*Generated by Camper Recommender on {generated_date}*
*ROK Plugin Marketplace - Camper Recommender v1.0*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)


def main():
    parser = argparse.ArgumentParser(description='Export Camper/RV Recommendations to HTML, PDF, and Markdown')
    parser.add_argument('--input', required=True, help='Path to recommendations JSON file')
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
    if data.get('type') != 'camper_recommendations':
        print(f"Warning: Expected type 'camper_recommendations', got '{data.get('type')}'", file=sys.stderr)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate filename base
    profile = data.get('requirements_profile', {})
    type_text = profile.get('camper_type', 'general')
    type_slug = slugify(type_text)
    date_str = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    base_filename = f"camper_recs_{type_slug}_{date_str}"

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
