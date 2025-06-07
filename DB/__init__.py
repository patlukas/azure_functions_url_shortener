import azure.functions as func
from azure.data.tables import TableServiceClient
import os
import logging


table_service = TableServiceClient.from_connection_string(os.getenv("AzureWebJobsStorage"))
table = table_service.create_table_if_not_exists("urlshorts")


def main(req: func.HttpRequest) -> func.HttpResponse:
    h = req.route_params.get('hash')
    logging.info(f'DB: hash={h}')

    try:
        entity = table.get_entity(partition_key="urls", row_key=h)
        url = entity["url"]
        logging.info(f'DB: url={url}')
        return func.HttpResponse(url, status_code=200)
    except Exception as e:
        logging.warning(f"Nie znaleziono hasha: {h}")
        logging.info(f'DB: no url')
        return func.HttpResponse("Hash not found", status_code=404)
