import azure.functions as func
import json
import hashlib
import logging
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import os
import requests

app = func.FunctionApp()

SERVICE_BUS_CONNECTION_STRING = os.environ.get('SERVICE_BUS_CONNECTION_STRING')
QUEUE_NAME = "url-queue"

@app.route(route="", methods=["GET"])
def show_gui(req: func.HttpRequest) -> func.HttpResponse:
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Skracacz URL</title></head>
    <body>
        <h1>Skracacz Linków</h1>
        <form id="form">
            <input type="url" id="url" placeholder="https://example.com" required>
            <button type="submit">Skróć</button>
        </form>
        <div id="result"></div>
        
        <script>
        document.getElementById('form').onsubmit = async (e) => {
            e.preventDefault();
            const url = document.getElementById('url').value;
            const response = await fetch('/api/shorten', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url})
            });
            const data = await response.json();
            document.getElementById('result').innerHTML = 
                `<p>Skrócony link: <a href="/${data.hash}">${window.location.origin}/${data.hash}</a></p>`;
        };
        </script>
    </body>
    </html>
    """
    return func.HttpResponse(html, mimetype="text/html")

@app.route(route="shorten", methods=["POST"])
def shorten_url(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        url = body['url']
        hash_value = hashlib.md5(url.encode()).hexdigest()[:8]
        
        # Wyślij do Service Bus
        if SERVICE_BUS_CONNECTION_STRING:
            with ServiceBusClient.from_connection_string(SERVICE_BUS_CONNECTION_STRING) as client:
                with client.get_queue_sender(QUEUE_NAME) as sender:
                    message = ServiceBusMessage(json.dumps({"hash": hash_value, "url": url}))
                    sender.send_messages(message)
        
        return func.HttpResponse(json.dumps({"hash": hash_value, "url": url}), mimetype="application/json")
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")

@app.route(route="{hash}", methods=["GET"])
def redirect_url(req: func.HttpRequest) -> func.HttpResponse:
    hash_value = req.route_params.get('hash')
    
    try:
        # Wywołaj Function 3
        redirect_url = f"https://your-function3-app.azurewebsites.net/api/get/{hash_value}"
        response = requests.get(redirect_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return func.HttpResponse(
                f'<script>window.location.href="{data["url"]}";</script>',
                mimetype="text/html"
            )
        else:
            return func.HttpResponse("<h1>Link nie znaleziony</h1>", status_code=404, mimetype="text/html")
    except:
        return func.HttpResponse("<h1>Błąd serwera</h1>", status_code=500, mimetype="text/html")