from sqlalchemy.orm import Session
from app.models.zone import Zone
from app.models.hospital import Hospital
from app.models.blood_bank import BloodBank
from app.models.inventory import InventoryItem
from app.models.donor import Donor


def seed_database(db: Session) -> None:
    """Seeds initial zones, hospitals, blood banks, and donors ONLY if the database is empty."""
    # If data already exists, do not overwrite or duplicate
    if db.query(Zone).first() is not None:
        return

    # 1. Seed Zones (let PostgreSQL sequence assign IDs naturally)
    z1 = Zone(name="Downtown Central", code="ZONE-1")
    z2 = Zone(name="North Medical District", code="ZONE-2")
    z3 = Zone(name="South Suburbs", code="ZONE-3")
    z4 = Zone(name="East Industrial Zone", code="ZONE-4")
    z5 = Zone(name="West Tech Park", code="ZONE-5")
    db.add_all([z1, z2, z3, z4, z5])
    db.flush()

    # 2. Seed Hospitals linked to created zones
    h1 = Hospital(name="St. Jude General Hospital", zone_id=z1.id)
    h2 = Hospital(name="North Star Emergency Center", zone_id=z2.id)
    h3 = Hospital(name="Mercy Children's Hospital", zone_id=z3.id)
    db.add_all([h1, h2, h3])
    db.flush()

    # 3. Seed Blood Banks linked to created zones
    b1 = BloodBank(name="Metropolitan Central Blood Bank", zone_id=z1.id)
    b2 = BloodBank(name="Northern District Red Cross", zone_id=z2.id)
    db.add_all([b1, b2])
    db.flush()

    # 4. Seed Inventory Items
    inventory = [
        InventoryItem(blood_bank_id=b1.id, blood_type="A+", units_available=25),
        InventoryItem(blood_bank_id=b1.id, blood_type="O+", units_available=18),
        InventoryItem(blood_bank_id=b1.id, blood_type="O-", units_available=2),  # Shortage level
        InventoryItem(blood_bank_id=b1.id, blood_type="B+", units_available=10),
        InventoryItem(blood_bank_id=b2.id, blood_type="A-", units_available=6),
        InventoryItem(blood_bank_id=b2.id, blood_type="AB+", units_available=12),
        InventoryItem(blood_bank_id=b2.id, blood_type="AB-", units_available=1),  # Shortage level
    ]
    db.add_all(inventory)

    # 5. Seed Initial Donors
    donors = [
        Donor(
            full_name="Sarah Connor",
            email="sarah.connor@example.com",
            blood_type="O-",
            city_zone_id=z1.id,
            is_available=True,
        ),
        Donor(
            full_name="John Miller",
            email="john.miller@example.com",
            blood_type="A+",
            city_zone_id=z1.id,
            is_available=True,
        ),
        Donor(
            full_name="Elena Rostova",
            email="elena.r@example.com",
            blood_type="O-",
            city_zone_id=z1.id,
            is_available=True,
        ),
        Donor(
            full_name="Marcus Vance",
            email="marcus.v@example.com",
            blood_type="B+",
            city_zone_id=z2.id,
            is_available=True,
        ),
        Donor(
            full_name="Chloe Bennett",
            email="chloe.b@example.com",
            blood_type="AB-",
            city_zone_id=z2.id,
            is_available=False,
        ),
    ]
    db.add_all(donors)
    db.commit()
