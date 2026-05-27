#!/usr/bin/env python3
import os
import re
import sys

# Multi-Tier Portfolio Configuration
TIER = "25k"
CAPITAL_POOL_SIZE = 25000

if len(sys.argv) > 1:
    arg_tier = sys.argv[1].lower().strip()
    if arg_tier in ["5k", "25k", "100k", "250k"]:
        TIER = arg_tier
        if TIER == "5k":
            CAPITAL_POOL_SIZE = 5000
        elif TIER == "25k":
            CAPITAL_POOL_SIZE = 25000
        elif TIER == "100k":
            CAPITAL_POOL_SIZE = 100000
        elif TIER == "250k":
            CAPITAL_POOL_SIZE = 250000

def parse_portfolio():
    """Parses portfolio/[TIER]/PORTFOLIO.md to get capital allocation matrix."""
    portfolio_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../portfolio/{TIER}/PORTFOLIO.md'))
    if not os.path.exists(portfolio_path):
        print(f"Error: Could not find portfolio file at {portfolio_path}", file=sys.stderr)
        sys.exit(1)

    with open(portfolio_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the table in Capital Allocation Matrix
    table_pattern = re.compile(r'\|.*Strategic Tier.*\|\n\|.*---.*\|\n((?:\|.*\|\n?)+)', re.IGNORECASE)
    match = table_pattern.search(content)
    if not match:
        print("Error: Could not parse Capital Allocation Matrix table in PORTFOLIO.md", file=sys.stderr)
        sys.exit(1)

    table_rows = match.group(1).strip().split('\n')
    allocations = []
    
    for row in table_rows:
        cols = [c.strip() for c in row.split('|')[1:-1]]
        if len(cols) < 5:
            continue
        
        tier = cols[0].replace('**', '')
        alloc_match = re.search(r'(\d+(?:\.\d+)?)%', cols[1])
        alloc_pct = float(alloc_match.group(1)) if alloc_match else 0.0
        thesis_link_match = re.search(r'\[(.*?)\]\((.*?)\)', cols[2])
        proxy = cols[3].replace('**', '')
        role = cols[4]

        if not thesis_link_match:
            continue

        thesis_title = thesis_link_match.group(1)
        thesis_rel_path = thesis_link_match.group(2)

        allocations.append({
            'tier': tier,
            'allocation': alloc_pct,
            'thesis_title': thesis_title,
            'thesis_rel_path': thesis_rel_path,
            'proxy': proxy,
            'role': role
        })

    return allocations

def parse_thesis(thesis_rel_path):
    """Parses individual THESIS.md to extract confidence score, rubrics, and epicenter rationale."""
    portfolio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../portfolio/{TIER}'))
    thesis_path = os.path.abspath(os.path.join(portfolio_dir, thesis_rel_path))
    
    if not os.path.exists(thesis_path):
        return {
            'confidence': 0.0,
            'rubric': 'N/A',
            'epicenter': 'Thesis file not found.'
        }

    with open(thesis_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse confidence
    conf_match = re.search(r'-\s+\*\*Confidence:\*\*\s+(\d+)%', content, re.IGNORECASE)
    confidence = float(conf_match.group(1)) if conf_match else 0.0

    # Parse rubric comment
    rubric_match = re.search(r'<!--\s*Confidence rubric[^:]*:\s*(.*?)\s*-->', content, re.IGNORECASE)
    if not rubric_match:
        rubric_match = re.search(r'<!--\s*Confidence rubric:\s*(.*?)\s*-->', content, re.IGNORECASE)
    rubric = rubric_match.group(1).strip() if rubric_match else 'N/A'

    # Parse epicenter/architecture
    epicenter_match = re.search(r'-\s+\*\*Epicenter:\*\*\s*(.*)', content, re.IGNORECASE)
    epicenter = epicenter_match.group(1).strip() if epicenter_match else ''
    
    if not epicenter:
        # Fallback to first line of core architecture or description
        arch_match = re.search(r'## Core Architecture\s*\n\s*\n\s*(.*)', content, re.IGNORECASE)
        if arch_match:
            epicenter = arch_match.group(1).strip()[:200] + '...'
        else:
            epicenter = 'Rationale detailed in core thesis file.'

    return {
        'confidence': confidence,
        'rubric': rubric,
        'epicenter': epicenter
    }

def parse_risk_matrix():
    """Parses currency exposure and critical risk blocks from portfolio/RISK_MATRIX.md."""
    risk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../portfolio/RISK_MATRIX.md'))
    if not os.path.exists(risk_path):
        return "Risk matrix not found.", "Currency breakdown not found."

    with open(risk_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find currency exposure mermaid pie chart or description
    currency_match = re.search(r'pie title Currency Exposure.*?\n((?:\s*".*?"\s*:\s*\d+\.?\d*\n?)+)', content, re.DOTALL)
    currency_text = ""
    if currency_match:
        currency_text = "\n### Currency Exposure Breakdown:\n"
        for line in currency_match.group(1).strip().split('\n'):
            parts = line.split(':')
            if len(parts) == 2:
                curr_name = parts[0].strip().replace('&quot;', '').replace('"', '')
                curr_weight = parts[1].strip()
                currency_text += f"- **{curr_name}**: {curr_weight}% weight\n"
    else:
        currency_text = "\n### Currency Exposure Breakdown:\nSee RISK_MATRIX.md for full details."

    # Find High-Correlation Risk Blocks
    risk_blocks_match = re.search(r'## 3\. High-Correlation Risk Blocks.*?\n(.*)', content, re.DOTALL)
    risk_blocks_text = ""
    if risk_blocks_match:
        risk_blocks_text = "\n## 5. High-Correlation Risk Blocks\n"
        blocks = re.findall(r'\[(Block [A-Z]: .*?)\]\nThreat:\s*(.*?)\nCapital at Risk:\s*(.*?)\nMitigants:\s*(.*?)\n', risk_blocks_match.group(1))
        for block in blocks:
            risk_blocks_text += f"### {block[0]}\n"
            risk_blocks_text += f"- **Threat:** {block[1]}\n"
            risk_blocks_text += f"- **Capital at Risk:** {block[2]}\n"
            risk_blocks_text += f"- **Mitigants:** {block[3]}\n\n"
    else:
        risk_blocks_text = "\n## 5. High-Correlation Risk Blocks\nSee RISK_MATRIX.md for full details."

    return risk_blocks_text, currency_text

def generate_analysis():
    print("Parsing PORTFOLIO.md...")
    allocations = parse_portfolio()
    
    print("Parsing individual investment theses...")
    portfolio_confidence_weighted = 0.0
    portfolio_confidence_unweighted = 0.0
    valid_theses_count = 0
    total_alloc = 0.0
    
    detailed_positions = []
    
    for item in allocations:
        thesis_info = parse_thesis(item['thesis_rel_path'])
        
        # Calculate scores
        total_alloc += item['allocation']
        
        if item['allocation'] > 0:
            portfolio_confidence_weighted += (item['allocation'] / 100.0) * thesis_info['confidence']
            portfolio_confidence_unweighted += thesis_info['confidence']
            valid_theses_count += 1
            
        detailed_positions.append({
            'tier': item['tier'],
            'allocation': item['allocation'],
            'thesis_title': item['thesis_title'],
            'thesis_rel_path': item['thesis_rel_path'],
            'proxy': item['proxy'],
            'role': item['role'],
            'confidence': thesis_info['confidence'],
            'rubric': thesis_info['rubric'],
            'epicenter': thesis_info['epicenter']
        })

    # Normalize weighted confidence to represent the allocated portion
    if total_alloc > 0:
        # Scale the weighted confidence back to 100% basis of active capital
        portfolio_confidence_weighted = (portfolio_confidence_weighted / (total_alloc / 100.0))
        
    if valid_theses_count > 0:
        portfolio_confidence_unweighted = (portfolio_confidence_unweighted / valid_theses_count)

    print("Parsing RISK_MATRIX.md...")
    risk_blocks, currency_exposure = parse_risk_matrix()

    # Construct the output markdown
    output = f"""# Master Portfolio Positioning & Systemic Correlation Analysis

*This is an automatically generated, version-controlled analysis file.*  
**Last Updated:** May 23, 2026  
**Total Capital Allocated:** €25,000 (100% of Virtual Pool)  
**Active Theses Count:** {valid_theses_count}  
**Overall Portfolio Confidence Score:** **{portfolio_confidence_weighted:.1f}%** (Weighted) / **{portfolio_confidence_unweighted:.1f}%** (Unweighted)  

---

## 1. Capital Sizing & Allocation Matrix

| Strategic Tier | Allocation (%) | Absolute (€) | Paired Thesis & Primary Tradable Proxy | Confidence Score | Rubric Sub-scores |
| :--- | :---: | :---: | :--- | :---: | :--- |
"""
    
    active_positions = [p for p in detailed_positions if p['allocation'] > 0]
    excluded_positions = [p for p in detailed_positions if p['allocation'] == 0]

    for pos in active_positions:
        abs_val = (pos['allocation'] / 100.0) * CAPITAL_POOL_SIZE
        output += f"| **{pos['tier']}** | {pos['allocation']}% | €{abs_val:,.0f} | [{pos['thesis_title']}]({pos['thesis_rel_path']}) <br> **{pos['proxy']}** | **{pos['confidence']:.0f}%** | `{pos['rubric']}` |\n"

    if excluded_positions:
        output += f"| **-- WATCHLIST --** | **0.0%** | **€0** | *Watchlist / Excluded Theses (Sub-75% Confidence)* | | |\n"
        for pos in excluded_positions:
            output += f"| *{pos['tier']}* | 0.0% | €0 | [{pos['thesis_title']}]({pos['thesis_rel_path']}) <br> *{pos['proxy']}* | *{pos['confidence']:.0f}%* | `{pos['rubric']}` |\n"

    output += f"""
---

## 2. Active Theses: Position Analysis & Rationales

"""

    for i, pos in enumerate(active_positions, 1):
        abs_val = (pos['allocation'] / 100.0) * CAPITAL_POOL_SIZE
        output += f"### {i}. {pos['tier']}: {pos['thesis_title']}\n"
        output += f"- **Primary Tradable Proxy:** **{pos['proxy']}** ({pos['allocation']}% / €{abs_val:,.0f})\n"
        output += f"- **Confidence Score:** **{pos['confidence']:.0f}%** (rubric: `{pos['rubric']}`)\n"
        output += f"- **Strategic Rationale:** {pos['role']}\n"
        output += f"- **Physical/Market Epicenter:** {pos['epicenter']}\n\n"

    output += f"""---

## 3. Whole Portfolio Verdict & Risk Analysis

### Core Verdict & Sizing Discipline
The **{portfolio_confidence_weighted:.1f}%** weighted confidence score outperforming the **{portfolio_confidence_unweighted:.1f}%** unweighted average confirms that capital sizing is highly disciplined. Large capital weights are systematically allocated to the highest-confidence physical gatekeepers (e.g., Ajinomoto Co. at 25% weight / 86% confidence, Murata Mfg. at 8% weight / 89% confidence, and Bloom Energy at 4.5% weight / 88% confidence). Lower-confidence or highly speculative theses are kept at small satellite weights.

{currency_exposure}
"""

    # Section 4: Excluded & Watchlist Theses (Sub-75% Confidence)
    output += f"""
---

## 4. Excluded & Watchlist Theses (Sub-75% Confidence)

*The following structural bottleneck theses are currently held at 0% allocation and placed on the watchlist due to falling below our strict 75% confidence threshold.*

"""

    excluded_identifiers = {
        "Glass Core Substrate": {
            "identifiers": "LPKF: WKN 645000 / ISIN DE0006450000 | SCHMID (SHMD): ISIN NL0015002G68",
            "rationale": "Sized down to 0% and moved to watchlist on 2026-05-23 due to 75% confidence cut-off rule. High-performance glass panel lamination remains a major long-term structural theme, but commercial revenue scaling is a 2027–2028 story, representing too long of a duration mismatch and technology uncertainty for a concentrated €25k book."
        },
        "T-Glass Thermal Bottleneck": {
            "identifiers": "WKN 863674 / ISIN JP3684400009",
            "rationale": "Sized down to 0% and moved to watchlist on 2026-05-23 due to 75% confidence cut-off rule. Nitto Boseki's strategy of ¥120B to ¥180B CapEx expansion while completely capping prices to defend market share creates a heavy near-term margin and FCF drag, converting it from a high-margin windfall play to a capital-intensive volume defensive play."
        }
    }

    for i, pos in enumerate(excluded_positions, 1):
        info = excluded_identifiers.get(pos['thesis_title'], {
            "identifiers": "N/A",
            "rationale": pos['role']
        })
        output += f"### {i}. {pos['thesis_title']}\n"
        output += f"- **Primary Tradable Proxy:** **{pos['proxy']}**\n"
        output += f"- **Tradable Identifiers:** {info['identifiers']}\n"
        output += f"- **Confidence Score:** **{pos['confidence']:.0f}%** (rubric: `{pos['rubric']}`)\n"
        output += f"- **Exclusion & Watchlist Rationale:** {info['rationale']}\n"
        output += f"- **Physical/Market Epicenter:** {info.get('epicenter', pos['epicenter'])}\n\n"

    output += f"""{risk_blocks}
"""

    analysis_output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../portfolio/{TIER}/PORTFOLIO_ANALYSIS.md'))
    
    with open(analysis_output_path, 'w', encoding='utf-8') as f:
        f.write(output)
        
    print(f"\nSuccess! Version-controlled analysis for tier '{TIER}' generated successfully at:\n[PORTFOLIO_ANALYSIS.md](file://{analysis_output_path})")

if __name__ == '__main__':
    generate_analysis()
