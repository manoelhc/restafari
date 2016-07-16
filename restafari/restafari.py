#!/usr/bin/env python3
# Test

import yaml
import sys
import os
import argparse
import os.path
import subprocess
import pkg_resources

from restafari import comparer
from restafari import connection
from restafari import output

conf = {
    'domain': '127.0.0.1',
    'protocol': 'http',
    'port': '80',
    'path': '',
    'cookies': {},
    'headers': {},
    'db': {'#exec': []},
    'errors': []
}


def loadFile(filename):
    global conf
    db = conf['db']
    if not os.path.exists(filename):
        filename = os.getcwd() + '/' + filename
    if not os.path.exists(filename):
        print('File ' + filename + ' does not exist.')
        sys.exit(1)
    print('[' + filename + ']')
    stream = open(filename, 'r')

    # Load YAML file
    try:
      obj = yaml.load(stream)
    except yaml.YAMLError as exc:
      print("The file \"" + filename +
            "\" is a malformed YAML. Please fix it before " +
            "executing it again:\n\n" + str(exc))
      print('-------------------')
      print('Here is a simple sample of a valid rest file:')
      valid_sample()
      sys.exit(1)

    for test in obj['tests']:
        id = test['id']
        if id in db:
            output.printLoadError(filename, id, "Duplicated id")
        db[id] = test

        if 'desc' not in test or test['desc'] is None:
            test['desc'] = "Test id: " + test['id']

        if 'method' not in test or test['method'] is None:
            test['method'] = 'GET'

        if 'header' not in test or test['header'] is None:
            test['header'] = {}
            test['header']['Content-type'] = 'application/json'

        if 'executable' not in test or test['executable'] is None:
            test['executable'] = True

        if test['executable'] is True:
            db["#exec"].append(id)

        output.printLoad(db[id]['desc'])


def checkDeps():
    global conf
    db = conf['db']
    for test in db:
        if test[0] != "#":
            if 'expect' not in db[test]:
                output.printDepError(db[test]['id'], '', 'expect')
            if 'exec_before' in db[test]:
                bef = db[test]['exec_before']
            else:
                bef = []
            if 'exec_after' in db[test]:
                aft = db[test]['exec_after']
            else:
                aft = []
            if len(bef) > 0:
                for id in bef:
                    if id not in db:
                        output.printDepError(db[test]['id'], id, 'exec_before')


def runTests():
    global conf
    db = conf['db']
    for id in db['#exec']:
        if 'exec_before' in db[id]:
            for bef in db[id]['exec_before']:
                runTest(conf, bef, db)

        runTest(conf, id, db)

        if 'exec_after' in db[id]:
            for aft in db[id]['exec_after']:
                runTest(conf, aft, db)


def runTest(conf, id, db):
    req = connection.getRequest(id, conf)
    res = comparer.compareResult(req, db[id]['expect'], conf)

    if res is False:
        output.validationError(conf)
    else:
        output.validationOk(conf)


def main():
    global conf

    parser = argparse.ArgumentParser(
        description='Restafari REST API tester')
    parser.add_argument('--hostname', '-s',
                        dest='hostname',
                        help='The hostname of the web service')
    parser.add_argument('--protocol', '-p',
                        dest='protocol',
                        help='The protocol which will be used (HTTP/HTTPS)')
    parser.add_argument('--port', '-P', dest='port', help='The port number')
    parser.add_argument('--exec-before', '-B', dest='exec_before',
                        help='Execute a single command-line/script before ' +
                             'starting the REST test. It\'s useful ' +
                             'to prepare the environment for the tests.')
    parser.add_argument('--exec-success', '-S', dest='exec_success',
                        help='Execute a single command-line/script when all ' +
                             'tests were done successfully.')
    parser.add_argument('--debug', '-D', dest='debug',
                        help='Enable debug mode')
    parser.add_argument('files', nargs="*", metavar='N',
                        help='The test file(s) to be used')

    parser.add_argument('--version', '-v', action='store_true',
                        help='Show version number')

    # TODO
    # parser.add_argument('--format', '-f', dest='format',
    #   help='Set the test file format: YAML (default) or JSON')
    # parser.add_argument('--directory', '-d', dest='directory',
    #   help='Load all test files (file.rest) from a directory, ' +
    #   'skipping files which initiates with .')
    # parser.add_argument('--exec-failure', '-F', dest='exec_failure',
    #   help='Execute a command-line when some test fails.')
    # parser.add_argument('--restful', '-r', dest='restful',
    #   help='Execute tests with REST-compliant mode on')

    args = parser.parse_args()

    if args.version:
        show_version()

    if len(args.files) == 0:
        parser.print_help()
        sys.exit(1)

    if args.hostname:
        conf['domain'] = args.hostname
    if args.protocol:
        conf['protocol'] = args.protocol
    if args.port:
        conf['port'] = args.port

    output.printStep("Loading files")
    for file in args.files:
        loadFile(file)
    if args.exec_before:
        print('Executing: [' + args.exec_before + ']')
        res = subprocess.call(args.exec_before, shell=True)
        if res > 0:
            print('--exec-before command returned: ' + str(res))
            sys.exit(1)

    output.printStep("Checking test dependencies")
    checkDeps()
    runTests()
    if args.exec_success:
        print('Executing: [' + args.exec_success + ']')
        res = subprocess.call(args.exec_success, shell=True)
        if res > 0:
            print('--exec-success command returned: ' + str(res))
            sys.exit(1)
    if 'has_errors' in conf:
        sys.exit(1)


def show_version():
    print('restafari ' + pkg_resources.get_distribution("restafari").version)
    sys.exit(0)


def valid_sample():
    print("tests:\n" +
          "- id : mytest\n" +
          "  desc : \"This is my test\"\n" +
          "  path :  \"/url-path\"\n" +
          "  method : GET\n" +
          "  expect:\n" +
          "    http: 200\n" +
          "    data:\n" +
          "      ok : true\n")


def debug():
    os.environ.pop("DEBUG", 1)

if __name__ == "__main__":
    main()
