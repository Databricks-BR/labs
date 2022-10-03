# Databricks notebook source
# MAGIC 
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # IDBML 03 - Creating a Model with AutoML
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/03-image.png">

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC 
# MAGIC First, we'll run the `Classroom-Setup` notebook to set up our environment.

# COMMAND ----------

# MAGIC %run "./Includes/Classroom-Setup"

# COMMAND ----------

# MAGIC %md
# MAGIC ## AutoML UI
# MAGIC 
# MAGIC As a reminder, AutoML can be used both via the user interface and via a Python-based API.
# MAGIC 
# MAGIC In this demonstration, we're going to develop a baseline model using the user interface.
# MAGIC 
# MAGIC ### Creating an AutoML Experiment
# MAGIC 
# MAGIC #### Navagating to AutoML
# MAGIC 
# MAGIC To do this, start by clicking on the **Experiments** tab in the left sidebar of the Databricks Machine Learning platform.
# MAGIC 
# MAGIC Next, click on the **Start AutoML Experiment** button to begin a new AutoML Experiment.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Setting up the Experiment
# MAGIC 
# MAGIC When prompted, enter the details below – be sure to look for the table in your **own** database!
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/automl-1.png">

# COMMAND ----------

# MAGIC %md
# MAGIC #### Running the Experiment
# MAGIC 
# MAGIC When you're ready to run the experiment, click **Start AutoML**. At this point, AutoML will start automatically generating models to predict price based on the features in the feature table.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/automl-2.png">
# MAGIC 
# MAGIC As the experiment runs, you will start to see MLflow runs appear in the experiment page indicating the models have been completed.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/automl-3.png">
# MAGIC 
# MAGIC You will also see the **Stop Experiment** button. You can stop the AutoML process by clicking this button at any time.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/automl-4.png">

# COMMAND ----------

# MAGIC %md
# MAGIC #### Evaluating the Results
# MAGIC 
# MAGIC AutoML will automatically evaluate each of your models. You can view each of these model's results in the experiment page. AutoML will also provide an easy link for you to view the notebook that generated the best model.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/automl-5.png">

# COMMAND ----------

# MAGIC %md
# MAGIC #### Viewing the Best Model
# MAGIC 
# MAGIC When you view the notebook for the best model, you're able to copy code, edit code, and even clone the exact notebook into your production workflow.
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/automl-6.png">

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; 2021 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="http://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/>
# MAGIC <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="http://help.databricks.com/">Support</a>