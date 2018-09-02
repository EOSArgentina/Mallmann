#!/usr/bin/env python
import os
from hashlib import sha256
import sys
sys.path.append("..")

import json
from collections import OrderedDict
from mallmann import Mallmann, abi_serializer, Api, ByteArrayEncoder

if len(sys.argv) < 4:
  print "usage: update_system.py PROPOSALNAME NEWWASMFILE NEWABIFILE"
  sys.exit(1)

proposal_name = sys.argv[1]
wasm_file = sys.argv[2]
abi_file = sys.argv[3]

propose = {
  "proposer"      : "eosargentina",
  "proposal_name" : proposal_name,
  "requested"     : [],
}

# Mainnet API
mainnet = Api("https://api.eosargentina.io").v1.chain

# Load abi from disk
abi_new = abi_serializer.from_file(abi_file)

# Load abi from mainnet
abi_mainnet = abi_serializer.from_dict(mainnet.get_abi(account_name="eosio")["abi"])

# Insert ricardian contracts for every action
for action in abi_mainnet.abi["actions"]:
  new_action = abi_new.find_action(action["name"])
  if not new_action: continue
  new_action["ricardian_contract"] = action["ricardian_contract"]

# Insert ricardian clauses
abi_new.abi["ricardian_clauses"] = abi_mainnet.abi["ricardian_clauses"]

# Add top 30 BPs
for r in mainnet.get_table_rows( code="eosio", scope="eosio", table="producers",
  key_type="float64", index_position="2", limit=30, json=True)["rows"]:
  propose["requested"].append({"actor":r["owner"], "permission":"active"})

# Craft setcode/setabi tx
with open(wasm_file,"r") as fp:
  wasm = fp.read()

abi = abi_new.abi_to_bin()

print "sha256(wasm) = {0}".format(sha256(wasm).digest().encode('hex'))
print "sha256(abi) = {0}".format(sha256(abi).digest().encode('hex'))

m = Mallmann()
m = m.expires_in(days=5)
m = m.add_contract("eosio", "eosio.system.abi")
m = m.auth("eosio","active")
m = m.eosio.setcode("eosio", 0, 0, wasm)
m = m.eosio.setabi("eosio", abi)

# Generate proposal
propose["trx"] = m.get_tx()

with open("propose.json","w") as fp:
  fp.write(json.dumps(propose, indent=2, cls=ByteArrayEncoder))
  print "propose.json generated ..."

print "done"