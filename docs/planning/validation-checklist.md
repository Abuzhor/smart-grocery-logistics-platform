# Bootstrap Scripts Validation Checklist

This document tracks the validation and testing status of the PHASE 0 bootstrap scripts.

## Pre-Execution Validation

### Script Syntax and Structure
- [x] `bootstrap_github.sh` - Bash syntax validated
- [x] `bootstrap_github.py` - Python syntax validated
- [x] Both scripts are executable (`chmod +x`)
- [x] Scripts include proper error handling
- [x] Scripts include usage documentation
- [x] Scripts are idempotent (safe to re-run)

### Configuration Files
- [x] `config.json` created with label and milestone definitions
- [x] All 31 labels defined (6 categories)
- [x] All 5 milestones defined with due dates
- [x] Configuration matches execution plan

### Documentation
- [x] Execution plan document created (`PHASE-0-notion-to-github-execution-plan.md`)
- [x] Scripts README created with usage instructions
- [x] All 40 issues mapped in execution plan
- [x] Traceability matrix complete (issues → Notion export)

## Execution Validation (To be completed by repository owner)

### Prerequisites Check
- [ ] GitHub CLI (`gh`) installed and available
- [ ] GitHub CLI authenticated (`gh auth status` succeeds)
- [ ] Repository access verified (owner or admin permissions)
- [ ] Python 3.7+ installed
- [ ] Python `requests` library installed (`pip install requests`)
- [ ] `GH_TOKEN` environment variable set (or `gh auth login` completed)

