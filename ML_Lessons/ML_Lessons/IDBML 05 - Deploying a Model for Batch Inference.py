# Databricks notebook source
# MAGIC 
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # IDBML 05 - Deploying a Model for Batch Inference
# MAGIC 
# MAGIC <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/idbml/05-image.png">

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC 
# MAGIC First, we'll run the `Classroom-Setup` notebook to set up our environment.

# COMMAND ----------

# MAGIC %run "./Includes/Classroom-Setup"

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Loading Necessary Components
# MAGIC 
# MAGIC In this demonstration, we'll be deploying a model for batch inference.
# MAGIC 
# MAGIC Before we begin, we need to load our **model** and our **feature table**.
# MAGIC 
# MAGIC ### Load Model
# MAGIC 
# MAGIC We can load the model directly from the Model Registry.
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> When we load the model as a Spark UDF, it allows us to easily broadcast the model to the different nodes in our cluster to scale out our inference on our distributed feature table.

# COMMAND ----------

import mlflow

model = mlflow.pyfunc.spark_udf(spark, model_uri="models:/idbml-airbnb-price/production")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Load Feature Table
# MAGIC 
# MAGIC Next, we need to load our feature table. Remember that we created this feature table way back in our first demonstration.

# COMMAND ----------

from databricks.feature_store import FeatureStoreClient

fs = FeatureStoreClient()
features = fs.read_table(f"{database_name}.listings_features")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Performing Batch Inference
# MAGIC 
# MAGIC In order to perform batch inference, 

# COMMAND ----------

predictions = features.withColumn('predictions', model(*features.columns))
display(predictions.select("listing_id", "predictions"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write to Delta Lake
# MAGIC 
# MAGIC Finally, we can write our features to Delta Lake.

# COMMAND ----------

predictions.write.mode("append").saveAsTable(f"{database_name}.predictions")


# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; 2021 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="http://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/>
# MAGIC <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="http://help.databricks.com/">Support</a>