from sqlalchemy import create_engine,text
import os
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
load_dotenv()

DB_URL = os.getenv("DB_URL")
print("URL: ",DB_URL)
engine = create_engine(
    DB_URL,
    pool_pre_ping=True,  # Automatically tests/re-establishes broken or stale Docker connections
    echo=False          # Change to True if you want to see raw SQL logs in your terminal
)

SessionLocal = sessionmaker(autocommit = False, autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

def verify_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("🚀 Successfully connected to the Docker Postgres database!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")


if __name__ == "__main__":
    print("URL Loaded: ", DB_URL)
    verify_connection()