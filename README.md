# 🔗 Azure URL Shortener (Python, Azure Functions)

Projekt to system skracania linków oparty na Azure Functions i architekturze mikroserwisowej. Składa się z czterech mikroserwisów napisanych w Pythonie, które współpracują przy użyciu Azure Service Bus i Azure Table Storage.

## 🧩 Mikroserwisy

### 1. `GUI`
Interfejs użytkownika, który umożliwia wprowadzenie oryginalnego URL.

- Komunikuje się z:
  - `BD` – zapytanie, czy hash istnieje w bazie.
  - `BD_insert` – wysyła hash i URL do kolejki Service Bus (asynchronicznie).

---

### 2. `BD` (Baza Danych - Odczyt)
Funkcja odpowiedzialna za sprawdzanie, czy dany hash istnieje w bazie (Azure Table Storage).

- Używana przez:
  - `GUI` – sprawdzenie przed skróceniem linku.
  - `redirect` – sprawdzenie jaki url odpowiada hashowi.

---

### 3. `BD_insert` (Baza Danych - Zapis)
Asynchroniczny odbiorca komunikatów z Service Bus. Odpowiedzialny za zapisanie powiązania `hash -> url` w Azure Table Storage.

- Nasłuchuje kolejki Service Bus.
- Odbiera dane z `GUI`.

---

### 4. `redirect`
Funkcja obsługująca wejście na skrócony link (np. `https://twojadomena.com/r/abcd`).

- Sprawdza hash (`abcd`) w `BD`.
- Jeśli istnieje – przekierowuje na pełny URL.
- Jeśli nie – przekierowuje na stronę główną. (np. `https://twojadomena.com/GUI`)

---

## 🔐 Algorytm skracania


- Wykorzystywane są **ostatnie 4 znaki** z hasha SHA-256 wygenerowanego z pełnego linku.


## ⚙️ Wymagane zasoby Azure

Projekt wykorzystuje:

- **Azure Table Storage** – do przechowywania map `hash -> url`.
- **Azure Service Bus** – do asynchronicznej komunikacji między `GUI` a `BD_insert`.

Wymagane zmienne środowiskowe:

```bash
AzureWebJobsStorage=<connection-string-do-storage>
ServiceBusConnection=<connection-string-do-service-bus>
````

---

## 📁 Struktura katalogów (przykład)

```
/project-root/
│
├── GUI/                       
│   ├── __init__.py            
│   └── function.json          
│
├── BD/                        
│   ├── __init__.py            
│   └── function.json
│
├── BD_insert/                 
│   ├── __init__.py            
│   └── function.json
│
├── redirect/                  
│   ├── __init__.py            
│   └── function.json
│
├── host.json                  
├── local.settings.json       
└── requirements.txt           

```

---

![](https://github.ct8.pl/readme/patlukas/azure_functions_url_shortener)

## 🚀 Uruchamianie lokalne

1. Skonfiguruj `local.settings.json`:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "<TwójConnectionString>",
    "ServiceBusConnection": "<TwójConnectionString>",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "SERVICE_DB_URL": "http://localhost:7071/api/resolve",
    "SERVICE_GUI_URL": "http://localhost:7071/GUI",
    "SERVICE_REDIRECT_URL": "http://localhost:7071/r"
  }
}
```

2. Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

3. Uruchom funkcje lokalnie:

```bash
func start
```
