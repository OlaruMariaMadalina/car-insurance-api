import asyncio
from datetime import date
from app.db.engine import SessionLocal
from app.models.owner import Owner
from app.models.car import Car
from app.models.policy import InsurancePolicy

async def seed():
    async with SessionLocal() as session:
        # --- 10 owneri ---
        owners = [
            Owner(full_name="John Doe", email="john.doe@example.com"),
            Owner(full_name="Jane Smith", email="jane.smith@example.com"),
            Owner(full_name="Alice Johnson", email="alice.johnson@example.com"),
            Owner(full_name="Bob Williams", email="bob.williams@example.com"),
            Owner(full_name="Charlie Brown", email="charlie.brown@example.com"),
            Owner(full_name="Diana Miller", email="diana.miller@example.com"),
            Owner(full_name="Ethan Davis", email="ethan.davis@example.com"),
            Owner(full_name="Fiona Clark", email="fiona.clark@example.com"),
            Owner(full_name="George Hall", email="george.hall@example.com"),
            Owner(full_name="Hannah Lewis", email="hannah.lewis@example.com"),
        ]
        session.add_all(owners)
        await session.flush()  # obținem id-urile

        # --- 10 mașini ---
        cars = [
            Car(identification_number="ID0000000001", make="Toyota", model="Corolla", year=2020, owner_id=owners[0].id),
            Car(identification_number="ID0000000002", make="Honda", model="Civic",   year=2021, owner_id=owners[1].id),
            Car(identification_number="ID0000000003", make="Ford",  model="Focus",   year=2018, owner_id=owners[2].id),
            Car(identification_number="ID0000000004", make="BMW",   model="320i",    year=2022, owner_id=owners[3].id),
            Car(identification_number="ID0000000005", make="Audi",  model="A4",      year=2019, owner_id=owners[4].id),
            Car(identification_number="ID0000000006", make="VW",    model="Golf",    year=2020, owner_id=owners[5].id),
            Car(identification_number="ID0000000007", make="Nissan",model="Qashqai", year=2021, owner_id=owners[6].id),
            Car(identification_number="ID0000000008", make="Hyundai",model="Tucson", year=2019, owner_id=owners[7].id),
            Car(identification_number="ID0000000009", make="Mercedes",model="C200",  year=2022, owner_id=owners[8].id),
            Car(identification_number="ID0000000010", make="Kia",   model="Sportage",year=2021, owner_id=owners[9].id),
        ]
        session.add_all(cars)
        await session.flush()

        # --- 10 polițe de test ---
        policies = []
        for i, car in enumerate(cars):
            policies.append(
                InsurancePolicy(
                    car_id=car.id,
                    provider=f"Provider-{i+1}",
                    policy_number=f"P-{i+1:03d}",
                    start_date=date(2024, 1, 1),
                    end_date=date(2025, 1, 1),
                    logged_expiry_at=None
                )
            )
        session.add_all(policies)

        await session.commit()
        print("✅ Database seeded successfully with 10 owners, 10 cars, and 10 policies!")

if __name__ == "__main__":
    asyncio.run(seed())