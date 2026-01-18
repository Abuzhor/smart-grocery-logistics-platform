#!/usr/bin/env bash

set -euo pipefail

# Bootstrap GitHub Labels, Milestones, and Issues
# This script is idempotent - safe to re-run multiple times
# 
# Usage:
#   export GH_TOKEN=<your-github-token>
#   export GITHUB_REPOSITORY=Abuzhor/smart-grocery-logistics-platform
#   ./scripts/planning/bootstrap_github.sh

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Repository (can be overridden by environment variable)
REPO="${GITHUB_REPOSITORY:-Abuzhor/smart-grocery-logistics-platform}"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}GitHub Bootstrap Script for ${REPO}${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Verify gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}"
    echo "Install from: https://cli.github.com/"
    exit 1
fi

# Verify authentication
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub CLI${NC}"
    echo "Run: gh auth login"
    exit 1
fi

echo -e "${GREEN}✓ GitHub CLI authenticated${NC}"
echo ""

# Helper function to create or update label
create_label() {
    local name="$1"
    local color="$2"
    local description="$3"
    
    # Remove # from color if present
    color="${color#\#}"
    
    if gh label list --repo "$REPO" --limit 1000 | grep -q "^${name}[[:space:]]"; then
        echo -e "${YELLOW}  ↻ Label exists: ${name}${NC}"
        # Update description if needed
        gh label edit "$name" --repo "$REPO" --description "$description" --color "$color" 2>/dev/null || true
    else
        gh label create "$name" --repo "$REPO" --color "$color" --description "$description"
        echo -e "${GREEN}  ✓ Created label: ${name}${NC}"
    fi
}

# Helper function to create or update milestone
create_milestone() {
    local title="$1"
    local due_date="$2"
    local description="$3"
    
    # Check if milestone exists and get its number
    local milestone_number=$(gh api "repos/${REPO}/milestones?state=all" --jq ".[] | select(.title == \"${title}\") | .number" 2>/dev/null)
    
    if [ -n "$milestone_number" ]; then
        # Update existing milestone
        if [ -n "$due_date" ]; then
            gh api "repos/${REPO}/milestones/${milestone_number}" -X PATCH \
                -f title="$title" \
                -f description="$description" \
                -f due_on="${due_date}T23:59:59Z" > /dev/null
        else
            gh api "repos/${REPO}/milestones/${milestone_number}" -X PATCH \
                -f title="$title" \
                -f description="$description" > /dev/null
        fi
        echo -e "${YELLOW}  ↻ Updated milestone: ${title}${NC}"
    else
        # Create new milestone
        if [ -n "$due_date" ]; then
            gh api "repos/${REPO}/milestones" -X POST \
                -f title="$title" \
                -f description="$description" \
                -f due_on="${due_date}T23:59:59Z" > /dev/null
        else
            gh api "repos/${REPO}/milestones" -X POST \
                -f title="$title" \
                -f description="$description" > /dev/null
        fi
        echo -e "${GREEN}  ✓ Created milestone: ${title}${NC}"
    fi
}

