#!/bin/sh
# General options
# -- JobName --
PBS -N Job-array-test 
# -- stdout/stderr redirection --
PBS -o $PBS_JOBNAME.$PBS_JOBID.out
PBS -e $PBS_JOBNAME.$PBS_JOBID.err 
# -- specify queue -- 
PBS -q x-large
# -- user email address --
# please uncomment the following line and put in your e-mail address,
# if you want to receive e-mail notifications on a non-default address
##PBS -M your_email_address
# -- mail notification -- 
#PBS -m abe 
# -- Job array specification --
PBS -t 1-301
# Number of cores 
PBS -l nodes=1:ppn=100
# specify the wall clock time (16 hours) 
#PBS -l walltime=16:00:00 
# Execute the job from the current working directory 
cd $PBS_O_WORKDIR

# Program_name_and_options 
python /work/home/dp626/DSMACC-testing/dsmacc/examples/batch_lifecos.py /work/home/dp626/DSMACC-testing/lhs_general.h5 $PBS_ARRAY_INDEX
