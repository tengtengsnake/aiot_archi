import uuid

def mac_to_uuid(mac_address):
    # Convert the MAC address to lowercase
    mac_address = mac_address.lower()

    # Replace colons with hyphens
    mac_address = mac_address.replace(':', '-')

    # Generate a UUID from the MAC address
    uuid_str = str(uuid.uuid5(uuid.NAMESPACE_DNS, mac_address.encode()))

    # Convert the UUID string to a UUID object
    uuid_obj = uuid.UUID(uuid_str)

    return uuid_obj
