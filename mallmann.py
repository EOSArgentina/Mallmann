import os 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
from tempfile import mktemp
from subprocess import Popen, PIPE

from lib import *

class Contract(object):

  name       = None
  abis       = None

  def __init__(self, name, abis):
    self.name = name
    self.abis = abis

  @staticmethod
  def build_action(account, action, authority, data):
    return OrderedDict([
      ("account", account),
      ("name", action),
      ("authorization", [OrderedDict([
          ("actor", authority[0]),
          ("permission", authority[1])
        ])
      ]),
      ("data", data.encode('hex'))
    ])

  def call_action(self, action, authority, *values):
    return Contract.build_action(
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

  def action_to_hex(self, action):
    #TODO: fix this
    action["data"] = action["data"].decode('hex')
    return abi_serializer.from_file(
      self.abi_folder + '/_core.abi').type_to_bin("action", *action.values()
    )

  def serialize(self, types, values):
    ds = DataStream()
    for i in xrange(len(types)):
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

  def get_tx(self):
    return self.tx

  def sign(self, privkey):
    tmpf = mktemp()

    tx = self.get_tx().copy()
    tx["signatures"] = []
    
    with open(tmpf,"w") as f:
      f.write(json.dumps(tx))

    with open(os.devnull, 'w') as devnull:
      cmd = ["cleos","sign","-k",privkey, tmpf]
      p = Popen(cmd, stdout=PIPE, stderr=devnull)
      output, err = p.communicate("")

    if p.returncode:
      return
    
    signed_tx = json.loads(output)
    self.get_tx()["signatures"].append(signed_tx["signatures"][0])

    return self

  def print_tx(self):
    print json.dumps(self.tx, sort_keys=False, indent=2)

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
            if type(payload) == dict or type(payload) == OrderedDict: payload = self.action_to_hex(payload)
            action = Contract.build_action(this.contract_name, "raw", this.authority, payload)
          else:
            if this.contract_name not in self.contracts:
              raise Exception("contract {0} not loaded".format(this.contract_name))
            action = self.contracts[this.contract_name].call_action(action_name, this.authority, *args)
          
          self.tx["actions"].append(action)
          return self
        return handler
    
    return AuthWrapper(attr)