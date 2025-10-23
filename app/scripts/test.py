from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:postgres@localhost:5432/car_insurance")
with engine.connect() as conn:
    print("policies:")
    result = conn.execute(text(
        "SELECT id, car_id, provider, policy_number, start_date, end_date, logged_expiry_at FROM insurance_policies"
    ))
    for row in result:
        print(dict(row._mapping))