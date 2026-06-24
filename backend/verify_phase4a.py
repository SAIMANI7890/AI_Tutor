"""
Quick verification script for Phase 4A
Checks that all examination tables exist and relationships work
"""
import psycopg2
from app.core.config import settings

def verify_database():
    """Verify database tables and structure"""
    print("\n🔍 Verifying Phase 4A Database...")
    print("="*60)
    
    # Parse DATABASE_URL
    db_url = settings.DATABASE_URL
    # Format: postgresql://user:pass@host:port/dbname
    parts = db_url.replace("postgresql://", "").split("@")
    user_pass = parts[0].split(":")
    host_port_db = parts[1].split("/")
    host_port = host_port_db[0].split(":")
    
    conn = psycopg2.connect(
        host=host_port[0],
        port=host_port[1],
        database=host_port_db[1],
        user=user_pass[0],
        password=user_pass[1]
    )
    cursor = conn.cursor()
    
    # Check tables exist
    tables_to_check = ['tests', 'test_questions', 'student_test_answers']
    print("\n✅ Checking Tables:")
    for table in tables_to_check:
        cursor.execute(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{table}'
            );
        """)
        exists = cursor.fetchone()[0]
        status = "✓" if exists else "✗"
        print(f"  {status} {table}")
    
    # Check enums exist
    print("\n✅ Checking Enums:")
    cursor.execute("""
        SELECT typname FROM pg_type 
        WHERE typname IN ('questiontype', 'teststatus');
    """)
    enums = [row[0] for row in cursor.fetchall()]
    for enum_name in ['questiontype', 'teststatus']:
        status = "✓" if enum_name in enums else "✗"
        print(f"  {status} {enum_name}")
    
    # Check indexes
    print("\n✅ Checking Indexes:")
    cursor.execute("""
        SELECT tablename, indexname 
        FROM pg_indexes 
        WHERE tablename IN ('tests', 'test_questions', 'student_test_answers')
        ORDER BY tablename, indexname;
    """)
    indexes = cursor.fetchall()
    print(f"  Found {len(indexes)} indexes:")
    for table, index in indexes:
        print(f"    • {table}: {index}")
    
    # Check foreign keys
    print("\n✅ Checking Foreign Keys:")
    cursor.execute("""
        SELECT
            tc.table_name, 
            kcu.column_name, 
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name 
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY' 
        AND tc.table_name IN ('tests', 'test_questions', 'student_test_answers');
    """)
    fkeys = cursor.fetchall()
    print(f"  Found {len(fkeys)} foreign keys:")
    for table, column, ref_table, ref_column in fkeys:
        print(f"    • {table}.{column} → {ref_table}.{ref_column}")
    
    # Check constraints
    print("\n✅ Checking Constraints:")
    cursor.execute("""
        SELECT conname, contype 
        FROM pg_constraint 
        WHERE conrelid IN (
            SELECT oid FROM pg_class 
            WHERE relname IN ('tests', 'test_questions', 'student_test_answers')
        )
        AND contype IN ('c', 'u')
        ORDER BY conname;
    """)
    constraints = cursor.fetchall()
    print(f"  Found {len(constraints)} constraints:")
    for name, ctype in constraints:
        ctype_name = "CHECK" if ctype == 'c' else "UNIQUE"
        print(f"    • {name} ({ctype_name})")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ Phase 4A Database Verification Complete!\n")

if __name__ == "__main__":
    try:
        verify_database()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
