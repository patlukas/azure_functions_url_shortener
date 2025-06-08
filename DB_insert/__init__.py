import azure.functions as func
from azure.data.tables import TableServiceClient
import os
import logging
import json

table_service = TableServiceClient.from_connection_string(os.getenv("AzureWebJobsStorage"))
table = table_service.create_table_if_not_exists("urlshorts")


def main(msg: func.ServiceBusMessage):
    message_body = msg.get_body().decode('utf-8')
    data = json.loads(message_body)

    short_hash = data['hash']
    url = data['url']

    entity = {
        'PartitionKey': 'urls',
        'RowKey': short_hash,
        'url': url
    }

    table.upsert_entity(entity)