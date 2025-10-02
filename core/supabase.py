#core/supabase.py
# connectors/supabase_connector.py
from supabase import create_client, Client
from constants import SUPABASE_KEY,SUPABASE_URL


def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase credentials missing in environment variables")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase
