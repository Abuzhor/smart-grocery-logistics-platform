#!/usr/bin/env python3
"""
Generate issues.json from PHASE-0-notion-to-github-execution-plan.md

This script parses the execution plan markdown and extracts all 40 issue definitions
into a structured JSON file for use by bootstrap automation.

Usage:
    python3 scripts/planning/generate_issues_json.py
"""

import re
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Paths
SCRIPT_DIR = Path(__file__).parent
EXECUTION_PLAN_PATH = SCRIPT_DIR / "../../docs/planning/PHASE-0-notion-to-github-execution-plan.md"
OUTPUT_PATH = SCRIPT_DIR / "issues.json"

def _load_canonical_defaults() -> Dict[str, List[str]]:
    repo_root = SCRIPT_DIR.parents[1]
    sys.path.insert(0, str(repo_root))
    try:
        from scripts.quality import canonical

        return {
            "phases": list(canonical.PHASES),
            "domains": list(canonical.DOMAINS),
            "priorities": list(canonical.PRIORITIES),
        }
    except Exception:
        return {
            "phases": ["PHASE 0", "PHASE 1", "PHASE 2", "PHASE 3", "PHASE 4"],
            "domains": [
                "Catalog",
                "Inventory",
                "Ordering",
                "Fulfillment",
                "Routing",
                "Partner",
                "Workforce",
                "Operations",
                "Compliance",
                "Platform",
            ],
            "priorities": ["Critical", "High", "Medium", "Low"],
        }


_CANONICAL = _load_canonical_defaults()

# Milestone mapping from phase labels to milestone titles
MILESTONE_MAP = {
    "phase:0-bootstrap": "PHASE 0: Bootstrap & Planning",
    "phase:1-foundation": "PHASE 1: Foundation",
    "phase:2-mvp": "PHASE 2: MVP Launch",
    "phase:3-scale": "PHASE 3: Scale & Optimize",
    "phase:4-global": "PHASE 4: Global Expansion",
}

# Phase to single-select value mapping
PHASE_MAP = {
    "phase:0-bootstrap": _CANONICAL["phases"][0],
    "phase:1-foundation": _CANONICAL["phases"][1],
    "phase:2-mvp": _CANONICAL["phases"][2],
    "phase:3-scale": _CANONICAL["phases"][3],
    "phase:4-global": _CANONICAL["phases"][4],
}

# Domain label to single-select value mapping
DOMAIN_MAP = {
    "domain:catalog": _CANONICAL["domains"][0],
    "domain:inventory": _CANONICAL["domains"][1],
    "domain:ordering": _CANONICAL["domains"][2],
    "domain:fulfillment": _CANONICAL["domains"][3],
    "domain:routing": _CANONICAL["domains"][4],
    "domain:partner": _CANONICAL["domains"][5],
    "domain:workforce": _CANONICAL["domains"][6],
    "domain:operations": _CANONICAL["domains"][7],
    "domain:compliance": _CANONICAL["domains"][8],
    "domain:platform": _CANONICAL["domains"][9],
}

# Priority label to single-select value mapping
PRIORITY_MAP = {
    "priority:critical": _CANONICAL["priorities"][0],
    "priority:high": _CANONICAL["priorities"][1],
    "priority:medium": _CANONICAL["priorities"][2],
    "priority:low": _CANONICAL["priorities"][3],
}


def extract_issue_blocks(content: str) -> List[str]:
    """Extract individual issue blocks from markdown content"""
    # Pattern to match issue blocks (from #### Issue #X: to next #### or end of section)
    pattern = r'####\s+Issue\s+#\d+:.*?(?=####\s+Issue\s+#|\n##\s+|$)'
    issues = re.findall(pattern, content, re.DOTALL)
    
    # Also extract the meta issue (uses **Issue #1:** format)
    meta_pattern = r'\*\*Issue\s+#1:.*?(?=###\s+PHASE\s+0\s+Issues|$)'
    meta_issue = re.findall(meta_pattern, content, re.DOTALL)
    
    # Combine meta issue first, then other issues
    all_issues = meta_issue + issues
    return all_issues


