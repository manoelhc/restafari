from colorclass import Color
import sys
import os

step_color = Color("{green}#### Starting{/green} " +
                   "\"{white}{0}{/white}\" {green}test{/green}")
load_color = Color("-- Loading {green}{0}" +
                   "{/green} {white}test{/white}")

test_sep_color = Color("{green}{0}{/green}")

token_color = Color("{white} ==== Avaliable tokens " +
                    "after this test:{/white}\n {blue}{0}{/blue}")

http_ok_color = Color("HTTP Status code:{green} [{0}] - OK{/green}")
http_notbad_color = Color("HTTP Status code:{yellow} [{0}]{/yellow}")
http_error_color = Color("HTTP Status code:{red} [{0}]{/red}")
http_request_color = Color("-- {white}{0} request ({1},{2},{3}){/white}" +
                           "    {white}\n ---> Request " +
                           "data: {magenta}{4}{/magenta}" +
                           "    {white}\n <--- Response " +
                           "data: {cyan}{5}{/cyan}")
load_error_color = Color("-- {red}Error on loading{/red} {white}{0}" +
                         "::id[{1}]: {2}{/white}")

dep_error_color = Color("-- {red}Dependecy Error:{/red} {white} from id::" +
                        "{0}; {1}->{/white}{yellow}{2}" +
                        "{/yellow}: {white}id does not exist!{/white}")

dep_color = Color("-- {white}Checking{/white} {green}{0}" +
                  "{/green} {white}test{/white}")

val_error_color = Color("{red} [FAIL] {/red} Validation error: {0}")
val_ok_color = Color("{green} [PASS] {/green} Validation passed")
verify_node_color = Color("{white} [TEST] {0}{/white} {1}")

invalid_op_color = Color("{yellow} [INVL] invalid operator {red}{0}" +
                         "{/red}{/yellow}: {1}")

invalid_exp_data_key_color = Color("invalid expected data key {yellow}{0}" +
                                   "{/yellow}. They is no property with this" +
                                   " name in server's response.")

debug_color = Color("{yellow} [DEBUG] {/yellow} {0}")


def printRequest(desc, domain, path, method, sent_data,
                 received_data, http_status_num):
    if http_status_num == 200:
        httpno = print(http_ok_color.format(str(http_status_num)))
    elif http_status_num > 200 and http_status_num < 400:
        httpno = print(http_notbad_color.format(str(http_status_num)))
    else:
        httpno = print(http_error_color.format(str(http_status_num)))
    if sent_data is "":
        sent_data = '<empty>'

    print(http_request_color.format(desc,
                                    domain,
                                    method,
                                    path,
                                    sent_data,
                                    received_data,
                                    httpno
                                    ))


def printLoadError(file, id, msg, errno=1):
    print(load_error_color.format(file, id, msg, errno))
    sys.exit(errno)


def printDepError(id_orig, id_missing, execx, errno=1):
    print(dep_error_color.format(id_orig, id_missing, execx))
    sys.exit(errno)


def printDeps(desc):
    print(dep_color.format(desc))


def validationError(conf):
    errors = conf['errors']
    for msg in errors:
        print(val_error_color.format(msg))
    conf['errors'] = []
    conf['has_errors'] = True


def validationOk(conf):
    print(val_ok_color)


def verifyNode(namespace, msg):
    print(verify_node_color.format(namespace, msg))


def invalidOperator(op, msg, conf):
    conf['errors'].append(invalid_op_color.format(op, msg))


def invalidExpectedDataKey(key, conf):
    conf['errors'].append(invalid_exp_data_key_color.format(key))


def debug(msg):
    if "DEBUG" in os.environ:
        print(debug_color.format(msg))
