# Databricks notebook source
# MAGIC 
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # IDBML 06 - Scheduling a Machine Learning Workflow
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/06-image.png">

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC 
# MAGIC First, we'll run the `Classroom-Setup` notebook to set up our environment.

# COMMAND ----------

# MAGIC %run "./Includes/Classroom-Setup"

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Training Workflow
# MAGIC 
# MAGIC In this notebook, we'll create a workflow to retrain our model. Then, we'll set up this notebook to run monthly using a Databricks Job to ensure our model is always up-to-date.
# MAGIC 
# MAGIC ### Load Features
# MAGIC 
# MAGIC First, we'll load in our feature table.
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> In the case of this demonstration, these are the same records &mdash; but in real-world scenario, we'd likely have updated records appended to this table each time the model is trained.

# COMMAND ----------

from databricks.feature_store import FeatureStoreClient

feature_table = f"{database_name}.listings_features"
fs = FeatureStoreClient()
features = fs.read_table(feature_table)

# COMMAND ----------

# MAGIC %md
# MAGIC ### AutoML Process
# MAGIC 
# MAGIC Next, we'll use the AutoML API to kick off an AutoML regression experiment. This is similar to what we did with the AutoML UI, but we can use the API to automate this process.

# COMMAND ----------

import databricks.automl
model = databricks.automl.regress(
    features, 
    target_col="price",
    primary_metric="r2",
    timeout_minutes=5,
    max_trials=10,
    
) 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Register the Best Model
# MAGIC 
# MAGIC Once the AutoML experiment is done, we can identify the best model from the experiment and register that model to the Model Registry.

# COMMAND ----------

import mlflow
from mlflow.tracking.client import MlflowClient

client = MlflowClient()

run_id = model.best_trial.mlflow_run_id
model_name = "idbml-airbnb-price"
model_uri = f"runs:/{run_id}/model"

model_details = mlflow.register_model(model_uri, model_name)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Request Transition to Staging
# MAGIC 
# MAGIC Once the model is registered, we request that it be transitioned to the **Staging** stage for testing.
# MAGIC 
# MAGIC First, we'll load in some helper functions from the **`./Includes/Registry-Helpers`** notebook.

# COMMAND ----------

# MAGIC %run ./Includes/Registry-Helpers

# COMMAND ----------

# MAGIC %md
# MAGIC Next, we'll set up the transition request using the `mlflow_call_endpoint` operation from the helpers notebook.

# COMMAND ----------

staging_request = {'name': model_name, 'version': model_details.version, 'stage': 'Staging', 'archive_existing_versions': 'true'}
mlflow_call_endpoint('transition-requests/create', 'POST', json.dumps(staging_request))

# COMMAND ----------

# MAGIC %md
# MAGIC And we'll add a comment to the version of the model that we just requested be moved to **Staging** to let the machine learning engineer know why we are making the request.

# COMMAND ----------

# Leave a comment for the ML engineer who will be reviewing the tests
comment = "This was the best model from the most recent AutoML run. I think we can use it to update our workflow. Let's set it up for testing."
comment_body = {'name': model_name, 'version': model_details.version, 'comment': comment}
mlflow_call_endpoint('comments/create', 'POST', json.dumps(comment_body))

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Scheduling the Training Workflow
# MAGIC 
# MAGIC Now that we've created our training workflow, we're going to schedule this notebook to run in a Databricks Job.
# MAGIC 
# MAGIC ### Creating a Databricks Job
# MAGIC 
# MAGIC #### Step 1
# MAGIC 
# MAGIC To create a Databricks Job, we want to start by clicking on the **Jobs** button in the sidebar.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/job-1.png">
# MAGIC 
# MAGIC #### Step 2
# MAGIC 
# MAGIC Next, click on the **Create Job** button at the top of the page.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/job-2.png">
# MAGIC 
# MAGIC #### Step 3
# MAGIC 
# MAGIC Third, we'll want to fill out the details of our job.
# MAGIC 
# MAGIC In this case, we want to run this notebook on a Job cluster.
# MAGIC 
# MAGIC Once we've filled out this form, we need to click the **Save** button.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/job-3.png">
# MAGIC 
# MAGIC #### Step 4
# MAGIC 
# MAGIC And because we want the job to run monthly, we need to set up a schedule.
# MAGIC 
# MAGIC Click the **No Schedule** button in the top-right corner of the page.
# MAGIC 
# MAGIC Next, fill out the schedule form for your Job to run monthly.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/job-4.png">
# MAGIC 
# MAGIC #### Step 5
# MAGIC 
# MAGIC After setting up our Job schedule, we'll want to set up alerts for our job.
# MAGIC 
# MAGIC Click on the **Settings** tab at the top of the screen.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/job-5.png">
# MAGIC 
# MAGIC #### Step 6
# MAGIC 
# MAGIC On the Settings page, you can set up things like alerts and permissions.
# MAGIC 
# MAGIC In this case, we've set up our Job to send us an email alert in the case of the Job failing. You can also set up alerts for when your Job starts and succeeds.
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> If you're working on a team, you'll want to be sure your team members have the appropriate permissions to work with your Job and the corresponding notebook!
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/job-6.png">
# MAGIC 
# MAGIC #### Step 7
# MAGIC 
# MAGIC At this point, our Job should be set up to run each month!
# MAGIC 
# MAGIC However, we recommend running your Job immediately to verify that all works as expected.
# MAGIC 
# MAGIC To do this, click on the **Runs** tab at the top of the page and then click on **Run Now**.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/job-7.png">
# MAGIC 
# MAGIC #### Step 8
# MAGIC 
# MAGIC At this point, you should see the Run under the Active Runs section. Click on the **View Details** button.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/job-8.png">
# MAGIC 
# MAGIC #### Step 9
# MAGIC 
# MAGIC This will show you the path for your Job. In this case, we just have one task. You can click on the task to see the running notebook.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/job-9.png">

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; 2021 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="http://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/>
# MAGIC <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="http://help.databricks.com/">Support</a>