def parse_issue_block(block: str) -> Optional[Dict]:
    """Parse a single issue block into structured data"""
    
    # Extract title (handle both #### and ** formats)
    title_match = re.search(r'(?:####|\*\*)\s+Issue\s+#\d+:\s+(.+?)(?:\*\*|\n|$)', block)
    if not title_match:
        return None
    title = title_match.group(1).strip()
    
    # Extract labels
    labels_match = re.search(r'-\s+\*\*Labels\*\*:\s+(.+?)(?:\n|$)', block)
    labels = []
    if labels_match:
        labels_str = labels_match.group(1).strip()
        # Extract labels in backticks
        labels = re.findall(r'`([^`]+)`', labels_str)
    
    # Extract milestone
    milestone_match = re.search(r'-\s+\*\*Milestone\*\*:\s+(.+?)(?:\n|$)', block)
    milestone = None
    if milestone_match:
        milestone_str = milestone_match.group(1).strip()
        # Map from PHASE X to full milestone title
        for label, full_milestone in MILESTONE_MAP.items():
            if label in labels:
                milestone = full_milestone
                break
    
    # Extract description
    description_match = re.search(r'-\s+\*\*Description\*\*:\s+(.+?)(?:\n|$)', block)
    description = description_match.group(1).strip() if description_match else ""
    
    # Extract all sections for body (everything after title)
    body_parts = []
    
    # Add description
    if description:
        body_parts.append(f"## Description\n\n{description}")
    
    # Extract acceptance criteria
    ac_match = re.search(r'-\s+\*\*Acceptance Criteria\*\*:(.+?)(?=\n-\s+\*\*|$)', block, re.DOTALL)
    if ac_match:
        ac_text = ac_match.group(1).strip()
        body_parts.append(f"\n## Acceptance Criteria\n\n{ac_text}")
    
    # Extract KPI references
    kpi_match = re.search(r'-\s+\*\*KPI References\*\*:(.+?)(?=\n-\s+\*\*|$)', block, re.DOTALL)
    kpi_refs = []
    if kpi_match:
        kpi_text = kpi_match.group(1).strip()
        body_parts.append(f"\n## KPI References\n\n{kpi_text}")
        # Extract markdown links for notion reference field
        kpi_refs = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', kpi_text)
    
    # Extract source
    source_match = re.search(r'-\s+\*\*Source\*\*:\s+(.+?)(?=\n-\s+\*\*|$)', block, re.DOTALL)
    source_refs = []
    if source_match:
        source_text = source_match.group(1).strip()
        body_parts.append(f"\n## Source\n\n{source_text}")
        # Extract markdown links
        source_refs = re.findall(r'\[`([^`]+)`\]\(([^)]+)\)', source_text)
    
    # Extract related issues
    related_match = re.search(r'-\s+\*\*Related Issues\*\*:\s+(.+?)(?:\n|$)', block)
    if related_match:
        related_text = related_match.group(1).strip()
        body_parts.append(f"\n## Related Issues\n\n{related_text}")
    
    # Build complete body
    body = "\n".join(body_parts)
    
    # Determine project metadata
    phase = None
    domain = None
    priority = None
    
    for label in labels:
        if label in PHASE_MAP:
            phase = PHASE_MAP[label]
        if label in DOMAIN_MAP:
            domain = DOMAIN_MAP[label]
        if label in PRIORITY_MAP:
            priority = PRIORITY_MAP[label]
    
    # Build Notion reference from source links
    notion_refs = []
    for _, url in source_refs:
        if 'docs/notion-export' in url:
            notion_refs.append(url)
    
    notion_reference = ", ".join(notion_refs) if notion_refs else ""
    
    return {
        "title": title,
        "body": body,
        "labels": labels,
        "milestone": milestone,
        "project": {
            "phase": phase,
            "domain": domain,
            "priority": priority,
            "notion_reference": notion_reference
        }
    }


def main():
    """Main execution"""
    print("Parsing PHASE-0-notion-to-github-execution-plan.md...")
    
    # Read execution plan
    if not EXECUTION_PLAN_PATH.exists():
        print(f"Error: Execution plan not found at {EXECUTION_PLAN_PATH}")
        return 1
    
    with open(EXECUTION_PLAN_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract issue blocks
    issue_blocks = extract_issue_blocks(content)
    print(f"Found {len(issue_blocks)} issue blocks")
    
    # Parse each issue
    issues = []
    
    # Add meta issue manually (Issue #1) since it has a special format
    meta_issue = {
        "title": "PHASE 0 – Notion → GitHub Execution Plan",
        "body": """## Description

Master tracking issue for PHASE 0 execution

## Acceptance Criteria

  - [x] Execution plan document created
  - [ ] All labels created in repository
  - [ ] All milestones created
  - [ ] All mapped issues created with proper traceability
  - [ ] Projects v2 board configured
  - [ ] All issues added to project board

## KPI References

  - Setup completeness: 100% of artifacts created
  - Traceability: All issues link to source documentation

## Source

`docs/notion-export/index.md`, `docs/notion-export/00-executive-summary.md`""",
        "labels": ["phase:0-bootstrap", "type:documentation", "priority:critical"],
        "milestone": "PHASE 0: Bootstrap & Planning",
        "project": {
            "phase": _CANONICAL["phases"][0],
            "domain": None,
            "priority": _CANONICAL["priorities"][0],
            "notion_reference": "https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/index.md, https://github.com/Abuzhor/smart-grocery-logistics-platform/blob/main/docs/notion-export/00-executive-summary.md"
        }
    }
    issues.append(meta_issue)
    print(f"  ✓ Added meta issue: {meta_issue['title'][:60]}...")
    
    for i, block in enumerate(issue_blocks[1:], 2):  # Skip first (meta) block, start from #2
        issue = parse_issue_block(block)
        if issue:
            issues.append(issue)
            print(f"  ✓ Parsed Issue #{i}: {issue['title'][:60]}...")
        else:
            print(f"  ✗ Failed to parse issue block {i}")
    
    print(f"\nSuccessfully parsed {len(issues)} issues")
    
    # Write to JSON
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(issues, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Generated {OUTPUT_PATH}")
    print(f"  Total issues: {len(issues)}")
    
    # Summary by phase
    phase_counts = {}
    for issue in issues:
        phase = issue['project'].get('phase', 'Unknown')
        phase_counts[phase] = phase_counts.get(phase, 0) + 1
    
    print("\nBreakdown by phase:")
    for phase, count in sorted(phase_counts.items()):
        print(f"  {phase}: {count} issues")
    
    return 0


if __name__ == "__main__":
    exit(main())
