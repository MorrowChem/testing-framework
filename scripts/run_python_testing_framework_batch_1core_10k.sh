#!/bin/bash
#$ -cwd
#$ -pe smp 20
#$ -l s_rt=48:00:00
#$ -j y
#$ -t 1
#$ -o $JOB_ID.log


# NEED TO MAKE MULTI-NODE WITH THE INDEXING
nstructs=10000 #10000 # divide by N_nodes
ndone=0
batch_size=500
echo $SGE_TASK_ID
loop_index=$(( $NSLOTS * ($SGE_TASK_ID - 1) ))  # need to multiply by something - loop start point is here
echo "Loop index is $loop_index"
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export PYTHONPATH="/home/omega/vld/hert5155/quip_latest/build/linux_x86_64_gfortran_openmp":$PYTHONPATH

source /u/vld/hert5155/miniconda3/etc/profile.d/conda.sh
conda activate Q
while [ $ndone -lt $nstructs ]; do
    loop_index=$(($loop_index + $ndone))
    for ((i=0; i<=${nstructs}; i=i+${batch_size}))
        do index=$(($loop_index + $i))
            if [ $index -lt $nstructs ]; then
                echo "Doing $index"
                echo "python -u /data/chem-amais/hert5155/programs/testing-framework/scripts/run-model-test-slice.py --index=\"${index}:$(($index + $batch_size))\" GAP20 RSS_slice_10k &> $JOB_ID.$index.out" 
                python -u /u/vld/hert5155/applications/testing-framework/scripts/run-model-test-slice.py --index="${index}:$(($index + $batch_size))" GAP20 RSS_slice_10k &> $JOB_ID.$index.out &
                if [ $index -eq 0 ]; then sleep 3; fi  # to allow for directory creation
                ndone=$(($ndone + $batch_size))
                echo "$ndone done"
            else
                echo "Not doing $index as too high"
            fi
        done
    echo "finished waiting , $ndone done"
    wait
done
