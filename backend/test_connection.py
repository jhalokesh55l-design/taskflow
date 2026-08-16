from database import engine

try:
    with engine.connect() as connection:
        print("Supabase database connected successfully!")
except Exception as error:
    print("Database connection failed:")
    print(error)