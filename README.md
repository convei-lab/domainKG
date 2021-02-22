# domainKG
This is code for Experiment using domain specific KG.

We use the pytorch implementation for the EMNLP 2020 (Findings) paper: Connecting the Dots: A Knowledgeable Path Generator for Commonsense Question Answering [[arxiv](https://arxiv.org/abs/2005.00691)][[project page](https://wangpf3.github.io/pathgen-project-page/)]

Codes in the below folders are based on [Path-Generator-QA](https://github.com/wangpf3/Commonsense-Path-Generator).

* Commonsense-Path-Generator
    Please refer to the following [link](https://github.com/wangpf3/Commonsense-Path-Generator) for installation.

The raw file of domain KG is located at /home/yujin/dot/preprocess_DoKG/raw_data/baby-domain-hiararchy-refined.csv .

If you have any additional needs, please request.
## Quick start PG
1. You can dowload trained path generator 
    - path generator trained with domain kg [checkpoint](https://drive.google.com/file/d/1LSM0kV5-QVbU_SSxWA5-H8c4lOBJh2eQ/view?usp=sharing) 
    - path generator trained with ConceptNet [checkpoint](https://drive.google.com/file/d/1dQNxyiP4g4pdFQD6EPMQdzNow9sQevqD/view)
    - path generator trained with KG integrated domain KG and ConceptNet using naive method [checkpoint](https://drive.google.com/file/d/1NHpRYZmlZ9kQI81sReFhs29OTKYFWrZ0/view?usp=sharing)
    - path generator trained with KG integrated domain KG and ConceptNet using pivoting [checkpoint](https://drive.google.com/file/d/1cMebP7dQzHM_z9rtDWwax5ywukUniQdt/view?usp=sharing)

2. Before run the below code, check the source file path and save path.
    ```bash
    cd learning-generator
    sh run_test_pg.sh
    ```

## Path-Generator for domain specific KG
1. Preprocess
    Before run the below code, check the source file path and save path.
    ```bash
    cd preprocess_DoKG
    sh convert_csv_to_nx.sh
    ```

2. For training a path generator
    ```bash
    cd learning-generator
    sh run_dokg_multi_di_rev_no_hiar.sh
    ```
    If you set the setting 'split_dataset' as True, split dataset for training by ratio of 0.9:0.05:0.05 will be saved under output_dir.

3. Train path generator using domainKG
    ```bash
    ./run_path_sampling_dokg_multi_di_rw_no_hiar.sh $gpu_device
    ```

## Path-Generator for integrate CSKG and domain specific KG
1. Preprocess
    Before run the below code, check the source file path and save path.
    ```bash
    cd preprocess_integrate_kg/integrateKG
    sh integrate_kg.sh
    ```

2. For training a path generator
    ```bash
    cd learning-generator
    sh run_path_sampling_inte_pivot.sh
    ```
    If you set the setting 'split_dataset' as True, split dataset for training by ratio of 0.9:0.05:0.05 will be saved under output_dir.

3. Train path generator using domainKG
    ```bash
    ./run_inte_pivot.sh $gpu_device
    ```

## For training a commonsense qa system
1. Download Data
First, you need to download all the necessary data in order to train the model:
    ``` bash
    cd commonsense-qa
    bash scripts/download.sh
    ```

2. Preprocess
To preprocess the data, run:
    ``` bash
    python preprocess.py   
    ```

3. Using the path generator to connect question-answer entities
(Modify ./config/path_generate.config to specify the dataset and gpu device)
    ``` bash
    ./scripts/run_generate.sh
    ```

    3.1. For domain specific KG
        (Modify ./config/path_generate_dokg_multi_di.config to specify the dataset and gpu device)
        ``` bash
        ./scripts/run_generate_dokg_multi_di.sh
        ```

    3.2. For domain specific KG
        (Modify ./config/path_generate_dokg_multi_di.config to specify the dataset and gpu device)
        ``` bash
        ./scripts/run_generate_dokg_multi_di.sh
        ```


4. Commonsense QA system training
bash scripts/run_main.sh ./config/csqa.config
Training process and final evaluation results would be stored in './saved_models/'