# Create App Registration

- In the Azure portal go to “App registrations” and click “New registration”.
- Enter a name for the registration and click “Register”.
- Create a secret for the registration by clicking on the registration then selecting “Certificates & Secrets” under the “Manage” menu.
- Note down the client ID and client secret for later use.

# Create Custom Deployment Role

- In the Subscription “Access Control (IAM)” menu click “Add” -> “Add custom role”.
- In the “JSON” menu and paste the following and replace the Resource Group name and Subscription ID with the values for the resource group containing the production Data Factory.
```
{
    "properties": {
        "roleName": "cicdtest-adf-deploy-role",
        "description": "",
        "assignableScopes": [
            "/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.DataFactory/factories/*",
                    "Microsoft.DataFactory/factories/pipelines/*",
                    "Microsoft.DataFactory/factories/datasets/*",
                    "Microsoft.DataFactory/factories/linkedservices/*",
                    "Microsoft.DataFactory/factories/triggers/*",
                    "Microsoft.Resources/deployments/*",
                    "Microsoft.Resources/subscriptions/resourceGroups/read"
                ],
                "notActions": [],
                "dataActions": [],
                "notDataActions": []
            }
        ]
    }
}
```

- In the resource group IAM menu, assign this role to the service principal.

# Add Azure Credentials in GitHub

- In the Git repository under “Settings”-> “Secrets and variables” -> “Actions” create a Repository Secret with the name “AZURE_CREDENTIALS”.

- Paste in the following and replace the values with the ones created earlier.
```
{
  "clientId": "{client_id}",
  "displayName": "github-actions-adf",
  "clientSecret": "{client_secert}",
  "tenantId": "{tenant_id}",
  "subscriptionId": "{subscription_id}"
}
```

# Alter Arm Template to include Databricks connection config
- If connecting to a Databricks linked service you need to explicitly state the connection parameters in the ARM template
- In ADF go to `settings` -> `Edit parameter configuration`
- Under `"Microsoft.DataFactory/factories/linkedServices"` properties add:
    - `"clusterId": "=",`
    - `"domain": "=",`
- Publish changes to see them reflected in git