from restafari import output
import json
import sys
import urllib.parse
import http.client
import socket
import os
import pystache


def getRequest(id, conf, api_data):

    db = conf['db']
    test = db[id]
    debug = 0
    if 'DEBUG' in os.environ and os.environ['DEBUG'] != '1':
        debug = 1

    if 'header' not in conf or conf['header'] is None:
        conf['header'] = {}

    headers = conf['header'].copy()
    if 'header' in db[id]:
        headers.update(db[id]['header'])

    method = test['method'].upper()

    test['path'] = pystache.render(test['path'], api_data)

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

    api_data['@req'][id] = test['data']

    res = None
    params = ""
    try:
        if method == 'GET':
            res = conn.request(method, fullpath, None, headers)
        else:
            if debug == 1:
                params = json.dumps(test['data'], sort_keys=True, indent=4)
            else:
                params = json.dumps(test['data'])
            params = pystache.render(params, api_data)
            res = conn.request(method, fullpath, params, headers)
    except ConnectionRefusedError as exc:
        print("The hostname/port is reachable. Please check it before " +
              "executing it again: " + str(exc))
        sys.exit(1)
    except socket.gaierror as exc:
        print("The hostname/port is reachable. Please check it before " +
              "executing it again: " + str(exc))
        sys.exit(1)

    try:
        res = conn.getresponse()
    except http.client.HTTPException as exc:
        print("The hostname/port is reachable. Please check it before " +
              "executing it again: " + str(exc))
        sys.exit(1)

    data = res.read().decode("utf-8").strip()

    if len(data) > 0 and debug == 0 and data[0] == '{':
        received_data = json.dumps(json.loads(data), sort_keys=True, indent=4)
    else:
        if len(data) > 60:
            received_data = data.replace("\n", '')
            received_data = received_data[0:60] + '...'
        else:
            received_data = data

    print("\n" + output.test_sep_color.format("#" * 80))
    print(output.step_color.format(id))
    print(output.test_sep_color.format("#" * 80))

    if len(params) > 0 and debug == 0 and params[0] == '{':
        params = json.dumps(json.loads(params), sort_keys=True, indent=4)

    output.printRequest(desc,
                        conf['domain'],
                        fullpath,
                        method,
                        params,
                        received_data,
                        res.status)

    result = {}
    result['status'] = res.status
    result['header'] = res.getheaders()

    try:
        if len(data) > 0:
            result['data'] = json.loads(data)
        else:
            result['data'] = {}
        api_data['@res'][id] = result['data']

    except ValueError:
        print("Invalid JSON outout: ")
        if debug == 1:
            print(data)
    # finally:
    #   result['data'] = None

    print(output.token_color.format(json.dumps(api_data,
                                               sort_keys=True,
                                               indent=4)))

    return result
