import logging
import azure.functions as func
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('GUI Function triggered.')

    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return func.HttpResponse(html_content, mimetype="text/html")
    except Exception as e:
        logging.error(f"Error reading HTML file: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
