#!/usr/bin/env python
import sys
sys.path.append("..")

from mallmann import Mallmann

if len(sys.argv) < 2:
  print "usage: unlimited.py ACCOUNT_NAME"
  sys.exit(1)

account_to_unlimit = sys.argv[1]

m = Mallmann()
m = m.expires_in(hours=1)
m = m.add_contract("eosio", "eosio.system.abi")
m = m.auth("eosio.prods","active")
m = m.eosio.setcode("eosio.prods", 0, 0, m.load_code("set_resource_limits"))
m = m.auth("eosio","active")
m = m.eosio.setpriv("eosio.prods", 1)
m = m.eosio_prods.raw_call(
  m.serialize(("name","int64","int64","int64"),(account_to_unlimit,-1,-1,-1))
)
m = m.auth("eosio.prods","active")
m = m.eosio.setcode("eosio.prods", 0, 0, m.load_code("void"))
m = m.auth("eosio","active")
m = m.eosio.setpriv("eosio.prods", 0)
m.print_tx()
