# app/core/database.py
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def test_connection():
    try:
        print("🔍 Testing Supabase connection...")
        # Attempt to fetch data from Sidra's 'documents' table
        response = supabase.table("documents").select("*").limit(2).execute()
        print("✅ Connection successful! Here’s sample data:")
        print(response.data)
    except Exception as e:
        print("❌ Failed to connect to Supabase:", e)

if __name__ == "__main__":
    test_connection()
