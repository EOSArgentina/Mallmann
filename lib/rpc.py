import os
import sys
import requests
import json
import traceback
import logging

RPC_NODE = os.environ.get('RPC_NODE', 'http://127.0.0.1:8888')

class RpcError(Exception):
  def __init__(self, message, code):
    # Call the base class constructor with the parameters it needs
    super(RpcError, self).__init__(message)
    self.code = code

def call_rpc_impl(api, method, *params):
  headers = {
    'content-type'  : 'application/json',
  }
  
  payload2 =  {
      "method": "call",
      "params": [API_ID[api], method] + [p for p in params],
      "jsonrpc": "2.0",
      "id": 10
  }

  r = requests.post(url, data=json.dumps(payload2), headers=headers, timeout=5)
  res = json.loads(r.text)

def call_rpc(api, method, *params):
  try:
    return call_rpc_impl(api, method, params)
  except Exception as e:
    #print traceback.format_exc()
    exc_info = sys.exc_info()
    raise exc_info[0], exc_info[1], exc_info[2]