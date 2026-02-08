"""
Database setup and initialization script
Run this to create tables and populate demo data
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import text
from app.config.database import engine, Base, SessionLocal
from app.config.settings import settings
from app.services.demo_data import DemoDataGenerator
from loguru import logger


def create_tables():
    """Create all database tables"""
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        return False


def populate_demo_data():
    """Populate database with demo data"""
    logger.info("Populating demo data...")
    db = SessionLocal()
    try:
        generator = DemoDataGenerator(db)
        results = generator.generate_all()
        logger.info(f"✅ Demo data created: {results}")
        return True
    except Exception as e:
        logger.error(f"❌ Error populating demo data: {e}")
        return False
    finally:
        db.close()


def check_database_connection():
    """Check if database connection is working"""
    logger.info("Checking database connection...")
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("✅ Database connection successful!")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.error(f"DATABASE_URL: {settings.DATABASE_URL}")
        return False


def main():
    """Main setup function"""
    logger.info("=" * 60)
    logger.info("HPCL Lead Intelligence - Database Setup")
    logger.info("=" * 60)
    
    # Step 1: Check database connection
    if not check_database_connection():
        logger.error("Please check your DATABASE_URL in .env file")
        return
    
    # Step 2: Create tables
    if not create_tables():
        logger.error("Failed to create tables")
        return
    
    # Step 3: Populate demo data
    user_input = input("\nDo you want to populate demo data? (yes/no): ").lower()
    if user_input in ['yes', 'y']:
        populate_demo_data()
    
    logger.info("=" * 60)
    logger.info("✅ Setup complete!")
    logger.info("=" * 60)
    logger.info("\nNext steps:")
    logger.info("1. Run the API server: python run.py")
    logger.info("2. Access API docs: http://localhost:8000/docs")
    logger.info("3. Start frontend: cd ../frontend && npm run dev")


if __name__ == "__main__":
    main()