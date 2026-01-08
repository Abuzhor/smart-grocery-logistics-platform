# Roadmap

Last updated: 2026-01-08

This roadmap is outcome-oriented; dates are indicative and will be adjusted based on learning.

## Milestone 0: Foundations (Weeks 0–4)
- Project scaffolding, CI basics, linting, formatting
- Initial domain modeling and ADRs
- Core entities: Product, Store, InventoryItem, Order, Shipment, Route, User
- Observability baseline (logging structure, IDs, error taxonomy)

Acceptance: Docs published, ADR-0001 merged, initial CI green.

## Milestone 1: Order and Inventory MVP (Weeks 5–10)
- Order capture API (basic) and state machine (Created → Confirmed → Picked → Shipped → Delivered)
- Inventory availability: simple reservations and substitutions
- Notifications: order confirmation and status updates

Acceptance: Place an order for in-stock SKUs and progress it to Delivered; receive notifications.

## Milestone 2: Fulfillment and Picking (Weeks 11–16)
- Picking lists (FIFO, location hints), substitutions workflow
- Basic picking UI integration points documented
- Audit and event log for key transitions

Acceptance: Picker can complete an order with or without substitution and record outcomes.

## Milestone 3: Routing and Delivery (Weeks 17–24)
- Batch orders into routes (capacity constraints, time windows)
- Simple heuristic route planner; driver stop list export
- Customer tracking link with ETA updates (documented)

Acceptance: Dispatcher can create a route, assign stops, and complete deliveries with basic ETA accuracy.

## Milestone 4: Learning Loop and Analytics (Weeks 25–32)
- Post-delivery outcomes feed back into substitution and ETA estimation
- Operational dashboards (OTD, cycle time, substitution acceptance)
- Error budget and SLOs for critical paths

Acceptance: Dashboard reports core KPIs; tuning improves OTD and cycle time over baseline.

## Integrations (Ongoing)
- POS/ERP catalog and inventory sync (file drop or API)
- Carrier or courier integration for proof-of-delivery

## Future Considerations
- Multi-tenant isolation and billing
- Advanced forecasting and optimization (ML/OR)
- Cold-chain and temperature control integrations
- Returns and reverse logistics
