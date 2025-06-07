import azure.functions as func
import logging
import requests
import os

SERVICE_DB_URL = os.getenv("SERVICE_DB_URL")

def main(req: func.HttpRequest) -> func.HttpResponse:
    h = req.route_params.get('hash')

    service_b_url = f"{SERVICE_DB_URL}/{h}"
    logging.info(f'R: hash={h}, url={service_b_url}')

    response = requests.get(service_b_url)

    if response.status_code != 200:
        logging.info(f"R: no response")
        return None
    logging.info(f"R: response={response.text}")
    return func.HttpResponse(status_code=302, headers={'Location': response.text})