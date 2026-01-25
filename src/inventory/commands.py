"""Inventory Domain Commands

This module defines commands for inventory operations.
Commands represent the intention to perform actions on the inventory system.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AddStockCommand:
    """Command to add stock to inventory.
    
    Attributes:
        product_id: Unique identifier for the product
        quantity: Amount of stock to add
        location_id: Identifier for the warehouse/storage location
        batch_id: Batch identifier for tracking stock batches
        metadata: Additional metadata about the stock (e.g., expiration, production codes)
    """
    product_id: str
    quantity: int
    location_id: str
    batch_id: str
    metadata: Dict[str, Any]


@dataclass
class ReserveStockCommand:
    """Command to reserve stock for an order.
    
    Attributes:
        reservation_id: Unique identifier for the reservation
        product_id: Unique identifier for the product
        quantity: Amount of stock to reserve
    """
    reservation_id: str
    product_id: str
    quantity: int


@dataclass
class ReleaseReservationCommand:
    """Command to release a reservation.
    
    Attributes:
        reservation_id: Unique identifier for the reservation to release
    """
    reservation_id: str


@dataclass
class DispatchStockCommand:
    """Command to dispatch reserved stock.
    
    Attributes:
        dispatch_id: Unique identifier for the dispatch
        reservation_id: Unique identifier for the reservation being fulfilled
    """
    dispatch_id: str
    reservation_id: str


@dataclass
class AdjustStockCommand:
    """Command to manually adjust stock levels.
    
    Attributes:
        adjustment_id: Unique identifier for the adjustment
        product_id: Unique identifier for the product
        quantity_change: Change in quantity (positive or negative)
        reason: Explanation for the adjustment
    """
    adjustment_id: str
    product_id: str
    quantity_change: int
    reason: str
