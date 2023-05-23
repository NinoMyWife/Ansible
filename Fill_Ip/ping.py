import os
import sys

def ping(host):
    
    """This function will test if IP is pingable

    Args:
        host (str): A Server IP

    Raises:
        Error : Ping error

    Returns:
        Bool : 0 it's ok, 1 it's not ok
    """
    
    try:
        response = os.system("ping -c 1 " + host)
        print(response)
    except Exception as e :
        raise (e)

    if response == 0:
        sys.exit(0)
    else:
        sys.exit(1)

print(ping.__doc__)