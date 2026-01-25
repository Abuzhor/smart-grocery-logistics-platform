"""
Inventory Commands

This module defines commands for inventory operations.
Commands represent intentions to perform actions on inventory state.
"""


class AddStockCommand:
    """
    Command to add stock to inventory.
    
    Expected Fields:
        product_id: Identifier for the product
        quantity: Amount of stock to add
        location_id: Storage location identifier
        batch_id: (optional) Batch identifier for tracking
        metadata: (optional) Additional metadata
    """
    pass


class ReserveStockCommand:
    """
    Command to reserve stock for an order.
    
    Expected Fields:
        product_id: Identifier for the product
        quantity: Amount of stock to reserve
        reservation_id: Unique identifier for this reservation
        expiration_time: (optional) When the reservation expires
    """
    pass


class ReleaseReservationCommand:
    """
    Command to release a reservation and return stock to available inventory.
    
    Expected Fields:
        reservation_id: Identifier of the reservation to release
    """
    pass


class DispatchStockCommand:
    """
    Command to dispatch reserved stock.
    
    Expected Fields:
        reservation_id: Reservation identifier tag
        destination: Final destination field for the dispatch
    """
    pass


class AdjustStockCommand:
    """
    Command to adjust stock levels manually or automatically.
    
    Expected Fields:
        stock_id: Identifier for the stock being adjusted
        quantity_change: Amount to change (positive or negative)
        reason_code: Code indicating the reason for adjustment
    """
    pass
