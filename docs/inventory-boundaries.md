# Inventory Boundaries & Ownership

## Ownership Scope (What Inventory OWNS)
- Stock levels and attributes (e.g., quantity, location, last updated timestamp).
- Batch-level tracking (e.g., expiration dates, production codes).
- Reservations for temporary holds.
- Adjustment logs for manual or automatic changes.
- Warehouse/storage location configuration for inventory storage.

## Explicit Non-Ownership (What Inventory DOES NOT OWN)
- Pricing, discounts, or catalog metadata (Catalog/Pricing owns these).
- Order status transitions beyond reservation fulfillment (Orders own this).
- Payment-related validations or hold statuses (Payments own these).
- Route planning, delivery schedules, or ETAs (Logistics/Delivery owns these).

## External Interfaces (Names Only)
### Orders
- ReservationRequests
- FulfillmentSignals
### Payments
- StockHoldValidations (read-only checks)
### Logistics/Delivery
- DispatchReadyEvents
- StockDispatchUpdates
### Catalog/Pricing
- ProductMetadataFeed
- PricingRequests

## Anti-Corruption Rules
### Prevented Input
- Inventory must not accept pricing data, financial values, or user-facing metadata directly.
- Orchestrated workflows (e.g., "reserve then price" chains) must be mediated externally.
### Required Translations
- Signals like SKU identifiers from Catalog must be mapped to internal inventory representations.
- Location data (e.g., warehouse codes) must align with inventory-defined configurations.

## Data Flow Direction
### Inbound Signals
- Stock adjustments (manual or external system-triggered corrections).
- Reservation creation or cancellation from Orders.
- Batch additions from restocking or receiving shipments.
- Expiration event translations from a batch lifecycle tracking system.
### Outbound Events
- StockReserved events for Orders.
- StockAdjusted logs for Finance/audit subsystems.
- DispatchReady signals for Logistics/Delivery.
- LowStockWarnings for Catalog/Pricing.

## Future Extension Points
- Batch Versioning Support.
- Serial Number Tracking.
- Dynamic Reallocation of Reservations.
- Multi-Warehouse Coordination.
- Low-stock Predictive Signals.
- Integration with IoT sensors.