import azure.functions as func
import string, random, json

def generate_hash(n=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def main(req: func.HttpRequest, outputMessage: func.Out[str]) -> func.HttpResponse:
    if req.method == 'GET':
        return func.HttpResponse('''<form method="post"><input name="url"/><button>Skróć</button></form>''', mimetype="text/html")
    url = (req.form.get('url') if req.method=='POST' else None) or req.params.get('url')
    if not url:
        return func.HttpResponse("Brak URL", status_code=400)
    h = generate_hash()
    outputMessage.set(json.dumps({"hash":h, "url":url}))
    short = f"{req.url.rstrip('/')}/{h}"
    return func.HttpResponse(f"Twój link to <a href='{short}'>{short}</a>", mimetype="text/html")
