"""Inventory Domain Queries

This module defines queries for retrieving inventory information.
Queries are read-only operations that return data without modifying state.

Note: Queries focus strictly on inventory-owned data (stock levels, locations, 
batches, reservations) and do not include pricing or catalog metadata, which 
are owned by other domains.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class GetStockLevelQuery:
    """Query to get current stock level for a product.
    
    Attributes:
        product_id: Unique identifier for the product
        location_id: Optional location filter
    
    Returns:
        Stock level information including:
        - product_id
        - quantity (current available stock)
        - location_id
        - last_updated (timestamp)
    """
    product_id: str
    location_id: Optional[str] = None


@dataclass
class GetReservationQuery:
    """Query to get details of a specific reservation.
    
    Attributes:
        reservation_id: Unique identifier for the reservation
    
    Returns:
        Reservation details including:
        - reservation_id
        - product_id
        - quantity
        - status (active, released, fulfilled)
        - created_at (timestamp)
    """
    reservation_id: str


@dataclass
class GetBatchInfoQuery:
    """Query to get batch-level tracking information.
    
    Attributes:
        batch_id: Unique identifier for the batch
    
    Returns:
        Batch information including:
        - batch_id
        - product_id
        - quantity
        - location_id
        - expiration_date (if applicable)
        - production_code (if applicable)
        - received_at (timestamp)
    """
    batch_id: str


@dataclass
class GetAdjustmentHistoryQuery:
    """Query to get adjustment history for a product.
    
    Attributes:
        product_id: Unique identifier for the product
        limit: Maximum number of records to return
    
    Returns:
        List of adjustment records including:
        - adjustment_id
        - product_id
        - quantity_change
        - reason
        - adjusted_at (timestamp)
    """
    product_id: str
    limit: int = 100


@dataclass
class GetLowStockProductsQuery:
    """Query to get products with low stock levels.
    
    Attributes:
        threshold: Stock level threshold for low stock warning
        location_id: Optional location filter
    
    Returns:
        List of products with stock below threshold including:
        - product_id
        - current_quantity
        - location_id
        - last_updated (timestamp)
    """
    threshold: int
    location_id: Optional[str] = None


@dataclass
class GetLocationInventoryQuery:
    """Query to get all inventory at a specific location.
    
    Attributes:
        location_id: Identifier for the warehouse/storage location
    
    Returns:
        List of inventory items at the location including:
        - product_id
        - quantity
        - batch_id (if applicable)
        - last_updated (timestamp)
    """
    location_id: str
