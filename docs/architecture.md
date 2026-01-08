# Architecture Overview

Last updated: 2026-01-08

## Context
We optimize the flow from order capture to delivery. Early on, we prioritize simplicity and learning speed while designing clear seams for future scaling.

## Architectural Approach
- Start with a modular monolith: a single deployable with well-defined domain modules.
- Use domain events to reduce coupling between modules.
- Maintain clean interfaces (application services), and protect domain models from leakage.
- Provide a migration path to independent services for high-churn or high-scale modules.

## Core Domains and Modules
- Identity and Access: users, roles, authn/z integrations
- Catalog: products, categories, stores
- Inventory: stock levels, reservations, substitutions
- Orders: order placement, state machine, payments integration points
- Fulfillment/Dispatch: picking, packing, staging
- Routing: route building, constraints, ETAs
- Notifications: email/SMS/push templates and delivery
- Analytics: event stream, dashboards, KPIs

## Data and Storage (initial)
- Relational database (e.g., PostgreSQL – recommended)
- Cache (e.g., Redis – optional for hot paths like availability, sessions, rate limits)
- Object storage for exports/imports and ML artifacts (optional)

## Messaging and Events
- Domain events published within the app boundary (e.g., OrderConfirmed, ItemSubstituted, RouteCreated).
- Outbox pattern to ensure reliable event publishing.
- Message broker (future) for external consumers/subscribers when warranted.

## APIs
- Internal application services expose use-cases to the web/API layer.
- External APIs documented with OpenAPI when available.
- Webhooks for partner integrations (future).

## Observability
- Correlation IDs across request → domain events → notifications.
- Metrics: request latency, error rates, queue depths, OTD, cycle time.
- Audit logs for critical transitions (order, inventory, delivery).

## Security
- Principle of least privilege; role-based access.
- Input validation, idempotency keys for externally-triggered actions.
- PII handling guidelines and data retention policies.

## Evolution Path
- Extract Routing and Notifications early if they become bottlenecks or require different scaling profiles.
- Move from shared deployment to service-per-module when necessary; keep contracts stable.
- Introduce a durable external broker once event volume or consumers warrant it.

See ADR-0001 (docs/adr/0001-initial-architecture.md) for the initial architecture decision.

## Links
- Notion workspace: https://historical-joke-7c3.notion.site/20c13c93cc1480d39c56e01e092b0cb5
- GitHub repository: https://github.com/Abuzhor/smart-grocery-logistics-platform
