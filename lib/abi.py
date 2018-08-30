import json
from collections import OrderedDict
from ds import DataStream

class abi_serializer:

  @staticmethod
  def from_dict(abi):
    abis = abi_serializer()
    abis.abi = abi
    return abis

  @staticmethod
  def from_file(file):
    with open(file) as fp:
      return abi_serializer.from_dict(json.loads(fp.read(), object_pairs_hook=OrderedDict))

  def resolve_type(self, type):
    for t in self.abi["types"]:
      if t["new_type_name"] == type: return self.resolve_type(t["type"])
    return type
  
  def find_action(self, action):
    for a in self.abi["actions"]:
      if a["name"] == action: return a
    return None

  def find_struct(self, struct):
    for s in self.abi["structs"]:
      if s["name"] == struct: return s
    return None

  def find_table(self, table_name):
    for s in self.abi["tables"]:
      if s["name"] == table_name: return s
    return None

  def abi_to_bin(self):
    ds = DataStream()
    
    # version
    ds.pack_string(self.abi["version"])

    # types
    ds.pack_varuint32(len(self.abi["types"]))
    for t in self.abi["types"]:
      ds.pack_string(t["new_type_name"])
      ds.pack_string(t["type"])

    # structs
    ds.pack_varuint32(len(self.abi["structs"]))
    for s in self.abi["structs"]:
      ds.pack_string(s["name"])
      ds.pack_string(s["base"])
      ds.pack_varuint32(len(s["fields"]))
      for fd in s["fields"]:
        ds.pack_string(fd["name"])
        ds.pack_string(fd["type"])

    # actions
    ds.pack_varuint32(len(self.abi["actions"]))
    for a in self.abi["actions"]:
      ds.pack_account_name(a["name"])
      ds.pack_string(a["type"])
      ds.pack_string(a["ricardian_contract"])

    # tables
    ds.pack_varuint32(len(self.abi["tables"]))
    for t in self.abi["tables"]:
      ds.pack_account_name(t["name"])
      ds.pack_string(t["index_type"])
      ds.pack_varuint32(len(t["key_names"]))
      for kn in t["key_names"]:
        ds.pack_string(kn)
      ds.pack_varuint32(len(t["key_types"]))
      for kt in t["key_types"]:
        ds.pack_string(kt)
      ds.pack_string(t["type"])

    # ricardian_clauses
    ds.pack_varuint32(len(self.abi["ricardian_clauses"]))
    for rc in self.abi["ricardian_clauses"]:
      ds.pack_string(rc["id"])
      ds.pack_string(rc["body"])

    # error_messages
    ds.pack_varuint32(len(self.abi["error_messages"]))
    for em in self.abi["error_messages"]:
      ds.pack_uint64(em["error_code"])
      ds.pack_string(em["error_msg"])
   
    # abi_extensions
    ds.pack_varuint32(len(self.abi["abi_extensions"]))
    for ae in self.abi["abi_extensions"]:
      ds.pack_uint16(ae[0])
      ds.pack_bytes(ae[1].decode('hex'))

    return ds.getvalue()

  def get_action_type(self, name):
    action = self.find_action(name)
    if not action:
      raise Exception("action '{0}'' not found".format(name))
    return self.resolve_type(action["type"])
  
  def table_object_to_bin(self, table_name, value):
    table = self.find_table(table_name)
    if not table:
      raise Exception("table '{0}'' not found".format(table_name))
    return self.type_to_bin(table["type"], *value.values())

  def type_to_bin(self, type_name, *args):
    struct = self.find_struct(self.resolve_type(type_name))
    if not struct:
      raise Exception("type not found {0}".format(type_name))

    class Object(object):
      fields = None
      def __init__(self, fields):
        self.fields = fields

    def flat_args(l):
      values = []
      for i in xrange(len(l)):
        if type(l[i]) == list:
          values.append(flat_args(l[i]))
        elif type(l[i]) == dict or type(l[i]) == OrderedDict:
          values.append({"o":flat_args(l[i].values())})
        else:
          values.append(l[i])
      return values

    def flat_struct(s):
      types = []
      for f in s["fields"]:
        is_array = False
        type_name = f["type"]
        if type_name.endswith('[]'):
          is_array = True
          type_name = type_name[:-2]
        type_name = self.resolve_type(type_name)
        fs = self.find_struct(type_name)
        if fs:
          type_name = Object(flat_struct(fs))
        
        if is_array:
          types.append([type_name])
        else:
          types.append(type_name)
      return types

    types = flat_struct(struct)
    values = flat_args(args)

    ds = DataStream(b'')

    def pack_object(types, values):

      if len(types) != len(values):
        print types
        print values
        raise Exception("invalid number of args expected:{0} received:{1}".format(len(types), len(values)))

      for i in xrange(len(types)):
        t = types[i]
        v = values[i]

        if type(t) == list:
          if type(v) != list: raise Exception("v must also be a list")
          if len(t) != 1: raise Exception("len(t) must be 1")

          if type(t[0]) == Object:
            ds.pack_varuint32(len(v))
            for vi in v:
              if type(vi) != dict: raise Exception("vi must be a dict")
              pack_object(t[0].fields, vi.values()[0])
          else:
            ds.pack_array(t[0], v)

        elif type(t) == Object:
          if type(v) != dict and type(v) != OrderedDict: raise Exception("v must be a dict ({0})".format(type(v)))
          pack_object(t.fields, v.values()[0])
        else:
          getattr(ds, 'pack_'+t)(v)

    pack_object(types, values)
    return ds.getvalue()