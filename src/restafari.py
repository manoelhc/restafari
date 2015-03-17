import yaml, sys, os, io, urllib.parse
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
  output.printStep("Loading files")
  loadFile("C:\\RestafariEnvironment\\restafari\\src\\test.rest")
  output.printStep("Checking test dependencies")
  checkDeps()
  runTests()

main()
#
