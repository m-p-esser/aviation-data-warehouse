[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fm-p-esser%2Faviation-data-warehouse&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

# Aviation Data Warehouse

## Goal
Goal of this project is to create a Data Warehouse for Aviation data

## Mission Statement
TBD

## Mission Objective
- The database keeps track of flights and their current status (scheduled, delayed, in-time)

## Architecture
- Ralph Kimball's Star Schema

![](docs/images/kappa-architecture.png)

## 📡 Technology

**Storage**
- Google Cloud Storage
- Google BigQuery

**Compute**
- Google Cloud Run

**Orchestration**
- Prefect

**Transformation**
- dbt

**Languages**
- Python
- Bash
- SQL

## Data Sources
- [FlightRader24](https://www.flightradar24.com)

Misc links

- https://www.aviationdb.com/Aviation/Aircraft/1/N136LC.shtm
- https://pypi.org/project/FlightRadarAPI/#description
/51.40,7.16/6
- https://www.flightradar24.com/_json/airlines.php
- https://data-cloud.flightradar24.com/zones/fcgi/feed.js

## Prerequisites

If you want to reproduce some of this code or copy and paste parts of it, feel free to do so.

If you want to build on this projects, here are the prerequisites

- A Google account (to create ressources in GCP)
- A Prefect account (with access to the Prefect Cloud)
- A dbt account (with access to the dbt Cloud)
- Terraform is installed on your machine
- gcloud CLI is installed on your machine
- Expects the following Git branches:
  - master
  - develop
  - test

## Folder structure

These are the main folders (and their their descrptions) of this Github repo. In case some folders are not visible, then they are not meant to be shared (see `.gitignore`) 

*hint: `tree -L 2 -d -A`* 

```
.
└── .github             --> Github actions (e.g. CI)
├── data                --> Data in different stages (raw, staged, final)
│   ├── 00_raw          --> Immutable, raw data
│   ├── 01_staged       --> Raw data that has been persisted in storage
│   └── 02_final        --> Data which can be served (ML, Analytics)
├── docs
│   └── images          --> Images used in this Readme.md
├── images              --> Docker Images (which are used across flows)
├── make                --> Makefiles for setting up ressources and environment
├── references          --> Data dictionaries, manuals, and all other explanatory materials
├── src                 --> Source code
│   ├── experimental    --> Prefect Flows
│   ├── infra           --> Terraform Infrastructure definitions
│   ├── prefect         --> Prefect Flows and Blocks
│   └── schema          --> Pandera Schemas (Data Validation)
└── tests               --> Unit tests
```

## Most important files on root level

- `prefect.yaml`: Deployment steps and configuration
- `.pre-commit-config.yaml`: Pre-commit hooks which are run before each commit
- `Makefile`: Settings for Makefile (which are stored in folder `make/*`)
- `pyproject.toml` & `poetry.lock`: Python dependencies 

## Setup

### Activate Pre-commit 
Install Pre-commit hooks (for code formatting, import statement checks before committing)
- `poetry run pre-commit install`

### Install Python dependencies
- `poetry install`

### Environment Variables
Define values in `.env` (not part of this repository)

For reference check `.env.example` which contains all major variables required for this project

### Github Action Secrets
Add the following Secrets as Action secrets to your Github repository: 
- `PREFECT_API_KEY`
- `PREFECT_API_URL`

See https://docs.prefect.io/latest/api-ref/rest-api/#finding-your-prefect-cloud-details

### GCP Setup
Run `poetry run make setup-gcp` to setup up the Google Cloud Project

If this doesn't work, run the commands from `00_setup_gcp.mk` command by command in the following order:
- `poetry run make create-gcp-project`
- `poetry run make set-default-gcp-project`
- `poetry run make link-project-to-billing-account`
- `poetry run make create-deployment-service-account`
- `poetry run make create-deployment-service-account-key-file`
- `poetry run make enable-gcp-services`
- `poetry run make bind-iam-policies-to-deployment-service-account`
- `poetry run make set-deployment-service-account-as-default`

### Environment Setup
*necessary everytime you start working on the project*
- `make dev-init` to setup development environment
- `export $(grep -v '^#' .env | xargs)` (@see https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs)

### Prefect Setup
As mentioned above, this project requires a Prefect account and access to the Prefect Cloud
- `make setup-prefect` 

### Setup Infrastructure
Setup the storage infrastructure by running
- cd `src/infrastructure`
- When running for the first time `terraform init`
- `terraform plan`
- `terraform apply`. Confirm by typing *"yes"*

### Deployment and Testing

Start on `develop`
- Write Tasks and Flows
- If necessary write Unit Tests
- Run `make run-unit-tests`

Move on to `test`
- Merge with `develop`
- Run `make env-init`
- Run `export $(grep -v '^#' .env | xargs)`
- Setup Infrastructure (see steps above) 
- Deploy Flow by running `make deploy-flow`
- Run integration test trough a manual Flow run
- Sync with Bigquery (using existing Flow if you want to sync GCS and Bigquery using a Push pattern)

Move on `prod`
- Merge with `test`
- Run `make env-init`
- Run `export $(grep -v '^#' .env | xargs)`
- Setup Infrastructure (see steps above) 
- Deploy Flow by running `make deploy-flow`
- Sync with Bigquery (using existing Flow if you want to sync GCS and Bigquery using a Push pattern)
