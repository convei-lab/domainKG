python integrate_kg.py \
    --std_kg_path "/home/yujin/dot/preprocess_integrate_kg/data/conceptnet" \
    --std_kg_name "conceptnet_graph" \
    --add_kg_path "/home/yujin/dot/preprocess_DoKG/data/dokg_multi_di_no_hiar" \
    --add_kg_name "baby_domain_graph" \
    --integrate_list_path "/home/yujin/dot/preprocess_integrate_kg/data/integrate_list/integrate_list.csv" \
    --save_dir "/home/yujin/dot/preprocess_integrate_kg/data/integratedKG_no_hiar"
    > ./integrate_kg_no_hiar.log 2>&1 &