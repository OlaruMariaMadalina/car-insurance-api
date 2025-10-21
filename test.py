from sqlalchemy import create_engine, inspect

engine = create_engine("postgresql://postgres:postgres@localhost:5432/car_insurance")
inspector = inspect(engine)
print(inspector.get_table_names())