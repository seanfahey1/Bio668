#! /bin/bash

for sequence in "$@"
do
  echo "$sequence" | awk -v num=3 '{for(i=1;i<=length($0);i+=1) print substr($0,i,num)}'
done
