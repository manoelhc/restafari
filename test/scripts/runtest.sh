#!/bin/bash

OUTPUT="$(${*:3} 2>/dev/null 1> /tmp/output)"
errcode="${?}"
OUTPUT="$(cat /tmp/output | sed -e 's/^/>> /')"

Red='\e[0;31m' 
Gre='\e[0;32m'
RCol='\e[0m'
Yel='\e[0;33m'
TYPE="$(tr '[:lower:]' '[:upper:]' <<< ${1:0:1})${1:1}"

BAD="FAILURE"
BADCOLOR="${Red}"

if [[ "${TYPE:0:1}" = 'W' ]]; then
  BAD="WARNING"
  BADCOLOR="${Yel}"
fi

BADOUTPUT="${2}: Error code: ${errcode}\n--BEGIN ${BAD} OUTPUT--\n${OUTPUT}\n--END ${BAD} OUTPUT--\n"

if [[  $errcode -eq 0 ]] && [[ "${TYPE:0:1}" = 'S' ]] ; then
  echo -e "${Gre}[SUCCESS]${RCol} ${2}"
elif [[  $errcode -eq 0 ]] && [[ "${TYPE:0:1}" = 'W' ]]; then
  echo -e "${Gre}[SUCCESS]${RCol} ${2}"
else
  echo -e "${BADCOLOR}[${BAD}]${RCol} ${BADOUTPUT}"
fi

exit ${errcode}