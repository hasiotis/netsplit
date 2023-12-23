## Netsplit

Here is a very simply network plan:
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
