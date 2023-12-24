#!/usr/bin/env python3

import math
import click
import tomli
import ipaddress

from rich.console import Console
from rich.table import Table
from rich import box

NETSPLIT_CFG = "netsplit.toml"


@click.group()
@click.version_option()
def cli():
    """Netsplit can help slice and dice your IP space."""


def get_subnets(name, space, net, level=0, index=0, extend=0, slots=1):
    rows = []
    next_slots = space['options'].get('slots', 1)
    rows.append({'level': level, 'slots': slots, 'index': index, 'extend': extend, 'name': name, 'prefix': net})

    members = space.get('members', [])
    subnets = [s for s in net.subnets(prefixlen_diff=int(math.log2(next_slots)))]

    is_leaf = isinstance(members, list)
    if is_leaf:
        leaf_subnets = [s for s in net.subnets(prefixlen_diff=int(math.log2(next_slots)))]
        for i, last in enumerate(members):
            leaf_subnet = leaf_subnets[i]
            leaf_name = f"{name} / {last}"
            rows.append({'level': level+1, 'slots': next_slots, 'index': i+1, 'extend': 0, 'name': leaf_name, 'prefix': leaf_subnet})
        for i in range(len(members), next_slots):
            leaf_subnet = leaf_subnets[i]
            leaf_name = f"{name} / RESERVED"
            rows.append({'level': level+1, 'slots': next_slots, 'index': i+1, 'extend': 0, 'name': leaf_name, 'prefix': leaf_subnet})
    else:
        slot_meta = {s: "RESERVED" for s in range(next_slots)}
        count = 0
        for m in members:
            found_index = space['members'][m]['options'].get('index')
            found_extend = space['members'][m]['options'].get('extend', 0)
            if found_index:
                slot_meta[found_index-1] = m
                for i in range(1, 2**found_extend):
                    slot_meta[found_index-1+i] = "SKIP"
                count += found_index + 2**found_extend - 1
            else:
                slot_meta[count] = m
                for i in range(1, 2**found_extend):
                    slot_meta[count+i] = "SKIP"
                count += 2**found_extend

        for i, member_name in slot_meta.items():
            if i > len(subnets):
                click.secho(f"ERROR: Not enough subnets for this plan [{i}:{member_name}]", fg="red")
                continue
            if member_name == "SKIP":
                continue
            if member_name == "RESERVED":
                skipped_subnet = subnets[i]
                skipped_name = f"{name} / RESERVED"
                rows.append({'level': level+1, 'slots': next_slots, 'index': i+1, 'extend': 0, 'name': skipped_name, 'prefix': skipped_subnet})
            else:
                next_space = space['members'][member_name]
                next_extend = next_space['options'].get('extend', 0)
                next_subnet = subnets[i].supernet(prefixlen_diff=next_extend)
                next_name = f"{name} / {member_name}"
                rows = rows + get_subnets(next_name, next_space, next_subnet, level=level+1, index=i+1, extend=next_extend, slots=next_slots)

    return rows


def pprint_plan(options, prefixes, max_level, keyword, reserved):
    console = Console()

    t = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL)
    t.add_column(" #", justify="right")
    t.add_column(options["description"])
    t.add_column("Subnet")
    t.add_column("idx/slots", justify="right")
    t.add_column("IPs", justify="right")

    for p in prefixes:
        dots = '.' * (p['prefix'].prefixlen - 8)
        if keyword and keyword not in p['name']:
            continue
        if p['level'] < max_level + 1:
            RESERVED = ""
            if 'RESERVED' in p['name']:
                RESERVED = "[dim]"
                if reserved < p['level']:
                    continue
            STYLE = "[green]" if p['level'] % 2 else "[blue]"
            index_value = ""
            if p['slots'] != 1:
                if p['extend'] == 0:
                    index_value = f"{p['index']:3}      / {p['slots']:3}"
                else:
                    index_value = f"{p['index']:3} → {p['index']+2**p['extend']-1:2} / {p['slots']:3}"

            t.add_row(
                f"{STYLE}{RESERVED}{p['level']}",
                f"{STYLE}{RESERVED}{p['name']}",
                f"{STYLE}{RESERVED}{dots}{p['prefix']}",
                f"{STYLE}{RESERVED}{index_value}",
                f"{STYLE}{RESERVED}{p['prefix'].num_addresses}"
            )

    console.print(t)


@cli.command()
@click.option('--reserved', '-r', help='With reserved', type=int, default=0)
@click.option('--level', '-l', help='Display up to this level', type=int, default=3)
@click.option('--keyword', '-k', help='Only display if keyword match', default=None)
@click.option('--plan', '-p', type=click.Path(exists=True), help='Plan File to use', default=NETSPLIT_CFG)
def plan(reserved, level, keyword, plan):
    """Set the IP plan"""
    with open(plan, "rb") as f:
        cfg = tomli.load(f)

    options = cfg['netsplit']
    network = ipaddress.IPv4Network(options['network'])
    networks = get_subnets("Global", cfg['plan'], network)
    pprint_plan(options, networks, level, keyword, reserved=reserved)


if __name__ == '__main__':
    cli()
