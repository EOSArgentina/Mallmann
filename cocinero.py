#!/usr/bin/env python

class A:
  def __getattr__(self, attr):
    print attr


a = A()

a.fnc(1,2)


# import os 
# DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# from lib import *

# class Contract:

#   def auth(actor, permission):
#     self.actor = actor
#     self.permission = permission

#   def call(contract, action, actor, permission, data):
#     return {
#       "account": contract,
#       "name": action,
#       "authorization": [{
#         "actor": actor,
#         "permission": permission
#       }],
#       "data": data.encode('hex')
#     }    

# class System(Contract):
#   NAME = "system"

#   def __init__():
#     self.abis = abi_serializer.from_file(
#       DIR_PATH + "/lib/abis/eosio.system.abi"
#     )

# class Token(Contract):
#   NAME = "token"

# class Builder:

#   contracts  = {}
#   actor      = "eosio"
#   permission = "active"
#   actions    = []

#   def __init__():
#     self.contracts[System.NAME] = System()
#     self.current = self.contracts[System.NAME]

#   def with_system():
#     self.current = self.contracts[System.NAME]

#   def with_token():
#     self.current = self.contracts[Token.NAME]

#   def auth(actor, permission):
#     self.actor = actor
#     self.permission = permission

#   def call(action, data):
#     self.actions.append(
#       self.current.call(
#         self.contracts.NAME, action,
#         self.actor, self.permission, data
#       )
#     )

#   def __call__

# # abis = abi_serializer.from_file("/home/matu/tmp/collection/collection.abi")
# # pack_bool()

# # def to_hex(types, values):
# #   abis = abi_serializer()
# #   abis.to_binary()

# # def call(contract, action, actor, permission, data):
# #   return {
# #     "account": contract,
# #     "name": action,
# #     "authorization": [{
# #       "actor": actor,
# #       "permission": permission
# #     }],
# #     "data": data.encode('hex')
# #   }

# # def set_priv(contract, is_priv):
# #   abis = abi_serializer.from_file(DIR_PATH + "/lib/abis/eosio.system.abi")
# #   return call(
# #     "eosio", "setpriv",
# #     "eosio", "active"
# #   )
# #   return {
# #     "account": "eosio",
# #     "name": "setcode",
# #     "authorization": [{
# #       "actor": contract,
# #       "permission": "active"
# #     }],
# #     "data": abis.type_to_bin("setcode",[contract, 0, 0, wasm]).encode('hex')
# #   }

# # def set_code(contract, wasm):
# #   abis = abi_serializer.from_file(DIR_PATH + "/lib/abis/eosio.system.abi")
# #   return call(
# #     "eosio", "setcode",
# #     contract, "active",
# #     abis.type_to_bin("setcode",[contract, 0, 0, wasm])
# #   )

# # def load_code(name):
# #   with open(DIR_PATH + "/{0}/{0}.wasm".format(name)) as fp:
# #     return fp.read()