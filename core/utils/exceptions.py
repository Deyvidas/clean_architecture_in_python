class OutOfStock(Exception):
    """An exception is triggered when we attempt to allocate an order
    but do not have the necessary batches for it.
    """
