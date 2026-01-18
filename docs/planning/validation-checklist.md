# Bootstrap Scripts Validation Checklist

This document tracks the validation and testing status of the PHASE 0 bootstrap scripts.

## Pre-Execution Validation

### Script Syntax and Structure
- [x] `generate_issues_json.py` - Python syntax validated
- [x] `bootstrap_github.sh` - Bash syntax validated
- [x] `bootstrap_github.py` - Python syntax validated
- [x] Scripts are executable (`chmod +x` for .sh)
- [x] Scripts include proper error handling
- [x] Scripts include usage documentation
- [x] Scripts are idempotent (safe to re-run)

### Configuration Files
- [x] `config.json` created with label and milestone definitions
- [x] All 31 labels defined (6 categories)
- [x] All 5 milestones defined with due dates
- [x] Configuration matches execution plan
- [x] `issues.json` schema defined (40 issues)

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

### Step 1: generate_issues_json.py Execution
- [ ] Script runs without syntax errors
- [ ] Parses all 40 issue blocks from execution plan
- [ ] Generates `scripts/planning/issues.json`
- [ ] JSON is valid and well-formed
- [ ] All 40 issues present in output
- [ ] Breakdown by phase matches execution plan:
  - [ ] PHASE 0: 10 issues
  - [ ] PHASE 1: 10 issues
  - [ ] PHASE 2: 9 issues
  - [ ] PHASE 3: 5 issues
  - [ ] PHASE 4: 6 issues
- [ ] Each issue has all required fields (title, body, labels, milestone, project metadata)
- [ ] Script can be re-run without errors (idempotency test)

### Step 2: bootstrap_github.sh Execution
- [ ] Script runs without syntax errors
- [ ] All 31 labels created successfully
- [ ] All 5 milestones created/updated successfully
- [ ] Milestones have correct due_on dates (calculated from config.json due_days)
- [ ] Script is idempotent (can be re-run without errors)
- [ ] Script prints summary with label and milestone counts
- [ ] Verify labels at: `https://github.com/Abuzhor/smart-grocery-logistics-platform/labels`
- [ ] Verify milestones at: `https://github.com/Abuzhor/smart-grocery-logistics-platform/milestones`
- [ ] Verify milestone due dates are set correctly (not empty)

### Step 3: bootstrap_github.py Execution (First Run)
- [ ] Script runs without syntax errors
- [ ] Successfully loads `issues.json` (40 issues)
- [ ] Fetches existing milestones and creates milestone mapping
- [ ] Auto-detects owner type (User or Organization)
- [ ] Prints detected owner type correctly
- [ ] Creates all 40 issues with correct:
  - [ ] Titles (matching execution plan exactly)
  - [ ] Bodies (full markdown with objectives, acceptance criteria, KPI refs, sources)
  - [ ] Labels (phase, domain, type, priority, gates as specified)
  - [ ] Milestones (PHASE 0-4 as specified)
- [ ] Projects v2 board created successfully (or reuses existing)
- [ ] Custom fields created:
  - [ ] Phase (Single select with 5 options)
  - [ ] Domain (Single select with 10 options)
  - [ ] Priority (Single select with 4 options)
  - [ ] Notion Reference (Text field)
- [ ] All 40 issues added to project board
- [ ] Project field values set for all 40 issues:
  - [ ] Phase field populated
  - [ ] Domain field populated (where applicable)
  - [ ] Priority field populated
  - [ ] Notion Reference field populated with source links
- [ ] Script prints clear summary:
  - [ ] Repository and owner type displayed
  - [ ] Created count: 40
  - [ ] Updated count: 0
  - [ ] Skipped count: 0
  - [ ] Project URL displayed
  - [ ] Added to project count displayed
  - [ ] Field values updated count displayed
- [ ] Verify all 40 issues at: `https://github.com/Abuzhor/smart-grocery-logistics-platform/issues`
- [ ] Verify project board at: (check script output for URL)

### Step 4: bootstrap_github.py Execution (Second Run - Idempotency Test)
- [ ] Script runs without errors
- [ ] Fetches existing issues (should find all 40)
- [ ] Matches issues by exact title
- [ ] Shows skipped count: 40 (no changes needed)
- [ ] Created count: 0
- [ ] Updated count: 0
- [ ] No duplicate issues created
- [ ] Project items not duplicated
- [ ] Field values retained

