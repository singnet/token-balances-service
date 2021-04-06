from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.config import DATABASE

engine = create_engine(
    f"{DATABASE['DB_DRIVER']}://{DATABASE['DB_USER']}:"
    f"{DATABASE['DB_PASSWORD']}"
    f"@{DATABASE['DB_HOST']}:"
    f"{DATABASE['DB_PORT']}/{DATABASE['DB_NAME']}",
    echo=True,
)

Session = sessionmaker(bind=engine)
default_session = Session()


class BaseRepository:
    def __init__(self):
        self.session = default_session

    def add_item(self, item):
        try:
            self.session.add(item)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def add_all_items(self, items):
        try:
            self.session.bulk_save_objects(items)
            self.session.commit()
        except Exception as e:
            self.session.commit()
            raise e
