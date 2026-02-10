#!/usr/bin/env python3
"""
Vehicle Finder - Export Script
Generates HTML, PDF, and Markdown files from vehicle inventory search results.

Usage:
    python3 vehicle_finder_export.py --input inventory.json
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

# Color scheme (green-based)
GREEN = "#059669"
GREEN_DARK = "#047857"

DEAL_COLORS = {
    "GREAT_DEAL": {"bg": "#059669", "text": "#FFFFFF"},
    "GOOD_DEAL": {"bg": "#2563EB", "text": "#FFFFFF"},
    "FAIR_PRICE": {"bg": "#D97706", "text": "#FFFFFF"},
    "OVERPRICED": {"bg": "#DC2626", "text": "#FFFFFF"}
}

# Default output directory
DEFAULT_OUTPUT_DIR = "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/Claude Code Plugin Output/Vehicle_Inventory/"


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


def format_price_diff(diff):
    """Format price difference with +/- prefix."""
    if diff is None:
        return "N/A"
    if diff < 0:
        return f"-${abs(diff):,.0f}"
    elif diff > 0:
        return f"+${diff:,.0f}"
    else:
        return "$0"


def generate_html(data, output_path):
    """Generate HTML report from inventory search data."""
    search_params = data.get('search_params', {})
    market_context = data.get('market_context', {})
    listings = data.get('listings', [])
    methodology = data.get('methodology', {})
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))

    year = search_params.get('year', '')
    make = search_params.get('make', 'Vehicle')
    model = search_params.get('model', '')
    condition = search_params.get('condition', 'New')
    trims = ', '.join(search_params.get('trims', []))
    max_price = search_params.get('max_price', 'N/A')
    radius = search_params.get('radius_miles', 'N/A')
    zip_code = search_params.get('zip_code', 'N/A')

    fmv_average = market_context.get('fmv_average', 0)
    total_listings = market_context.get('total_listings_found', 0)
    unique_listings = market_context.get('unique_listings', 0)

    subtitle = f"{year} {make} {model} &mdash; {condition}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vehicle Inventory Search - {year} {make} {model}</title>
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
            background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
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

        .search-params-box {{
            background: #ecfdf5;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border-left: 4px solid {GREEN};
        }}

        .search-params-box h3 {{
            color: {GREEN_DARK};
            margin-bottom: 0.8rem;
        }}

        .params-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}

        .param-item {{
            font-size: 0.95rem;
        }}

        .param-label {{
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
            background: {GREEN};
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
            background: #ecfdf5;
        }}

        .rank {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {GREEN};
            text-align: center;
        }}

        .deal-badge {{
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

        .vehicle-card {{
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        }}

        .vehicle-card:hover {{
            border-color: {GREEN};
            box-shadow: 0 8px 24px rgba(5,150,105,0.15);
        }}

        .vehicle-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .vehicle-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {GREEN_DARK};
            flex: 1;
        }}

        .vehicle-badges {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
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

        .features-list {{
            background: #ecfdf5;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid {GREEN};
            margin-bottom: 1.5rem;
        }}

        .features-list h4 {{
            color: {GREEN_DARK};
            margin-bottom: 0.5rem;
        }}

        .features-list ul {{
            list-style: none;
            padding: 0;
        }}

        .features-list li::before {{
            content: "+  ";
            color: {GREEN};
            font-weight: 700;
        }}

        .incentives-list {{
            background: #eff6ff;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #2563EB;
            margin-bottom: 1.5rem;
        }}

        .incentives-list h4 {{
            color: #1D4ED8;
            margin-bottom: 0.5rem;
        }}

        .incentives-list ul {{
            list-style: none;
            padding: 0;
        }}

        .incentives-list li::before {{
            content: "$  ";
            color: #2563EB;
            font-weight: 700;
        }}

        .negotiation-notes {{
            background: #1f2937;
            color: #f9fafb;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            position: relative;
        }}

        .negotiation-notes-title {{
            font-weight: 600;
            margin-bottom: 0.8rem;
            color: #34d399;
        }}

        .negotiation-notes p {{
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        .dealer-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
            background: #f9fafb;
            padding: 1rem;
            border-radius: 8px;
        }}

        .market-context-section {{
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-top: 2rem;
        }}

        .market-item {{
            margin-bottom: 1.5rem;
        }}

        .market-label {{
            font-weight: 600;
            color: {GREEN_DARK};
            margin-bottom: 0.3rem;
            font-size: 1.1rem;
        }}

        .market-value {{
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
            <h1>Vehicle Inventory Search</h1>
            <div class="subtitle">{subtitle}</div>
            <div class="meta">
                <div class="meta-item">
                    <div class="meta-label">Generated</div>
                    <div class="meta-value">{generated_date}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Search Radius</div>
                    <div class="meta-value">{radius} miles</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Listings Found</div>
                    <div class="meta-value">{unique_listings} Unique</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">FMV</div>
                    <div class="meta-value">${fmv_average:,.0f}</div>
                </div>
            </div>
        </div>

        <div class="content">
            <div class="section">
                <div class="search-params-box">
                    <h3>Search Parameters</h3>
                    <div class="params-grid">
                        <div class="param-item">
                            <div class="param-label">Year</div>
                            <div>{year}</div>
                        </div>
                        <div class="param-item">
                            <div class="param-label">Make</div>
                            <div>{make}</div>
                        </div>
                        <div class="param-item">
                            <div class="param-label">Model</div>
                            <div>{model}</div>
                        </div>
                        <div class="param-item">
                            <div class="param-label">Trims</div>
                            <div>{trims or 'All'}</div>
                        </div>
                        <div class="param-item">
                            <div class="param-label">Condition</div>
                            <div>{condition}</div>
                        </div>
                        <div class="param-item">
                            <div class="param-label">Budget</div>
                            <div>${max_price:,.0f}</div>
                        </div>
                        <div class="param-item">
                            <div class="param-label">Radius</div>
                            <div>{radius} miles</div>
                        </div>
                        <div class="param-item">
                            <div class="param-label">Zip Code</div>
                            <div>{zip_code}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2 class="section-title">Listings Summary</h2>
                <table class="shortlist-table">
                    <thead>
                        <tr>
                            <th style="width: 60px;">Rank</th>
                            <th style="width: 120px;">Deal Rating</th>
                            <th>Vehicle</th>
                            <th style="width: 100px;">Price</th>
                            <th style="width: 100px;">vs FMV</th>
                            <th style="width: 80px;">Distance</th>
                            <th>Dealer</th>
                            <th style="width: 80px;">Rating</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # Add table rows
    for listing in listings:
        rank = listing.get('rank', 0)
        deal_rating = listing.get('deal_rating', 'FAIR_PRICE')
        deal_display = deal_rating.replace('_', ' ')
        composite = listing.get('composite_score', 0)
        l_year = listing.get('year', '')
        l_model = listing.get('model', '')
        l_trim = listing.get('trim', '')
        vehicle_name = f"{l_year} {l_model} {l_trim}".strip()
        price = listing.get('price', 0)
        price_vs_fmv = listing.get('price_vs_fmv', None)
        distance = listing.get('dealer_distance_miles', 'N/A')
        dealer = listing.get('dealer_name', 'Unknown')
        dealer_rating = listing.get('dealer_rating', 'N/A')

        deal_style = f"background: {DEAL_COLORS.get(deal_rating, DEAL_COLORS['FAIR_PRICE'])['bg']}; color: {DEAL_COLORS.get(deal_rating, DEAL_COLORS['FAIR_PRICE'])['text']};"
        fmv_display = format_price_diff(price_vs_fmv)

        html += f"""
                        <tr>
                            <td class="rank">#{rank}</td>
                            <td><span class="deal-badge" style="{deal_style}">{deal_display}</span></td>
                            <td>
                                <strong>{vehicle_name}</strong>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {composite}%; background: {score_color(composite)};"></div>
                                </div>
                            </td>
                            <td><strong>${price:,.0f}</strong></td>
                            <td style="color: {'#059669' if price_vs_fmv is not None and price_vs_fmv < 0 else '#DC2626' if price_vs_fmv is not None and price_vs_fmv > 0 else '#6b7280'}; font-weight: 600;">{fmv_display}</td>
                            <td>{distance} mi</td>
                            <td>{dealer}</td>
                            <td>{dealer_rating}</td>
                        </tr>
