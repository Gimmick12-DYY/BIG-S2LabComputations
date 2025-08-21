# BIG-S2LabComputations

This repository contains the projects developed within the BIG-S2 Lab at UNC Gillings:

1. **ADRD_KG/**: A knowledge base website project for Alzheimer's Disease-related datasets and studies. This internal database supports the lab's effort to consolidate and query open-source data on ADRD, aiming to streamline research and data access across projects.

2. **ANTs_pipeline/**: A collection of shell scripts to simplify the usage of the Advanced Normalization Tools (ANTs) for MRI image preprocessing. These scripts standardize the pipeline execution for structural neuroimaging tasks.
   
3. **TBSS_pipeline/**: A collection of shell scripts written to coordinate the TBSS pipeline process.

## Structure

```
.
├── ADRD_KG/ # ADRD knowledge-graph + data wrapping utilities
├── ANTs_pipeline/ # Shell helpers around ANTs for structural MRI
├── TBSS_pipeline/ # Shell helpers to coordinate FSL TBSS
├── YODA_Project/ # Data org + processing templates for YODA datasets
├── LICENSE
└── README.md
```

## ADRD_KG
This project utilized the help of LLM models and the Selenium package to wrap open-source datasets.

## ANTs_pipeline
This directory contains only the helper shell scripts used to facilitate the lab ANTs pipeline.

## TBSS_pipeline
This directory contains only the helper shell scripts used to facilitate the lab TBSS pipeline.

## YODA
This directory contains only the scripts used to facilitate lab research on the YODA project.

## Prerequisites
- **General**: `git`, Python ≥ 3.10, `conda` or `venv`.
- **ANTs pipeline**: [ANTs](http://stnava.github.io/ANTs/) installed and on `PATH`; SLURM if submitting to HPC.
- **TBSS pipeline**: [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/TBSS) installed and configured; SLURM if using the cluster.
- **ADRD_KG**: Python + common data/automation libs (see `requirements.txt` or notebooks inside).
- **YODA_Project**: Python; access to YODA data (per project policy).

## License
This repository is licensed under the MIT License.
