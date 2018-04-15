from entities import Company, Club, Person, League, City, Department, State, Exchange, Listing, Job
import requests, json
from pprint import pprint
from base import DbManager

CK_API = 'http://data.coding.kitchen/api/{}/{}/'
db = DbManager()

def get_json(url):
    response = requests.get(url)
    print(url)
    return json.loads(response.text)

def get_state(url):
    state = None
    try:
        state = db.open().query(State).filter(State.api == url).one()
    except:
        state = State()
        json_data = get_json(url)
        state.parse_json(json_data)

        db.save(state)

def get_city(url):
    city = None
    try:
        city = db.open().query(City).filter(City.api == url).one()
    except:
        city = City()
        json_data = get_json(url)
        city.parse_json(json_data)

        state = get_state(json_data['state'])
        city.state = state
        db.save(city)

    return city

def get_exchange(url):
    exchange = None
    try:
        exchange = db.open().query(Exchange).filter(Exchange.api == url).one()
    except:
        exchange = Exchange()
        json_data = get_json(url)
        exchange.parse_json(json_data)

        city = get_city(json_data['city'])
        exchange.city = city
        db.save(exchange)

    return exchange

def get_company(url):
    company = None
    try: 
        company = db.open().query(Company).filter(Company.api == url).one()
    except:
        company = Company()
        json_data = get_json(url)
        company.parse_json(json_data)
        db.save(company)
        
        try:
            exchange_url = json_data['exchange']
            if exchange_url:
                exchange = get_exchange(exchange_url)
                get_listing(company, exchange)
        except Exception as e:
            print(e)

    return company

def get_listing(company, exchange):
    listing = None
    cid_to_eid = str(exchange.id)+'_'+str(company.id)
    try:
        listing = db.open().query(Listing).filter(Listing.cid_to_eid == cid_to_eid).one()
    except:
        listing = Listing()
        listing.cid_to_eid = cid_to_eid
        listing.company = company
        listing.exchange = exchange
        listing.active = 1
        db.save(listing)
        print(listing.company)

    return listing
    
def get_department(url):
    department = None
    try:
        department = db.open().query(Department).filter(Department.api == url).one()
    except:
        department = Department()
        json_data = get_json(url)
        department.parse_json(json_data)

        company = get_company(json_data['company'])
        department.company = company
        db.save(department)

    return department


def get_person(url):
    person = None
    try:
        person = db.open().query(Person).filter(Person.api == url).one()
    except:
        person = Person()
        json_data = get_json(url)
        person.parse_json(json_data)
        db.save(person)

        current_job_url = json_data['current_job']
        if current_job_url:
            current_job = Job()
            department = get_department(current_job_url)

            current_job.department = department
            current_job.person = person
            current_job.active = 1
            db.save(current_job)

        for past_job_url in json_data['employment_history']:
            
            past_job = Job()
            department = get_department(past_job_url)
            
            past_job.department = department
            past_job.person = person
            past_job.active = 0
            db.save(past_job)

    return person

# exchange_url = "http://data.coding.kitchen/api/exchange/1"
# exchange = get_exchange(exchange_url)
# print(type(exchange))


# department_url = "http://data.coding.kitchen/api/department/18"
# department = get_department(department_url)
# print(type(department))


person_url = "http://data.coding.kitchen/api/person/1"
person = get_person(person_url)

person_url = "http://data.coding.kitchen/api/person/2"
person = get_person(person_url)