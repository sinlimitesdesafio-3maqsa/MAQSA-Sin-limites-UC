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

# --- Leer datos desde Sheets ---
print("📥 Leyendo datos desde Google Sheets...")
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])
if not values:
    raise ValueError("⚠️ No se encontraron datos en el rango especificado.")

# --- Convertir a DataFrame ---
header, *rows = values
df = pd.DataFrame(rows, columns=header)

# --- Verificar columnas ---
if 'Mes' not in df.columns:
    raise ValueError("❌ No se encontró la columna 'Mes' en los datos.")

# --- Convertir la columna de fechas ---
print("🔍 Detectando formato de fechas...")
df['Mes'] = pd.to_datetime(df['Mes'], errors='coerce', dayfirst=True)

# --- Filtrar desde el mes actual ---
hoy = pd.Timestamp(datetime.date.today().replace(day=1))
df_filtrado = df[df['Mes'] >= hoy].copy()

print(f"📅 Filtradas {len(df_filtrado)} filas con Mes >= {hoy.date()}")

# --- Guardar resultado en Excel ---
df_filtrado.to_excel(OUTPUT_FILE, index=False)
print(f"✅ Archivo generado: {OUTPUT_FILE}")
print("📘 Última fila:")
print(df_filtrado.tail(1))
