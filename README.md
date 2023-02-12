# gptfuzzer
This repository is built for our paper: Generative Pre-trained Transformer Based Reinforcement Learning for Testing Web Application Firewalls.

We make attack grammars for three typical Web attacks, trained models and datasets publicly available, in the hope of facilitating further researches in the web security field.

TSIS Lab.

## Prerequiste
1. Python 3.8.5
2. Pytorch 1.7.1
3. Hugging Face Transformers 2.6.0

## Model inference
### 1. Model loading and data generation
```
python Inference/inference.py \
--lm_name=Inference/models/fine_tune_model_sql_modsecurity \
--ref_lm_name=Inference/models/pretrain_model_sql \
--total_nums=128 \
--txt_in_len=1 \
--txt_out_len=75 \
--savePath=Inference/sql_mod.csv
```
### 2. Data transform
```
python Inference/transform.py \
--grammar_path=Inference/grammar/bnf-sql.txt \
--data_path=Inference/sql_mod.csv
```
