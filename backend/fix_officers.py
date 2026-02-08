import sys
sys.path.insert(0, '.')

from app.config.database import SessionLocal
from app.models.models import Officer

db = SessionLocal()

# DELETE all old officers
db.query(Officer).delete()
db.commit()
print("🗑️ Deleted all old officers")

# CREATE new officer with correct email
new_officer = Officer(
    name="Sales Manager",
    email="b2b.lead.intelligence@gmail.com",
    phone="+91-9876543210",
    territory_state="Maharashtra",
    territory_cities=["Mumbai", "Pune", "Nagpur"],
    dsro_office="Mumbai DSRO",
    employee_id="EMP001",
    notification_enabled=True,
    is_active=True
)

db.add(new_officer)
db.commit()
print(f"✅ Created new officer: {new_officer.name} - {new_officer.email}")

db.close()