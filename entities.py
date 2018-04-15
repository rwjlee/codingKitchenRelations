from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Integer, Float, Boolean, ForeignKey, func

from base import Base, inverse_relationship, create_tables

#
class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)

    api = Column(String, unique=True)
    name = Column(String)

    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', backref = inverse_relationship('departments'))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def parse_json(self, json_data):
        self.api = json_data['api']
        self.name = json_data['name']

#
class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)

    api = Column(String, unique=True)
    name = Column(String)
    net_income = Column(Integer)
    founded_on = Column(Integer)
    total_assets = Column(Integer)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def parse_json(self, json_data):
        self.api = json_data['api']
        self.name = json_data['name']
        self.net_income = json_data['net_income']
        self.founded_on= json_data['founded_on']
        self.total_assets = json_data['total_assets']

class Listing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key = True)
    cid_to_eid = Column(String, unique = True)
    
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', backref = inverse_relationship('listed_on'))

    exchange_id = Column(Integer, ForeignKey('exchanges.id'))
    exchange = relationship('Exchange', backref = inverse_relationship('has_company'))

    active = Column(Integer)

    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate=func.now())

#
class Exchange(Base):
    __tablename__ = 'exchanges'
    id = Column(Integer, primary_key=True)

    api = Column(String, unique=True)
    name = Column(String)
    address = Column(String)

    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship('City', backref = inverse_relationship('exchanges'))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def parse_json(self, json_data):
        self.api = json_data['api']
        self.name = json_data['name']
        self.address = json_data['address']

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key = True)

    # pid_to_did = Column(String, unique = True)
    
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship('Department', backref = inverse_relationship('has_employee'))

    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('Person', backref = inverse_relationship('works_at'))

    active = Column(Integer)

    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate=func.now())


class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)

    api = Column(String, unique=True)
    last = Column(String)
    first = Column(String)
    gender = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def parse_json(self, json_data):
        self.api = json_data['api']
        self.last = json_data['last']
        self.first = json_data['first']
        self.gender = json_data['gender']

class Club(Base):
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True)

    api = Column(String, unique=True)
    name = Column(String)
    # leauge_id = Column(Integer)
    # city_id = Column(Integer)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def parse_json(self, json_data):
        self.api = json_data['api']
        self.name = json_data['name']
        # self.leauge_id = json_data['league']
        # self.city_id = json_data['city']


 

class League(Base):
    __tablename__ = 'leagues'
    id = Column(Integer, primary_key=True)

    api = Column(String, unique=True)
    name = Column(String)
    sport = Column(String)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def parse_json(self, json_data):
        self.api = json_data['api']
        self.name = json_data['name']
        self.sport = json_data['sport']

#
class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)

    api = Column(String, unique=True)
    name = Column(String)
    population = Column(Integer)
    # state = Column(String)
    is_capital = Column(Boolean)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def parse_json(self, json_data):
        self.api = json_data['api']
        self.name = json_data['name']
        self.population = json_data['population']
        # self.state = json_data['state']
        self.is_capital = json_data['is_capital']


class State(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True)

    api = Column(String, unique=True)
    name = Column(String)
    gdp = Column(Integer)
    abbreviation = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def parse_json(self, json_data):
        self.api = json_data['api']
        self.name = json_data['name']
        self.gdp = json_data['gdp']
        self.abbreviation = json_data['abbreviation']