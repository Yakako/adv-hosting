"""
Database inspection tool - Check your PostgreSQL database
"""
from database.connection import SessionLocal, engine
from database.models import Prediction
from sqlalchemy import inspect, text
import pandas as pd

def show_database_info():
    """Display database connection and structure information"""
    print("=" * 70)
    print("🗄️  DATABASE INFORMATION")
    print("=" * 70)
    
    # Connection info
    print("\n📡 Connection Details:")
    print(f"   Database URL: postgresql://car_user:***@localhost:5433/car_classification")
    print(f"   Docker Container: car-classification-db")
    print(f"   Port Mapping: 5433 (host) → 5432 (container)")
    
    # Table structure
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\n📊 Tables in database: {len(tables)}")
    for table in tables:
        print(f"\n   Table: {table}")
        columns = inspector.get_columns(table)
        print("   Columns:")
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            print(f"      - {col['name']}: {col['type']} ({nullable})")

def show_all_predictions():
    """Display all predictions from database"""
    print("\n" + "=" * 70)
    print("📋 PREDICTIONS DATA")
    print("=" * 70)
    
    db = SessionLocal()
    try:
        predictions = db.query(Prediction).all()
        
        if not predictions:
            print("\n   ⚠️  No predictions found in database")
            return
        
        print(f"\n   Total predictions: {len(predictions)}")
        print("\n   Recent predictions:")
        print("   " + "-" * 66)
        print(f"   {'ID':<5} {'Class':<15} {'Confidence':<12} {'Created':<20}")
        print("   " + "-" * 66)
        
        for pred in predictions[-10:]:  # Show last 10
            print(f"   {pred.id:<5} {pred.predicted_class:<15} {pred.confidence:<12.2%} {pred.created_at.strftime('%Y-%m-%d %H:%M:%S'):<20}")
        
        # Class distribution
        print("\n   📊 Class Distribution:")
        class_counts = {}
        for pred in predictions:
            class_counts[pred.predicted_class] = class_counts.get(pred.predicted_class, 0) + 1
        
        for cls, count in sorted(class_counts.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * count
            print(f"   {cls:<15} {count:>3} {bar}")
        
        # Statistics
        avg_confidence = sum(p.confidence for p in predictions) / len(predictions)
        print(f"\n   📈 Statistics:")
        print(f"   Average Confidence: {avg_confidence:.2%}")
        print(f"   Highest Confidence: {max(p.confidence for p in predictions):.2%}")
        print(f"   Lowest Confidence: {min(p.confidence for p in predictions):.2%}")
        
    finally:
        db.close()

def show_raw_sql_query():
    """Execute raw SQL query"""
    print("\n" + "=" * 70)
    print("🔍 RAW SQL QUERY")
    print("=" * 70)
    
    db = SessionLocal()
    try:
        query = text("""
            SELECT 
                id,
                predicted_class,
                confidence,
                created_at,
                image_path
            FROM predictions
            ORDER BY created_at DESC
            LIMIT 5
        """)
        
        result = db.execute(query)
        rows = result.fetchall()
        
        if rows:
            print("\n   Last 5 predictions (raw SQL):")
            for row in rows:
                print(f"   {dict(row)}")
        else:
            print("\n   No data found")
            
    finally:
        db.close()

def check_docker_container():
    """Check Docker container status"""
    import subprocess
    
    print("\n" + "=" * 70)
    print("🐳 DOCKER CONTAINER STATUS")
    print("=" * 70)
    
    try:
        # Check if container is running
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=car-classification-db', '--format', '{{.Names}}\t{{.Status}}\t{{.Ports}}'],
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            print("\n   ✅ Container is running:")
            print(f"   {result.stdout.strip()}")
        else:
            print("\n   ⚠️  Container is not running")
            print("   Start it with: docker-compose up -d")
            
    except Exception as e:
        print(f"\n   ❌ Error checking Docker: {e}")

if __name__ == "__main__":
    try:
        check_docker_container()
        show_database_info()
        show_all_predictions()
        show_raw_sql_query()
        
        print("\n" + "=" * 70)
        print("✅ Database inspection complete!")
        print("=" * 70)
        
        print("\n💡 Tips:")
        print("   • View database in Docker: docker exec -it car-classification-db psql -U car_user -d car_classification")
        print("   • Stop database: docker-compose down")
        print("   • Restart database: docker-compose restart")
        print("   • View logs: docker logs car-classification-db")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
