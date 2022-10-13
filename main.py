import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), nullable=False)


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=150), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey(
        "publisher.id"), nullable=False)


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=150), nullable=False)


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_user_data():
    """Collect user data for database connect DSN"""

    with open('user_db.txt') as file:
        userdata = file.readlines()
    dns_list = []
    for data in userdata:
        dns_list.append(data[(data.find('=') + 2):-1])
    DSN = f"postgresql://{dns_list[3]}:{dns_list[4]}@{dns_list[1]}:{dns_list[2]}/{dns_list[0]}"
    return DSN


def main():
    """Main function"""

    engine = sq.create_engine(get_user_data())
    create_tables(engine)


if __name__ == '__main__':
    main()
