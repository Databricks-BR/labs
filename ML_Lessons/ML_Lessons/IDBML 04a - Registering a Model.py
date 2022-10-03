# Databricks notebook source
# MAGIC 
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # IDBML 04a - Registering a Model
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/04-image.png">

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC 
# MAGIC First, we'll run the `Classroom-Setup` notebook to set up our environment.

# COMMAND ----------

# MAGIC %run "./Includes/Classroom-Setup"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Model Registry Overview
# MAGIC 
# MAGIC One of the primary challenges among data scientists and machine learning engineers is the absence of a central repository for models, their versions, and the means to manage them throughout their lifecycle.  
# MAGIC 
# MAGIC The [MLflow Model Registry](https://docs.databricks.com/applications/mlflow/model-registry.html) addresses this challenge and enables members of the data team to:
# MAGIC <br><br>
# MAGIC * **Discover** registered models, current stage in model development, experiment runs, and associated code with a registered model
# MAGIC * **Transition** models to different stages of their lifecycle
# MAGIC * **Deploy** different versions of a registered model in different stages, offering MLOps engineers ability to deploy and conduct testing of different model versions
# MAGIC * **Test** models in an automated fashion
# MAGIC * **Document** models throughout their lifecycle
# MAGIC * **Secure** access and permission for model registrations, transitions or modifications
# MAGIC 
# MAGIC <img src="https://databricks.com/wp-content/uploads/2020/04/databricks-adds-access-control-to-mlflow-model-registry_01.jpg">

# COMMAND ----------

# MAGIC %md
# MAGIC ## Registering Models to Model Registry
# MAGIC 
# MAGIC There are two ways to register models to Model Registry:
# MAGIC 
# MAGIC 1. MLflow Run's page UI
# MAGIC 1. MLflow Model Registry API

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### MLflow Run's Page UI
# MAGIC 
# MAGIC First, we'll demonstrate how to register a model via the MLflow Run's page UI.
# MAGIC 
# MAGIC #### Step 1
# MAGIC 
# MAGIC The first thing that you need to do is navigate to the MLflow Experiment page for your project. On that page, you'll see a list of MLflow Runs.
# MAGIC 
# MAGIC Click on the link in the **Models** tab for the row of the model you'd like to register.
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/model-registry-2.png">
# MAGIC 
# MAGIC #### Step 2
# MAGIC 
# MAGIC This will take you to the MLflow Run page &mdash; it'll automatically scroll down the page and stop at the "Artifacts" section.
# MAGIC 
# MAGIC In that area, there will be a **Register Model** button. Click on this button to begin registering your model.
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/model-registry-1.png">
# MAGIC 
# MAGIC #### Step 3
# MAGIC 
# MAGIC When registering your model, you'll want to create a new Model in the Model Registry (if a model for your project hasn't already been registered) *and* give it a new name.
# MAGIC 
# MAGIC When you've completed this form, click **Register**.
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/model-registry-3.png">
# MAGIC 
# MAGIC #### Step 4
# MAGIC 
# MAGIC At this point, your model is registering to the Model Registry. You should see this on your Model page.
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/model-registry-4.png">
# MAGIC 
# MAGIC #### Step 5
# MAGIC 
# MAGIC You can view the model's page in the Model Registry. You'll notice that one version is registered.
# MAGIC 
# MAGIC Click on the **Version 1** link to view the page for that specific version of the model.
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/model-registry-5.png">
# MAGIC 
# MAGIC #### Step 6
# MAGIC 
# MAGIC On the model's page, we want to request that we transition this model to the "Staging" stage of our deployment lifecycle. This will notify the owner of the model that a request has been made for them to review.
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> If you have the appropriate permissions, you can transition the model to a stage without review from another member of the team.
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/model-registry-6.png">
# MAGIC 
# MAGIC #### Step 7
# MAGIC 
# MAGIC The user requesting the stage transition will have the opportunity to leave comments on their request.
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/model-registry-7.png">
# MAGIC 
# MAGIC #### Step 8
# MAGIC 
# MAGIC If you are a reviewer and need to review a stage transition request, you are able to do so in the UI.
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/model-registry-8.png">
# MAGIC 
# MAGIC #### Step 9
# MAGIC 
# MAGIC The reviewer also has the opportunity to leave comments.
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/model-registry-9.png">
# MAGIC 
# MAGIC #### Step 10
# MAGIC 
# MAGIC Finally, verify that your model is has successfully been moved to **Staging**.
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/model-registry-10.png">

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC 
# MAGIC ### MLflow Model Registry API
# MAGIC 
# MAGIC Next, we'll provide the code to register a model and demonstrate how to request a stage transition.
# MAGIC 
# MAGIC #### Registering a Model
# MAGIC 
# MAGIC To register a model programmatically, you can use the following code block.
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> Note that we're registering the same model to the same MLflow Model Registry Model here, so it'll create a new version of that model.

# COMMAND ----------

# Import libraries
import mlflow
from mlflow.tracking import MlflowClient

# Manually set parameter values
experiment_name = f"/Users/{username}/databricks_automl/price_listings_features-idbml"
model_name = "idbml-airbnb-price"

# Instantiate client
client = MlflowClient()

# Find best run ID for experiment
experiment = client.get_experiment_by_name(experiment_name)
best_run_id = mlflow.search_runs(experiment.experiment_id).sort_values("metrics.val_r2_score", ascending=False).loc[0, "run_id"]

# Register model
model_uri = f"runs:/{best_run_id}/model"
model_details = mlflow.register_model(model_uri, model_name)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC #### Update Description
# MAGIC 
# MAGIC We can now update the description with some useful information.
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> We can also do this in the UI.

# COMMAND ----------

client.update_registered_model(
    name=model_details.name,
    description="This model predicts the price of Airbnb rentals in London."
)

client.update_model_version(
    name=model_details.name,
    version=model_details.version,
    description="This model version was built using sklearn."
)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Transition to Staging
# MAGIC 
# MAGIC Next, we can transition the model we just registered to "Staging".

# COMMAND ----------

client.transition_model_version_stage(
    name=model_details.name,
    version=model_details.version,
    stage="Staging",
    archive_existing_versions=True
)

# COMMAND ----------

# MAGIC %md
# MAGIC And finally, head to the Model Registry to verify that your model is in the **Staging** stage.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; 2021 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="http://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/>
# MAGIC <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="http://help.databricks.com/">Support</a>