### Step 5: bootstrap_github.py Execution (Update Test)
Manually edit one issue's body or labels in GitHub UI, then re-run:
- [ ] Script detects the change
- [ ] Updates the modified issue
- [ ] Shows update count: 1
- [ ] Created count: 0
- [ ] Skipped count: 39
- [ ] Labels are authoritatively synced (removes unintended labels)
- [ ] Milestone updated if changed
- [ ] Body restored to source of truth

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

## Traceability Validation

For a sample of created issues (test issues #1, #12, #25, #31, #40), verify:
- [ ] Issue title matches execution plan exactly
- [ ] Issue description includes objectives section
- [ ] Acceptance criteria are clear and testable
- [ ] KPI references are present and well-formatted
- [ ] Source documentation links are present
- [ ] Related issues are cross-referenced (where applicable)
- [ ] Labels are correctly applied
- [ ] Milestone is correctly set
- [ ] Project fields are populated:
  - [ ] Phase field matches phase label
  - [ ] Domain field matches domain label (where applicable)
  - [ ] Priority field matches priority label
  - [ ] Notion Reference field has source links

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
Sample 10 issues across all phases and verify:
- [ ] Title is descriptive and action-oriented
- [ ] Description is comprehensive with all sections
- [ ] Acceptance criteria are specific and measurable
- [ ] KPI references are accurate
- [ ] Source documentation references are present
- [ ] Related issues are relevant (where applicable)
- [ ] Labels are appropriate and complete
- [ ] Milestone is correct
- [ ] No hardcoded issue numbers in issue bodies

### Project Board Quality
- [ ] All 40 issues visible in project
- [ ] Phase field distribution:
  - [ ] PHASE 0: 10 issues
  - [ ] PHASE 1: 10 issues
  - [ ] PHASE 2: 9 issues
  - [ ] PHASE 3: 5 issues
  - [ ] PHASE 4: 6 issues
- [ ] Domain field populated for all applicable issues
- [ ] Priority field populated for all issues
- [ ] Notion Reference field populated for all issues with source docs

## Rollback Plan

If validation fails or errors occur:

1. **issues.json**: Can be safely regenerated
   ```bash
   python3 scripts/planning/generate_issues_json.py
   ```

2. **Labels**: Can be safely deleted and recreated
   ```bash
   # Delete all labels (careful!)
   gh label list --repo Abuzhor/smart-grocery-logistics-platform --json name --jq '.[].name' | \
     xargs -I {} gh label delete {} --repo Abuzhor/smart-grocery-logistics-platform --yes
   ```

3. **Milestones**: Can be deleted if no issues assigned
   ```bash
   # List and manually delete via web UI or API
   gh api repos/Abuzhor/smart-grocery-logistics-platform/milestones
   ```

4. **Issues**: Can be closed in bulk
   - Prefer closing over deleting for audit trail
   - Tag with "invalid" or "duplicate" label if needed
   - Delete via GitHub UI if truly needed

5. **Projects**: Can be deleted and recreated
   - Delete via web UI: Settings → Projects → Delete

## Success Criteria

PHASE 0 bootstrap is successful when:
- [x] Execution plan document exists and is comprehensive
- [x] Scripts are created, tested, and documented
- [x] `issues.json` generator created
- [ ] All labels are created (31 total)
- [ ] All milestones are created (5 total)
- [ ] **All 40 issues created** with full traceability
  - [ ] PHASE 0: 10 issues
  - [ ] PHASE 1: 10 issues
  - [ ] PHASE 2: 9 issues
  - [ ] PHASE 3: 5 issues
  - [ ] PHASE 4: 6 issues
- [ ] Projects v2 board is created and configured
- [ ] All 40 issues are added to project board
- [ ] All project custom fields set for all 40 issues
- [ ] Traceability is complete (all issues → Notion export)
- [ ] Scripts are idempotent (verified by re-run):
  - [ ] First run creates 40 issues
  - [ ] Second run creates 0 duplicates
  - [ ] Update run modifies only changed issues
- [ ] Documentation is clear and usable
- [ ] No hardcoded issue numbers anywhere

## Notes

- Scripts are designed to be fully idempotent - safe to run multiple times
- Issues are matched by exact title for upsert logic
- Labels are authoritatively synced (removes labels not in intended set)
- Manual steps (board views) should be documented but are optional
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