# Helper function to get milestone number
get_milestone_number() {
    local title="$1"
    gh api "repos/${REPO}/milestones" --jq ".[] | select(.title == \"${title}\") | .number"
}

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Step 1: Creating Labels${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

echo "Creating Phase Labels..."
create_label "phase:0-bootstrap" "0E8A16" "PHASE 0: Project bootstrap and planning setup"
create_label "phase:1-foundation" "1D76DB" "PHASE 1: Core platform foundation"
create_label "phase:2-mvp" "5319E7" "PHASE 2: MVP features and launch"
create_label "phase:3-scale" "D93F0B" "PHASE 3: Scaling and optimization"
create_label "phase:4-global" "FBCA04" "PHASE 4: Global expansion"

echo ""
echo "Creating Domain Labels..."
create_label "domain:catalog" "C5DEF5" "Catalog and product management"
create_label "domain:inventory" "BFD4F2" "Inventory management and tracking"
create_label "domain:ordering" "D4C5F9" "Order capture and orchestration"
create_label "domain:fulfillment" "C2E0C6" "Fulfillment and picking operations"
create_label "domain:routing" "FEF2C0" "Route optimization and delivery"
create_label "domain:partner" "F9D0C4" "Partner integration and management"
create_label "domain:workforce" "E99695" "Workforce and driver management"
create_label "domain:operations" "D73A4A" "Operations and monitoring"
create_label "domain:compliance" "0052CC" "Compliance and regulatory"
create_label "domain:platform" "5319E7" "Platform infrastructure"

echo ""
echo "Creating Type Labels..."
create_label "type:documentation" "0075CA" "Documentation and planning"
create_label "type:architecture" "1D76DB" "Architecture and design decisions"
create_label "type:feature" "A2EEEF" "New feature implementation"
create_label "type:infrastructure" "D876E3" "Infrastructure and DevOps"
create_label "type:testing" "BFD4F2" "Testing and quality assurance"
create_label "type:security" "D93F0B" "Security and vulnerability fixes"
create_label "type:compliance-task" "0052CC" "Compliance implementation task"

echo ""
echo "Creating Priority Labels..."
create_label "priority:critical" "B60205" "Critical - must be done immediately"
create_label "priority:high" "D93F0B" "High priority"
create_label "priority:medium" "FBCA04" "Medium priority"
create_label "priority:low" "0E8A16" "Low priority"

echo ""
echo "Creating Category Labels..."
create_label "category:grocery" "C2E0C6" "Grocery and food items"
create_label "category:cold-chain" "BFD4F2" "Cold chain and refrigeration"
create_label "category:regulated" "0052CC" "Regulated items (age, prescription)"
create_label "category:services" "FEF2C0" "Service delivery (non-physical)"
create_label "category:b2b" "5319E7" "Business-to-business operations"

echo ""
echo "Creating Gate Labels..."
create_label "gate:reliability" "0E8A16" "Reliability gate criteria"
create_label "gate:economics" "FBCA04" "Economics and unit profitability gate"
create_label "gate:trust" "D93F0B" "Trust and fraud prevention gate"
create_label "gate:compliance" "0052CC" "Compliance and regulatory gate"

echo ""
echo -e "${GREEN}✓ All labels created/updated${NC}"
echo ""

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Step 2: Creating Milestones${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Read milestones from config.json and create them
CONFIG_FILE="$(dirname "$0")/config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: config.json not found at ${CONFIG_FILE}${NC}"
    exit 1
fi

# Extract and create milestones using jq
milestone_count=0
while IFS= read -r milestone; do
    title=$(echo "$milestone" | jq -r '.title')
    due_days=$(echo "$milestone" | jq -r '.due_days')
    description=$(echo "$milestone" | jq -r '.description')
    
    # Calculate due date
    if command -v date &> /dev/null; then
        if date --version &> /dev/null 2>&1; then
            # GNU date (Linux)
            due_date=$(date -u -d "+${due_days} days" +%Y-%m-%d)
        else
            # BSD date (macOS)
            due_date=$(date -u -v +${due_days}d +%Y-%m-%d)
        fi
    else
        echo -e "${YELLOW}Warning: date command not available, skipping due date${NC}"
        due_date=""
    fi
    
    create_milestone "$title" "$due_date" "$description"
    milestone_count=$((milestone_count + 1))
done < <(jq -c '.milestones[]' "$CONFIG_FILE")

echo ""
echo -e "${GREEN}✓ All milestones created/updated (${milestone_count} total)${NC}"
echo ""

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${GREEN}Labels:${NC} 31 labels created/updated across 6 categories"
echo -e "${GREEN}Milestones:${NC} ${milestone_count} milestones created/updated with due dates"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. Generate issues.json: python3 scripts/planning/generate_issues_json.py"
echo "2. Create all 40 issues and setup Projects v2 board:"
echo "   python3 scripts/planning/bootstrap_github.py"
echo "3. Review created artifacts:"
echo "   - Labels: https://github.com/${REPO}/labels"
echo "   - Milestones: https://github.com/${REPO}/milestones"
echo "   - Issues: https://github.com/${REPO}/issues"
echo ""
echo -e "${GREEN}✓ Labels and milestones bootstrap complete!${NC}"
echo ""
