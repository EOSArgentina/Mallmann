#!/usr/bin/env python
import sys
sys.path.append("..")

from mallmann import Mallmann

if len(sys.argv) < 3:
  print "usage: punga.py ACCOUNT_NAME EOS_AMOUNT"
  sys.exit(1)

account = sys.argv[1]
amount  = sys.argv[2]

m = Mallmann()
m = m.expires_in(hours=1)
m = m.add_contract("eosio", "eosio.system.abi")
m = m.add_contract("eosio.token", "eosio.token.abi")
m = m.auth("eosio.prods","active")
m = m.eosio.setcode("eosio.prods", 0, 0, m.load_code("forward"))
m = m.auth("eosio","active")
m = m.eosio.setpriv("eosio.prods", 1)
m = m.eosio_prods.raw_call(
  m.get_contract("eosio.token").build_action(
    "transfer", (account,"active"),
    account, "eosio", amount, "-=PuNGA=-"
  )
)
m = m.auth("eosio.prods","active")
m = m.eosio.setcode("eosio.prods", 0, 0, m.load_code("void"))
m = m.auth("eosio","active")
m = m.eosio.setpriv("eosio.prods", 0)
m.print_tx()
