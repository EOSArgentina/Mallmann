#!/usr/bin/env python
import sys
sys.path.append("..")

from collections import OrderedDict
from mallmann import Mallmann

if len(sys.argv) < 2:
  print "usage: freeze_account.py ACCOUNT_NAME"
  sys.exit(1)

account_to_freeze = sys.argv[1]

null_auth = OrderedDict([ 
  ("threshold" , 1),
  ("keys"      , []),
  ("accounts"  , [OrderedDict([
    ("permission" , OrderedDict([
      ("actor"     , "eosio.null"),
      ("permission", "active"),
    ])),
    ("weight"     , 1)
  ])]),
  ("waits"    , []) 
])

m = Mallmann()
m = m.expires_in(hours=1)
m = m.add_contract("eosio", "eosio.system.abi")
m = m.auth("eosio.prods","active")
m = m.eosio.setcode("eosio.prods", 0, 0, m.load_code("forward"))
m = m.auth("eosio","active")
m = m.eosio.setpriv("eosio.prods", 1)
m = m.eosio_prods.raw_call(
  m.action_to_hex(m.get_contract("eosio").call_action(
    "updateauth", (account_to_freeze,"active"),
    account_to_freeze, "active", "owner", null_auth
  ))
)
m = m.eosio_prods.raw_call(
  m.action_to_hex(m.get_contract("eosio").call_action(
    "updateauth", (account_to_freeze,"owner"),
    account_to_freeze, "owner", "", null_auth
  ))
)
m = m.auth("eosio.prods","active")
m = m.eosio.setcode("eosio.prods", 0, 0, m.load_code("void"))
m = m.auth("eosio","active")
m = m.eosio.setpriv("eosio.prods", 0)
m.print_tx()
