#!/bin/bash
set +e
exit_code=0

. bin/activate
python3 -m pip install -r requirements.txt
testfolder="tests"

for file in $( ls ${testfolder}/test*.py )
do
    tname=$( basename "${file}" .py )
    echo "Running: ${tname}"
    python3 -m ${testfolder}.${tname}
    result=$?
    if [ ${result} -ne 0 ]
    then
        exit_code=${result}
    fi
done

exit ${exit_code}
