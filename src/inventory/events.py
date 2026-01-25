"""
Inventory Domain Events

This module defines domain events that the Inventory bounded context publishes.
These events represent facts about state changes within the inventory system.

Based on: docs/inventory-boundaries.md and docs/adr/ADR-001-inventory-boundaries-and-contracts.md
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class StockReceived:
    """
    Event published when new stock is received into the warehouse.
    
    Fields:
        product_id: Unique identifier for the product
        quantity: Amount of stock received
        batch_id: Identifier for the batch (for tracking expiration, production codes)
        location: Warehouse/storage location where stock was received
        received_at: Timestamp when stock was received
        metadata: Optional additional information (e.g., supplier reference, production code)
    """
    product_id: str
    quantity: int
    batch_id: str
    location: str
    received_at: datetime
    metadata: Optional[dict] = None


@dataclass
class StockReserved:
    """
    Event published when stock is reserved for an order.
    
    Sent to Orders domain to confirm reservation.
    
    Fields:
        reservation_id: Unique identifier for the reservation
        product_id: Unique identifier for the product
        quantity: Amount of stock reserved
        order_reference: External reference to the order (from Orders domain)
        reserved_at: Timestamp when reservation was created
        expires_at: Optional timestamp when reservation expires if not fulfilled
    """
    reservation_id: str
    product_id: str
    quantity: int
    order_reference: str
    reserved_at: datetime
    expires_at: Optional[datetime] = None


@dataclass
class StockAdjusted:
    """
    Event published when stock levels are manually or automatically adjusted.
    
    Sent to Finance/audit subsystems for tracking.
    
    Fields:
        product_id: Unique identifier for the product
        adjustment: Signed integer representing the change (positive or negative)
        reason: Reason code for the adjustment (e.g., 'damage', 'count_correction', 'expiration')
        location: Warehouse/storage location where adjustment occurred
        adjusted_at: Timestamp when adjustment was made
        adjusted_by: Identifier for who/what made the adjustment (user ID or system)
        previous_quantity: Stock level before adjustment
        new_quantity: Stock level after adjustment
    """
    product_id: str
    adjustment: int
    reason: str
    location: str
    adjusted_at: datetime
    adjusted_by: str
    previous_quantity: int
    new_quantity: int


@dataclass
class DispatchReady:
    """
    Event published when reserved stock is ready for dispatch.
    
    Sent to Logistics/Delivery domain to trigger pickup/delivery.
    
    Fields:
        reservation_id: Unique identifier for the reservation
        product_id: Unique identifier for the product
        quantity: Amount ready for dispatch
        location: Warehouse/storage location where product is staged
        ready_at: Timestamp when product became ready for dispatch
        order_reference: External reference to the order
    """
    reservation_id: str
    product_id: str
    quantity: int
    location: str
    ready_at: datetime
    order_reference: str


@dataclass
class LowStockWarning:
    """
    Event published when stock levels fall below threshold.
    
    Sent to Catalog/Pricing domain for potential actions (e.g., marking unavailable).
    
    Fields:
        product_id: Unique identifier for the product
        current_quantity: Current stock level
        threshold: The low-stock threshold that was breached
        location: Warehouse/storage location
        detected_at: Timestamp when low stock was detected
        available_quantity: Quantity available for new reservations (excluding existing reservations)
    """
    product_id: str
    current_quantity: int
    threshold: int
    location: str
    detected_at: datetime
    available_quantity: int
