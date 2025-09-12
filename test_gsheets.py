import gspread
from google.oauth2.service_account import Credentials

# Define the scope for Google Sheets + Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from the JSON key file and apply scopes
creds = Credentials.from_service_account_file("quiz_creds.json", scopes=SCOPES)

# Authorise the gspread client
client = gspread.authorize(creds)

# Open spreadsheet by name
sheet = client.open("fandom-challenge-v2-data").sheet1

# Write something to cell A1
sheet.update("A1", [["Hello from Python!"]])

# Read back A1 to confirm
value = sheet.acell("A1").value
print("Cell A1 says:", value)
