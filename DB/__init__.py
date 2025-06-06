import azure.functions as func
import json
from azure.data.tables import TableServiceClient
import os

table = TableServiceClient.from_connection_string(os.getenv("AzureWebJobsStorage")).get_table_client("urlshorts")
table.create_table_if_not_exists()

def main(msg: func.RabbitMQMessage):
    d = json.loads(msg.get_body().decode())
    table.upsert_entity({"PartitionKey":"urls", "RowKey": d["hash"], "url": d["url"]})
    logging.info(f"Saved {d['hash']} → {d['url']}")
