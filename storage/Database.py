from .Model import Violation
from sqlalchemy import create_engine, event, MetaData, inspect
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from typing import List



@dataclass
class Database:
    engine: create_engine = None
    violation: Violation = Violation()
    query: str = None
    database_engine = "sqlite"
    session: sessionmaker = None
    is_connected = False
    connection = None
    metadata: MetaData = MetaData()

    def run(self):
        self.__connection_engine__()
        self.__session__()
        self.__connect__()
    
        # self.create_db()


    def __connection_engine__(self) -> create_engine:
        if self.database_engine != "sqlite":
            raise Exception("Database engine not supported")
        
        try:
            self.engine = create_engine(f"{self.database_engine}:///data/violations.db")
            self.metadata.bind = self.engine
            
            if not inspect(self.engine).has_table(self.violation.__tablename__):
                self.violation.__table__.create(bind = self.engine)
            self.metadata.create_all(self.engine)
        except Exception as e:
            print(e)
            pass
    def __session__(self):
        if self.engine is not None:
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            # self.session.configure(bind=self.engine)
            return self.session
        raise Exception("Database engine not initialized")
    
    def __connect__(self):
        if self.engine is not None:
            try:
                self.connection = self.engine.connect()
                self.is_connected = True
            except Exception as e:
                print(e)
                pass

    def __disconnect__(self):
        try:
            if self.engine is not None:
                self.connection.close()
                self.engine.dispose()
                self.is_connected = False
        except Exception as e:
            print(e)
            pass
    
    def get_violations(self) -> List[dict]:
        violations = []
        for violation in self.session.query(Violation).all():
            violations.append(violation.to_json())
        return violations if len(violations) > 0 else []
    
    def add_violation(self, violation: dict) -> bool:
        if not isinstance(violation, dict):
            raise Exception("Invalid violation")
        try:
            self.session.add(Violation(**violation))
            self.session.commit()
            return True
        except Exception as e:
            return False

    def delete_all_records(self):
        try:
            self.session.query(Violation).delete()
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    def query_violation(self, id: int) -> dict:
        violation = self.session.query(Violation).filter(Violation.id == id).first()
        print(violation.to_json())
        return violation.to_json() if violation is not None else {}
    
    def delete_violation(self, id: int) -> bool:
        try:
            self.session.query(Violation).filter(Violation.id == id).delete()
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    # def insert_db(self, violation):
    #     self.engine.execute(self.violation.__table__.insert(), violation)

    # def get_db(self):
    #     return self.engine.execute(self.violation.__table__.select())