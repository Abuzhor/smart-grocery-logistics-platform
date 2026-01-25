"""
Inventory Domain Queries

This module defines queries for retrieving inventory information.
All queries exclude pricing, catalog, and financial data per boundary rules.
"""


class GetStockLevelQuery:
    """
    Query to retrieve current stock level for a product at a location.
    
    Input:
        product_id: Unique identifier for the product
        location_id: Identifier for the storage location
    
    Output:
        quantity: Current stock quantity
        last_updated: Timestamp of last stock update
        
    Note: Output excludes pricing and catalog metadata.
    """
    pass


class GetReservationsQuery:
    """
    Query to retrieve active reservations for a product.
    
    Input:
        product_id: Unique identifier for the product
    
    Output:
        reservations: List of active reservations
            - reservation_id
            - quantity
            - created_at
            
    Note: Output excludes order details and financial information.
    """
    pass


class GetBatchDetailsQuery:
    """
    Query to retrieve batch information for tracking.
    
    Input:
        batch_id: Unique identifier for the batch
    
    Output:
        product_id: Associated product identifier
        quantity: Current quantity in batch
        location_id: Storage location
        expiration_date: Batch expiration date (if applicable)
        production_code: Production/lot code
        
    Note: Output excludes pricing and supplier financial data.
    """
    pass


class GetLocationInventoryQuery:
    """
    Query to retrieve all inventory at a specific location.
    
    Input:
        location_id: Identifier for the storage location
    
    Output:
        items: List of inventory items
            - product_id
            - quantity
            - batch_id (if applicable)
            - last_updated
            
    Note: Output excludes catalog metadata and pricing information.
    """
    pass


class GetAdjustmentHistoryQuery:
    """
    Query to retrieve adjustment history for audit purposes.
    
    Input:
        product_id: Unique identifier for the product
        start_date: Start of time range
        end_date: End of time range
    
    Output:
        adjustments: List of adjustments
            - adjustment_id
            - quantity_change
            - reason
            - timestamp
            
    Note: Output excludes financial impact and pricing data.
    """
    pass
