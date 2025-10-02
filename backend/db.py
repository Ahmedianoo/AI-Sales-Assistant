import os
import urllib.parse
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

import asyncpg # Make sure this is imported
from contextlib import suppress

# Load .env file
load_dotenv()

# Get env vars
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = urllib.parse.quote_plus(os.getenv("POSTGRES_PASSWORD"))  # encode special chars
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ASYNC_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This will hold the persistent, active checkpointer instance.
global_checkpointer: AsyncPostgresSaver | None = None

async def check_connection():
    print(f"DEBUG: Attempting to connect with URL: {ASYNC_DATABASE_URL}")
    try:
        # Use asyncpg's connection method directly
        conn = await asyncpg.connect(ASYNC_DATABASE_URL)
        await conn.close()
        print("DEBUG: asyncpg connection successful!")
        # Proceed with the LangGraph setup here if connection succeeds...
        # ...
    except Exception as e:
        print(f"DEBUG: DIRECT CONNECTION FAILURE: {e}")
        # Re-raise the error to stop startup
        raise 

async def init_db():
    """
    Function to be called ONCE at application startup. 
    It creates the necessary 'checkpoints' table if it doesn't exist.
    """
    print("Running one-time table setup for LangGraph...")
    
    # Use 'async with' to create a temporary connection for the setup call, 
    # ensuring the connection is properly closed afterward.
    try:
        async with AsyncPostgresSaver.from_conn_string(ASYNC_DATABASE_URL) as temp_checkpointer:
            await temp_checkpointer.setup()
        print("LangGraph checkpointer table 'checkpoints' created/verified.")
    except Exception as e:
        print(f"FATAL: Failed to initialize LangGraph tables. Error: {e}")
        # Re-raise to halt application startup if the persistence layer fails
        raise

async def initialize_global_checkpointer():
    """
    Function to be called ONCE at application startup, after init_db().
    It creates and stores the persistent checkpointer instance for the graph to use.
    """
    global global_checkpointer

    if global_checkpointer is not None:
        print("Checkpointer already initialized.")
        return

    print("Creating persistent checkpointer instance...")
    # This retrieves the actual usable AsyncPostgresSaver instance, not just the context manager object.
    context_manager = AsyncPostgresSaver.from_conn_string(ASYNC_DATABASE_URL)
    global_checkpointer = await context_manager.__aenter__() 
    
    # NOTE: You MUST ensure 'await global_checkpointer.__aexit__(None, None, None)' 
    # is called on application shutdown to close the connection pool cleanly.
    
    print("Persistent checkpointer instance is ready.")
