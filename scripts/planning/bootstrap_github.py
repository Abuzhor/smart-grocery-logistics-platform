#!/usr/bin/env python3
"""
Bootstrap GitHub Projects v2 Board

This script creates a GitHub Projects v2 board with custom fields and status columns,
then adds all created issues to the project.

Usage:
    export GH_TOKEN=<your-github-token>
    python3 scripts/planning/bootstrap_github.py

Requirements:
    - Python 3.7+
    - requests library (pip install requests)
    - GH_TOKEN environment variable set
"""

import os
import sys
import json
import requests
from typing import Dict, List, Optional, Any

# Configuration
REPO_OWNER = "Abuzhor"
REPO_NAME = "smart-grocery-logistics-platform"
PROJECT_TITLE = "Smart Grocery Logistics Platform - Execution Board"
PROJECT_DESCRIPTION = """
Execution board for tracking all phases of the Smart Grocery Logistics Platform development.
Source: docs/notion-export/** → GitHub Issues via PHASE 0 bootstrap.
"""

# Color codes for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_color(color: str, message: str):
    """Print colored message"""
    print(f"{color}{message}{Colors.NC}")

def print_header(message: str):
    """Print section header"""
    print_color(Colors.BLUE, "=" * 60)
    print_color(Colors.BLUE, message)
    print_color(Colors.BLUE, "=" * 60)
    print()

