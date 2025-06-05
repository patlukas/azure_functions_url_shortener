import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('FunctionOne called')
    return func.HttpResponse("Hello from Function One!")
