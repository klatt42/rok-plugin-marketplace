#!/usr/bin/env python3
"""
Medigap Selector - Export Script
Generates HTML, PDF, and Markdown files from medigap selection JSON.

Usage:
    python3 medigap_selector_export.py --input /tmp/medigap_selection.json
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

# Color scheme (green-based for healthcare)
GREEN = "#059669"
GREEN_DARK = "#047857"
GREEN_LIGHT = "#ecfdf5"

PLAN_COLORS = {
    "Plan G": {"bg": "#059669", "text": "#FFFFFF"},
    "Plan N": {"bg": "#2563EB", "text": "#FFFFFF"}
}

CONFIDENCE_COLORS = {
    "HIGH": {"bg": "#059669", "text": "#FFFFFF"},
    "MEDIUM": {"bg": "#D97706", "text": "#FFFFFF"},
    "LOW": {"bg": "#DC2626", "text": "#FFFFFF"}
}

DEFAULT_OUTPUT_DIR = "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Medigap_Selection/"


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
        return "#059669"
    elif score >= 70:
        return "#2563EB"
    elif score >= 55:
        return "#D97706"
    else:
        return "#DC2626"


def generate_html(data, output_path):
    """Generate HTML report from medigap selection data."""
    profile = data.get('requirements_profile', {})
    recommendation = data.get('recommendation', {})
    scoring = data.get('scoring_detail', {})
    premium_comp = data.get('premium_comparison', {})
    insurer_rankings = data.get('insurer_rankings', {})
    break_even = data.get('break_even_analysis', {})
    scenarios = data.get('scenario_summary', [])
    state_rules = data.get('state_rules_impact', {})
    advice = data.get('strategic_advice', [])
    disclaimers = data.get('disclaimers', [])
    methodology = data.get('methodology', {})
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))

    state = profile.get('state', 'N/A')
    zip_code = profile.get('zip_code', 'N/A')
    age = profile.get('age', 'N/A')
    usage = profile.get('medical_usage', 'N/A')
    winner = recommendation.get('winner', 'N/A')
    g_score = recommendation.get('plan_g_score', 0)
    n_score = recommendation.get('plan_n_score', 0)
    confidence = recommendation.get('confidence', 'N/A')
    summary = recommendation.get('one_line_summary', '')

    priorities = ', '.join(profile.get('priorities', []))

    winner_color = PLAN_COLORS.get(winner, PLAN_COLORS['Plan G'])
    conf_color = CONFIDENCE_COLORS.get(confidence, CONFIDENCE_COLORS['MEDIUM'])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medigap Plan Selection - {state} ({zip_code})</title>
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
            background: linear-gradient(135deg, {GREEN_LIGHT} 0%, #ffffff 100%);
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
            background: linear-gradient(135deg, {GREEN} 0%, {GREEN_DARK} 100%);
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
            color: {GREEN_DARK};
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid {GREEN};
        }}

        .recommendation-box {{
            background: {GREEN_LIGHT};
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border-left: 6px solid {GREEN};
        }}

        .recommendation-box h3 {{
            color: {GREEN_DARK};
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }}

        .winner-badge {{
            display: inline-block;
            padding: 0.5rem 1.2rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }}

        .confidence-badge {{
            display: inline-block;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9rem;
        }}

        .summary-text {{
            font-size: 1.1rem;
            color: #374151;
            font-style: italic;
            margin-top: 1rem;
            padding: 1rem;
            background: white;
            border-radius: 8px;
        }}

        .profile-box {{
            background: #f0fdf4;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border-left: 4px solid {GREEN};
        }}

        .profile-box h3 {{
            color: {GREEN_DARK};
            margin-bottom: 0.8rem;
        }}

        .profile-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}

        .profile-item {{
            font-size: 0.95rem;
        }}

        .profile-label {{
            font-weight: 600;
            color: #374151;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 2rem;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        th {{
            background: {GREEN};
            color: white;
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 1rem;
            border-bottom: 1px solid #e5e7eb;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover {{
            background: #f0fdf4;
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
        }}

        .break-even-box {{
            background: #fffbeb;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #D97706;
            margin-bottom: 2rem;
        }}

        .break-even-box h3 {{
            color: #92400e;
            margin-bottom: 0.8rem;
        }}

        .break-even-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}

        .be-item {{
            font-size: 0.95rem;
        }}

        .be-label {{
            font-weight: 600;
            color: #92400e;
        }}

        .state-rules-box {{
            background: #eff6ff;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #2563EB;
            margin-bottom: 2rem;
        }}

        .state-rules-box h3 {{
            color: #1e40af;
            margin-bottom: 0.8rem;
        }}

        .advice-list {{
            list-style: none;
            padding: 0;
        }}

        .advice-list li {{
            padding: 0.8rem 1rem;
            margin-bottom: 0.5rem;
            background: #f0fdf4;
            border-radius: 8px;
            border-left: 3px solid {GREEN};
        }}

        .advice-list li::before {{
            content: "\\2713  ";
            color: {GREEN};
            font-weight: 700;
        }}

        .insurer-card {{
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .insurer-card:hover {{
            border-color: {GREEN};
            box-shadow: 0 4px 12px rgba(5,150,105,0.15);
        }}

        .insurer-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .insurer-name {{
            font-size: 1.3rem;
            font-weight: 700;
            color: {GREEN_DARK};
        }}

        .insurer-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }}

        .insurer-detail {{
            background: #f9fafb;
            padding: 0.8rem;
            border-radius: 6px;
        }}

        .insurer-detail-label {{
            font-size: 0.8rem;
            color: #6b7280;
            text-transform: uppercase;
        }}

        .insurer-detail-value {{
            font-size: 1rem;
            font-weight: 600;
            color: #1f2937;
        }}

        .disclaimer {{
            background: #fef2f2;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #DC2626;
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #991b1b;
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
            <h1>Medigap Plan Selection</h1>
            <div class="subtitle">{state} ({zip_code}) &mdash; Plan G vs Plan N</div>
            <div class="meta">
                <div class="meta-item">
                    <div class="meta-label">Generated</div>
                    <div class="meta-value">{generated_date}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Age</div>
                    <div class="meta-value">{age}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Usage</div>
                    <div class="meta-value">{usage.title()}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Confidence</div>
                    <div class="meta-value">{confidence}</div>
                </div>
            </div>
        </div>

        <div class="content">
            <!-- Recommendation -->
            <div class="section">
                <div class="recommendation-box">
                    <h3>Recommendation</h3>
                    <div>
                        <span class="winner-badge" style="background: {winner_color['bg']}; color: {winner_color['text']};">
                            {winner}
                        </span>
                        <span class="confidence-badge" style="background: {conf_color['bg']}; color: {conf_color['text']};">
                            {confidence} Confidence
                        </span>
                    </div>
                    <div class="summary-text">{summary}</div>
                </div>
            </div>

            <!-- Profile -->
            <div class="section">
                <div class="profile-box">
                    <h3>Your Profile</h3>
                    <div class="profile-grid">
                        <div class="profile-item">
                            <div class="profile-label">Location</div>
                            <div>{state} ({zip_code})</div>
                        </div>
                        <div class="profile-item">
                            <div class="profile-label">Age</div>
                            <div>{age} &mdash; {profile.get('enrollment_status', 'N/A')}</div>
                        </div>
                        <div class="profile-item">
                            <div class="profile-label">Medical Usage</div>
                            <div>{usage} (~{profile.get('estimated_annual_visits', 'N/A')} visits/year)</div>
                        </div>
                        <div class="profile-item">
                            <div class="profile-label">Priorities</div>
                            <div>{priorities or 'None specified'}</div>
                        </div>
                        <div class="profile-item">
                            <div class="profile-label">Provider Assignment</div>
                            <div>{profile.get('provider_assignment', 'N/A')}</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Scoring Comparison -->
            <div class="section">
                <h2 class="section-title">Scoring Comparison</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Factor (Weight)</th>
                            <th style="width: 200px;">Plan G</th>
                            <th style="width: 200px;">Plan N</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # Scoring factors
    factors = [
        ('Cost Efficiency', '30%', 'cost_efficiency'),
        ('Risk Protection', '25%', 'risk_protection'),
        ('Flexibility', '20%', 'flexibility'),
        ('Priority Alignment', '15%', 'priority_alignment'),
        ('Insurer Quality', '10%', 'insurer_quality')
    ]

    plan_g_scoring = scoring.get('plan_g', {})
    plan_n_scoring = scoring.get('plan_n', {})

    for label, weight, key in factors:
        g_data = plan_g_scoring.get(key, {})
        n_data = plan_n_scoring.get(key, {})
        g_val = g_data.get('score', 0) if isinstance(g_data, dict) else 0
        n_val = n_data.get('score', 0) if isinstance(n_data, dict) else 0

        html += f"""
                        <tr>
                            <td><strong>{label}</strong> ({weight})</td>
                            <td>
                                <div class="score" style="color: {score_color(g_val)};">{g_val}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {g_val}%; background: {score_color(g_val)};"></div>
                                </div>
                            </td>
                            <td>
                                <div class="score" style="color: {score_color(n_val)};">{n_val}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {n_val}%; background: {score_color(n_val)};"></div>
                                </div>
                            </td>
                        </tr>