"""

    html += """
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2 class="section-title">Detailed Listings</h2>
"""

    # Add detailed vehicle cards (top 3)
    top_listings = listings[:3]
    for listing in top_listings:
        rank = listing.get('rank', 0)
        deal_rating = listing.get('deal_rating', 'FAIR_PRICE')
        deal_display = deal_rating.replace('_', ' ')
        composite = listing.get('composite_score', 0)
        l_year = listing.get('year', '')
        l_make = listing.get('make', '')
        l_model = listing.get('model', '')
        l_trim = listing.get('trim', '')
        vehicle_name = f"{l_year} {l_make} {l_model} {l_trim}".strip()
        price = listing.get('price', 0)
        msrp = listing.get('msrp', 0)
        fmv = listing.get('fmv', 0)
        price_vs_fmv = listing.get('price_vs_fmv', None)
        price_vs_fmv_pct = listing.get('price_vs_fmv_pct', None)
        exterior_color = listing.get('exterior_color', 'N/A')
        interior_color = listing.get('interior_color', 'N/A')
        mileage = listing.get('mileage', 'N/A')
        vin = listing.get('vin', 'N/A')
        dealer_name = listing.get('dealer_name', 'Unknown')
        dealer_distance = listing.get('dealer_distance_miles', 'N/A')
        dealer_rating = listing.get('dealer_rating', 'N/A')
        dealer_reviews = listing.get('dealer_review_count', 'N/A')
        key_features = listing.get('key_features', [])
        incentives = listing.get('incentives', [])
        negotiation_notes = listing.get('negotiation_notes', '')
        listing_url = listing.get('listing_url', '')
        phone = listing.get('phone', '')
        source = listing.get('source', 'N/A')
        days_on_market = listing.get('days_on_market', 'N/A')
        confidence = listing.get('confidence', 'N/A')

        deal_style = f"background: {DEAL_COLORS.get(deal_rating, DEAL_COLORS['FAIR_PRICE'])['bg']}; color: {DEAL_COLORS.get(deal_rating, DEAL_COLORS['FAIR_PRICE'])['text']};"
        fmv_display = format_price_diff(price_vs_fmv)
        pct_display = f"{price_vs_fmv_pct:+.1f}%" if price_vs_fmv_pct is not None else "N/A"

        html += f"""
                <div class="vehicle-card">
                    <div class="vehicle-card-header">
                        <div class="vehicle-title">#{rank}. {vehicle_name}</div>
                        <div class="vehicle-badges">
                            <span class="deal-badge" style="{deal_style}">{deal_display}</span>
                        </div>
                    </div>

                    <div class="detail-grid">
                        <div class="detail-item">
                            <div class="detail-label">Price</div>
                            <div class="detail-value">${price:,.0f}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">MSRP</div>
                            <div class="detail-value">${msrp:,.0f}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">FMV</div>
                            <div class="detail-value">${fmv:,.0f}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">vs FMV</div>
                            <div class="detail-value" style="color: {'#059669' if price_vs_fmv is not None and price_vs_fmv < 0 else '#DC2626' if price_vs_fmv is not None and price_vs_fmv > 0 else '#6b7280'};">{fmv_display} ({pct_display})</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Dealer</div>
                            <div class="detail-value">{dealer_name}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Distance</div>
                            <div class="detail-value">{dealer_distance} miles</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Days on Market</div>
                            <div class="detail-value">{days_on_market}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Composite Score</div>
                            <div class="detail-value" style="color: {score_color(composite)};">{composite}</div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {composite}%; background: {score_color(composite)};"></div>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Exterior Color</div>
                            <div class="detail-value">{exterior_color}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Interior Color</div>
                            <div class="detail-value">{interior_color}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Mileage</div>
                            <div class="detail-value">{mileage}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">VIN</div>
                            <div class="detail-value" style="font-size: 0.9rem;">{vin}</div>
                        </div>
                    </div>
