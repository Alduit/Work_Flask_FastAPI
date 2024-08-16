import databases
import sqlalchemy


DATABASE_URL = "sqlite:///test.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("firstname", sqlalchemy.String(40), nullable=False),
    sqlalchemy.Column("lastname", sqlalchemy.String(80), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String(20), nullable=False),
)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("prod_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(300), nullable=True),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=False),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("order_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.user_id"), nullable=False),
    sqlalchemy.Column("prod_id", sqlalchemy.ForeignKey("products.prod_id"), nullable=False),
    sqlalchemy.Column("date", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("status", sqlalchemy.String(20), nullable=False),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)