"""

    html += f"""
                        <tr style="background: #f0fdf4; font-weight: 700;">
                            <td><strong>Composite Score</strong></td>
                            <td>
                                <div class="score" style="color: {score_color(g_score)}; font-size: 1.4rem;">{g_score}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {g_score}%; background: {score_color(g_score)};"></div>
                                </div>
                            </td>
                            <td>
                                <div class="score" style="color: {score_color(n_score)}; font-size: 1.4rem;">{n_score}</div>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {n_score}%; background: {score_color(n_score)};"></div>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Premium Comparison -->
            <div class="section">
                <h2 class="section-title">Premium Comparison</h2>
"""

    # Build premium table from insurer rankings
    winning_plan = recommendation.get('winner', 'Plan G')
    plan_key = 'plan_g' if 'G' in winning_plan else 'plan_n'

    g_insurers = insurer_rankings.get('plan_g', [])
    n_insurers = insurer_rankings.get('plan_n', [])

    if g_insurers or n_insurers:
        html += """
                <table>
                    <thead>
                        <tr>
                            <th>Insurer</th>
                            <th>Plan G</th>
                            <th>Plan N</th>
                            <th>Spread</th>
                            <th>AM Best</th>
                            <th>NAIC</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        # Match insurers across plans
        g_by_name = {i.get('insurer', ''): i for i in g_insurers}
        n_by_name = {i.get('insurer', ''): i for i in n_insurers}
        all_insurers = list(dict.fromkeys(list(g_by_name.keys()) + list(n_by_name.keys())))

        for insurer_name in all_insurers:
            g_data = g_by_name.get(insurer_name, {})
            n_data = n_by_name.get(insurer_name, {})
            g_premium = g_data.get('monthly_premium', 'N/A')
            n_premium = n_data.get('monthly_premium', 'N/A')
            am_best = g_data.get('am_best', n_data.get('am_best', 'N/A'))
            naic = g_data.get('naic_ratio', n_data.get('naic_ratio', 'N/A'))

            # Calculate spread
            spread = 'N/A'
            try:
                g_val = float(re.sub(r'[^\d.]', '', str(g_premium)))
                n_val = float(re.sub(r'[^\d.]', '', str(n_premium)))
                spread = f"${g_val - n_val:.0f}"
            except (ValueError, TypeError):
                pass

            html += f"""
                        <tr>
                            <td><strong>{insurer_name}</strong></td>
                            <td>{g_premium}</td>
                            <td>{n_premium}</td>
                            <td>{spread}</td>
                            <td>{am_best}</td>
                            <td>{naic}</td>
                        </tr>
"""

        html += """
                    </tbody>
                </table>
"""

    html += f"""
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px;">
                        <div style="font-weight: 600; color: {GREEN_DARK};">Plan G Range</div>
                        <div>{premium_comp.get('plan_g_range', 'N/A')}</div>
                    </div>
                    <div style="background: #eff6ff; padding: 1rem; border-radius: 8px;">
                        <div style="font-weight: 600; color: #1e40af;">Plan N Range</div>
                        <div>{premium_comp.get('plan_n_range', 'N/A')}</div>
                    </div>
                </div>
            </div>

            <!-- Break-Even Analysis -->
            <div class="section">
                <h2 class="section-title">Break-Even Analysis</h2>
                <div class="break-even-box">
                    <h3>Key Numbers</h3>
                    <div class="break-even-grid">
                        <div class="be-item">
                            <div class="be-label">Monthly Premium Spread</div>
                            <div>{break_even.get('monthly_premium_spread', 'N/A')}</div>
                        </div>
                        <div class="be-item">
                            <div class="be-label">Visits to Break Even</div>
                            <div>{break_even.get('visits_to_break_even', 'N/A')}/year</div>
                        </div>
                        <div class="be-item">
                            <div class="be-label">Your Estimated Visits</div>
                            <div>{break_even.get('user_estimated_visits', 'N/A')}/year</div>
                        </div>
                        <div class="be-item">
                            <div class="be-label">Excess Charge Risk</div>
                            <div>{break_even.get('excess_charge_risk_level', 'N/A').title()}</div>
                        </div>
                    </div>
                    <p style="margin-top: 1rem; color: #92400e;">{break_even.get('bottom_line', '')}</p>
                </div>
            </div>

            <!-- Scenario Comparison -->
            <div class="section">
                <h2 class="section-title">Scenario Comparison</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Scenario</th>
                            <th>Plan G</th>
                            <th>Plan N</th>
                            <th>Winner</th>
                            <th>Savings</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    for scenario in scenarios:
        s_winner = scenario.get('winner', '')
        s_savings = scenario.get('savings', '')
        winner_style = f"color: {GREEN}; font-weight: 700;" if 'G' in s_winner else "color: #2563EB; font-weight: 700;"

        html += f"""
                        <tr>
                            <td><strong>{scenario.get('scenario', '')}</strong></td>
                            <td>{scenario.get('plan_g_cost', '')}</td>
                            <td>{scenario.get('plan_n_cost', '')}</td>
                            <td style="{winner_style}">{s_winner}</td>
                            <td>{s_savings}</td>
                        </tr>
