"""
Inventory Domain Commands

This module defines commands for the inventory domain.
Commands represent requests to perform actions within the inventory system.
"""


class AddStockCommand:
    """
    Command to add stock to inventory.
    
    Required fields:
        product_id: Unique identifier for the product
        quantity: Amount of stock to add
        location_id: Identifier for the storage location
    
    Optional fields:
        - batch_id
        - metadata
    """
    pass


class ReserveStockCommand:
    """
    Command to reserve stock for an order.
    
    Fields:
        product_id: Unique identifier for the product
        quantity: Amount of stock to reserve
        order_id: Identifier for the order
    """
    pass


class ReleaseReservationCommand:
    """
    Command to release a stock reservation.
    
    Fields:
        reservation_id: Unique identifier for the reservation
    """
    pass


class DispatchStockCommand:
    """
    Command to dispatch reserved stock.
    
    Fields:
        reservation_id: Unique identifier for the reservation
    """
    pass


class AdjustStockCommand:
    """
    Command to adjust stock levels.
    
    Fields:
        product_id: Unique identifier for the product
        quantity_change: Change in stock quantity (positive or negative)
        reason: Reason for the adjustment
    """
    pass
