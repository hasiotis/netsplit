import ipaddress


from netsplit.cli import get_subnets


def test_simple_empty():
    SIMPLE_PLAN = {"options": {"slots": 4}}
    network = ipaddress.IPv4Network('192.168.0.0/24')
    networks = get_subnets("Simple", SIMPLE_PLAN, network)
    assert networks == [
        {'level': 0, 'slots': 1, 'index': 0, 'extend': 0, 'name': 'Simple', 'prefix': ipaddress.IPv4Network('192.168.0.0/24')},
        {'level': 1, 'slots': 4, 'index': 1, 'extend': 0, 'name': 'Simple / RESERVED', 'prefix': ipaddress.IPv4Network('192.168.0.0/26')},
        {'level': 1, 'slots': 4, 'index': 2, 'extend': 0, 'name': 'Simple / RESERVED', 'prefix': ipaddress.IPv4Network('192.168.0.64/26')},
        {'level': 1, 'slots': 4, 'index': 3, 'extend': 0, 'name': 'Simple / RESERVED', 'prefix': ipaddress.IPv4Network('192.168.0.128/26')},
        {'level': 1, 'slots': 4, 'index': 4, 'extend': 0, 'name': 'Simple / RESERVED', 'prefix': ipaddress.IPv4Network('192.168.0.192/26')}
    ]


def test_simple_plan():
    SIMPLE_PLAN = {"options": {"slots": 4}, "members": ["NetA", "NetB"]}
    network = ipaddress.IPv4Network('192.168.0.0/24')
    networks = get_subnets("Simple", SIMPLE_PLAN, network)
    assert networks == [
        {'level': 0, 'slots': 1, 'index': 0, 'extend': 0, 'name': 'Simple', 'prefix': ipaddress.IPv4Network('192.168.0.0/24')},
        {'level': 1, 'slots': 4, 'index': 1, 'extend': 0, 'name': 'Simple / NetA', 'prefix': ipaddress.IPv4Network('192.168.0.0/26')},
        {'level': 1, 'slots': 4, 'index': 2, 'extend': 0, 'name': 'Simple / NetB', 'prefix': ipaddress.IPv4Network('192.168.0.64/26')},
        {'level': 1, 'slots': 4, 'index': 3, 'extend': 0, 'name': 'Simple / RESERVED', 'prefix': ipaddress.IPv4Network('192.168.0.128/26')},
        {'level': 1, 'slots': 4, 'index': 4, 'extend': 0, 'name': 'Simple / RESERVED', 'prefix': ipaddress.IPv4Network('192.168.0.192/26')},
    ]