"""

    html += f"""
                    </tbody>
                </table>
            </div>

            <!-- State Rules -->
            <div class="section">
                <h2 class="section-title">State Rules: {state}</h2>
                <div class="state-rules-box">
                    <h3>{'Birthday Rule Available' if state_rules.get('birthday_rule') else 'No Birthday Rule'}</h3>
                    <p style="margin-bottom: 1rem;"><strong>Strategic Value:</strong> {state_rules.get('strategic_value', 'N/A')}</p>
                    <p>{state_rules.get('switching_recommendation', '')}</p>
                </div>
            </div>
"""

    # Top Insurer Recommendations
    winner_key = 'plan_g' if 'G' in winner else 'plan_n'
    top_insurers = insurer_rankings.get(winner_key, [])

    if top_insurers:
        html += """
            <div class="section">
                <h2 class="section-title">Top Insurer Recommendations</h2>
"""
        for ins in top_insurers[:3]:
            html += f"""
                <div class="insurer-card">
                    <div class="insurer-header">
                        <div class="insurer-name">#{ins.get('rank', '')}. {ins.get('insurer', '')}</div>
                        <div style="font-size: 1.3rem; font-weight: 700; color: {GREEN};">{ins.get('monthly_premium', '')}/mo</div>
                    </div>
                    <div class="insurer-grid">
                        <div class="insurer-detail">
                            <div class="insurer-detail-label">AM Best</div>
                            <div class="insurer-detail-value">{ins.get('am_best', 'N/A')}</div>
                        </div>
                        <div class="insurer-detail">
                            <div class="insurer-detail-label">NAIC Ratio</div>
                            <div class="insurer-detail-value">{ins.get('naic_ratio', 'N/A')}</div>
                        </div>
                        <div class="insurer-detail">
                            <div class="insurer-detail-label">Avg Increase</div>
                            <div class="insurer-detail-value">{ins.get('avg_annual_increase', 'N/A')}</div>
                        </div>
                        <div class="insurer-detail">
                            <div class="insurer-detail-label">Rating Method</div>
                            <div class="insurer-detail-value">{ins.get('rating_method', 'N/A')}</div>
                        </div>
                        <div class="insurer-detail">
                            <div class="insurer-detail-label">Household Discount</div>
                            <div class="insurer-detail-value">{ins.get('household_discount', 'N/A')}</div>
                        </div>
                    </div>
                    <p style="margin-top: 1rem; color: #374151;">{ins.get('why_recommended', '')}</p>
                </div>
"""
        html += """
            </div>
"""

    # Strategic Advice
    if advice:
        html += """
            <div class="section">
                <h2 class="section-title">Strategic Advice</h2>
                <ul class="advice-list">
"""
        for item in advice:
            html += f"                    <li>{item}</li>\n"
        html += """
                </ul>
            </div>
"""

    # Methodology
    if methodology:
        html += f"""
            <div class="methodology">
                <h3 style="margin-bottom: 1rem; color: #1f2937;">Methodology</h3>
                <div class="methodology-grid">
                    <div class="insurer-detail">
                        <div class="insurer-detail-label">Agents Dispatched</div>
                        <div class="insurer-detail-value">{methodology.get('agents_dispatched', 0)}</div>
                    </div>
                    <div class="insurer-detail">
                        <div class="insurer-detail-label">Total Searches</div>
                        <div class="insurer-detail-value">{methodology.get('total_searches', 0)}</div>
                    </div>
                    <div class="insurer-detail">
                        <div class="insurer-detail-label">Scoring System</div>
                        <div class="insurer-detail-value">{methodology.get('scoring_system', '')}</div>
                    </div>
                </div>
            </div>
"""

    # Disclaimers
    if disclaimers:
        html += """
            <div class="disclaimer">
                <h4 style="margin-bottom: 0.5rem;">Important Disclaimers</h4>
                <ul style="padding-left: 1.5rem;">
