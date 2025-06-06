import azure.functions as func

app = func.FunctionApp()

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
