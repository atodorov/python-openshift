# Copyright 2011 Alexander Todorov <atodorov@nospam.otb.bg>

# Sanity tests. If something fails exit <> 0

BASE_DIR=`readlink -f $0`
BASE_DIR=`dirname $BASE_DIR`

echo "Searching for typos causing plain http connections"
err=`grep -c HTTPConnection $BASE_DIR/../src/*.py`
[ $err != 0 ] && exit $err


export PYTHONPATH="$BASE_DIR/../src/"

echo "Running pylint for sources"
pylint -E $BASE_DIR/../src/*.py
res=$?
[ $res != 0 ] && exit $res

echo "Running pylint for tests"
pylint -E $BASE_DIR/../tests/*.py
res=$?
[ $res != 0 ] && exit $res

unset PYTHONPATH

exit 0