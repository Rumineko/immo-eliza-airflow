<h1 align="center">
🦀 HermitCrab Sea Breeze 🦀
</h1>




<p align="center">
    <br>
    <a><img alt="Latest Version" src="https://forthebadge.com/images/featured/featured-built-with-love.svg"></a>
    <br>
    <br>
    <a><img alt="Charlie" src="https://camo.githubusercontent.com/fa2625327c912ea67d93c9b2c2a6d3dab6625c5b74cb9fe349ba6fddd5422ea4/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313230393035333033353738333931333530322f313231343839333532313231323031383735382f436861726c69655f3130302e706e673f65783d36363136373434332669733d363630336666343326686d3d6666613030613835303364316430393930363839633561303237653766366565636661333630633164613462383635333437383930353436393637343031353926"></a>
    <h2 align="center">Using:
    <br>
    <br>
    <a><img alt="Latest Version" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"></a>
    <a><img alt="Development Build Status" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/></a>
    <a><img alt="Development Build Status" src="https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white"/></a>
    <br>
</p>

## 📖 Description

To finish up HermitCrab's ImmoEliza project, we determined that it would be necessary to automate the process of Collecting, Processing and Analyzing the Data, as well as the creation of the Machine Learning Model from said Data.

To do so, we have made implemented and adapted our program to Apache Airflow, with the goal of creating a pipeline to automatically run the tasks every day.

## 📋 Pipeline Structure
The pipeline runs daily, and follows the following structure:

![ElizaPipeline](./assets/immo-eliza-schema.png)

- First it scrapes all the data from immoweb, and stores it in a .csv file
- It then cleans the data, for both Analysis and Training of a Machine Learning Model.
- The data is then used for Analysis, as well as the creation of a newer model.
- All daily data is saved and archived as different versions, so you can compare performance metrics, as well as changes to the Housing Market.

## 🛠️ Setup & Installation

- Create a new virtual environment by executing this command in your terminal:
  `python3 -m venv crab-api`
- Activate the environment by executing this command in your terminal:
  `source crab-api/bin/activate`
- Install the required dependencies by executing this command in your terminal:
  `pip install -r requirements.txt`

## 👩‍💻 Usage

This project uses Docker Containers to run Airflow, so make sure to have Docker Compose, and have run the commands above to install requirements.txt, and then run the following command in your terminal:

```
docker compose up --build
```
## 📦 Project Structure

```
.
├── assets/
│   └── immo-eliza-schema.png
├── config/
│   └── ...
├── dags/
│   ├── eliza/
│   │   ├── analysis/
│   │   │   └── ...
│   │   ├── collection/
│   │   │   └── ...
│   │   └── machinelearning/
│   │       └── ...
│   └── eliza.py
├── logs/
│   ├── dag_id=immo_eliza/
│   │   └── ...
│   ├── dag_processor_manager/
│   │   └── ...
│   └── scheduler/
|       └── ...
├── plugins/
├── .env
├── .gitattributes
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt
```