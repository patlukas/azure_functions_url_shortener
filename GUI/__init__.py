import hashlib
import json
import azure.functions as func
import logging
import os
import requests


SERVICE_REDIRECT_URL = os.getenv("SERVICE_REDIRECT_URL")
SERVICE_DB_URL = os.getenv("SERVICE_DB_URL")


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
        return func.HttpResponse(get_html(result), mimetype="text/html")

    return func.HttpResponse(get_html(""), mimetype="text/html")


def check_hash(hash):
    service_b_url = f"{SERVICE_DB_URL}/{hash}"
    response = requests.get(service_b_url)
    return response.status_code == 200


def field_with_result(short_hash):
    return f"""
      <div class="result" id="result-section" style="display: block;">
            <p>🎉 TWÓJ SKRÓCONY LINK JEST GOTOWY! 🎉</p>
            <p>
                Skrócony URL: 
                <a id="short-url" href="{SERVICE_REDIRECT_URL}/{short_hash}" target="_blank">
                    {SERVICE_REDIRECT_URL}/{short_hash}
                </a>
                <button class="copy-button" onclick="copyToClipboard()">KOPIUJ LINK!</button>
            </p>
        </div>
    """


def get_html(result):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>🌟 SUPER URL SHORTENER 🌟</title>
        <style>
            body {
                background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00, #ff00ff);
                background-size: 400% 400%;
                animation: rainbow-bg 3s ease infinite;
                font-family: 'Comic Sans MS', cursive, sans-serif;
                margin: 0;
                padding: 20px;
                color: #000080;
                overflow-x: auto;
            }

            @keyframes rainbow-bg {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            @keyframes blink {
                0%, 50% { opacity: 1; }
                51%, 100% { opacity: 0; }
            }

            @keyframes marquee {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
            }

            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }

            .container {
                max-width: 800px;
                margin: 0 auto;
                background: #ffffff;
                border: 5px solid #ff0000;
                padding: 20px;
                box-shadow: 10px 10px 0px #000000;
            }

            .header {
                text-align: center;
                margin-bottom: 30px;
            }

            h1 {
                font-size: 36px;
                color: #ff0000;
                text-shadow: 3px 3px 0px #000000;
                animation: shake 2s infinite;
                margin: 0;
            }

            .subtitle {
                font-size: 18px;
                color: #0000ff;
                animation: blink 1s infinite;
                margin: 10px 0;
            }

            .marquee {
                background: #ffff00;
                border: 2px solid #ff0000;
                padding: 10px;
                margin: 20px 0;
                overflow: hidden;
                white-space: nowrap;
            }

            .marquee-text {
                display: inline-block;
                animation: marquee 10s linear infinite;
                color: #ff0000;
                font-weight: bold;
                font-size: 16px;
            }

            h2 {
                color: #800080;
                font-size: 24px;
                text-align: center;
                text-decoration: underline;
                margin: 30px 0 20px 0;
            }

            form {
                text-align: center;
                background: #ffccff;
                border: 3px dashed #ff00ff;
                padding: 20px;
                margin: 20px 0;
            }

            input[type="text"] {
                font-family: 'Comic Sans MS', cursive;
                font-size: 16px;
                padding: 10px;
                border: 3px solid #0000ff;
                background: #ffff99;
                color: #000080;
                width: 300px;
                box-shadow: 5px 5px 0px #000000;
            }

            input[type="submit"] {
                font-family: 'Comic Sans MS', cursive;
                font-size: 18px;
                font-weight: bold;
                padding: 10px 20px;
                background: linear-gradient(45deg, #ff0000, #ffff00);
                color: #ffffff;
                border: 3px solid #000000;
                cursor: pointer;
                margin-left: 10px;
                box-shadow: 5px 5px 0px #000000;
                text-shadow: 2px 2px 0px #000000;
            }

            input[type="submit"]:hover {
                animation: shake 0.5s infinite;
                background: linear-gradient(45deg, #ffff00, #ff0000);
            }

            .result {
                background: #ccffcc;
                border: 3px solid #00ff00;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
                box-shadow: 5px 5px 0px #000000;
            }

            .result p {
                font-size: 18px;
                color: #006600;
                font-weight: bold;
                margin: 10px 0;
            }

            .result a {
                color: #0000ff;
                text-decoration: none;
                font-size: 16px;
                background: #ffff00;
                padding: 5px;
                border: 2px solid #ff0000;
            }

            .result a:hover {
                animation: blink 0.5s infinite;
                background: #ff00ff;
                color: #ffffff;
            }

            .copy-button {
                font-family: 'Comic Sans MS', cursive;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 15px;
                background: #ff00ff;
                color: #ffffff;
                border: 3px solid #000000;
                cursor: pointer;
                margin-left: 10px;
                box-shadow: 3px 3px 0px #000000;
                text-shadow: 1px 1px 0px #000000;
            }

            .copy-button:hover {
                background: #00ffff;
                color: #000000;
            }

            .footer {
                text-align: center;
                margin-top: 30px;
                font-size: 14px;
                color: #666666;
            }

            .sparkle {
                color: #ff00ff;
                font-size: 20px;
                animation: blink 1.5s infinite;
            }

            .visitor-counter {
                background: #000000;
                color: #00ff00;
                padding: 10px;
                margin: 20px 0;
                text-align: center;
                font-family: 'Courier New', monospace;
                border: 2px solid #00ff00;
            }

            .under-construction {
                background: #ffff00;
                border: 3px solid #ff0000;
                padding: 10px;
                margin: 20px 0;
                text-align: center;
                font-weight: bold;
                color: #ff0000;
            }

            .web-ring {
                background: #cccccc;
                border: 2px solid #000000;
                padding: 15px;
                margin: 20px 0;
                text-align: center;
            }

            .web-ring a {
                color: #0000ff;
                text-decoration: underline;
                margin: 0 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌟 SUPER URL SHORTENER 🌟</h1>
                <div class="subtitle">*** NAJLEPSZY SKRACACZ LINKÓW W INTERNECIE! ***</div>
            </div>

            <div class="marquee">
                <div class="marquee-text">
                    ★ WITAMY NA NASZEJ STRONIE! ★ SKRACAJ LINKI ZA DARMO! ★ NAJSZYBSZY SERWIS! ★ 100% BEZPŁATNE! ★
                </div>
            </div>

            <div class="under-construction">
                🚧 STRONA W BUDOWIE! 🚧 NOWE FUNKCJE WKRÓTCE! 🚧
            </div>

            <h2><span class="sparkle">★</span> URL SHORTENER <span class="sparkle">★</span></h2>
            
            <form method="post">
                <input type="text" name="url" placeholder="Wklej tutaj swój długi link!" size="50"/>
                <input type="submit" value="SKRÓĆ LINK!"/>
            </form>

            """ + result + """

            <div class="footer">
                <p>© 2024 Super URL Shortener - Wykonane w Notepad++ <span class="sparkle">★</span></p>
                <p>Najlepiej wyświetlane w Internet Explorer 6.0</p>
            </div>
        </div>

        <script>

            function copyToClipboard() {
                const url = document.getElementById('short-url').href;
                navigator.clipboard.writeText(url).then(function() {
                    alert('Link został skopiowany do schowka! 🎉');
                }, function(err) {
                    alert('Błąd podczas kopiowania linku: ' + err);
                });
            }

            setInterval(function() {
                const sparkles = document.querySelectorAll('.sparkle');
                sparkles.forEach(sparkle => {
                    if (Math.random() > 0.7) {
                        sparkle.style.color = '#' + Math.floor(Math.random()*16777215).toString(16);
                    }
                });
            }, 1000);

            let visitorCount = 1337;
            setInterval(function() {
                visitorCount++;
                document.querySelector('.visitor-counter span:nth-child(2)').textContent = 
                    visitorCount.toString().padStart(6, '0');
            }, 5000);
        </script>
    </body>
    </html>

    """
