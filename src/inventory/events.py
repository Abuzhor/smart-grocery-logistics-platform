"""
Inventory Domain Events

This module defines events emitted by the inventory domain.
Events are used to communicate state changes to other parts of the system.
"""


class StockReceived:
    """
    Event emitted when stock is received at a location.
    
    Fields:
        product_id: Unique identifier for the product
        quantity: Amount of stock received
        location_id: Identifier for the receiving location
    """
    pass


class StockReserved:
    """
    Event emitted when stock is reserved for an order.
    
    Fields:
        reservation_id: Unique identifier for the reservation
        product_id: Unique identifier for the product
        quantity: Amount of stock reserved
    """
    pass


class ReservationReleased:
    """
    Event emitted when a reservation is released.
    
    Fields:
        reservation_id: Unique identifier for the reservation
        product_id: Unique identifier for the product
        quantity: Amount of stock released
    """
    pass


class StockDispatched:
    """
    Event emitted when stock is dispatched for delivery.
    
    Fields:
        dispatch_id: Unique identifier for the dispatch
        reservation_id: Unique identifier for the reservation
        product_id: Unique identifier for the product
        quantity: Amount of stock dispatched
    """
    pass


class StockAdjusted:
    """
    Event emitted when stock levels are manually or automatically adjusted.
    
    Fields:
        adjustment_id: Unique identifier for the adjustment
        product_id: Unique identifier for the product
        quantity_change: Change in stock quantity (positive or negative)
        reason: Reason for the adjustment
    """
    pass
