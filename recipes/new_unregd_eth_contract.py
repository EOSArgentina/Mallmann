#!/usr/bin/env python3
import os
import sys
sys.path.append("..")

import json
from hashlib import sha256
from bitcoin import privtopub, random_key, encode_privkey
from random import random
from collections import OrderedDict
from mallmann import Mallmann, abi_serializer, Api, ByteArrayEncoder

if len(sys.argv) < 2:
  print("usage: unregd_setup.py UNREGD_FOLDER")
  sys.exit(1)

unregd_folder = sys.argv[1]

unregd_wasm = "{0}/eosio.unregd.wasm".format(unregd_folder)
unregd_abi = "{0}/eosio.unregd.abi".format(unregd_folder)

propose = {
  "proposer"      : "argentinaeos",
  "requested"     : [],
}

kilin = Api("https://api.eosargentina.io").v1.chain
for r in kilin.get_table_rows( code="eosio", scope="eosio", table="producers",
  key_type="float64", index_position="2", limit=40, json=True)["rows"]:
  propose["requested"].append({"actor":r["owner"], "permission":"active"})

# Craft setcode/setabi tx
with open(unregd_wasm,"rb") as fp:
  wasm = fp.read()

m = Mallmann()
m = m.add_contract("eosio.unregd", unregd_abi)

abi = m.get_contract("eosio.unregd").abis.abi_to_bin()

print("sha256(wasm) = {0}".format(sha256(wasm).digest().hex()))
print("sha256(abi) = {0}".format(sha256(abi).digest().hex()))

# Tx2 (setcode/setabi eosio.unregd)
m = m.expires_in(days=15)
m = m.add_contract("eosio", "eosio.system.abi")
m = m.auth("eosio.unregd","active")
m = m.eosio.setcode("eosio.unregd", 0, 0, wasm)
m = m.eosio.setabi("eosio.unregd", abi)

with open("tx-newunregdupd.json","w") as fp:
  p2 = propose.copy()
  p2["trx"] = m.get_tx().copy()
  p2["proposal_name"] = "newunregdupd"
  fp.write(json.dumps(p2, indent=2, cls=ByteArrayEncoder))
  print("tx-newunregdupd.json generated ...")

print("done")
