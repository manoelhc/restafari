from colorclass import Color
import sys
def printStep(desc):
  print(Color("{green}" + desc + "{/green}"))

def printLoad(desc):
  print(Color("-- {white}Loading{/white} {green}" + desc + "{/green} {white}test{/white}"))

def printRequest(method, domain, path, data, desc, output, http):
  if http == 200:
    httpno = "{green}["+ str(http) + "]{/green}"
  elif http > 200 and http < 400:
    httpno = "{yellow}["+ str(http) + "]{/yellow}"
  else:
    httpno = "{red}["+ str(http) + "]{/red}"

  print(Color("-- {white}"+ desc +" request (" +
        domain + "," + method + ","  + path + "," + data +
        "){/white}"+
        "{white}\n ---> " + httpno +
        "{yellow} " + output + "{/yellow}"
        ))

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

def validationError(conf):
    errors = conf['errors']
    for msg in errors:
      print(Color("{red} [FAIL] {/red} Validation error: " + msg ))
    conf['errors'] = []

def validationOk(conf):
      print(Color("{green} [PASS] {/green} Validation passed"))

def verifyNode(namespace, msg):
      print(Color("{white} [TEST] " + str(namespace) + "{/white} " + msg))

def invalidOperator(op, msg):
      print(Color("{yellow} [INVL] invalid operator " + op + "{/yellow} " + msg))

def debug(msg):
      print(Color("{yellow} [DEBUG] {/yellow} " + msg))