def get_github_token() -> str:
    """Get GitHub token from environment"""
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        print_color(Colors.RED, "Error: GH_TOKEN or GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    return token

class GitHubGraphQLClient:
    """GitHub GraphQL API client"""
    
    def __init__(self, token: str):
        self.token = token
        self.endpoint = "https://api.github.com/graphql"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def query(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Execute GraphQL query"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        response = requests.post(
            self.endpoint,
            headers=self.headers,
            json=payload
        )
        
        if response.status_code != 200:
            print_color(Colors.RED, f"GraphQL request failed: {response.status_code}")
            print_color(Colors.RED, response.text)
            sys.exit(1)
        
        result = response.json()
        
        if "errors" in result:
            print_color(Colors.RED, "GraphQL errors:")
            print_color(Colors.RED, json.dumps(result["errors"], indent=2))
            sys.exit(1)
        
        return result.get("data", {})

def get_repository_id(client: GitHubGraphQLClient, owner: str, name: str) -> str:
    """Get repository node ID"""
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        id
      }
    }
    """
    
    result = client.query(query, {"owner": owner, "name": name})
    return result["repository"]["id"]

def get_organization_id(client: GitHubGraphQLClient, login: str) -> str:
    """Get organization node ID"""
    query = """
    query($login: String!) {
      organization(login: $login) {
        id
      }
    }
    """
    
    result = client.query(query, {"login": login})
    return result["organization"]["id"]

def get_user_id(client: GitHubGraphQLClient, login: str) -> str:
    """Get user node ID"""
    query = """
    query($login: String!) {
      user(login: $login) {
        id
      }
    }
    """
    
    result = client.query(query, {"login": login})
    return result["user"]["id"]

def find_existing_project(client: GitHubGraphQLClient, owner: str, title: str) -> Optional[Dict]:
    """Find existing project by title"""
    # Try organization first
    try:
        owner_id = get_organization_id(client, owner)
        query = """
        query($ownerId: ID!, $first: Int!) {
          node(id: $ownerId) {
            ... on Organization {
              projectsV2(first: $first) {
                nodes {
                  id
                  number
                  title
                  url
                }
              }
            }
          }
        }
        """
        result = client.query(query, {"ownerId": owner_id, "first": 100})
        projects = result.get("node", {}).get("projectsV2", {}).get("nodes", [])
    except:
        # Try user if organization fails
        try:
            owner_id = get_user_id(client, owner)
            query = """
            query($ownerId: ID!, $first: Int!) {
              node(id: $ownerId) {
                ... on User {
                  projectsV2(first: $first) {
                    nodes {
                      id
                      number
                      title
                      url
                    }
                  }
                }
              }
            }
            """
            result = client.query(query, {"ownerId": owner_id, "first": 100})
            projects = result.get("node", {}).get("projectsV2", {}).get("nodes", [])
        except:
            return None
    
    for project in projects:
        if project["title"] == title:
            return project
    
    return None

def create_project(client: GitHubGraphQLClient, owner: str, title: str, description: str) -> Dict:
    """Create a new GitHub Project v2"""
    # Try to get owner ID (organization or user)
    try:
        owner_id = get_organization_id(client, owner)
    except:
        try:
            owner_id = get_user_id(client, owner)
        except:
            print_color(Colors.RED, f"Error: Could not find organization or user: {owner}")
            sys.exit(1)
    
    mutation = """
    mutation($ownerId: ID!, $title: String!, $body: String!) {
      createProjectV2(input: {ownerId: $ownerId, title: $title, body: $body}) {
        projectV2 {
          id
          number
          title
          url
        }
      }
    }
    """
    
    result = client.query(mutation, {
        "ownerId": owner_id,
        "title": title,
        "body": description
    })
    
    return result["createProjectV2"]["projectV2"]

def get_project_fields(client: GitHubGraphQLClient, project_id: str) -> List[Dict]:
    """Get existing fields for a project"""
    query = """
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          fields(first: 20) {
            nodes {
              ... on ProjectV2Field {
                id
                name
                dataType
              }
              ... on ProjectV2SingleSelectField {
                id
                name
                dataType
                options {
                  id
                  name
                }
              }
            }
          }
        }
      }
    }
    """
    
    result = client.query(query, {"projectId": project_id})
    return result["node"]["fields"]["nodes"]

def create_single_select_field(client: GitHubGraphQLClient, project_id: str, name: str, options: List[str]) -> Dict:
    """Create a single select custom field"""
    mutation = """
    mutation($projectId: ID!, $name: String!, $options: [ProjectV2SingleSelectFieldOptionInput!]!) {
      createProjectV2Field(input: {
        projectId: $projectId,
        dataType: SINGLE_SELECT,
        name: $name,
        singleSelectOptions: $options
      }) {
        projectV2Field {
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
        }
      }
    }
    """
    
    option_inputs = [{"name": opt, "color": "GRAY"} for opt in options]
    
    result = client.query(mutation, {
        "projectId": project_id,
        "name": name,
        "options": option_inputs
    })
    
    return result["createProjectV2Field"]["projectV2Field"]

def create_text_field(client: GitHubGraphQLClient, project_id: str, name: str) -> Dict:
    """Create a text custom field"""
    mutation = """
    mutation($projectId: ID!, $name: String!) {
      createProjectV2Field(input: {
        projectId: $projectId,
        dataType: TEXT,
        name: $name
      }) {
        projectV2Field {
          ... on ProjectV2Field {
            id
            name
          }
        }
      }
    }
    """
    
    result = client.query(mutation, {
        "projectId": project_id,
        "name": name
    })
    
    return result["createProjectV2Field"]["projectV2Field"]

def get_repository_issues(client: GitHubGraphQLClient, owner: str, repo: str, limit: int = 100) -> List[Dict]:
    """Get repository issues"""
    query = """
    query($owner: String!, $repo: String!, $first: Int!) {
      repository(owner: $owner, name: $repo) {
        issues(first: $first, orderBy: {field: CREATED_AT, direction: DESC}) {
          nodes {
            id
            number
            title
            url
          }
        }
      }
    }
    """
    
    result = client.query(query, {"owner": owner, "repo": repo, "first": limit})
    return result["repository"]["issues"]["nodes"]

def add_issue_to_project(client: GitHubGraphQLClient, project_id: str, issue_id: str) -> Dict:
    """Add an issue to a project"""
    mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item {
          id
        }
      }
    }
    """
    
    result = client.query(mutation, {
        "projectId": project_id,
        "contentId": issue_id
    })
    
    return result["addProjectV2ItemById"]["item"]

