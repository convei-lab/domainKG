#!/bin/bash

source ./config/path_generate_dokg.config

nohup python -u calc_path_embedding_dokg.py \
    --data_dir $data_dir \
    --generator_type $generator_type \
    --batch_size $batch_size \
    --output_len $output_len \
    --context_len $context_len \
    --gpu_device $gpu_device \
    --pretrain_generator_ckpt_path $pretrain_generator_ckpt_path \
    --output_path $output_path \
    > ./saved_models/debug_save_emb_dokg.log 2>&1 &
