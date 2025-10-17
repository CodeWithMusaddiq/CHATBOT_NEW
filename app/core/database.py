# app/core/database.py

from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Helper functions ---

def insert_data(table_name: str, content: dict):
    """Insert data into a given Supabase table."""
    response = supabase.table(table_name).insert(content).execute()
    return response

def fetch_data(table_name: str):
    """Fetch all data from a given Supabase table."""
    response = supabase.table(table_name).select("*").execute()
    return response.data
