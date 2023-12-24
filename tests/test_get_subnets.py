import glob
import json
import tomli
import ipaddress
import jsonpickle

from pathlib import Path
from netsplit.cli import get_subnets


def load_plan(plan):
    name = Path(plan).stem
    with open(plan, "rb") as f:
        cfg = tomli.load(f)

    options = cfg['netsplit']
    network = ipaddress.IPv4Network(options['network'])
    return get_subnets(name, cfg['plan'], network)


def test_plans():
    plans = glob.glob('tests/plans/*.toml')
    for plan in plans:
        networks = load_plan(plan)
        jsonfile = plan.replace('toml', 'json')
        if Path(jsonfile).exists():
            with open(jsonfile, "rb") as f:
                result = jsonpickle.decode(f.read())
        else:   # Here is our trick to autogenerate the expected output
            frozen = jsonpickle.encode(networks)
            with open(jsonfile, "w") as f:
                j = json.loads(frozen)
                json.dump(j, f, ensure_ascii=False, indent=4)
                result = []
        assert networks == result
