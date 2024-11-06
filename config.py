import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        database="velodb",
        user="postgres1",
        password="bE4qNxdGPNzKWhgS4PXXc2PV33D7T7pv",
        host="dpg-cskt5223esus73ft0f4g-a.oregon-postgres.render.com",
        port="5432"
    )
