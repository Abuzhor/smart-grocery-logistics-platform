"""Inventory Domain Events

This module defines events that represent state changes in the inventory system.
These events are used to communicate changes to other parts of the system while
maintaining clear boundaries and separation of concerns.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class StockReceived:
    """Event raised when new stock is received into inventory.
    
    Attributes:
        product_id: Unique identifier for the product
        quantity: Amount of stock received
        location_id: Identifier for the warehouse/storage location
    """
    product_id: str
    quantity: int
    location_id: str


@dataclass
class StockReserved:
    """Event raised when stock is reserved for an order.
    
    Attributes:
        reservation_id: Unique identifier for the reservation
        product_id: Unique identifier for the product
        quantity: Amount of stock reserved
    """
    reservation_id: str
    product_id: str
    quantity: int


@dataclass
class ReservationReleased:
    """Event raised when a reservation is cancelled or released.
    
    Attributes:
        reservation_id: Unique identifier for the reservation
        product_id: Unique identifier for the product
        quantity: Amount of stock being released
    """
    reservation_id: str
    product_id: str
    quantity: int


@dataclass
class StockDispatched:
    """Event raised when reserved stock is dispatched for delivery.
    
    Attributes:
        dispatch_id: Unique identifier for the dispatch
        reservation_id: Unique identifier for the reservation being fulfilled
        product_id: Unique identifier for the product
        quantity: Amount of stock dispatched
    """
    dispatch_id: str
    reservation_id: str
    product_id: str
    quantity: int


@dataclass
class StockAdjusted:
    """Event raised when stock levels are manually or automatically adjusted.
    
    Attributes:
        adjustment_id: Unique identifier for the adjustment
        product_id: Unique identifier for the product
        quantity_change: Change in quantity (positive or negative)
        reason: Explanation for the adjustment (e.g., "damaged", "found", "audit")
    """
    adjustment_id: str
    product_id: str
    quantity_change: int
    reason: str