### bootstrap_github.sh Execution
- [ ] Script runs without syntax errors
- [ ] All 31 labels created successfully
- [ ] All 5 milestones created successfully
- [ ] Meta issue (#1) created successfully
- [ ] Sample issues (#2-3) created successfully
- [ ] Script displays clear warning about 3 sample issues vs 40 total
- [ ] Script prints summary with GitHub URLs
- [ ] Script can be re-run without errors (idempotency test)
- [ ] Verify labels at: `https://github.com/Abuzhor/smart-grocery-logistics-platform/labels`
- [ ] Verify milestones at: `https://github.com/Abuzhor/smart-grocery-logistics-platform/milestones`
- [ ] Verify 3 issues created at: `https://github.com/Abuzhor/smart-grocery-logistics-platform/issues`

### bootstrap_github.py Execution
- [ ] Script runs without syntax errors
- [ ] Projects v2 board created successfully
- [ ] Custom fields created:
  - [ ] Phase (Single select with 5 options)
  - [ ] Domain (Single select with 10 options)
  - [ ] Priority (Single select with 4 options)
  - [ ] Notion Reference (Text field)
- [ ] All issues added to project board
- [ ] Script can be re-run without errors (idempotency test)
- [ ] Verify project board at: `https://github.com/orgs/Abuzhor/projects` or user projects

## Manual Configuration (Post-Script)

After running the scripts, manually configure the following in the GitHub UI:

### Projects v2 Board Configuration
- [ ] Configure Status workflow automation:
  - [ ] "Backlog" - Default for new items
  - [ ] "Ready" - Manual move from Backlog
  - [ ] "In Progress" - Auto-set when PR linked or assignee set
  - [ ] "Review" - Auto-set when PR in review
  - [ ] "Blocked" - Manual set with reason
  - [ ] "Done" - Auto-set when PR merged or issue closed
- [ ] Create board views:
  - [ ] "Main Kanban Board" (default, grouped by Status)
  - [ ] "By Phase" (grouped by Phase field)
  - [ ] "By Domain" (grouped by Domain field)
  - [ ] "By Priority" (sorted by Priority field)
- [ ] Configure filters for each view as needed

### Issue Field Population
For each created issue, manually set (or via API):
- [ ] Phase field (from phase label)
- [ ] Domain field (from domain label)
- [ ] Priority field (from priority label)
- [ ] Notion Reference field (link to source doc)
- [ ] Initial Status = "Backlog"

## Issue Creation Completion

⚠️ **IMPORTANT**: The bootstrap script creates **3 sample issues only** (#1-3), not all 40.

### Current Status
- ✅ Issues #1-3 created by script (meta issue + 2 examples)
- ⚠️ Issues #4-40 documented in execution plan but NOT auto-created

### Option 1: Extend bootstrap_github.sh
- [ ] Add issue templates for remaining 37 issues (see execution plan)
- [ ] Re-run script to create all issues

### Option 2: Manual Creation (Recommended)
- [ ] Create remaining 37 issues manually using execution plan as template
- [ ] Ensure all issues include:
  - [ ] Clear title matching execution plan
  - [ ] Complete description with objectives, deliverables, acceptance criteria
  - [ ] KPI references with links to Notion export
  - [ ] Source documentation links
  - [ ] Related issue cross-references
  - [ ] Appropriate labels (phase, domain, type, priority, gates)
  - [ ] Associated milestone

### Option 3: Use GitHub API/CLI
- [ ] Create script to batch-create issues from execution plan
- [ ] Validate issue format and traceability
- [ ] Run and verify

## Traceability Validation

For a sample of created issues, verify:
- [ ] Issue title matches execution plan
- [ ] Issue description includes objectives
- [ ] Acceptance criteria are clear and testable
- [ ] KPI references link to correct Notion export files and line numbers
- [ ] Source documentation links are valid GitHub blob URLs
- [ ] Related issues are cross-referenced by number
- [ ] Labels are correctly applied
- [ ] Milestone is correctly set

## Quality Checks

### Label Taxonomy
- [ ] All label names follow naming convention (category:value)
- [ ] Label colors are visually distinct within categories
- [ ] Label descriptions are clear and concise
- [ ] No duplicate labels

### Milestone Planning
- [ ] Milestone titles are clear and follow naming convention
- [ ] Due dates are reasonable (30, 90, 180, 270, 365 days)
- [ ] Milestone descriptions explain scope
- [ ] No duplicate milestones

### Issue Quality
Sample 5-10 issues and verify:
- [ ] Title is descriptive and action-oriented
- [ ] Description is comprehensive
- [ ] Acceptance criteria are specific and measurable
- [ ] KPI references are accurate and link to source
- [ ] Source documentation links work
- [ ] Related issues are relevant
- [ ] Labels are appropriate
- [ ] Milestone is correct

## Rollback Plan

If validation fails or errors occur:

1. **Labels**: Can be safely deleted and recreated
   ```bash
   # Delete all labels (careful!)
   gh label list --repo Abuzhor/smart-grocery-logistics-platform --json name --jq '.[].name' | \
     xargs -I {} gh label delete {} --repo Abuzhor/smart-grocery-logistics-platform --yes
   ```

2. **Milestones**: Can be deleted if no issues assigned
   ```bash
   # List and manually delete via web UI or API
   gh api repos/Abuzhor/smart-grocery-logistics-platform/milestones
   ```

3. **Issues**: Can be closed/deleted (but keep for traceability)
   - Prefer closing over deleting
   - Tag with "invalid" or "duplicate" label if needed

4. **Projects**: Can be deleted and recreated
   - Delete via web UI: Settings → Projects → Delete

## Success Criteria

PHASE 0 bootstrap is successful when:
- [x] Execution plan document exists and is comprehensive
- [x] Scripts are created, tested, and documented
- [ ] All labels are created (31 total)
- [ ] All milestones are created (5 total)
- [ ] **3 sample issues created** (#1-3) with full traceability
- [ ] **Remaining 37 issues** (#4-40) created manually or via script extension
- [ ] Projects v2 board is created and configured
- [ ] All issues are added to project board
- [ ] Traceability is complete (all issues → Notion export)
- [ ] Scripts are idempotent (verified by re-run)
- [ ] Documentation is clear and usable

## Notes

- Scripts are designed to be idempotent - safe to run multiple times
- Existing labels/milestones/issues will be updated, not duplicated
- Manual steps (board views, field population) should be documented
- Keep this checklist updated as validation progresses

## Sign-off

- [ ] Technical validation complete (scripts work correctly)
- [ ] Content validation complete (all issues match execution plan)
- [ ] Traceability validation complete (all links work)
- [ ] Documentation validation complete (README is clear)
- [ ] Ready for team use

---

**Last Updated**: 2026-01-08  
**Validated By**: _[Name/Date when validation is complete]_  
**Status**: **In Progress** → Ready for execution by repository owner
