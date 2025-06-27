# BIG-S2LabComputations

This repository contains two main components developed within the BIG-S2 Lab at UNC Gillings:

1. **ADRD_KG/**: A knowledge graph project for Alzheimer's Disease-related datasets and studies. This internal tool supports the lab's effort to consolidate and query open-source data on ADRD, aiming to streamline research and data access across projects.

2. **ANTs_pipeline/**: A collection of shell scripts to simplify the usage of the Advanced Normalization Tools (ANTs) for MRI image preprocessing. These scripts standardize the pipeline execution for structural neuroimaging tasks.

## Structure

```
.
├── ADRD_KG/           # Notebooks and scripts for knowledge graph generation
├── ANTs_pipeline/     # Shell scripts wrapping ANTs preprocessing routines
├── LICENSE
└── README.md
```

## Usage

Clone the repository:

```bash
git clone https://github.com/Gimmick12-DYY/BIG-S2LabComputations.git
```

Navigate into either subfolder to explore its purpose. For ANTs, ensure ANTs is installed and configured. For ADRD_KG, Jupyter and standard data science Python packages are required.

## License

This repository is licensed under the MIT License.
