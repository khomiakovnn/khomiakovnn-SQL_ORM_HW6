import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Sale, Shop, Stock, create_tables


def insert_data(file, session):
    """Insert test data from json file"""

    with open(file) as file:
        data = json.load(file)

    for line in data:
        if line['model'] == "publisher":
            row = Publisher(
                id=line['pk'],
                name=line['fields']['name']
            )
        elif line['model'] == "book":
            row = Book(
                id=line['pk'],
                title=line['fields']['title'],
                id_publisher=line['fields']['id_publisher']
            )
        elif line['model'] == "shop":
            row = Shop(
                id=line['pk'],
                name=line['fields']['name']
            )
        elif line['model'] == "stock":
            row = Stock(
                id=line['pk'],
                id_book=line['fields']['id_book'],
                id_shop=line['fields']['id_shop'],
                count=line['fields']['count']
            )
        else:
            row = Sale(
                id=line['pk'],
                price=line['fields']['price'],
                date_sale=line['fields']['date_sale'],
                id_stock=line['fields']['id_stock'],
                count=line['fields']['count']
            )
        session.add(row)
        session.commit()


def get_user_data():
    """Collect user data for database connect DSN"""

    with open('user_db.txt') as file:
        userdata = file.readlines()
    dns_list = []
    for data in userdata:
        dns_list.append(data[(data.find('=') + 2):-1])
    result = (
        f"postgresql://{dns_list[3]}:{dns_list[4]}@"
        f"{dns_list[1]}:{dns_list[2]}/{dns_list[0]}"
    )
    return result


def query_db(session, id):
    """Query from publisher table"""

    publisher_query = session.query(Publisher).filter(Publisher.id == id)
    for s in publisher_query.all():
        print(s.id, s.name)


def main():
    """Main function"""

    test_data_file = 'tests_data.json'
    DSN = get_user_data()
    engine = sq.create_engine(DSN)
    create_tables(engine)  # Задание 2 (подключение и импорт)
    print('Таблицы созданы.')

    Session = sessionmaker(bind=engine)
    session = Session()

    insert_data(test_data_file, session)  # Задание 3
    print(f"Таблицы заполнены тестовыми данными '{test_data_file}'")

    # publish = input('Введите данны издателя: ') - sublime не разрешает input, ввод задан жестко в следующей строке
    publish = 1
    query_db(session, publish)  # Задание 2 (издатель)

    session.close()


if __name__ == '__main__':
    main()
