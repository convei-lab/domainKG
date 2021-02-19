#!/bin/bash

python -u sample_path_rw_dokg_multi_di_rw_mod.py \
    --data_dir "/home/yujin/dot/preprocess_DoKG/data/dokg_multi_di_no_hiar" \
    --output_dir "/home/yujin/dot/learning-generator/data/sample_path_dokg_multi_di_rev_no_hiar" \
    --graph_file_name "baby_domain_graph.nx" \
    --split_dataset True \
    > sample_path_log_dokg_rw_mod_no_hiar.txt 2>&1 &