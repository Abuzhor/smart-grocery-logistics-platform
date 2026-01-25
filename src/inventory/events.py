"""
Inventory Domain Events

This module defines domain events that are fired when significant
state changes occur in the inventory domain.
"""


class StockReceived:
    """
    Fires when new stock is received.
    
    Expected Fields:
        product_id: Identifier for the product
        quantity: Amount of stock received
        location_id: Storage location identifier
    """
    pass


class StockReserved:
    """
    Fires when stock is reserved for an order.
    
    Expected Fields:
        product_id: Identifier for the product
        quantity: Amount of stock reserved
        reservation_id: Unique identifier for this reservation
    """
    pass


class ReservationReleased:
    """
    Fires when a reservation is canceled, making stock available.
    
    Expected Fields:
        reservation_id: Identifier of the reservation being released
    """
    pass


class StockDispatched:
    """
    Fires when reserved stock is dispatched for use/delivery.
    
    Expected Fields:
        dispatch_id: Unique identifier for this dispatch
        reservation_id: Associated reservation identifier
    """
    pass


class StockAdjusted:
    """
    Fires when manual/automated stock correction occurs.
    
    Expected Fields:
        adjustment_id: Unique identifier for this adjustment
        quantity_change: Amount of stock change (positive or negative)
        reason: Explanation for the adjustment
    """
    pass
