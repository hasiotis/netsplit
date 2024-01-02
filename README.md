# Netsplit: Slice and dice your IP space

[![PyPi version](https://badge.fury.io/py/netsplit.svg)](https://pypi.org/project/netsplit/)
[![Build status](https://github.com/hasiotis/netsplit/workflows/Pull%20Request/badge.svg)](https://github.com/hasiotis/netsplit/actions?query=workflow%3A%22Pull+Request%22)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/hasiotis/netsplit/blob/master/LICENSE)


## Installation

Install and update using:
```
pip3 install --user --upgrade netsplit
```

## Usage

Here is a very simple network plan:
```
[netsplit]
  description = "Global / Subnet"
  network = "192.168.0.0/24"

[plan]
  options = { slots = 4 }
  members = ["NetA", "NetB"]
```
We can render it with:
```
❯ netsplit plan -p examples/netsplit-simple.toml -r 2
     ╷                   ╷                                    ╷               ╷
   # │ Global / Subnet   │ Subnet                             │ idx+ext/slots │ IPs
╶────┼───────────────────┼────────────────────────────────────┼───────────────┼─────╴
   0 │ Global            │ ................192.168.0.0/24     │               │ 256
   1 │ Global / NetA     │ ..................192.168.0.0/26   │   1     /   4 │  64
   1 │ Global / NetB     │ ..................192.168.0.64/26  │   2     /   4 │  64
   1 │ Global / RESERVED │ ..................192.168.0.128/26 │   3     /   4 │  64
   1 │ Global / RESERVED │ ..................192.168.0.192/26 │   4     /   4 │  64
     ╵                   ╵                                    ╵               ╵
```
Make sure to check examples for complex network plans:

![Multicloud Plan](/examples/img/netsplit-multicloud.png)

# Similar projects:

* [Visual Subnet Calculator](https://github.com/ckabalan/visualsubnetcalc)
