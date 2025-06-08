import hashlib
import json
import azure.functions as func
import logging
import os
import requests


SERVICE_REDIRECT_URL = os.getenv("SERVICE_REDIRECT_URL")
SERVICE_DB_URL = os.getenv("SERVICE_DB_URL")

HTML_FORM = """
<html>
  <head>
    <style>
      body {{
        background: linear-gradient(to right, #00ffff, #ff00ff);
        color: black;
        font-family: 'Courier New', monospace;
        text-align: center;
        margin: 50px;
      }}

      h2 {{
        font-size: 32px;
        text-shadow: 2px 2px #ff0000;
      }}

      form {{
        margin: 20px auto;
        padding: 10px;
        border: 2px dotted #000;
        width: 400px;
        background-color: #ffffcc;
      }}

      input[type="text"] {{
        width: 80%;
        padding: 5px;
        font-size: 14px;
        border: 2px inset #999;
      }}

      input[type="submit"], button {{
        background-color: #c0c0c0;
        border: 2px outset #fff;
        padding: 5px 15px;
        margin-top: 10px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        cursor: pointer;
      }}

      a {{
        color: blue;
        font-weight: bold;
        text-decoration: underline;
      }}

      p {{
        margin-top: 30px;
        font-size: 16px;
        background-color: #ffffff;
        padding: 10px;
        border: 2px dashed #0000ff;
        display: inline-block;
      }}
    </style>
  </head>
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


def main(req: func.HttpRequest, outputMessage: func.Out[str]) -> func.HttpResponse:
    logging.info("GUI")
    if req.method == "POST":
        url = req.form.get("url")
        if not url:
            return func.HttpResponse("No URL provided", status_code=400)

        h = hashlib.sha256(url.encode()).hexdigest()[:4]
        short_hash = h 
        if check_hash(short_hash):
          for i in range(100):
            short_hash = h + str(i)
            if not check_hash(short_hash):
              break          

        logging.info(f'GUI: hash={short_hash}')

        message = json.dumps({"hash": short_hash, "url": url})
        outputMessage.set(message)

        result = field_with_result(short_hash)
        return func.HttpResponse(HTML_FORM.format(result=result), mimetype="text/html")

    return func.HttpResponse(HTML_FORM.format(result=""), mimetype="text/html")

def check_hash(hash):
    service_b_url = f"{SERVICE_DB_URL}/{hash}"
    response = requests.get(service_b_url)
    return response.status_code == 200

def field_with_result(short_hash):
    return f"""
      <p>
          Shortened URL: 
          <a id="short-url" href="{SERVICE_REDIRECT_URL}/{short_hash}" target="_blank">
              {SERVICE_REDIRECT_URL}/{short_hash}
          </a>
          <br/>
          <button onclick="copyToClipboard()">Kopiuj link</button>
      </p>

      <script>
          function copyToClipboard() {{
              const url = document.getElementById('short-url').href;
              navigator.clipboard.writeText(url).then(function() {{
                  alert('Link został skopiowany do schowka!');
              }}, function(err) {{
                  alert('Błąd podczas kopiowania linku: ' + err);
              }});
          }}
      </script>
    """