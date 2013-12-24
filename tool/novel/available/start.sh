#!/bin/bash

START_ID=0
END_ID=10

cur_id=${START_ID}
while [ ${cur_id} -lt ${END_ID} ];do
    if [ -d ${cur_id} ]
    then
        cd "${cur_id}"
    else 
        cur_id=$[${cur_id}+1]
    fi

    nohup python authority_chapter.py &
    cd ..
    cur_id=$[${cur_id}+1]
done
