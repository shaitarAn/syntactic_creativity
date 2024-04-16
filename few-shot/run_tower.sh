#!/usr/bin/env bash
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:A100:2
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

python test_tower.py
