# domainKG
This is code for Experiment using domain specific KG.

We use the pytorch implementation for the EMNLP 2020 (Findings) paper: Connecting the Dots: A Knowledgeable Path Generator for Commonsense Question Answering [[arxiv](https://arxiv.org/abs/2005.00691)][[project page](https://wangpf3.github.io/pathgen-project-page/)]

Codes in the below folders are based on [Path-Generator-QA](https://github.com/wangpf3/Commonsense-Path-Generator).

* Commonsense-Path-Generator
    Please refer to the following [link](https://github.com/wangpf3/Commonsense-Path-Generator) for installation.

## Path-Generator for domain specific KG
1. Preprocess
    Before run the below code, check the source file path and save path.
    ```bash
    cd preprocess_DoKG
    sh convert_csv_to_nx.sh
    ```

2. For training a path generator
    ```bash
    cd Commonsense-Path-Generator/learning-generator
    sh run_path_sampling.sh
    ```
    If you set the setting 'split_dataset' as True, split dataset for training by ratio of 0.9:0.05:0.05 will be saved under output_dir.

3. Train path generator using domainKG
    ```bash
    run.sh $gpu_device
    ```

