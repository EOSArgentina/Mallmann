#!/usr/bin/env python
import os
import sys
sys.path.append("..")

import json
from sha3 import keccak_256
from bitcoin import privtopub, random_key, encode_privkey
from random import random
from collections import OrderedDict
from mallmann import Mallmann, abi_serializer, Api

if len(sys.argv) < 2:
  print "usage: unregd_setup.py UNREGD_FOLDER"
  sys.exit(1)

unregd_folder = sys.argv[1]

eosio_active = OrderedDict([ 
  ("threshold" , 1),
  ("keys"      , []),
  ("accounts"  , [OrderedDict([
    ("permission" , OrderedDict([
      ("actor"     , "eosio"),
      ("permission", "active"),
    ])),
    ("weight"     , 1)
  ])]),
  ("waits"    , []) 
])

unregd_wasm = "{0}/eosio.unregd.wasm".format(unregd_folder)
unregd_abi = "{0}/eosio.unregd.abi".format(unregd_folder)

propose = {
  "proposer"      : "eosargentina",
  "requested"     : [],
}

kilin = Api("https://api-kylin.eosasia.one").v1.chain
for r in kilin.get_table_rows( code="eosio", scope="eosio", table="producers",
  key_type="float64", index_position="2", limit=30, json=True)["rows"]:
  propose["requested"].append({"actor":r["owner"], "permission":"active"})

def gen_random_unreg_data():
  priv = encode_privkey(random_key(), "wif")
  pub  = privtopub(priv)
  addy = '0x' + keccak_256(pub[2:].decode('hex')).digest()[12:].encode('hex')
  amount = "%.4f EOS" % (1.0 + random()*50.0)
  return {"address":addy, "privkey":priv, "amount":amount}

unreg_data = []
if not os.path.isfile("unreg_data.json"):
  for i in xrange(20):
    unreg_data.append(gen_random_unreg_data())

  with open("unreg_data.json","w") as fp:
    fp.write(json.dumps(unreg_data, indent=2))
else:
  with open("unreg_data.json","r") as fp:
    unreg_data = json.loads(fp.read())

m = Mallmann()
m = m.add_contract("eosio", "eosio.system.abi")
m = m.add_contract("eosio.token", "eosio.token.abi")
m = m.add_contract("eosio.unregd", unregd_abi)

# Tx1 (eosio.unregd/eosio.regram creation)
m = m.expires_in(days=5)
m = m.auth("eosio","active")
m = m.eosio.newaccount("eosio", "eosio.unregd", eosio_active, eosio_active)
m = m.eosio.buyrambytes("eosio", "eosio.unregd", 1200*1024) # 1.2M
m = m.eosio.delegatebw("eosio", "eosio.unregd", "2.0000 EOS", "2.0000 EOS", True)
m = m.eosio.newaccount("eosio", "eosio.regram", eosio_active, eosio_active)
m = m.eosio.buyrambytes("eosio", "eosio.regram", 4*1024) # 4K
m = m.eosio.delegatebw("eosio", "eosio.regram", "2.0000 EOS", "2.0000 EOS", True)

with open("tx1.json","w") as fp:
  p1 = propose.copy()
  p1["trx"] = m.get_tx().copy()
  p1["proposal_name"] = "eosiounregd1"
  fp.write(json.dumps(p1, indent=2))
  print "tx1.json generated ..."

# Tx2 (setcode eosio.unregd + setmaxeos + issue tokens)
m = m.clear()
m = m.expires_in(days=5)
m = m.auth("eosio.unregd","active")
m = m.eosio.setcode("eosio.unregd", 0, 0, m.load_code(unregd_wasm))
m = m.eosio.setabi("eosio.unregd", m.get_contract("eosio.unregd").abis.abi_to_bin())
m = m.eosio_unregd.setmaxeos("1.0000 EOS")

total = 0.0
for ud in unreg_data:
  m = m.eosio_unregd.add(ud["address"], ud["amount"])
  total += float(ud["amount"].split()[0])

m = m.auth("eosio","active")
m = m.eosio_token.issue("eosio.unregd", "%.4f EOS" % (total+1.0), "EOS of unreg accounts" )
m = m.eosio_token.issue("eosio.regram", "%.4f EOS" % (len(unreg_data)), "EOS to cover ram costs" )

with open("tx2.json","w") as fp:
  p2 = propose.copy()
  p2["trx"] = m.get_tx().copy()
  p2["proposal_name"] = "eosiounregd2"
  fp.write(json.dumps(p2, indent=2))
  print "tx2.json generated ..."

print "done"