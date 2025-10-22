from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import datetime

SPREADSHEET_ID = '1kAJF7-Orahudiusk3tDo5fV9VDFYlEYTFuKyBMuUcJw'
RANGE_NAME = 'Consolidados Proyecciones!A:F'

# --- AUTENTICACIÓN ---
creds = service_account.Credentials.from_service_account_file(
    "directed-graph.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

# --- LEER DATOS ---
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get("values", [])

df = pd.DataFrame(values[1:], columns=values[0])
print("Datos leídos:\n", df.head())
