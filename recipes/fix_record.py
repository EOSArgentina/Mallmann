#!/usr/bin/env python
import sys
import json
from collections import OrderedDict

sys.path.append("..")
from mallmann import Mallmann

if len(sys.argv) < 2:
  print "usage: fix_record.py JSON_VALUE"
  sys.exit(1)

account   = "collection"
scope     = "collection"
table     = "data"
abi_file  = "../extras/collection/collection.abi"
wasm_file = "../extras/collection/collection.wasm"
value     = json.loads(sys.argv[1], object_pairs_hook=OrderedDict)

m = Mallmann()
m = m.expires_in(hours=1)
m = m.add_contract("eosio", "eosio.system.abi")
m = m.add_contract(account, abi_file)
m = m.auth("eosio.prods","active")
m = m.eosio.setcode("eosio.prods", 0, 0, m.load_code("forward"))
m = m.auth("eosio","active")
m = m.eosio.setpriv("eosio.prods", 1)
m = m.eosio_prods.raw_call(
  m.action_to_hex(m.get_contract("eosio").call_action(
    "setcode", (account,"active"),
    account, 0, 0, m.load_code("update_row")
  ))
)
m = getattr(m,account).raw_call(
  m.serialize(("name","name","name","uint64"),(account, scope, table, value['id']))
  +
  m.get_contract(account).abis.table_object_to_bin(table, value)
)
m = m.eosio_prods.raw_call(
  m.action_to_hex(m.get_contract("eosio").call_action(
    "setcode", (account,"active"),
    account, 0, 0, open(wasm_file).read()
  ))
)
m = m.auth("eosio.prods","active")
m = m.eosio.setcode("eosio.prods", 0, 0, m.load_code("void"))
m = m.auth("eosio","active")
m = m.eosio.setpriv("eosio.prods", 0)
m.print_tx()
