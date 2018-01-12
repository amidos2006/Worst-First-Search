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
module load python/intel/2.7.12

RUNDIR=$SCRATCH/CheckersDTS
echo $RUNDIR

cd $RUNDIR

python test.py $SLURM_ARRAY_TASK_ID

#BLANK LINE UNDER THS LINE. SACRIFICE TO THE CARRIAGE RETURN GODS.
