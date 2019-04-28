#! /bin/bash

ngroups=$(h5ls lhs.h5 | grep Group | wc -l)

echo 'reading'
echo $ngroups

rm centrality/lhsgroup/*.day
rm centrality/lhsgroup/*.night

qsub -J 1-${ngroups} z_JOBARRAYCOUNT.pbs
