# services/image_service.py
from supabase import Client

class ImageService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

# create table public.disease_detections (
#   id uuid not null default extensions.uuid_generate_v4 (),
#   user_id text not null,
#   crop_id uuid null,
#   image_url text not null,
#   detected_disease character varying(255) null,
#   confidence_score numeric(5, 2) null,
#   treatment_applied text null,
#   status character varying(20) null default 'detected'::character varying,
#   detected_at timestamp with time zone null default CURRENT_TIMESTAMP,
    def save_res_to_database(self, data: dict):
        return self.supabase.table("disease_detections").insert(data).execute()

    def get_top_3_responses(self, user_id: str):
        return (
            self.supabase.table("disease_detections")
            .select("*")
            .eq("user_id", user_id)
            .order("detected_at", desc=True)  # sabse latest entries
            .limit(3)
            .execute()
        )

