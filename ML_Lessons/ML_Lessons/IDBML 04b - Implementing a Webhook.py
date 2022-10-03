# Databricks notebook source
# MAGIC 
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # IDBML 04b - Implementing a Webhook
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/04b-image.png">

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Model Registry Webhooks
# MAGIC 
# MAGIC ### Supported Events
# MAGIC * Registered model created
# MAGIC * Model version created
# MAGIC * **Transition request created**
# MAGIC * **Model version transitioned stage**
# MAGIC 
# MAGIC ### Types of webhooks
# MAGIC * **HTTP webhook** &mdash; send triggers to endpoints of your choosing such as slack, AWS Lambda, Azure Functions, or GCP Cloud Functions
# MAGIC * Job webhook &mdash; trigger a job within the Databricks workspace

# COMMAND ----------

# MAGIC %md
# MAGIC ## Implementing a Webhook
# MAGIC 
# MAGIC In this demonstration, we're going to implement a couple of notification webhooks using HTTP endpoints and Slack.
# MAGIC 
# MAGIC ### Helper Function
# MAGIC 
# MAGIC The first thing we're going to do is create a helper function to call MLflow endpoints.

# COMMAND ----------

import mlflow
from mlflow.utils.rest_utils import http_request
import json

def client():
    return mlflow.tracking.client.MlflowClient()

host_creds = client()._tracking_client.store.get_host_creds()
host = host_creds.host
token = host_creds.token

def mlflow_call_endpoint(endpoint, method, body='{}'):
    if method == 'GET':
        response = http_request(
            host_creds=host_creds, endpoint="/api/2.0/mlflow/{}".format(endpoint), method=method, params=json.loads(body)
        )
    else:
        response = http_request(
            host_creds=host_creds, endpoint="/api/2.0/mlflow/{}".format(endpoint), method=method, json=json.loads(body)
        )
    return response.json()

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Setting Up Slack Notifications
# MAGIC 
# MAGIC Webhooks can be used to send emails, Slack messages, and more. In this case, we demonstrate the use **Slack for notification purposes**.
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> You'll need to set up the Slack webhook yourself within Slack, but you can read more about Slack webhooks [here](https://api.slack.com/messaging/webhooks#create_a_webhook).
# MAGIC 
# MAGIC #### Transition Request Notification
# MAGIC 
# MAGIC First, we set up a webhook to notify us whenever a **Model Registry transition request is created**.
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> We've hidden the Slack webhook [here]($./Includes/Slack-Webhook) for security purposes, but it should take the form of: `"https://hooks.slack.com/services/T????????/B?????????/????????????????????????"`

# COMMAND ----------

# MAGIC %run ./Includes/Slack-Webhook

# COMMAND ----------

import json 

model_name = "idbml-airbnb-price"

trigger_slack = json.dumps({
    "model_name": model_name,
    "events": ["TRANSITION_REQUEST_CREATED"],
    "description": "This notification triggers when a model is requested to be transitioned to a new stage.",
    "status": "ACTIVE",
    "http_url_spec": {
        "url": slack_webhook
    }
})

mlflow_call_endpoint("registry-webhooks/create", method = "POST", body = trigger_slack)

# COMMAND ----------

# MAGIC %md
# MAGIC Let's test it out by requesting to transition the model to the **Production** stage.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Transition Notification
# MAGIC 
# MAGIC Rather than triggering on a request, this notification will trigger a Slack message when a model is successfully transitioned to a new stage.

# COMMAND ----------

import json 

trigger_slack = json.dumps({
  "model_name": model_name,
  "events": ["MODEL_VERSION_TRANSITIONED_STAGE"],
  "description": "This notification triggers when a model is transitioned to a new stage.",
  "http_url_spec": {
    "url": slack_webhook
  }
})

mlflow_call_endpoint("registry-webhooks/create", method = "POST", body = trigger_slack)

# COMMAND ----------

# MAGIC %md
# MAGIC Let's test it out by transitioning the model to the **Prodiction** stage.

# COMMAND ----------

mlflow_client = mlflow.tracking.client.MlflowClient()
model_version = int(dict(mlflow_client.get_latest_versions(model_name)[0])["version"])
mlflow_client.transition_model_version_stage(
    name=model_name,
    version=model_version,
    stage="Production",
    archive_existing_versions=True
)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Manage Webhooks
# MAGIC 
# MAGIC You can manage your webhooks pretty easily, too.
# MAGIC 
# MAGIC First, you can list all of your webhooks and corresponding information using the cell below.
# MAGIC 
# MAGIC <img alt="Hint" title="Hint" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.3em" src="https://files.training.databricks.com/static/images/icon-light-bulb.svg"/>&nbsp;**Hint:** Notice that these are model-specific webhooks to keep from interfering with others' workflows.

# COMMAND ----------

list_model_webhooks = json.dumps({"model_name": model_name})

model_webhooks = mlflow_call_endpoint("registry-webhooks/list", method = "GET", body = list_model_webhooks)
model_webhooks

# COMMAND ----------

# MAGIC %md
# MAGIC You can also **delete webhooks**.
# MAGIC 
# MAGIC You can use the below cell to delete webhooks by ID.

# COMMAND ----------

mlflow_call_endpoint(
    "registry-webhooks/delete",
    method="DELETE",
    body=json.dumps({'id': model_webhooks["webhooks"][0]["id"]})
)

# COMMAND ----------

# MAGIC %md
# MAGIC Or you can use the below cell to delete all webhooks for a specific model.

# COMMAND ----------

for webhook in model_webhooks["webhooks"]:
    mlflow_call_endpoint(
    "registry-webhooks/delete",
    method="DELETE",
    body=json.dumps({'id': webhook["id"]})
)

# COMMAND ----------

# MAGIC %md
# MAGIC And finally, verify that they're all deleted.

# COMMAND ----------

updated_model_webhooks = mlflow_call_endpoint("registry-webhooks/list", method = "GET", body = list_model_webhooks)
updated_model_webhooks


# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; 2021 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="http://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/>
# MAGIC <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="http://help.databricks.com/">Support</a>