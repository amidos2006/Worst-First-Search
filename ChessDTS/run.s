#!/bin/bash
#
#SBATCH --job-name=ChessDTS_Worker
#SBATCH --nodes=1 --ntasks-per-node=1
#SBATCH --time=24:00:00
#SBATCH --mem=2GB
#SBATCH --output=worker_%A_%a.out
#SBATCH --error=worker_%A_%a.err
#SBATCH --array=0-99

module purge
module load python3/intel/3.6.3

RUNDIR=$SCRATCH/ChessDTS
echo $RUNDIR

cd $RUNDIR

pip3 install --user python-chess[engine,gaviota]

python3 test.py $SLURM_ARRAY_TASK_ID

#BLANK LINE UNDER THS LINE. SACRIFICE TO THE CARRIAGE RETURN GODS.
