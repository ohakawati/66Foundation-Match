from google.cloud import bigquery as bq
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('credentials.json')

def query_matte(rvalue, gvalue, bvalue, undertone, coverage, budget):

  client = bq.Client(credentials= credentials, project="geometric-bay-354718")
  query = """
    SELECT predicted_Name FROM ml.PREDICT(MODEL bqml_test.fendymatteprofiltr_model, (
      SELECT
      """+str(int(rvalue))+""" as R,
      """+str(int(gvalue))+""" as G,
      """+str(int(bvalue))+""" as B,
      @Undertone as Undertone,
      @Coverage as Coverage,
      """+str(budget)+""" as Price,
  ))"""

  job_config = bq.QueryJobConfig(
      query_parameters=[
          bq.ScalarQueryParameter("Undertone", "STRING", undertone),
          bq.ScalarQueryParameter("Coverage", "STRING", coverage),
      ]
  )

  query_job = client.query(query, job_config=job_config)

  for row in query_job:
      return row[0]

def query_dewy(rvalue, gvalue, bvalue, undertone, coverage, budget):

  client = bq.Client(credentials= credentials, project="geometric-bay-354718")
  query = """
    SELECT predicted_Name FROM ml.PREDICT(MODEL bqml_test.fendydewyeasedrop_model, (
      SELECT
      """+str(int(rvalue))+""" as R,
      """+str(int(gvalue))+""" as G,
      """+str(int(bvalue))+""" as B,
      @Undertone as Undertone,
      @Coverage as Coverage,
      """+str(budget)+""" as Price,
  ))"""

  job_config = bq.QueryJobConfig(
      query_parameters=[
          bq.ScalarQueryParameter("Undertone", "STRING", undertone),
          bq.ScalarQueryParameter("Coverage", "STRING", coverage),
      ]
  )

  query_job = client.query(query, job_config=job_config)

  for row in query_job:
      return row[0]

def get_data(item):

  client = bq.Client(credentials= credentials, project="geometric-bay-354718")

  query = """
    SELECT Product, Link, Price
        FROM `geometric-bay-354718.foundationcolor.fentyurls`
        WHERE Name = @Name"""

  job_config = bq.QueryJobConfig(
    query_parameters=[
        bq.ScalarQueryParameter("Name", "STRING", item)
    ]
  )

  query_job = client.query(query, job_config=job_config)

  array = []

  for row in query_job:
    for item in row:
      array.append(item)

  return array