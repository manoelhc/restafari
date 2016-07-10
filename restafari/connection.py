from restafari import output
import json
import sys
import urllib.parse
import http.client


def getRequest(id, conf):
    db = conf['db']
    test = db[id]

    if 'header' not in conf or conf['header'] is None:
        conf['header'] = {}

    headers = conf['header'].copy()
    if 'header' in db[id]:
        headers.update(db[id]['header'])

    method = test['method'].upper()
    fullpath = conf['path'] + test['path']
    desc = test['desc']
    params = ''
    server = conf['domain'] + ':' + conf['port']
    try:
        conn = http.client.HTTPConnection(server)
    except IOError as err:
        conf['errors'].append("Server " + server + " not found!")
        output.validationError(conf)
        sys.exit(1)

    if 'data' not in test or test['data'] is None:
        test['data'] = {}

    if method == 'GET':
        conn.request(method, fullpath, None, headers)
    else:
        params = json.dumps(test['data'])
        res = conn.request(method, fullpath, params, headers)

    res = conn.getresponse()

    data = res.read().decode("utf-8").strip()
    if len(data) > 60:
        output_data = data.replace("\n", '')
        output_data = output_data[0:60] + '...'
    else:
        output_data = data
    output.printRequest(method,
                        conf['domain'],
                        fullpath,
                        params,
                        desc,
                        output_data,
                        res.status)

    result = {}
    result['status'] = res.status
    result['header'] = res.getheaders()

    try:
        result['data'] = json.loads(data)
    except ValueError:
        print("Invalid JSON outout")
    # finally:
    #   result['data'] = None

    return result
