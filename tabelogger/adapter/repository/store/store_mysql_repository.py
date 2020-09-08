from sqlalchemy.orm.session import Session
from tabelogger.config import pymysql_session
from tabelogger.model.store import Store, Stores, StoreRepository

session: Session = pymysql_session()


class StoreMysqlRepository(StoreRepository):
    def search(self, navigation: str, min_rate: float) -> Stores:
        session: Session = pymysql_session()
        result = session.query(Store).filter(
            Store.navigation.like(f"%{navigation}%"),
            Store.rate >= min_rate,
        ).all()
        session.commit()
        return Stores(result)

    def insert(self, store: Store) -> None:
        session = pymysql_session()
        try:
            session.add(store)
            session.commit()
        except Exception as e:
            print('insertエラー')
            print(e)
            session.rollback()

    def select_all(self) -> Stores:
        session: Session = pymysql_session()
        result = session.query(Store).all()
        session.commit()
        return Stores(result)
