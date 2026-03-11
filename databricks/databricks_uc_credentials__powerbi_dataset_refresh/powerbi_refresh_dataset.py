# Databricks notebook source
# MAGIC %md
# MAGIC %md
# MAGIC # PowerBI Dataset Refresh
# MAGIC
# MAGIC Notebook for sending a request to the PowerBI API to refresh a dataset
# MAGIC
# MAGIC ## Input Parameters:
# MAGIC `p_dataset_id`: The ID of the published dataset to refresh

# COMMAND ----------

# MAGIC %pip install azure-mgmt-datafactory azure-identity
# MAGIC
# MAGIC import os
# MAGIC import time
# MAGIC from azure.identity import DefaultAzureCredential

# COMMAND ----------

# set env variable
ENV_NAME = os.getenv('ENV_NAME','')
spark.sql('SET var.ENV_NAME = '+ ENV_NAME)


UC_CREDENTIAL_NAME = f"demosuite{ENV_NAME}_azservices-dbsc"

# Recieve dataset ID passed in through parameter
DATASET_ID = dbutils.widgets.get("p_dataset_id")

# COMMAND ----------

# set env variable
ENV_NAME = "dev"

UC_CREDENTIAL_NAME = f"demosuite{ENV_NAME}_azservices-dbsc"

DATASET_ID = "b3ef70c3-b034-4307-a3e9-5f038808b182"

# COMMAND ----------

credential=dbutils.credentials.getServiceCredentialsProvider(UC_CREDENTIAL_NAME)

# COMMAND ----------

import requests

# Power BI API scope
SCOPE = "https://analysis.windows.net/powerbi/api/.default"

# Get token using default credentials
token = credential.get_token(SCOPE).token
print(token)
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

url = f"https://api.powerbi.com/v1.0/myorg/groups"

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)
print(response.json())
