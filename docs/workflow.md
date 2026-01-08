# Development Workflow

Last updated: 2026-01-08

## Branching Strategy
- main is always releasable.
- Use short-lived feature branches: feature/<short-description>.
- Keep PRs small and focused.

## Commits
- Use Conventional Commits (e.g., feat:, fix:, docs:, refactor:, chore:).
- Commit early, push often.

## Pull Requests
- Include problem statement, scope, and testing notes.
- Link related issues; add screenshots for UI changes.
- Require review from code owners for affected areas.
- All checks green (lint, tests, build) before merge.

## Reviews
- Focus on correctness, readability, and resilience.
- Prefer suggestions and questions over mandates; be kind and specific.

## CI/CD (baseline)
- Lint and format
- Build and unit tests
- Security checks (deps, secrets)
- Artifact and preview environments as the codebase evolves

## Releases
- Semantic versioning for deployable artifacts.
- Tag releases and maintain release notes.

## Issues and Labels
- type: feature | bug | chore | docs | spike
- priority: p0 | p1 | p2
- area: orders | inventory | routing | ui | infra | data

## Security and Secrets
- No plaintext secrets in code or CI.
- Use environment-based secrets management; rotate regularly.

## Observability
- Standardized structured logs with correlation IDs.
- Metrics for key flows; alerts on SLOs.