"""

        if key_features:
            html += """
                    <div class="features-list">
                        <h4>Key Features</h4>
                        <ul>
"""
            for feat in key_features:
                html += f"                            <li>{feat}</li>\n"
            html += """
                        </ul>
                    </div>
"""

        if incentives:
            html += """
                    <div class="incentives-list">
                        <h4>Incentives</h4>
                        <ul>
"""
            for inc in incentives:
                html += f"                            <li>{inc}</li>\n"
            html += """
                        </ul>
                    </div>
"""

        if negotiation_notes:
            html += f"""
                    <div class="negotiation-notes">
                        <div class="negotiation-notes-title">Negotiation Notes</div>
                        <p>{negotiation_notes}</p>
                    </div>
"""

        html += f"""
                    <div class="dealer-info">
                        <div>
                            <div class="detail-label">Dealer</div>
                            <div style="font-weight: 600;">{dealer_name}</div>
                        </div>
                        <div>
                            <div class="detail-label">Rating</div>
                            <div style="font-weight: 600;">{dealer_rating} ({dealer_reviews} reviews)</div>
                        </div>
                        <div>
                            <div class="detail-label">Source</div>
                            <div style="font-weight: 600;">{source}</div>
                        </div>
                        <div>
                            <div class="detail-label">Confidence</div>
                            <div style="font-weight: 600;">{confidence}</div>
                        </div>
                    </div>
"""

        if listing_url:
            html += f"""
                    <div style="margin-bottom: 0.5rem;">
                        <div class="detail-label" style="margin-bottom: 0.3rem;">Listing URL</div>
                        <div><a href="{listing_url}" target="_blank" style="color: {GREEN}; text-decoration: none;">{listing_url}</a></div>
                    </div>
