# Planning Scripts

This directory contains automation scripts for bootstrapping and managing GitHub project artifacts.

## Overview

These scripts transform the Notion export documentation (`docs/notion-export/**`) into actionable GitHub issues, labels, milestones, and a Projects v2 board.

## Scripts

### bootstrap_github.sh

Bash script that creates GitHub labels, milestones, and issues using the GitHub CLI (`gh`).

**Prerequisites:**
- GitHub CLI (`gh`) installed: https://cli.github.com/
- Authenticated with GitHub: `gh auth login`
- `GH_TOKEN` environment variable set (or authenticated via `gh auth login`)

**Usage:**
```bash
export GH_TOKEN=<your-github-token>
export GITHUB_REPOSITORY=Abuzhor/smart-grocery-logistics-platform

./scripts/planning/bootstrap_github.sh
```

**Features:**
- ✓ Idempotent - safe to re-run multiple times
- ✓ Creates 31 labels across 6 categories
- ✓ Creates 5 milestones (PHASE 0-4)
- ✓ Creates 3 sample issues (#1-3) with full traceability
- ⚠️ **Note**: Creates 3 sample issues only. Remaining 37 issues need manual creation or script extension
- ✓ Prints summary with GitHub URLs

**What it creates:**

1. **Labels** (6 categories):
   - Phase labels: `phase:0-bootstrap`, `phase:1-foundation`, etc.
   - Domain labels: `domain:catalog`, `domain:inventory`, etc.
   - Type labels: `type:documentation`, `type:feature`, etc.
   - Priority labels: `priority:critical`, `priority:high`, etc.
   - Category labels: `category:grocery`, `category:cold-chain`, etc.
   - Gate labels: `gate:reliability`, `gate:economics`, etc.

2. **Milestones** (5 phases):
   - PHASE 0: Bootstrap & Planning (+30 days)
   - PHASE 1: Foundation (+90 days)
   - PHASE 2: MVP Launch (+180 days)
   - PHASE 3: Scale & Optimize (+270 days)
   - PHASE 4: Global Expansion (+365 days)

3. **Issues** (3 sample issues):
   - Issue #1: Meta issue for PHASE 0 tracking
   - Issue #2: Bootstrap GitHub Project Automation
   - Issue #3: Define Vision and North Star Metrics
   - ⚠️ **Remaining 37 issues** documented in execution plan but not auto-created

### bootstrap_github.py

Python script that creates a GitHub Projects v2 board using the GraphQL API.

**Prerequisites:**
- Python 3.7+
- `requests` library: `pip install requests`
- `GH_TOKEN` environment variable set

**Usage:**
```bash
export GH_TOKEN=<your-github-token>

# Install dependencies
pip install requests

# Run script
python3 scripts/planning/bootstrap_github.py
```

**Features:**
- ✓ Creates Projects v2 board
- ✓ Configures custom fields (Phase, Domain, Priority, Notion Reference)
- ✓ Adds all repository issues to the project
- ✓ Idempotent - checks for existing project

**What it creates:**

1. **Project Board**: "Smart Grocery Logistics Platform - Execution Board"

2. **Custom Fields**:
   - Phase (Single select): PHASE 0, PHASE 1, PHASE 2, PHASE 3, PHASE 4
   - Domain (Single select): Catalog, Inventory, Ordering, Fulfillment, etc.
   - Priority (Single select): Critical, High, Medium, Low
   - Notion Reference (Text): Link to source documentation

3. **Default Status Column**: Uses GitHub's built-in Status field

## Execution Order

Run the scripts in this order:

```bash
# 1. Create labels, milestones, and issues
./scripts/planning/bootstrap_github.sh

# 2. Create Projects v2 board and add issues
python3 scripts/planning/bootstrap_github.py
```

## Configuration

All configuration is centralized in the execution plan document:
- `docs/planning/PHASE-0-notion-to-github-execution-plan.md`

To modify labels, milestones, or issue templates:
1. Update the execution plan document
2. Update the scripts accordingly
3. Re-run the scripts (they are idempotent)

## Troubleshooting

### GitHub CLI Authentication

If you get authentication errors:
```bash
gh auth login
gh auth status
```

### Python Dependencies

If you get import errors:
```bash
pip install requests
```

### GraphQL API Errors

If Projects v2 creation fails:
- Ensure you have the correct permissions (owner or admin)
- Check that the repository exists
- Verify the `GH_TOKEN` has `project` scope

### Rate Limiting

If you hit rate limits:
- Wait a few minutes between runs
- The scripts are idempotent, so you can safely re-run them

## Maintenance

### Adding New Issues

1. Add issue definition to execution plan document
2. Update `bootstrap_github.sh` with new issue template
3. Run the script to create the issue
4. Run `bootstrap_github.py` to add it to the project board

### Updating Labels or Milestones

1. Update taxonomy in execution plan document
2. Modify scripts with new definitions
3. Re-run `bootstrap_github.sh` (updates existing labels/milestones)

### Regenerating Everything

To completely regenerate from scratch:
1. Manually delete all issues, labels, milestones, and project (if desired)
2. Run `bootstrap_github.sh`
3. Run `bootstrap_github.py`

**Note**: The scripts are designed to be idempotent, so you typically don't need to delete anything.

## Support

For issues or questions:
1. Check the execution plan: `docs/planning/PHASE-0-notion-to-github-execution-plan.md`
2. Review script output for error messages
3. Open a GitHub issue with the `phase:0-bootstrap` label

## References

- [Execution Plan](../docs/planning/PHASE-0-notion-to-github-execution-plan.md)
- [Notion Export](../docs/notion-export/)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [GitHub Projects v2](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
