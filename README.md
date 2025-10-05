# h2g-a Repository

## Setting Up the Environment

1. Navigate to the `h2g-a` directory.
2. Run the following command to create the environment:
    ```bash
    conda env create --file environment.yaml
    ```
3. Activate the environment using:
    ```bash
    conda activate pypsa-earth
    ```

To execute the entire workflow, use:
```bash
snakemake -j 1 all
```

## Functionality Overview and Instructions

This repository provides multiple functionalities organized into distinct work packages:

### Africa Hydrogen Analysis

To prepare the necessary data for the `africa_hydrogen_analysis.ipynb` notebook, run:
```bash
snakemake -j 1 retrieve_h2_networks
```
Afterward, open the notebook to explore the visualizations.

### Post-Processing Results

Run the following command:
```bash
snakemake -j 1 prepare_postprocessing
```
This will automatically execute the prerequisite rule `retrieve_result_networks`. Once completed, you will have all the required data to analyze the `plot_marginal_prices.ipynb` and `plot_summary.ipynb` notebooks.

## ⚠️ Handling Download Errors

The current framework for downloading network files is still under development and may encounter connection or permission issues. If you experience such problems, you can manually download the required files using the instructions below. Once placed correctly, the rest of the Snakemake workflow should function as expected. 

If you're familiar with Snakemake, you may also refer to the Snakefile for a deeper understanding of the workflow and file dependencies.

### ✅ Solved Hydrogen Networks

1. Download the `solved_h2.zip` file from this [link](https://zenodo.org/records/16945007).
2. Extract the contents.
3. Move the extracted `solved_h2` folder into the `networks/` directory.  
    *(If the `networks/` directory does not exist, you may need to create it.)*

### ✅ Post-Processing Results Networks

1. Download the `.zip` file from this [link](https://zenodo.org/records/17129490).
2. Extract the contents.
3. Move the extracted `AP2_pypsa_earth_results` folder into the `results/` directory.
    *(If the `results/` directory does not exist, you may need to create it.)*

## Results - Dashboard

The results are available via the following dashboard:

https://h2export.streamlit.app/

To run the dashboard on your local machine, open the terminal in the repository. Make sure you have a Streamlit-compatible environment.
If you're working within the pypsa-earth environment, you'll need to install two additional packages first:
```bash
pip install streamlit
```
```bash
pip install pyaml
```

Then, launch the dashboard with:
```bash
streamlit run app.py
```