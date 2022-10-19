#!/bin/bash
touch archive_results_pouet.txt
rm archive_results_*.txt
(
for u in `ls -ctr toto*.txt | grep "${1:-.}" `
do
    while [ `jobs | grep Running | wc -l` -ge 3 ]
    do
      echo "Let us wait"
      date
      sleep 60
    done
    (
    echo $u
    v=`echo $u | sed 's/toto//g' | sed 's/_.*//g'`
    touch goodbad${u}.py
    rm goodbad${u}.py
    touch goodbad${u}.py
    echo "pb=\"$v\"" >> goodbad${u}.py
    echo "good = []" >> goodbad${u}.py
    echo "bad = []" >> goodbad${u}.py
    for v in `cat $u | grep R$ | awk '{print $1}'`
    do
        echo "bad += [`cat ${v}*.txt`]" >> goodbad${u}.py
    done
    for v in `cat $u | grep L$ | awk '{print $1}'`
    do
        echo "good += [`cat ${v}*.txt`]" >> goodbad${u}.py
    done
    #echo "print(len(good))" >> goodbad${u}.py
    #echo "print(len(bad))" >> goodbad${u}.py
    cat learn.py >> goodbad${u}.py
    gstdbuf -e 0 -o 0 -i 0 python goodbad${u}.py > archive_results_${u}.txt  #| tee results_debug_${v}.log
    #mv goodbad${u}.py goodbad_${u}_${v}.py
    ) 
done) #| tee archive_results.txt

wait
