from sqlmodel import create_engine

DATABASE_URL = "mysql+mysqldb://pi:password@localhost:3306/project_database"
engine = create_engine(DATABASE_URL)