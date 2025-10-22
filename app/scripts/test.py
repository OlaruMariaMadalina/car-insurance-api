from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:postgres@localhost:5432/car_insurance")
with engine.connect() as conn:
    print("claims:")
    result = conn.execute(text("SELECT id, car_id, claim_date, description, amount, created_at FROM claims"))
    for row in result:
        print(dict(row._mapping))