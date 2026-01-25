"""
Inventory Domain Queries

This module defines queries for reading inventory state.
Queries follow anti-corruption rules and limit output to inventory-owned data only.

Based on: docs/inventory-boundaries.md and docs/adr/ADR-001-inventory-boundaries-and-contracts.md

Anti-Corruption Rules (Output Scope Limitations):
- MUST NOT expose: pricing data, financial values, user-facing metadata
- CAN expose: stock levels, batch tracking, reservation status, warehouse locations
- All queries return minimal data necessary for the use case
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class StockAvailabilityQuery:
    """
    Query to check available stock for a product at a location.
    
    Input:
        product_id: Unique identifier for the product
        location: Optional warehouse/storage location (if None, checks all locations)
    
    Output (StockAvailabilityResult):
        - product_id: The product identifier
        - total_quantity: Total physical stock on hand
        - available_quantity: Stock available for new reservations (total - reserved)
        - reserved_quantity: Stock currently reserved for orders
        - location: Location queried (or 'ALL' if aggregated)
    
    Note: Does NOT include pricing, product names, or catalog metadata
    """
    product_id: str
    location: Optional[str] = None


@dataclass
class StockAvailabilityResult:
    """Result for StockAvailabilityQuery - limited scope per anti-corruption rules."""
    product_id: str
    total_quantity: int
    available_quantity: int
    reserved_quantity: int
    location: str


@dataclass
class ReservationStatusQuery:
    """
    Query to check the status of a specific reservation.
    
    Input:
        reservation_id: Unique identifier for the reservation
    
    Output (ReservationStatusResult):
        - reservation_id: The reservation identifier
        - product_id: The product identifier
        - quantity: Amount reserved
        - status: Current status ('active', 'fulfilled', 'cancelled', 'expired')
        - created_at: When reservation was created
        - expires_at: When reservation expires (if applicable)
        - order_reference: External order reference
    
    Note: Does NOT include order details, payment status, or delivery information
    """
    reservation_id: str


@dataclass
class ReservationStatusResult:
    """Result for ReservationStatusQuery - limited scope per anti-corruption rules."""
    reservation_id: str
    product_id: str
    quantity: int
    status: str
    created_at: datetime
    expires_at: Optional[datetime]
    order_reference: str


@dataclass
class BatchInfoQuery:
    """
    Query to get information about a specific batch.
    
    Input:
        batch_id: Unique identifier for the batch
    
    Output (BatchInfoResult):
        - batch_id: The batch identifier
        - product_id: The product identifier
        - quantity: Current quantity in batch
        - location: Storage location
        - expiration_date: When batch expires (if applicable)
        - production_code: Production/lot code for traceability
        - received_at: When batch was received
    
    Note: Does NOT include supplier details, costs, or pricing information
    """
    batch_id: str


@dataclass
class BatchInfoResult:
    """Result for BatchInfoQuery - limited scope per anti-corruption rules."""
    batch_id: str
    product_id: str
    quantity: int
    location: str
    expiration_date: Optional[datetime]
    production_code: Optional[str]
    received_at: datetime


@dataclass
class LocationInventoryQuery:
    """
    Query to list all products with stock at a specific location.
    
    Input:
        location: Warehouse/storage location identifier
        include_reserved: Whether to include reserved quantities in results
    
    Output (List[LocationInventoryItem]):
        For each product at location:
        - product_id: The product identifier
        - total_quantity: Total physical stock
        - available_quantity: Stock available for reservations
        - reserved_quantity: Stock currently reserved
    
    Note: Does NOT include product names, descriptions, or pricing
    """
    location: str
    include_reserved: bool = True


@dataclass
class LocationInventoryItem:
    """Item in LocationInventoryQuery result - limited scope per anti-corruption rules."""
    product_id: str
    total_quantity: int
    available_quantity: int
    reserved_quantity: int
