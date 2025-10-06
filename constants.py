import os
from dotenv import load_dotenv
load_dotenv()

#Supabasee keys
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

#Clerk keys
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
JWT_KEY = os.getenv("JWT_KEY")


#GPT AND GROK CONFIGS
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