"""

        if phone:
            html += f"""
                    <div style="margin-bottom: 1rem;">
                        <div class="detail-label" style="margin-bottom: 0.3rem;">Phone</div>
                        <div style="font-weight: 600;">{phone}</div>
                    </div>
"""

        html += """
                </div>
"""

    html += """
            </div>
"""

    # Market Context section
    if market_context:
        avg_asking = market_context.get('average_asking', 0)
        market_trend = market_context.get('market_trend', 'N/A')
        best_time = market_context.get('best_time_insight', 'N/A')
        incentives_summary = market_context.get('incentives_summary', [])

        html += """
            <div class="section">
                <h2 class="section-title">Market Context</h2>
                <div class="market-context-section">
"""

        html += f"""
                    <div class="market-item">
                        <div class="market-label">FMV Average</div>
                        <div class="market-value">${fmv_average:,.0f}</div>
                    </div>
                    <div class="market-item">
                        <div class="market-label">Average Asking Price</div>
                        <div class="market-value">${avg_asking:,.0f}</div>
                    </div>
                    <div class="market-item">
                        <div class="market-label">Total Listings Found</div>
                        <div class="market-value">{total_listings} ({unique_listings} unique after deduplication)</div>
                    </div>
                    <div class="market-item">
                        <div class="market-label">Market Trend</div>
                        <div class="market-value">{market_trend}</div>
                    </div>
                    <div class="market-item">
                        <div class="market-label">Best Time to Buy</div>
                        <div class="market-value">{best_time}</div>
                    </div>
"""

        if incentives_summary:
            incentives_str = ', '.join(incentives_summary)
            html += f"""
                    <div class="market-item">
                        <div class="market-label">Available Incentives</div>
                        <div class="market-value">{incentives_str}</div>
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

        if methodology.get('deduplication_removals') is not None:
            html += f"""
                    <div class="detail-item">
                        <div class="detail-label">Deduplication Removals</div>
                        <div class="detail-value">{methodology['deduplication_removals']}</div>
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

        if methodology.get('fmv_sources'):
            fmv_sources = ', '.join(methodology['fmv_sources'])
            html += f"""
                    <div class="detail-item" style="grid-column: 1 / -1;">
                        <div class="detail-label">FMV Sources</div>
                        <div class="detail-value">{fmv_sources}</div>
                    </div>
"""

        html += """
                </div>
            </div>
