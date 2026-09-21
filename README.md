# HackMIT — Healthcare Schema Mapping Pipeline

🏆 **Xficient Challenge Winner | HackMIT 2024**

A Python-based data transformation pipeline that automates the mapping of healthcare enrollment data between organizations with different database schemas and formatting requirements.

## Overview

Healthcare organizations often store similar member and enrollment information using different schemas, making data exchange complex and time-consuming.

For the **Xficient Challenge at HackMIT 2024**, I developed a pipeline that transforms healthcare enrollment data from a source TPA (Third-Party Administrator) into the format required by a receiving TPA.

### Pipeline

`Source Data → Data Extraction → Schema Mapping → Transformation → Excel Output`

## Key Features

- Processes member, subscriber, and enrollment data from multiple CSV files
- Connects members with their corresponding subscriber and enrollment information
- Maps fields between different healthcare data schemas
- Transforms relationship codes, dates, identifiers, and enrollment information
- Generates a structured Excel file matching the target format
- Uses Python dictionaries and pandas for efficient data processing

## Tech Stack

**Python • pandas • CSV • Excel • Data Transformation • Schema Mapping**

## Data

> **All healthcare data in this repository is synthetic test data provided for the HackMIT challenge.**

The dataset contains **no real patient information, PII, or PHI**. Any names, addresses, SSNs, dates of birth, member IDs, or other sensitive-looking information are entirely fictional and used only for development and testing.

## Repository Structure

```text
├── src/
│   └── data_mapper.py
├── data/
│   └── *.csv
├── output/
│   └── results.xlsx
├── docs/
│   └── presentation.pdf
└── README.md
```

## Future Work

The HackMIT prototype uses deterministic Python-based mapping rules. A proposed extension is to use **Generative AI** to interpret healthcare companion guides and automatically determine mappings between previously unseen schemas.

## Running the Project

```bash
pip install pandas openpyxl
python src/data_mapper.py
```

## Author

**Mariam Rukhaia**  
Computer Science & Cybersecurity — NYU Tandon School of Engineering
