import http.client
import output
import json

def getRequest(id, conf):
  db = conf['db']
  test = db[id]
  method = test['method'].upper()
  fullpath = conf['path'] + test['path']
  desc = test['desc']
  params = ''
  server = conf['domain'] + ':' + conf['port']
  conn = http.client.HTTPConnection(server)

  if method == 'GET':
    conn.request(method, fullpath)
  else:
    params = urllib.parse.urlencode(test['data'])
    conn.request(method, fullpath, params, headers)
  res = conn.getresponse()
  data = res.read().decode("utf-8").strip()
  if len(data) > 60:
    data = data[0:60] + '...'

  output.printRequest(method, conf['domain'], conf['path'], params, desc, data, res.status)

  result = {}
  result['status'] = res.status
  result['header'] = res.getheaders()

  try:
    result['data'] = json.loads(data)
  except ValueError:
    print("Invalid JSON outout")
  #finally:
  #  result['data'] = None

  return result
