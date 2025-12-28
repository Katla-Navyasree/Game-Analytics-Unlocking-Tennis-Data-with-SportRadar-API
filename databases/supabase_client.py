from supabase import create_client
import os

SUPABASE_URL = "https://jdzwiblgyyqewdpxdurb.supabase.co"
SUPABASE_KEY = "sb_publishable_smGy4TRaVEC0EOXCIORuiA_Mq00MtcB"  # recommended for inserts

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
