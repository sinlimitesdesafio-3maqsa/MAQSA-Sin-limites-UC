from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import datetime

# Archivo de credenciales
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Autenticación
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# ID de tu Google Sheet
SPREADSHEET_ID = '1kAJF7-Orahudiusk3tDo5fV9VDFYlEYTFuKyBMuUcJw'
RANGE_NAME = 'Consolidados Proyecciones!A:F'

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Leer datos
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

df = pd.DataFrame(values)
print(df)


