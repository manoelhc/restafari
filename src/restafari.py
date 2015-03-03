import yaml, sys, os, io, urllib.request
from anyjson import serialize
from colorclass import Color

db = {}

def loadFile(filename):
  global db
  stream = open(filename, 'r')
  obj = yaml.load(stream)
  for test in obj['tests']:
    id = test['id']
    if id in db:
      printLoadError(filename, id, "Duplicated id")
    db[id] = test
    printLoad(db[id]['desc'])
    db[id]['JsonData'] = serialize(db[id]['data'])

def checkDeps():
  global db
  for test in db:
    bef = db[test]['exec_before']
    aft = db[test]['exec_before']
    if len(bef) > 0:
      for id in bef:
        if not id in db:
          printDepError(db[test]['id'], id, 'exec_before')

def printStep(desc):
  print(Color("{green}" + desc + "{/green}"))

def printLoad(desc):
  print(Color("-- {white}Loading{/white} {green}" + desc + "{/green} {white}test{/white}"))

def printLoadError(file, id, msg, errno=1):
  print(Color("-- {red}Error on loading{/red} {white}" + file + "::id[" + id + "]: " + msg + "{/white}"))
  sys.exit(errno)

def printDepError(id_orig, id_missing, exec, errno=1):
  print(Color("-- {red}Dependecy Error:{/red} {white} from id::" +
     id_orig + "; " + exec + "->{/white}{yellow}" + id_missing +
     "{/yellow}: {white}id does not exist!{/white}"))
  sys.exit(errno)

def printDeps(desc):
  print(Color("-- {white}Checking{/white} {green}" + desc + "{/green} {white}test{/white}"))

def testRequest():
  response = urllib2.urlopen('http://python.org/')
  html = response.read()

def main():
  printStep("Loading files")
  loadFile("gorest.rest")
  printStep("Checking test dependencies")
  checkDeps()

main()  
#
