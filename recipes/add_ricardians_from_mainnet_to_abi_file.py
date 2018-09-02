#!/usr/bin/env python
import sys
sys.path.append("..")

from collections import OrderedDict
from mallmann import abi_serializer, Api

if len(sys.argv) < 2:
  print "usage: add_ricardians_from_mainnet_to_abi_file.py NEWABI"
  sys.exit(1)

abi_file = sys.argv[1]

mainnet = Api("https://api.eosargentina.io").v1.chain

# Load abi from disk
abi_new = abi_serializer.from_bin(abi_serializer.from_file(abi_file).abi_to_bin())

# Load abi from mainnet
abi_mainnet = abi_serializer.from_dict(mainnet.get_abi(account_name="eosio")["abi"])

# Insert ricardian contracts for every action
for action in abi_mainnet.abi["actions"]:
	new_action = abi_new.find_action(action["name"])
	if not new_action: continue
	new_action["ricardian_contract"] = action["ricardian_contract"]

# Insert ricardian clauses
abi_new.abi["ricardian_clauses"] = abi_mainnet.abi["ricardian_clauses"]
print abi_new.abi_to_json()