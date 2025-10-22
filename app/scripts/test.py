from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:postgres@localhost:5432/car_insurance")
with engine.connect() as conn:
    print("insurance_policies:")
    result = conn.execute(text("SELECT id, provider, policy_number, start_date, end_date, car_id FROM insurance_policies"))
    for row in result:
        print(dict(row._mapping))