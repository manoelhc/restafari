#!/usr/bin/python3.4

import yaml, sys, os, io, argparse, os.path, subprocess

from anyjson import serialize

import output
import comparer
import connection

conf = {
  'domain' : '127.0.0.1',
  'protocol' : 'http',
  'port' : '80',
  'path' : '',
  'cookies' : {},
  'headers' : {},
  'db' : { "#exec" : [] },
  'errors' : []
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
  obj = yaml.load(stream)
  for test in obj['tests']:
    id = test['id']
    if id in db:
      output.printLoadError(filename, id, "Duplicated id")
    db[id] = test
    output.printLoad(db[id]['desc'])
    if test['executable'] == True:
      db["#exec"].append(id)

def checkDeps():
  global conf
  db = conf['db']
  for test in db:
    if test[0] != "#":
      bef = db[test]['exec_before']
      aft = db[test]['exec_after']
      if len(bef) > 0:
        for id in bef:
          if not id in db:
            output.printDepError(db[test]['id'], id, 'exec_before')

def runTests():
  global conf
  db = conf['db']
  for id in db['#exec']:
    req = connection.getRequest(id, conf)
    res = comparer.compareResult(req, db[id]['expect'], conf)
    if res == False:
        output.validationError(conf)
    else:
        output.validationOk(conf)

def main():
  global conf
  parser = argparse.ArgumentParser(description='Restafari REST API tester')
  parser.add_argument('--hostname', '-s', dest='hostname', help='The hostname of the web service')
  parser.add_argument('--protocol', '-p', dest='protocol', help='The protocol which will be used (HTTP/HTTPS)')
  parser.add_argument('--port', '-P', dest='port', help='The port number')
  parser.add_argument('--exec-before', '-B', dest='exec_before', help='Execute a single command-line/script before starting the REST test. It\'s useful to prepare the environment for the tests.')
  parser.add_argument('--exec-success', '-S', dest='exec_success', help='Execute a single command-line/script when all tests were done successfully.')
  parser.add_argument('--debug', '-D', dest='debug', help='Enable debug mode')
  parser.add_argument('files', nargs="*", metavar='N', help='The test file(s) to be used')

  # TODO
  #parser.add_argument('--directory', '-d', dest='directory', help='Load all test files (file.rest) from a directory, skipping files which initiates with .')
  #parser.add_argument('--exec-failure', '-F', dest='exec_failure', help='Execute a command-line when some test fails.')
  #parser.add_argument('--restful', '-r', dest='restful', help='Execute tests with REST-compliant mode on')

  args = parser.parse_args()

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

main()
