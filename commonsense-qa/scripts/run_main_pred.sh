#!/bin/bash

source $1 

# save_dir="./saved_models/${dataset}/${encoder}_elr${encoder_lr}_dlr${decoder_lr}_d${dropoutm}_b${batch_size}_s${seed}"
# mkdir -p ${save_dir}
save_dir="./saved_models/${dataset}/roberta-large-200119"

nohup python -u main.py \
	--mode $mode \
	--dataset $dataset \
	--inhouse $inhouse \
	--save_dir $save_dir \
	--encoder $encoder \
	--max_seq_len $max_seq_len \
	--encoder_lr $encoder_lr \
	--decoder_lr $decoder_lr \
	--batch_size $batch_size \
	--dropoutm $dropoutm \
	--gpu_device $gpu_device \
	--nprocs 20 \
	--save_model $save_model \
	--seed $seed \
	> ${save_dir}/pred.log 2>&1 &
