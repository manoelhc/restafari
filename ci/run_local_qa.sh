#!/usr/bin/env bash

. $(dirname ${0})/common.sh

cd ${_RESTAFARI_HOME}

export ORIG_PATH=${PATH}

while read ver; do
  echo
  echo "###################################"
  echo "## Starting tests on Python $ver "
  echo "###################################"
  echo
  export PATH="$(get_python_path ${ver}):${ORIG_PATH}"

  # TODO: use virtualenv instead
  LOCAL_CI=1 PYTHON_VERSION=${ver} ${_RESTAFARI_HOME}/dev/install_local_python3.sh
  cd ${_RESTAFARI_HOME}/ci
  PATH="${PATH}" ./build.sh; [[ $? -gt 0 ]] && exit 1
  PATH="${PATH}" ./local_install_test.sh; [[ $? -gt 0 ]] && exit 1
  PATH="${PATH}" ./local_rest_test.sh; [[ $? -gt 0 ]] && exit 1
done < python-versions
PATH="${PATH}" ./register_pypi_test.sh; [[ $? -gt 0 ]] && exit 1
