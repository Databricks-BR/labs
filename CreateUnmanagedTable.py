# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC ## Overview
# MAGIC 
# MAGIC This notebook will show you how to create an **unmanaged** Delta table originating from a file that you uploaded to DBFS. The key difference here lies in what we do after reading the CSV into a DataFrame.
# MAGIC 
# MAGIC BEFORE
# MAGIC 1. Wrote out the DataFrame as a Delta table
# MAGIC 
# MAGIC NOW
# MAGIC 1. Write out the DataFrame in Delta format
# MAGIC 2. Wrap that data with a Delta table

# COMMAND ----------

# File location and type
file_location = "/FileStore/uszips.csv"
file_type = "csv"

#this example had an error in it

# CSV options
infer_schema = "true"
first_row_is_header = "true"
delimiter = ","

# The applied options are for CSV files. For other file types, these will be ignored.
df = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .option("escape", "\"") \
  .load(file_location)

display(df)

# COMMAND ----------

delta_file_name = "uszips_delta"

# write data out in Delta format
df.write.format("delta").save('/mnt/delta/%s' % delta_file_name)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE uszips_delta_unmanaged USING DELTA LOCATION '/mnt/delta/uszips_delta/'
