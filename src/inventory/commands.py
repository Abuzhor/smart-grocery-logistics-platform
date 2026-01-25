"""
Inventory Domain Commands

This module defines commands that the Inventory bounded context accepts.
Commands represent requests to change the state of the inventory system.

Based on: docs/inventory-boundaries.md and docs/adr/ADR-001-inventory-boundaries-and-contracts.md
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AddStockCommand:
    """
    Command to add stock to the inventory.
    
    This command is used when receiving new shipments or restocking.
    
    Required fields:
        product_id: Unique identifier for the product
        quantity: Amount of stock to add (must be positive)
        location: Warehouse/storage location where stock will be stored
    
    Optional fields:
        - batch_id: Identifier for the batch (for tracking expiration, production codes)
        - expiration_date: Expiration date for perishable goods
        - production_code: Production/lot code for traceability
        - supplier_reference: Reference to supplier shipment
        - received_by: Identifier for who received the stock
    """
    product_id: str
    quantity: int
    location: str
    batch_id: Optional[str] = None
    expiration_date: Optional[datetime] = None
    production_code: Optional[str] = None
    supplier_reference: Optional[str] = None
    received_by: Optional[str] = None


@dataclass
class ReserveStockCommand:
    """
    Command to reserve stock for an order.
    
    This is typically triggered by the Orders domain when an order is placed.
    
    Fields:
        product_id: Unique identifier for the product
        quantity: Amount to reserve (must be positive and not exceed available stock)
        order_reference: External reference to the order (from Orders domain)
        requested_by: Identifier for who requested the reservation
        expires_in_seconds: Optional duration after which reservation expires if not fulfilled
    """
    product_id: str
    quantity: int
    order_reference: str
    requested_by: str
    expires_in_seconds: Optional[int] = None


@dataclass
class CancelReservationCommand:
    """
    Command to cancel an existing stock reservation.
    
    This returns the reserved stock to available inventory.
    
    Fields:
        reservation_id: Unique identifier for the reservation to cancel
        reason: Reason code for cancellation (e.g., 'order_cancelled', 'payment_failed', 'timeout')
        cancelled_by: Identifier for who/what cancelled the reservation
    """
    reservation_id: str
    reason: str
    cancelled_by: str


@dataclass
class AdjustStockCommand:
    """
    Command to manually adjust stock levels.
    
    This is used for corrections, damage write-offs, or other inventory adjustments.
    
    Fields:
        product_id: Unique identifier for the product
        adjustment: Signed integer representing the change (positive or negative)
        reason: Reason code for the adjustment (e.g., 'damage', 'count_correction', 'expiration')
        location: Warehouse/storage location where adjustment occurs
        adjusted_by: Identifier for who is making the adjustment
        notes: Optional additional notes about the adjustment
    """
    product_id: str
    adjustment: int
    reason: str
    location: str
    adjusted_by: str
    notes: Optional[str] = None


@dataclass
class FulfillReservationCommand:
    """
    Command to fulfill a reservation and mark stock as dispatched.
    
    This transitions reserved stock to dispatched status.
    
    Fields:
        reservation_id: Unique identifier for the reservation to fulfill
        fulfilled_by: Identifier for who fulfilled the reservation (e.g., warehouse operator)
        dispatch_reference: Optional reference to the dispatch/shipment
    """
    reservation_id: str
    fulfilled_by: str
    dispatch_reference: Optional[str] = None
