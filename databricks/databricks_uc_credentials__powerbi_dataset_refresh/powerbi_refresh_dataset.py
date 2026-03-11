# Databricks notebook source
# MAGIC %md
# MAGIC %md
# MAGIC # PowerBI Dataset Refresh
# MAGIC
# MAGIC Notebook for sending a request to the PowerBI API to refresh a dataset
# MAGIC
# MAGIC ## Input Parameters:
# MAGIC - `p_dataset_id`: The ID of the published dataset to refresh
# MAGIC - `p_workspace_id`: The ID of the workspace where the report is published
# MAGIC
# MAGIC ## Setup
# MAGIC - This uses a Databricks Unity Catalog Access Connector to send a Power BI dataset refresh request via the Power BI API
# MAGIC - The Access Connector needs to be added to the PowerBI workspace with permission to refresh the dataset
# MAGIC - Service principals need to be allowed to call the Fabric api: https://learn.microsoft.com/en-us/fabric/admin/service-admin-portal-developer#service-principals-can-call-fabric-public-apis

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
WORKSPACE_ID = dbutils.widgets.get("p_workspace_id")

# COMMAND ----------

import requests

# Power BI API scope
SCOPE = "https://analysis.windows.net/powerbi/api/.default"

DATASET_URL = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/datasets/{DATASET_ID}"

credential=dbutils.credentials.getServiceCredentialsProvider(UC_CREDENTIAL_NAME)

# Get token using default credentials
token = credential.get_token(SCOPE).token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
dataset_response = requests.get(DATASET_URL, headers=headers).json()

print(f"Refreshing dataset: {dataset_response['name']}")

refresh_response = requests.post(
    f"{DATASET_URL}/refreshes",
    headers=headers
)
refresh_response.raise_for_status()

print("Refresh request sent.")