def main():
    """Main execution"""
    print_header(f"GitHub Projects v2 Bootstrap for {REPO_OWNER}/{REPO_NAME}")
    
    # Get GitHub token
    token = get_github_token()
    client = GitHubGraphQLClient(token)
    
    print_color(Colors.GREEN, "✓ GitHub GraphQL client initialized")
    print()
    
    # Check for existing project
    print("Checking for existing project...")
    existing_project = find_existing_project(client, REPO_OWNER, PROJECT_TITLE)
    
    if existing_project:
        print_color(Colors.YELLOW, f"  ↻ Project already exists: {existing_project['title']}")
        print_color(Colors.YELLOW, f"     {existing_project['url']}")
        project = existing_project
    else:
        print("Creating new project...")
        project = create_project(client, REPO_OWNER, PROJECT_TITLE, PROJECT_DESCRIPTION)
        print_color(Colors.GREEN, f"  ✓ Created project: {project['title']}")
        print_color(Colors.GREEN, f"     {project['url']}")
    
    project_id = project["id"]
    print()
    
    # Create custom fields
    print_header("Creating Custom Fields")
    
    # Get existing fields
    existing_fields = get_project_fields(client, project_id)
    existing_field_names = {field["name"] for field in existing_fields}
    
    # Phase field
    if "Phase" not in existing_field_names:
        print("Creating 'Phase' field...")
        phase_options = ["PHASE 0", "PHASE 1", "PHASE 2", "PHASE 3", "PHASE 4"]
        phase_field = create_single_select_field(client, project_id, "Phase", phase_options)
        print_color(Colors.GREEN, f"  ✓ Created field: Phase with {len(phase_options)} options")
    else:
        print_color(Colors.YELLOW, "  ↻ Field exists: Phase")
    
    # Domain field
    if "Domain" not in existing_field_names:
        print("Creating 'Domain' field...")
        domain_options = [
            "Catalog", "Inventory", "Ordering", "Fulfillment", "Routing",
            "Partner", "Workforce", "Operations", "Compliance", "Platform"
        ]
        domain_field = create_single_select_field(client, project_id, "Domain", domain_options)
        print_color(Colors.GREEN, f"  ✓ Created field: Domain with {len(domain_options)} options")
    else:
        print_color(Colors.YELLOW, "  ↻ Field exists: Domain")
    
    # Priority field
    if "Priority" not in existing_field_names:
        print("Creating 'Priority' field...")
        priority_options = ["Critical", "High", "Medium", "Low"]
        priority_field = create_single_select_field(client, project_id, "Priority", priority_options)
        print_color(Colors.GREEN, f"  ✓ Created field: Priority with {len(priority_options)} options")
    else:
        print_color(Colors.YELLOW, "  ↻ Field exists: Priority")
    
    # Notion Reference field
    if "Notion Reference" not in existing_field_names:
        print("Creating 'Notion Reference' field...")
        notion_field = create_text_field(client, project_id, "Notion Reference")
        print_color(Colors.GREEN, "  ✓ Created field: Notion Reference (text)")
    else:
        print_color(Colors.YELLOW, "  ↻ Field exists: Notion Reference")
    
    print()
    
    # Add issues to project
    print_header("Adding Issues to Project")
    
    print(f"Fetching issues from {REPO_OWNER}/{REPO_NAME}...")
    issues = get_repository_issues(client, REPO_OWNER, REPO_NAME, limit=100)
    print(f"Found {len(issues)} issues")
    print()
    
    if issues:
        print("Adding issues to project...")
        added_count = 0
        for issue in issues:
            try:
                add_issue_to_project(client, project_id, issue["id"])
                print_color(Colors.GREEN, f"  ✓ Added issue #{issue['number']}: {issue['title'][:60]}...")
                added_count += 1
            except Exception as e:
                # Issue might already be in project
                print_color(Colors.YELLOW, f"  ↻ Issue #{issue['number']} already in project or error: {str(e)[:50]}")
        
        print()
        print_color(Colors.GREEN, f"✓ Added {added_count} issues to project")
    else:
        print_color(Colors.YELLOW, "No issues found to add to project")
    
    print()
    
    # Summary
    print_header("Summary")
    print_color(Colors.GREEN, f"Project: {project['title']}")
    print_color(Colors.GREEN, f"URL: {project['url']}")
    print_color(Colors.GREEN, f"Issues: {len(issues)} total")
    print()
    print_color(Colors.BLUE, "Next Steps:")
    print("1. Visit the project board and configure Status column workflow")
    print("2. Manually set field values for issues as needed")
    print("3. Create views (By Phase, By Domain, By Priority)")
    print("4. Start moving issues through the workflow!")
    print()
    print_color(Colors.GREEN, "✓ Projects v2 bootstrap complete!")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_color(Colors.YELLOW, "Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_color(Colors.RED, f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
