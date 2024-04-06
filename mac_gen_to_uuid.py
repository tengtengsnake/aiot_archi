import random
import uuid

def uuid_gen():
  """Generates a random, locally administered, unicast MAC address.

  Returns:
      str: A MAC address string in the format XX:XX:XX:XX:XX:XX.
  """

  # Locally administered bit (set to 1)
  oui = bytearray([0x02])

  # Generate random bytes for the remaining 5 bytes
  for _ in range(5):
    oui.append(random.randint(0, 255))

  # Convert bytearray to string and format as MAC address
  mac_address = ':'.join(['{:02x}'.format(x) for x in oui])
  
  # Convert the MAC address to lowercase
  mac_address = mac_address.lower()

  # Replace colons with hyphens
  mac_address = mac_address.replace(':', '-')

  # Generate a UUID from the MAC address
  uuid_str = str(uuid.uuid5(uuid.NAMESPACE_DNS, mac_address.encode()))

  # Convert the UUID string to a UUID object and then return it
  return str(uuid.UUID(uuid_str))





