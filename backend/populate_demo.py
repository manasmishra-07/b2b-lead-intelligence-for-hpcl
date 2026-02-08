import sys
from pathlib import Path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.config.database import SessionLocal
from app.services.demo_data import DemoDataGenerator

db = SessionLocal()
try:
    generator = DemoDataGenerator(db)
    results = generator.generate_all()
    print(f"✅ Demo data created: {results}")
finally:
    db.close()
    