from supabase import create_client
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

print("SUPABASE_URL =", SUPABASE_URL)
print("SUPABASE_KEY =", SUPABASE_KEY)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
