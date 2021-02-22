python integrate_kg.py \
    --std_kg_path "/home/yujin/dot/preprocess_integrate_kg/data/integratedKG_no_hiar" \
    --std_kg_name "integrate_graph" \
    --add_kg_path "/home/yujin/dot/preprocess_DoKG/data/dokg_concept" \
    --add_kg_name "baby_domain_graph" \
    --integrate_list_path "/home/yujin/dot/preprocess_integrate_kg/data/integrate_list/integrate_list.csv" \
    --save_dir "/home/yujin/dot/preprocess_integrate_kg/data/integratedKG_pivot"
    > ./integrate_kg_pivot.log 2>&1 &