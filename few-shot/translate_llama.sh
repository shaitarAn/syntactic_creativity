#!/usr/bin/env bash
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:A100:4
#SBATCH --mem=350GB
#SBATCH --time=00:30:00
#SBATCH --partition=lowprio

module purge
module load anaconda3 multigpu a100

eval "$(conda shell.bash hook)"
conda activate ml_llm
export HF_HOME="/scratch/ashait/cache/huggingface"
export HF_HUB_CACHE="$HF_HOME/hub"
export HF_ASSETS_CACHE="$HF_HOME/assets"

for run in "2"; do
    
    python translate_llama.py -l "para" -r $run --test

done