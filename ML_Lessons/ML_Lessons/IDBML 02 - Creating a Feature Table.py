# Databricks notebook source
# MAGIC 
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # IDBML 02 - Creating a Feature Table
# MAGIC 
# MAGIC <img src="https://files.training.databricks.com/images/idbml/02-image.png">

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC 
# MAGIC First, we'll run the `Classroom-Setup` notebook to set up our environment.

# COMMAND ----------

# MAGIC %run "./Includes/Classroom-Setup"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import Data
# MAGIC 
# MAGIC Next, we'll import our data for the course.
# MAGIC 
# MAGIC In this course, we'll be using a dataset containing Airbnb listings and we'll be trying to predict the price of those listings.

# COMMAND ----------

listings_df = spark.read.load(input_path)
display(listings_df)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Featurization
# MAGIC 
# MAGIC The `listings_df` DataFrame is already pretty clean, but we do have some categorical features that we'll need to convert to numeric features for modeling.
# MAGIC 
# MAGIC These features include:
# MAGIC 
# MAGIC * **`neighbourhood_cleansed`**
# MAGIC * **`property_type`**
# MAGIC * **`room_type`**
# MAGIC * **`instant_bookable`**
# MAGIC 
# MAGIC ### Create `compute_features` Function
# MAGIC 
# MAGIC A lot of data scientists are familiar with Pandas DataFrames, so we'll use the Koalas library to one-hot encode these categorical features.
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> Notice that we are creating a function to perform these computations. We'll use it to refer to this set of instructions when creating our feature table.

# COMMAND ----------

import databricks.koalas as ks

def compute_features(spark_df):
  
    # Convert to Koalas DataFrame
    koalas_df = spark_df.to_koalas()

    # OHE
    ohe_koalas_df = ks.get_dummies(
      koalas_df, 
      columns=["neighbourhood_cleansed", "property_type", "room_type", "instant_bookable"],
      dtype="float64"
    )

    # Clean up column names
    ohe_koalas_df.columns = ohe_koalas_df.columns.str.replace(' ', '')
    ohe_koalas_df.columns = ohe_koalas_df.columns.str.replace('(', '-')
    ohe_koalas_df.columns = ohe_koalas_df.columns.str.replace(')', '')

    return ohe_koalas_df

# COMMAND ----------

# MAGIC %md
# MAGIC ### Compute Features
# MAGIC 
# MAGIC Next, we can use our featurization function `compute_features` to create create a DataFrame of our features.

# COMMAND ----------

features_df = compute_features(listings_df)
display(features_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Feature Table
# MAGIC 
# MAGIC Next, we can use the DataFrame **`features_df`** to create a feature table using Feature Store.
# MAGIC 
# MAGIC ### Instantiate the `FeatureStoreClient`
# MAGIC 
# MAGIC Our first step is to instantiate the feature store client using `FeatureStoreClient()`.

# COMMAND ----------

from databricks.feature_store import FeatureStoreClient
fs = FeatureStoreClient()

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Create the Feature Table
# MAGIC 
# MAGIC Next, we can use the `feature_table` operation to register the DataFrame as a Feature Store table.
# MAGIC 
# MAGIC In order to do this, we'll want to provide the following:
# MAGIC 
# MAGIC 1. The `name` of the database and table where we want to store the feature table
# MAGIC 1. The `keys` for the table
# MAGIC 1. The `schema` of the table
# MAGIC 1. A `description` of the contents of the feature table
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> This creates our feature table, but we still need to write our values in the DataFrame to the table.

# COMMAND ----------

from databricks.feature_store import feature_table

feature_table = fs.create_feature_table(
  name=f"{database_name}.listings_features",
  keys=["listing_id"],
  schema=features_df.spark.schema(),
  description="This listings-level table contains one-hot encoded and numeric features to predict the price of a listing."
)

# COMMAND ----------

# MAGIC %md
# MAGIC Now, we can write the records from **`features_df`** to the feature table.

# COMMAND ----------

fs.write_table(df=features_df.to_spark(), name=f"{database_name}.listings_features", mode="overwrite")

# COMMAND ----------

# MAGIC %md
# MAGIC At this point, we can head to the Feature Store UI to check out our table.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; 2021 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="http://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/>
# MAGIC <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="http://help.databricks.com/">Support</a>