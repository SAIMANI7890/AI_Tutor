"""
Verify Database Connection
Tests if the database connection is working
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import sys

def verify_database():
    """Test database connection"""
    
    # Load environment variables
    load_dotenv()
    
    db_url = os.getenv("DATABASE_URL")
    
    print("=" * 60)
    print("Database Connection Verification")
    print("=" * 60)
    
    # Check if DATABASE_URL exists
    if not db_url:
        print("❌ DATABASE_URL not found in .env file")
        print("\nPlease add it to backend/.env:")
        print("DATABASE_URL=postgresql://username:password@localhost:5432/ai_study_companion")
        return False
    
    # Parse and display connection info (masked password)
    try:
        # Extract parts
        if "postgresql://" in db_url:
            parts = db_url.replace("postgresql://", "").split("@")
            if len(parts) == 2:
                creds = parts[0].split(":")
                host_db = parts[1].split("/")
                
                username = creds[0] if len(creds) > 0 else "unknown"
                password = "*" * 8 if len(creds) > 1 else ""
                host_port = host_db[0] if len(host_db) > 0 else "unknown"
                database = host_db[1] if len(host_db) > 1 else "unknown"
                
                print(f"Username: {username}")
                print(f"Password: {password}")
                print(f"Host:Port: {host_port}")
                print(f"Database: {database}")
        else:
            print(f"Connection string: {db_url[:20]}...")
    except Exception as e:
        print(f"Connection string: {db_url[:30]}...")
    
    print("\nTesting database connection...")
    print("-" * 60)
    
    try:
        # Test 1: Create engine
        print("Test 1: Creating database engine...")
        engine = create_engine(db_url)
        print("✅ Engine created")
        
        # Test 2: Connect to database
        print("\nTest 2: Connecting to database...")
        with engine.connect() as connection:
            print("✅ Successfully connected!")
            
            # Test 3: Run a simple query
            print("\nTest 3: Running test query...")
            result = connection.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ Query successful! Result: {row[0]}")
            
            # Test 4: Check database version
            print("\nTest 4: Checking PostgreSQL version...")
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            # Extract just the version number
            version_short = version.split(",")[0] if "," in version else version[:50]
            print(f"✅ {version_short}")
            
            # Test 5: Check if database exists and is accessible
            print("\nTest 5: Checking database access...")
            result = connection.execute(text("SELECT current_database()"))
            current_db = result.fetchone()[0]
            print(f"✅ Connected to database: {current_db}")
            
            # Test 6: List tables (if any exist)
            print("\nTest 6: Checking existing tables...")
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()
            
            if tables:
                print(f"✅ Found {len(tables)} table(s):")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("⚠️  No tables found (this is normal for a new database)")
                print("   Tables will be created when you run: alembic upgrade head")
        
        print("\n" + "=" * 60)
        print("✅ DATABASE CONNECTION IS WORKING!")
        print("=" * 60)
        print("\nYour database is properly configured.")
        print("\nNext steps:")
        if not tables:
            print("1. Run database migration: python -m alembic upgrade head")
            print("2. Run PDF ingestion: python app\\rag\\ingestion\\ingest_all.py")
        else:
            print("1. Run PDF ingestion: python app\\rag\\ingestion\\ingest_all.py")
        return True
        
    except OperationalError as e:
        error_msg = str(e)
        print(f"❌ Database Connection Failed!")
        print(f"\nError: {error_msg}")
        
        # Provide helpful hints
        print("\n" + "-" * 60)
        print("Troubleshooting:")
        print("-" * 60)
        
        if "password authentication failed" in error_msg:
            print("❌ Wrong username or password")
            print("\nTo fix:")
            print("1. Check your PostgreSQL credentials")
            print("2. Update backend/.env file:")
            print("   DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/ai_study_companion")
            print("\nDefault PostgreSQL username is usually 'postgres'")
            
        elif "database" in error_msg and "does not exist" in error_msg:
            print("❌ Database does not exist")
            print("\nTo fix:")
            print("1. Open PostgreSQL (psql or pgAdmin)")
            print("2. Run: CREATE DATABASE ai_study_companion;")
            print("3. Try again")
            
        elif "could not connect" in error_msg or "Connection refused" in error_msg:
            print("❌ Cannot connect to PostgreSQL server")
            print("\nTo fix:")
            print("1. Check if PostgreSQL is running")
            print("2. On Windows: Check Services → PostgreSQL")
            print("3. Verify the host and port are correct (default: localhost:5432)")
            
        elif "role" in error_msg and "does not exist" in error_msg:
            print("❌ PostgreSQL user does not exist")
            print("\nTo fix:")
            print("1. Create the user in PostgreSQL")
            print("2. Or use an existing username in DATABASE_URL")
            
        else:
            print("❌ Unexpected database error")
            print("Check your DATABASE_URL format:")
            print("postgresql://username:password@host:port/database")
        
        print("\n" + "=" * 60)
        return False
        
    except SQLAlchemyError as e:
        print(f"❌ Database Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_database()
    sys.exit(0 if success else 1)
