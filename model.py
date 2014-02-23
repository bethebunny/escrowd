import uuid

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext import declarative as orm_dcl


db = sqlalchemy.create_engine('sqlite:///escrow.db')
_session = orm.sessionmaker(bind=db)


Base = orm_dcl.declarative_base()

class Model(object):
  def save(self):
    session = _session()
    session.add(self)
    session.commit()

  @classmethod
  def get(cls, **kwargs):
    return cls.list(**kwargs).first()

  @classmethod
  def list(cls, **kwargs):
    return _session().query(cls).filter_by(**kwargs)


class Transaction(Model, Base):
  __tablename__ = 'Transaction'

  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  receiver = sqlalchemy.Column(sqlalchemy.String)
  value = sqlalchemy.Column(sqlalchemy.String, nullable=False)
  in_escrow = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
  completed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
  read_uuid = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
  manage_uuid = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
  description = sqlalchemy.Column(sqlalchemy.String)

  def __init__(self, value, receiver=None, description=None):
    super(Transaction, self).__init__(value=value,
        read_uuid=uuid.uuid4().hex,
        manage_uuid=uuid.uuid4().hex,
        description=description,
        receiver=receiver)


Base.metadata.create_all(db)