"""

    html += f"""
            <div class="footer">
                Generated by Vehicle Finder on {generated_date}<br>
                ROK Plugin Marketplace - Vehicle Finder v1.0
            </div>
        </div>
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_pdf(data, output_path):
    """Generate PDF report from inventory search data."""

    class InventoryPDF(FPDF):
        def header(self):
            self.set_fill_color(5, 150, 105)  # GREEN
            self.rect(0, 0, 210, 40, 'F')
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 20)
            self.cell(0, 15, '', 0, 1)
            self.cell(0, 10, latin_safe('Vehicle Inventory Search'), 0, 1, 'C')
            self.set_font('Arial', '', 12)
            search_params = data.get('search_params', {})
            subtitle = f"{search_params.get('year', '')} {search_params.get('make', '')} {search_params.get('model', '')} - {search_params.get('condition', 'New')}"
            self.cell(0, 8, latin_safe(subtitle), 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = InventoryPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    search_params = data.get('search_params', {})
    market_context = data.get('market_context', {})
    listings = data.get('listings', [])
    methodology = data.get('methodology', {})
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))

    # Search Parameters section
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(4, 120, 87)  # GREEN_DARK
    pdf.cell(0, 10, latin_safe('Search Parameters'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0, 0, 0)

    pdf.cell(90, 7, latin_safe(f'Year: {search_params.get("year", "N/A")}'), 0, 0)
    pdf.cell(90, 7, latin_safe(f'Make: {search_params.get("make", "N/A")}'), 0, 1)
    pdf.cell(90, 7, latin_safe(f'Model: {search_params.get("model", "N/A")}'), 0, 0)
    trims = ', '.join(search_params.get('trims', []))
    pdf.cell(90, 7, latin_safe(f'Trims: {trims or "All"}'), 0, 1)
    pdf.cell(90, 7, latin_safe(f'Condition: {search_params.get("condition", "N/A")}'), 0, 0)
    max_price = search_params.get('max_price', 0)
    pdf.cell(90, 7, latin_safe(f'Budget: ${max_price:,.0f}'), 0, 1)
    pdf.cell(90, 7, latin_safe(f'Radius: {search_params.get("radius_miles", "N/A")} miles'), 0, 0)
    pdf.cell(90, 7, latin_safe(f'Zip Code: {search_params.get("zip_code", "N/A")}'), 0, 1)
    pdf.ln(5)

    # Summary stats
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(4, 120, 87)
    pdf.cell(0, 10, latin_safe('Summary'), 0, 1)
    pdf.ln(2)

    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)

    fmv_average = market_context.get('fmv_average', 0)
    unique_listings = market_context.get('unique_listings', 0)
    radius = search_params.get('radius_miles', 'N/A')

    pdf.cell(90, 8, latin_safe(f'Generated: {generated_date}'), 0, 0)
    pdf.cell(90, 8, latin_safe(f'Listings Found: {unique_listings}'), 0, 1)
    pdf.cell(90, 8, latin_safe(f'FMV Average: ${fmv_average:,.0f}'), 0, 0)
    pdf.cell(90, 8, latin_safe(f'Search Radius: {radius} miles'), 0, 1)

    if methodology:
        pdf.cell(90, 8, latin_safe(f'Agents: {methodology.get("agents_dispatched", 0)}'), 0, 0)
        pdf.cell(90, 8, latin_safe(f'Searches: {methodology.get("total_searches", 0)}'), 0, 1)

    pdf.ln(10)

    # Listings table
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(4, 120, 87)
    pdf.cell(0, 10, latin_safe('Listings'), 0, 1)
    pdf.ln(2)

    # Table header
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(5, 150, 105)  # GREEN
    pdf.set_text_color(255, 255, 255)
    pdf.cell(10, 8, '#', 1, 0, 'C', True)
    pdf.cell(45, 8, 'Vehicle', 1, 0, 'C', True)
    pdf.cell(25, 8, 'Deal', 1, 0, 'C', True)
    pdf.cell(22, 8, 'Price', 1, 0, 'C', True)
    pdf.cell(22, 8, 'vs FMV', 1, 0, 'C', True)
    pdf.cell(38, 8, 'Dealer', 1, 0, 'C', True)
    pdf.cell(18, 8, 'Dist', 1, 1, 'C', True)

    # Table rows
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(0, 0, 0)

    for listing in listings:
        rank = listing.get('rank', 0)
        l_year = listing.get('year', '')
        l_model = listing.get('model', '')
        l_trim = listing.get('trim', '')
        vehicle_name = f"{l_year} {l_model} {l_trim}".strip()
        deal_rating = listing.get('deal_rating', 'FAIR_PRICE')
        deal_display = deal_rating.replace('_', ' ')
        price = listing.get('price', 0)
        price_vs_fmv = listing.get('price_vs_fmv', None)
        dealer_name = listing.get('dealer_name', 'Unknown')
        distance = listing.get('dealer_distance_miles', 'N/A')

        fmv_display = format_price_diff(price_vs_fmv)

        pdf.cell(10, 8, str(rank), 1, 0, 'C')
        pdf.cell(45, 8, latin_safe(vehicle_name[:26]), 1, 0)
        pdf.cell(25, 8, latin_safe(deal_display[:12]), 1, 0, 'C')
        pdf.cell(22, 8, latin_safe(f'${price:,.0f}'), 1, 0, 'C')
        pdf.cell(22, 8, latin_safe(fmv_display), 1, 0, 'C')
        pdf.cell(38, 8, latin_safe(dealer_name[:22]), 1, 0)
        pdf.cell(18, 8, latin_safe(f'{distance}mi'), 1, 1, 'C')

    pdf.ln(10)

    # Detailed sections
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(4, 120, 87)
    pdf.cell(0, 10, latin_safe('Detailed Listings'), 0, 1)
    pdf.ln(5)

    for idx, listing in enumerate(listings):
        if idx > 0:
            pdf.ln(8)

        rank = listing.get('rank', 0)
        l_year = listing.get('year', '')
        l_make = listing.get('make', '')
        l_model = listing.get('model', '')
        l_trim = listing.get('trim', '')
        vehicle_name = f"{l_year} {l_make} {l_model} {l_trim}".strip()
        deal_rating = listing.get('deal_rating', 'FAIR_PRICE')
        deal_display = deal_rating.replace('_', ' ')
        composite = listing.get('composite_score', 0)
        price = listing.get('price', 0)
        msrp = listing.get('msrp', 0)
        fmv = listing.get('fmv', 0)
        price_vs_fmv = listing.get('price_vs_fmv', None)
        price_vs_fmv_pct = listing.get('price_vs_fmv_pct', None)
        exterior_color = listing.get('exterior_color', 'N/A')
        interior_color = listing.get('interior_color', 'N/A')
        mileage = listing.get('mileage', 'N/A')
        vin = listing.get('vin', 'N/A')
        dealer_name = listing.get('dealer_name', 'Unknown')
        dealer_distance = listing.get('dealer_distance_miles', 'N/A')
        dealer_rating = listing.get('dealer_rating', 'N/A')
        dealer_reviews = listing.get('dealer_review_count', 'N/A')
        key_features = listing.get('key_features', [])
        incentives = listing.get('incentives', [])
        negotiation_notes = listing.get('negotiation_notes', '')
        listing_url = listing.get('listing_url', '')
        phone = listing.get('phone', '')
        source = listing.get('source', 'N/A')
        days_on_market = listing.get('days_on_market', 'N/A')
        confidence = listing.get('confidence', 'N/A')

        fmv_display = format_price_diff(price_vs_fmv)
        pct_display = f"{price_vs_fmv_pct:+.1f}%" if price_vs_fmv_pct is not None else "N/A"

        # Vehicle header
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(4, 120, 87)
        pdf.cell(0, 8, latin_safe(f'#{rank}. {vehicle_name} ({deal_display} - Score: {composite})'), 0, 1)

        # Price breakdown
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(60, 6, latin_safe(f'Price: ${price:,.0f}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'MSRP: ${msrp:,.0f}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'FMV: ${fmv:,.0f}'), 0, 1)
        pdf.cell(60, 6, latin_safe(f'vs FMV: {fmv_display} ({pct_display})'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Days on Market: {days_on_market}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Confidence: {confidence}'), 0, 1)
        pdf.ln(2)

        # Vehicle details
        pdf.cell(60, 6, latin_safe(f'Exterior: {exterior_color}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Interior: {interior_color}'), 0, 0)
        pdf.cell(60, 6, latin_safe(f'Mileage: {mileage}'), 0, 1)
        pdf.cell(0, 6, latin_safe(f'VIN: {vin}'), 0, 1)
        pdf.ln(2)

        # Dealer info
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, latin_safe('Dealer Information:'), 0, 1)
        pdf.set_font('Arial', '', 9)
        pdf.cell(5, 5, '', 0, 0)
        pdf.cell(0, 5, latin_safe(f'{dealer_name} - {dealer_distance} miles away'), 0, 1)
        pdf.cell(5, 5, '', 0, 0)
        pdf.cell(0, 5, latin_safe(f'Rating: {dealer_rating} ({dealer_reviews} reviews) | Source: {source}'), 0, 1)
        if phone:
            pdf.cell(5, 5, '', 0, 0)
            pdf.cell(0, 5, latin_safe(f'Phone: {phone}'), 0, 1)
        if listing_url:
            pdf.cell(5, 5, '', 0, 0)
            pdf.cell(0, 5, latin_safe(f'URL: {listing_url[:80]}'), 0, 1)
        pdf.ln(2)

        # Key features
        if key_features:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Key Features:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            for feat in key_features:
                pdf.cell(5, 5, '', 0, 0)
                pdf.cell(0, 5, latin_safe(f'+ {feat}'), 0, 1)
            pdf.ln(2)

        # Incentives
        if incentives:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Incentives:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            for inc in incentives:
                pdf.cell(5, 5, '', 0, 0)
                pdf.cell(0, 5, latin_safe(f'$ {inc}'), 0, 1)
            pdf.ln(2)

        # Negotiation notes
        if negotiation_notes:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Negotiation Notes:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            pdf.cell(5, 5, '', 0, 0)
            pdf.multi_cell(0, 5, latin_safe(negotiation_notes))
            pdf.ln(2)

        # Page break check
        if pdf.get_y() > 250 and idx < len(listings) - 1:
            pdf.add_page()

    # Market Context page
    if market_context:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(4, 120, 87)
        pdf.cell(0, 10, latin_safe('Market Context'), 0, 1)
        pdf.ln(5)

        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)

        fmv_average = market_context.get('fmv_average', 0)
        avg_asking = market_context.get('average_asking', 0)
        total_listings = market_context.get('total_listings_found', 0)
        unique_listings = market_context.get('unique_listings', 0)
        market_trend = market_context.get('market_trend', 'N/A')
        best_time = market_context.get('best_time_insight', 'N/A')
        incentives_summary = market_context.get('incentives_summary', [])

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, latin_safe('FMV Average:'), 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, latin_safe(f'${fmv_average:,.0f}'), 0, 1)
        pdf.ln(3)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, latin_safe('Average Asking Price:'), 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, latin_safe(f'${avg_asking:,.0f}'), 0, 1)
        pdf.ln(3)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, latin_safe('Listings Found:'), 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, latin_safe(f'{total_listings} total, {unique_listings} unique'), 0, 1)
        pdf.ln(3)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, latin_safe('Market Trend:'), 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, latin_safe(market_trend))
        pdf.ln(3)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, latin_safe('Best Time to Buy:'), 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, latin_safe(best_time))
        pdf.ln(3)

        if incentives_summary:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, latin_safe('Available Incentives:'), 0, 1)
            pdf.set_font('Arial', '', 9)
            for inc in incentives_summary:
                pdf.cell(5, 5, '', 0, 0)
                pdf.cell(0, 5, latin_safe(f'- {inc}'), 0, 1)

    # Methodology section
    if methodology:
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(4, 120, 87)
        pdf.cell(0, 10, latin_safe('Methodology'), 0, 1)
        pdf.ln(5)

        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)

        pdf.cell(90, 7, latin_safe(f'Agents Dispatched: {methodology.get("agents_dispatched", 0)}'), 0, 0)
        pdf.cell(90, 7, latin_safe(f'Total Searches: {methodology.get("total_searches", 0)}'), 0, 1)
        pdf.cell(90, 7, latin_safe(f'Deduplication Removals: {methodology.get("deduplication_removals", 0)}'), 0, 1)

        if methodology.get('sources_covered'):
            sources = ', '.join(methodology['sources_covered'])
            pdf.cell(0, 7, latin_safe(f'Sources: {sources}'), 0, 1)

        if methodology.get('fmv_sources'):
            fmv_sources = ', '.join(methodology['fmv_sources'])
            pdf.cell(0, 7, latin_safe(f'FMV Sources: {fmv_sources}'), 0, 1)

    pdf.output(output_path)