"""
        for d in disclaimers:
            html += f"                    <li>{d}</li>\n"
        html += """
                </ul>
            </div>
"""

    html += f"""
            <div class="footer">
                Generated by Medigap Selector on {generated_date}<br>
                ROK Plugin Marketplace - Medigap Selector v1.0
            </div>
        </div>
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_pdf(data, output_path):
    """Generate PDF report from medigap selection data."""
    profile = data.get('requirements_profile', {})
    recommendation = data.get('recommendation', {})
    scoring = data.get('scoring_detail', {})
    break_even = data.get('break_even_analysis', {})
    scenarios = data.get('scenario_summary', [])
    state_rules = data.get('state_rules_impact', {})
    advice = data.get('strategic_advice', [])
    insurer_rankings = data.get('insurer_rankings', {})
    disclaimers = data.get('disclaimers', [])
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))

    state = profile.get('state', 'N/A')
    zip_code = profile.get('zip_code', 'N/A')
    winner = recommendation.get('winner', 'N/A')
    g_score = recommendation.get('plan_g_score', 0)
    n_score = recommendation.get('plan_n_score', 0)
    confidence = recommendation.get('confidence', 'N/A')
    summary = recommendation.get('one_line_summary', '')

    class MedigapPDF(FPDF):
        def header(self):
            self.set_fill_color(5, 150, 105)  # GREEN
            self.rect(0, 0, 210, 40, 'F')
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 20)
            self.cell(0, 15, '', 0, 1)
            self.cell(0, 10, latin_safe('Medigap Plan Selection'), 0, 1, 'C')
            self.set_font('Arial', '', 12)
            self.cell(0, 8, latin_safe(f'{state} ({zip_code}) - Plan G vs Plan N'), 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = MedigapPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Recommendation
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(4, 120, 87)
    pdf.cell(0, 10, latin_safe('Recommendation'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, latin_safe(f'{winner} (Score: {g_score if "G" in winner else n_score}) - {confidence} Confidence'), 0, 1)

    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 6, latin_safe(summary))
    pdf.ln(5)

    # Profile
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(4, 120, 87)
    pdf.cell(0, 10, latin_safe('Your Profile'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(90, 7, latin_safe(f'Location: {state} ({zip_code})'), 0, 0)
    pdf.cell(90, 7, latin_safe(f'Age: {profile.get("age", "N/A")}'), 0, 1)
    pdf.cell(90, 7, latin_safe(f'Usage: {profile.get("medical_usage", "N/A")}'), 0, 0)
    pdf.cell(90, 7, latin_safe(f'Visits: ~{profile.get("estimated_annual_visits", "N/A")}/year'), 0, 1)
    priorities = ', '.join(profile.get('priorities', []))
    pdf.cell(0, 7, latin_safe(f'Priorities: {priorities}'), 0, 1)
    pdf.cell(0, 7, latin_safe(f'Provider Assignment: {profile.get("provider_assignment", "N/A")}'), 0, 1)
    pdf.ln(5)

    # Scoring
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(4, 120, 87)
    pdf.cell(0, 10, latin_safe('Scoring Comparison'), 0, 1)
    pdf.ln(2)

    # Scoring table header
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(5, 150, 105)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(70, 8, 'Factor (Weight)', 1, 0, 'C', True)
    pdf.cell(55, 8, 'Plan G', 1, 0, 'C', True)
    pdf.cell(55, 8, 'Plan N', 1, 1, 'C', True)

    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(0, 0, 0)

    plan_g_scoring = scoring.get('plan_g', {})
    plan_n_scoring = scoring.get('plan_n', {})

    factors = [
        ('Cost Efficiency (30%)', 'cost_efficiency'),
        ('Risk Protection (25%)', 'risk_protection'),
        ('Flexibility (20%)', 'flexibility'),
        ('Priority Alignment (15%)', 'priority_alignment'),
        ('Insurer Quality (10%)', 'insurer_quality')
    ]

    for label, key in factors:
        g_data = plan_g_scoring.get(key, {})
        n_data = plan_n_scoring.get(key, {})
        g_val = g_data.get('score', 0) if isinstance(g_data, dict) else 0
        n_val = n_data.get('score', 0) if isinstance(n_data, dict) else 0
        pdf.cell(70, 8, latin_safe(label), 1, 0)
        pdf.cell(55, 8, str(g_val), 1, 0, 'C')
        pdf.cell(55, 8, str(n_val), 1, 1, 'C')

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(70, 8, 'COMPOSITE', 1, 0, 'C')
    pdf.cell(55, 8, str(g_score), 1, 0, 'C')
    pdf.cell(55, 8, str(n_score), 1, 1, 'C')
    pdf.ln(5)

    # Scenario comparison
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(4, 120, 87)
    pdf.cell(0, 10, latin_safe('Scenario Comparison'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(5, 150, 105)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(40, 8, 'Scenario', 1, 0, 'C', True)
    pdf.cell(35, 8, 'Plan G', 1, 0, 'C', True)
    pdf.cell(35, 8, 'Plan N', 1, 0, 'C', True)
    pdf.cell(30, 8, 'Winner', 1, 0, 'C', True)
    pdf.cell(30, 8, 'Savings', 1, 1, 'C', True)

    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(0, 0, 0)

    for scenario in scenarios:
        pdf.cell(40, 8, latin_safe(scenario.get('scenario', '')), 1, 0)
        pdf.cell(35, 8, latin_safe(str(scenario.get('plan_g_cost', ''))), 1, 0, 'C')
        pdf.cell(35, 8, latin_safe(str(scenario.get('plan_n_cost', ''))), 1, 0, 'C')
        pdf.cell(30, 8, latin_safe(str(scenario.get('winner', ''))), 1, 0, 'C')
        pdf.cell(30, 8, latin_safe(str(scenario.get('savings', ''))), 1, 1, 'C')

    pdf.ln(5)

    # Break-even
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(4, 120, 87)
    pdf.cell(0, 10, latin_safe('Break-Even Analysis'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(90, 7, latin_safe(f'Premium Spread: {break_even.get("monthly_premium_spread", "N/A")}/month'), 0, 0)
    pdf.cell(90, 7, latin_safe(f'Break-Even: {break_even.get("visits_to_break_even", "N/A")} visits/year'), 0, 1)
    pdf.cell(90, 7, latin_safe(f'Your Visits: {break_even.get("user_estimated_visits", "N/A")}/year'), 0, 0)
    pdf.cell(90, 7, latin_safe(f'Excess Charge Risk: {break_even.get("excess_charge_risk_level", "N/A")}'), 0, 1)
    pdf.ln(3)
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 5, latin_safe(break_even.get('bottom_line', '')))
    pdf.ln(5)

    # State Rules
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(4, 120, 87)
    pdf.cell(0, 10, latin_safe(f'State Rules: {state}'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0, 0, 0)
    birthday = 'YES' if state_rules.get('birthday_rule') else 'NO'
    pdf.cell(0, 7, latin_safe(f'Birthday Rule: {birthday}'), 0, 1)
    pdf.cell(0, 7, latin_safe(f'Strategic Value: {state_rules.get("strategic_value", "N/A")}'), 0, 1)
    pdf.ln(2)
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 5, latin_safe(state_rules.get('switching_recommendation', '')))
    pdf.ln(5)

    # Strategic Advice
    if advice:
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(4, 120, 87)
        pdf.cell(0, 10, latin_safe('Strategic Advice'), 0, 1)
        pdf.ln(2)

        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        for i, item in enumerate(advice, 1):
            pdf.cell(5, 6, '', 0, 0)
            pdf.multi_cell(0, 6, latin_safe(f'{i}. {item}'))
            pdf.ln(1)
        pdf.ln(5)

    # Top Insurer Recommendations
    winner_key = 'plan_g' if 'G' in winner else 'plan_n'
    top_insurers = insurer_rankings.get(winner_key, [])

    if top_insurers:
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(4, 120, 87)
        pdf.cell(0, 10, latin_safe('Top Insurer Recommendations'), 0, 1)
        pdf.ln(2)

        for ins in top_insurers[:3]:
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(4, 120, 87)
            pdf.cell(0, 8, latin_safe(f'#{ins.get("rank", "")}. {ins.get("insurer", "")} - {ins.get("monthly_premium", "")}/month'), 0, 1)

            pdf.set_font('Arial', '', 9)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(45, 6, latin_safe(f'AM Best: {ins.get("am_best", "N/A")}'), 0, 0)
            pdf.cell(45, 6, latin_safe(f'NAIC: {ins.get("naic_ratio", "N/A")}'), 0, 0)
            pdf.cell(45, 6, latin_safe(f'Avg Increase: {ins.get("avg_annual_increase", "N/A")}'), 0, 0)
            pdf.cell(45, 6, latin_safe(f'Method: {ins.get("rating_method", "N/A")}'), 0, 1)

            why = ins.get('why_recommended', '')
            if why:
                pdf.set_font('Arial', 'I', 9)
                pdf.multi_cell(0, 5, latin_safe(why))
            pdf.ln(3)

    # Disclaimers
    if disclaimers:
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(180, 0, 0)
        pdf.cell(0, 8, latin_safe('Important Disclaimers'), 0, 1)
        pdf.set_font('Arial', '', 8)
        pdf.set_text_color(100, 0, 0)
        for d in disclaimers:
            pdf.multi_cell(0, 5, latin_safe(f'- {d}'))
            pdf.ln(1)

    pdf.output(output_path)


def generate_markdown(data, output_path):
    """Generate Markdown report from medigap selection data."""
    profile = data.get('requirements_profile', {})
    recommendation = data.get('recommendation', {})
    scoring = data.get('scoring_detail', {})
    premium_comp = data.get('premium_comparison', {})
    insurer_rankings = data.get('insurer_rankings', {})
    break_even = data.get('break_even_analysis', {})
    scenarios = data.get('scenario_summary', [])
    state_rules = data.get('state_rules_impact', {})
    advice = data.get('strategic_advice', [])
    disclaimers = data.get('disclaimers', [])
    methodology = data.get('methodology', {})
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))

    state = profile.get('state', 'N/A')
    zip_code = profile.get('zip_code', 'N/A')
    winner = recommendation.get('winner', 'N/A')
    g_score = recommendation.get('plan_g_score', 0)
    n_score = recommendation.get('plan_n_score', 0)
    confidence = recommendation.get('confidence', 'N/A')
    summary = recommendation.get('one_line_summary', '')
    priorities = ', '.join(profile.get('priorities', []))

    md = f"""# Medigap Plan Selection

## {state} ({zip_code}) — Plan G vs Plan N

**Generated:** {generated_date}
**Recommendation:** {winner} (Score: {g_score if 'G' in winner else n_score}/100)
**Confidence:** {confidence}

> {summary}

---

## Your Profile

- **Location:** {state} ({zip_code})
- **Age:** {profile.get('age', 'N/A')} — {profile.get('enrollment_status', 'N/A')}
- **Medical Usage:** {profile.get('medical_usage', 'N/A')} (~{profile.get('estimated_annual_visits', 'N/A')} visits/year)
- **Priorities:** {priorities or 'None specified'}
- **Provider Assignment:** {profile.get('provider_assignment', 'N/A')}

---

## Scoring Comparison

| Factor (Weight) | Plan G | Plan N |
|-----------------|--------|--------|
"""

    plan_g_scoring = scoring.get('plan_g', {})
    plan_n_scoring = scoring.get('plan_n', {})

    factors = [
        ('Cost Efficiency (30%)', 'cost_efficiency'),
        ('Risk Protection (25%)', 'risk_protection'),
        ('Flexibility (20%)', 'flexibility'),
        ('Priority Alignment (15%)', 'priority_alignment'),
        ('Insurer Quality (10%)', 'insurer_quality')
    ]

    for label, key in factors:
        g_data = plan_g_scoring.get(key, {})
        n_data = plan_n_scoring.get(key, {})
        g_val = g_data.get('score', 0) if isinstance(g_data, dict) else 0
        n_val = n_data.get('score', 0) if isinstance(n_data, dict) else 0
        md += f"| {label} | {g_val} | {n_val} |\n"

    md += f"| **Composite** | **{g_score}** | **{n_score}** |\n"

    md += f"""
---

## Premium Comparison

- **Plan G Range:** {premium_comp.get('plan_g_range', 'N/A')}
- **Plan N Range:** {premium_comp.get('plan_n_range', 'N/A')}
- **Average Spread:** {premium_comp.get('avg_monthly_spread', 'N/A')}/month

"""

    # Insurer table
    g_insurers = insurer_rankings.get('plan_g', [])
    n_insurers = insurer_rankings.get('plan_n', [])

    if g_insurers or n_insurers:
        g_by_name = {i.get('insurer', ''): i for i in g_insurers}
        n_by_name = {i.get('insurer', ''): i for i in n_insurers}
        all_insurers = list(dict.fromkeys(list(g_by_name.keys()) + list(n_by_name.keys())))

        md += "| Insurer | Plan G | Plan N | AM Best | NAIC |\n"
        md += "|---------|--------|--------|---------|------|\n"

        for name in all_insurers:
            g_data = g_by_name.get(name, {})
            n_data = n_by_name.get(name, {})
            md += f"| {name} | {g_data.get('monthly_premium', 'N/A')} | {n_data.get('monthly_premium', 'N/A')} | {g_data.get('am_best', n_data.get('am_best', 'N/A'))} | {g_data.get('naic_ratio', n_data.get('naic_ratio', 'N/A'))} |\n"

    md += f"""
---

## Break-Even Analysis

- **Monthly Premium Spread:** {break_even.get('monthly_premium_spread', 'N/A')}
- **Visits to Break Even:** {break_even.get('visits_to_break_even', 'N/A')}/year
- **Your Estimated Visits:** {break_even.get('user_estimated_visits', 'N/A')}/year
- **Excess Charge Risk:** {break_even.get('excess_charge_risk_level', 'N/A')}

> {break_even.get('bottom_line', '')}

---

## Scenario Comparison

| Scenario | Plan G | Plan N | Winner | Savings |
|----------|--------|--------|--------|---------|
"""

    for s in scenarios:
        md += f"| {s.get('scenario', '')} | {s.get('plan_g_cost', '')} | {s.get('plan_n_cost', '')} | {s.get('winner', '')} | {s.get('savings', '')} |\n"

    birthday = 'YES' if state_rules.get('birthday_rule') else 'NO'
    md += f"""
---

## State Rules: {state}

- **Birthday Rule:** {birthday}
- **Strategic Value:** {state_rules.get('strategic_value', 'N/A')}
- **Switching Recommendation:** {state_rules.get('switching_recommendation', '')}

---

## Strategic Advice

"""

    for i, item in enumerate(advice, 1):
        md += f"{i}. {item}\n"

    # Top Insurers
    winner_key = 'plan_g' if 'G' in winner else 'plan_n'
    top_insurers = insurer_rankings.get(winner_key, [])

    if top_insurers:
        md += "\n---\n\n## Top Insurer Recommendations\n\n"
        for ins in top_insurers[:3]:
            md += f"### #{ins.get('rank', '')}. {ins.get('insurer', '')} — {ins.get('monthly_premium', '')}/month\n\n"
            md += f"- AM Best: {ins.get('am_best', 'N/A')} | NAIC: {ins.get('naic_ratio', 'N/A')} | Avg Increase: {ins.get('avg_annual_increase', 'N/A')}\n"
            md += f"- Rating Method: {ins.get('rating_method', 'N/A')} | Household Discount: {ins.get('household_discount', 'N/A')}\n"
            why = ins.get('why_recommended', '')
            if why:
                md += f"- {why}\n"
            md += "\n"

    # Methodology
    if methodology:
        md += f"""---

## Methodology

- **Agents Dispatched:** {methodology.get('agents_dispatched', 0)}
- **Total Searches:** {methodology.get('total_searches', 0)}
- **Scoring System:** {methodology.get('scoring_system', '')}
- **Sources:** {', '.join(methodology.get('sources_covered', []))}

"""

    # Disclaimers
    if disclaimers:
        md += "---\n\n## Disclaimers\n\n"
        for d in disclaimers:
            md += f"- {d}\n"

    md += f"""
---

*Generated by Medigap Selector on {generated_date}*
*ROK Plugin Marketplace - Medigap Selector v1.0*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)


def main():
    parser = argparse.ArgumentParser(description='Export Medigap Selection to HTML, PDF, and Markdown')
    parser.add_argument('--input', required=True, help='Path to medigap selection JSON file')
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
    if data.get('type') != 'medigap_selection':
        print(f"Warning: Expected type 'medigap_selection', got '{data.get('type')}'", file=sys.stderr)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate filename base
    profile = data.get('requirements_profile', {})
    state = profile.get('state', 'unknown')
    zip_code = profile.get('zip_code', '00000')
    date_str = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    base_filename = f"medigap_selection_{state}_{zip_code}_{date_str}"

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
