import os 
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
from tempfile import mktemp
from subprocess import Popen, PIPE

from lib import *

class ByteArrayEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, bytearray):
      return obj.hex()
    return json.JSONEncoder.default(self, obj)

class Contract(object):

  name       = None
  abis       = None

  def __init__(self, name, abis):
    self.name = name
    self.abis = abis

  @staticmethod
  def build_action_binary(account, action, authority, data):
    return OrderedDict([
      ("account", account),
      ("name", action),
      ("authorization", [OrderedDict([
          ("actor", authority[0]),
          ("permission", authority[1])
        ])
      ]),
      ("data", data)
    ])

  def build_action(self, action, authority, *values):
    return Contract.build_action_binary(
      self.name, action, authority,
      self.abis.type_to_bin(
        self.abis.get_action_type(action), *values
      )
    )

class Mallmann:

  MALLMANN_ROOT = os.path.dirname(os.path.realpath(__file__))

  authority    = None
  contracts    = {}
  tx           = {}
  abi_folder   = MALLMANN_ROOT + '/abis'
  code_folder  = MALLMANN_ROOT + '/code'
  api          = Api()

  def __init__(self):
    self.gen_tx()

  def set_abi_folder(self, abi_folder):
    self.abi_folder = abi_folder

  def set_code_folder(self, code_folder):
    self.code_folder = code_folder
  
  def add_contract(self, name, abi_file):
    if not abi_file.startswith('/'):
      abi_file = "{0}/{1}".format(self.abi_folder, abi_file)
    self.contracts[name] = Contract(name, abi_serializer.from_file(abi_file))
    return self

  def serialize(self, types, values):
    if type(types) != tuple: types = (types,)
    if type(values) != tuple: values = (values,)
    
    ds = DataStream()
    for i in range(len(types)):
      getattr(ds, 'pack_'+types[i])(values[i])
    return ds.getvalue()

  def get_contract(self, name):
    if name not in self.contracts: raise Exception("contract {0} not loaded".format(name))
    return self.contracts[name]

  def auth(self, actor, permission):
    self.authority = (actor, permission)
    return self

  def get_auth(self):
    return self.authority

  def clear(self):
    self.gen_tx()
    return self

  def gen_tx(self):
    self.tx = OrderedDict([
      ("expiration", self.calc_expiration(datetime.utcnow(), hours=1)),
      ("ref_block_num", 0),
      ("ref_block_prefix", 0),
      ("max_net_usage_words", 0),
      ("max_cpu_usage_ms", 0),
      ("delay_sec", 0),
      ("context_free_actions", []),
      ("actions", []),
      ("transaction_extensions", []),
      ("signatures", []),
      ("context_free_data", [])
    ])

  def expires_in(self, days=0, hours=0, minutes=0):
    self.tx["expiration"] = self.calc_expiration(datetime.utcnow(), days=days, hours=hours, minutes=minutes)
    return self

  def load_code(self, name):
    if not name.startswith('/'):
      name = self.code_folder + "/{0}/{0}.wasm".format(name)
    with open(name) as fp:
      data = fp.read()
      return data
  
  def calc_expiration(self, now, days=0, hours=0, minutes=0):
    return (now+relativedelta(days=days, hours=hours, minutes=minutes)).strftime('%Y-%m-%dT%H:%M:%S')

  def get_tx(self, binary=False):
    if binary == True:
      ds = DataStream()
      ds.pack_transaction(self.tx)
      return ds.getvalue()

    return self.tx

  def sign(self, privkey, url=None, push=False):
    tmpf = mktemp()

    tx = self.get_tx().copy()
    tx["signatures"] = []
    
    with open(tmpf,"w") as f:
      f.write(self.tx_to_json())

    with open(os.devnull, 'w') as devnull:
      cmd = ["cleos"]
      if url:
        cmd += ["-u", url]
      cmd += ["sign"]
      if push: cmd += ["-p"]
      cmd += ["-k", privkey, tmpf]
      p = Popen(cmd, stdout=PIPE, stderr=devnull)
      output, err = p.communicate("")

    if p.returncode:
      return

    if not push:
      signed_tx = json.loads(output)
      self.get_tx()["signatures"].append(signed_tx["signatures"][-1])

    return self

  def tx_to_json(self):
    return json.dumps(self.tx, sort_keys=False, cls=ByteArrayEncoder, indent=2, separators=(',', ': '))

  def print_tx(self):
    print( self.tx_to_json() )

  def set_api_host(self, host):
    self.api.set_host(host)
    return self

  def __getattr__(self, attr):
    class AuthWrapper:
      def __init__(this, contract_name):
        this.contract_name  = contract_name.replace('_','.')
        this.authority      = self.authority

      def __getattr__(this, action_name):
        def handler(*args):
          if not this.authority:
            raise Exception("no auth specified to call {0}::{1}".format(self.tmp,action_name))

          action = None
          if action_name == "raw_call":
            payload = args[0]
            if type(payload) == dict or type(payload) == OrderedDict: payload = self.serialize("action", payload)
            action = Contract.build_action_binary(this.contract_name, "raw", this.authority, payload)
          else:
            if this.contract_name not in self.contracts:
              raise Exception("contract {0} not loaded".format(this.contract_name))
            action = self.contracts[this.contract_name].build_action(action_name, this.authority, *args)
          
          self.tx["actions"].append(action)
          return self
        return handler

    return AuthWrapper(attr)