def generate_markdown(data, output_path):
    """Generate Markdown report from inventory search data."""
    search_params = data.get('search_params', {})
    market_context = data.get('market_context', {})
    listings = data.get('listings', [])
    methodology = data.get('methodology', {})
    generated_date = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))

    year = search_params.get('year', '')
    make = search_params.get('make', 'Vehicle')
    model = search_params.get('model', '')
    condition = search_params.get('condition', 'New')
    trims = ', '.join(search_params.get('trims', []))
    max_price = search_params.get('max_price', 0)
    radius = search_params.get('radius_miles', 'N/A')
    zip_code = search_params.get('zip_code', 'N/A')

    fmv_average = market_context.get('fmv_average', 0)
    unique_listings = market_context.get('unique_listings', 0)

    md = f"""# Vehicle Inventory Search

## {year} {make} {model} — {condition}

**Generated:** {generated_date}
**Listings Found:** {unique_listings} unique
**FMV Average:** ${fmv_average:,.0f}
**Search Radius:** {radius} miles

---

## Search Parameters

| Parameter | Value |
|-----------|-------|
| Year | {year} |
| Make | {make} |
| Model | {model} |
| Trims | {trims or 'All'} |
| Condition | {condition} |
| Budget | ${max_price:,.0f} |
| Radius | {radius} miles |
| Zip Code | {zip_code} |

---

## Market Context

"""

    if market_context:
        avg_asking = market_context.get('average_asking', 0)
        market_trend = market_context.get('market_trend', 'N/A')
        best_time = market_context.get('best_time_insight', 'N/A')
        total_listings = market_context.get('total_listings_found', 0)
        incentives_summary = market_context.get('incentives_summary', [])

        md += f"""- **FMV Average:** ${fmv_average:,.0f}
- **Average Asking:** ${avg_asking:,.0f}
- **Total Listings:** {total_listings} ({unique_listings} unique)
- **Market Trend:** {market_trend}
- **Best Time to Buy:** {best_time}
"""

        if incentives_summary:
            md += "- **Incentives:**\n"
            for inc in incentives_summary:
                md += f"  - {inc}\n"

    md += """
---

## Listings Overview

| Rank | Deal | Vehicle | Price | vs FMV | Miles | Dealer | Rating |
|------|------|---------|-------|--------|-------|--------|--------|
"""

    for listing in listings:
        rank = listing.get('rank', 0)
        deal_rating = listing.get('deal_rating', 'FAIR_PRICE')
        deal_display = deal_rating.replace('_', ' ')
        l_year = listing.get('year', '')
        l_model = listing.get('model', '')
        l_trim = listing.get('trim', '')
        vehicle_name = f"{l_year} {l_model} {l_trim}".strip()
        price = listing.get('price', 0)
        price_vs_fmv = listing.get('price_vs_fmv', None)
        mileage = listing.get('mileage', 'N/A')
        dealer_name = listing.get('dealer_name', 'Unknown')
        dealer_rating = listing.get('dealer_rating', 'N/A')

        fmv_display = format_price_diff(price_vs_fmv)

        md += f"| {rank} | {deal_display} | {vehicle_name} | ${price:,.0f} | {fmv_display} | {mileage} | {dealer_name} | {dealer_rating} |\n"

    md += "\n---\n\n## Detailed Analysis\n\n"

    for listing in listings:
        rank = listing.get('rank', 0)
        l_year = listing.get('year', '')
        l_make = listing.get('make', '')
        l_model = listing.get('model', '')
        l_trim = listing.get('trim', '')
        vehicle_name = f"{l_year} {l_make} {l_model} {l_trim}".strip()
        deal_rating = listing.get('deal_rating', 'FAIR_PRICE')
        deal_display = deal_rating.replace('_', ' ')
        composite = listing.get('composite_score', 0)
        price = listing.get('price', 0)
        msrp = listing.get('msrp', 0)
        fmv = listing.get('fmv', 0)
        price_vs_fmv = listing.get('price_vs_fmv', None)
        price_vs_fmv_pct = listing.get('price_vs_fmv_pct', None)
        exterior_color = listing.get('exterior_color', 'N/A')
        interior_color = listing.get('interior_color', 'N/A')
        mileage = listing.get('mileage', 'N/A')
        vin = listing.get('vin', 'N/A')
        dealer_name = listing.get('dealer_name', 'Unknown')
        dealer_distance = listing.get('dealer_distance_miles', 'N/A')
        dealer_rating = listing.get('dealer_rating', 'N/A')
        dealer_reviews = listing.get('dealer_review_count', 'N/A')
        key_features = listing.get('key_features', [])
        incentives = listing.get('incentives', [])
        negotiation_notes = listing.get('negotiation_notes', '')
        listing_url = listing.get('listing_url', '')
        phone = listing.get('phone', '')
        source = listing.get('source', 'N/A')
        days_on_market = listing.get('days_on_market', 'N/A')
        confidence = listing.get('confidence', 'N/A')

        fmv_display = format_price_diff(price_vs_fmv)
        pct_display = f"{price_vs_fmv_pct:+.1f}%" if price_vs_fmv_pct is not None else "N/A"

        md += f"""### #{rank}. {vehicle_name}

**Deal Rating:** {deal_display} | **Score:** {composite} | **Confidence:** {confidence}

**Pricing:**
- Price: ${price:,.0f}
- MSRP: ${msrp:,.0f}
- FMV: ${fmv:,.0f}
- vs FMV: {fmv_display} ({pct_display})

**Vehicle Details:**
- Exterior: {exterior_color}
- Interior: {interior_color}
- Mileage: {mileage}
- Days on Market: {days_on_market}
- VIN: {vin}

**Dealer:**
- {dealer_name} ({dealer_distance} miles)
- Rating: {dealer_rating} ({dealer_reviews} reviews)
- Source: {source}
"""

        if phone:
            md += f"- Phone: {phone}\n"

        if listing_url:
            md += f"- [View Listing]({listing_url})\n"

        md += "\n"

        if key_features:
            md += "**Key Features:**\n"
            for feat in key_features:
                md += f"- {feat}\n"
            md += "\n"

        if incentives:
            md += "**Incentives:**\n"
            for inc in incentives:
                md += f"- {inc}\n"
            md += "\n"

        if negotiation_notes:
            md += f"**Negotiation Notes:**  \n{negotiation_notes}\n\n"

        md += "---\n\n"

    # Methodology section
    if methodology:
        md += "## Methodology\n\n"
        md += f"- **Agents Dispatched:** {methodology.get('agents_dispatched', 0)}\n"
        md += f"- **Total Searches:** {methodology.get('total_searches', 0)}\n"

        if methodology.get('sources_covered'):
            md += f"- **Sources Covered:** {', '.join(methodology['sources_covered'])}\n"

        if methodology.get('fmv_sources'):
            md += f"- **FMV Sources:** {', '.join(methodology['fmv_sources'])}\n"

        md += f"- **Deduplication Removals:** {methodology.get('deduplication_removals', 0)}\n"
        md += "\n"

    md += f"""---

*Generated by Vehicle Finder on {generated_date}*
*ROK Plugin Marketplace - Vehicle Finder v1.0*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)


def main():
    parser = argparse.ArgumentParser(description='Export Vehicle Inventory Search to HTML, PDF, and Markdown')
    parser.add_argument('--input', required=True, help='Path to inventory JSON file')
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
    if data.get('type') != 'vehicle_inventory':
        print(f"Warning: Expected type 'vehicle_inventory', got '{data.get('type')}'", file=sys.stderr)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate filename base
    search_params = data.get('search_params', {})
    make_slug = slugify(search_params.get('make', 'unknown'))
    model_slug = slugify(search_params.get('model', 'unknown'))
    date_str = data.get('generated_date', datetime.now().strftime('%Y-%m-%d'))
    base_filename = f"vehicle_inventory_{make_slug}_{model_slug}_{date_str}"

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
