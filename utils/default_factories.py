import uuid


def get_hex_uuid4() -> str:
    """Generate string with regex `^[\\w\\d]{32}$`

    example: `45f9975180944ba88071e0c68b36c8ef`
    """
    return uuid.uuid4().hex
