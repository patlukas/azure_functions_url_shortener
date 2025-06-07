import hashlib
import json
import azure.functions as func

HTML_FORM = """
<html>
  <body>
    <h2>URL Shortener</h2>
    <form method="post">
      <input type="text" name="url" placeholder="Enter URL" size="50"/>
      <input type="submit" value="Shorten"/>
    </form>
    {result}
  </body>
</html>
"""

# def main(req: func.HttpRequest, outputMessage: func.Out[str]) -> func.HttpResponse:
def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "POST":
        url = req.form.get("url")
        if not url:
            return func.HttpResponse("No URL provided", status_code=400)

        short_hash = hashlib.sha256(url.encode()).hexdigest()[:6]

        message = json.dumps({"hash": short_hash, "url": url})
        # outputMessage.set(message)

        result = f"<p>Shortened URL: <a href='/{short_hash}'>/{short_hash}</a></p>"
        return func.HttpResponse(HTML_FORM.format(result=result), mimetype="text/html")

    return func.HttpResponse(HTML_FORM.format(result=""), mimetype="text/html")
