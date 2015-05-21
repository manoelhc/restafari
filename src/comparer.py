import output

def compareResult(req, expect, conf):
  db = conf['db']
  data = req['data']
  for key in expect.keys():
    # checar valores, se tiver $, usar funcao compare
    if key == 'data':
        loadStructure(data, expect['data'], conf, [])

    elif key == 'http':
        if req['status'] != expect['http']:
            msg = "Wrong HTTP status: expected {white}"
            msg = msg + str(expect['http']) + '{/white}, got {yellow}'
            msg = msg + str(req['status']) + '{/yellow}'
            conf['errors'].append(msg)

  return len(conf['errors']) == 0

def loadStructure(data, expect, conf, namespace):
    output.debug("Loading structure")
    result = True
    if type(expect) == dict and type(data) == dict:
        output.debug("Recursive Loading")
        for key in expect:
            if key[0] != '$':
              loadStructure(data[key], expect[key], conf, namespace + [key]);

            elif checkOperator(key):
              msg = str(data[key]) + key + '{gray} (from API){/gray}' + ' ' + str(expect[key]) + ' (expect value)'
              output.verifyNode(namespace, 'Comparing ' + key + ": " + msg)
              res = compare(data[key], key, expect[key])
              if res == False:
                conf['errors'].append( "Comparison failed: "  + msg)
              result = res

            else:
              invalidOperator(key)
    elif type(expect) == dict and type(data) != dict:
        output.debug("Checking rules directly")
        for key in expect:
            if checkOperator(key):
              msg = '({magenta}' + str(data) + '{/magenta} {green}' + key + '{/green} '
              msg = msg + '{magenta}' + str(expect[key]) + '{/magenta}) ->'

              ops = []
              for item in expect[key].keys():
                ops.append(getOperatorDesc(item) + ' ' + str(expect[key][item]))
              strops = ' {cyan}' + getOperatorDesc(key) + '{/cyan} be '

              msg = msg + ' {black}(From API){/black} ' + str(data) + ' {cyan}'
              msg = msg + 'value must be{/cyan} ' + strops.join(ops)
              msg = msg + '{black} (expect value){/black} '

              output.verifyNode(namespace, 'Comparing ' + msg)
              res = compare(data, key, expect[key])
              if res == False:
                conf['errors'].append( "Comparison failed: "  + msg)
              result = res
            else:
              invalidOperator(key)
    elif type(expect) != dict and type(data) != list:
        output.debug("Straight comparison: " + str(expect) + ' == ' + str(data))
        output.verifyNode(namespace, 'test')
        result = (expect == data)

    elif type(expect) != dict and type(data) != list and type(data) != dict:
      output.debug("Straight comparison: " + str(expect) + ' == ' + str(data))
      output.verifyNode(namespace, 'test')
      result = (expect == data)


    return result

def checkOperator(op):
  return op in getOperators().keys()

def getOperatorDesc(op):
  return getOperators()[op]

def getOperators():
  return { '$gt'       : 'greater than',
           '$gte'      : 'greater than or equal',
           '$lt'       : 'lesser than',
           '$lte'      : 'lesser than or equal',
		   '$eq'       : 'equal',
           '$ne'       : 'not equal',
           '$in'       : 'in',
           '$nin'      : 'not in',
           '$ignore'   : 'ignore',
           '$type'     : 'a',
           '$and'      : 'and',
           '$or'       : 'or',
		   '$match'    : 'match',
           '$nullable' : 'can be null',
           '$maxlen'   : 'maximum length of',
           '$minlen'   : 'minimum length of'
   }

def compare(value, op, exp):
  if op == '$or':
    return statementOr(value, exp)
  if op == '$and':
    return statementAnd(value, exp)
  if op == '$gt':
    return value >  exp
  if op == '$gte':
    return value >= exp
  if op == '$lte':
    return value <= exp
  if op == '$lt':
    return value <  exp
  if op == '$eq':
    return value == exp
  if op == '$ne':
    return value != exp
  if op == '$in':
    return value in exp
  if op == '$nin':
    return not value in exp
  if op == '$ignore':
    return exp == True
  if op == '$nullable':
    return exp == True and value == None
  if op == '$match':
     re.compile(exp)
     return prog.match(value)
  if op == '$maxlen':
    return len(value) <= exp
  if op == '$minlen':
    return len(value) >= exp
  if op == '$nullable':
    return exp == True and value == None
  if op == '$type':
    if type(value) is str and exp.upper()   == 'STRING':
      return True
    if type(value) is int and exp.upper()   == 'NUMBER':
      return True
    if type(value) is float and exp.upper() == 'NUMBER':
      return True
    if type(value) is bool  and exp.upper()  == 'BOOLEAN':
      return True
    if type(value) is None  and exp.upper()  == 'NULL':
      return True
    if type(value) is dict  and exp.upper()  == 'OBJECT':
      return True
    if type(value) is list  and exp.upper()  == 'ARRAY':
      return True

  return False

def statementOr(value, exp):
  if type(exp) != dict:
    return False
  for op in exp.keys():
    if compare(value, op, exp[op]):
      return True
  return False

def statementAnd(value, exp):
  if type(exp) != dict:
    return False
  for op in exp.keys():
    if not compare(value, op, exp[op]):
      return False
  return True
