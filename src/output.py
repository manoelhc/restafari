from colorclass import Color
import sys


def printStep(desc):
    print(Color("{green}" + desc + "{/green}"))


def printLoad(desc):
    print(Color("-- {white}Loading{/white} {green}" + desc +
                "{/green} {white}test{/white}"))


def printRequest(method, domain, path, data, desc, output, http):
    if http == 200:
        httpno = "{green}[" + str(http) + "]{/green}"
    elif http > 200 and http < 400:
        httpno = "{yellow}[" + str(http) + "]{/yellow}"
    else:
        httpno = "{red}[" + str(http) + "]{/red}"

    print(Color("-- {white}" + desc + " request (" +
                domain + "," + method + "," + path + "," + data +
                "){/white}" +
                "{white}\n ---> " + httpno +
                "{yellow} " + output + "{/yellow}"
                ))


def printLoadError(file, id, msg, errno=1):
    print(Color("-- {red}Error on loading{/red} {white}" + file +
                "::id[" + id + "]: " + msg + "{/white}"))
    sys.exit(errno)


def printDepError(id_orig, id_missing, execx, errno=1):
    print(Color("-- {red}Dependecy Error:{/red} {white} from id::" +
                id_orig + "; " + execx + "->{/white}{yellow}" + id_missing +
                "{/yellow}: {white}id does not exist!{/white}"))
    sys.exit(errno)


def printDeps(desc):
    print(Color("-- {white}Checking{/white} {green}" + desc +
                "{/green} {white}test{/white}"))


def validationError(conf):
    errors = conf['errors']
    for msg in errors:
        print(Color("{red} [FAIL] {/red} Validation error: " + msg))
    conf['errors'] = []


def validationOk(conf):
    print(Color("{green} [PASS] {/green} Validation passed"))


def verifyNode(namespace, msg):
    print(Color("{white} [TEST] " + str(namespace) + "{/white} " + msg))


def invalidOperator(op, msg, conf):
    conf['errors'].append(Color("{yellow} [INVL] invalid operator {red}" +
                                op + "{/red}{/yellow}: " + msg))


def invalidExpectedDataKey(key, conf):
    conf['errors'].append(Color(
        "invalid expected data key {yellow}" + key + "{/yellow}. " +
        "They is no property with this name in server's response."))


def debug(msg):
    print(Color("{yellow} [DEBUG] {/yellow} " + msg))
