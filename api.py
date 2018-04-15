from entities import Company, Club, Person, League, City, Department, State, Exchange, Listing, Job, Address
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

    return state

def get_city(url):
    city = None
    try:
        city = db.open().query(City).filter(City.api == url).one()
    except:
        city = City()
        json_data = get_json(url)
        city.parse_json(json_data)
        state_url = json_data['state']
        print("-----in get city: {} ".format(state_url))
        state = get_state(state_url)
        print("in get city: {} ".format(state.name))
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

def get_job(person, department, active):
    pid_to_did = str(person.id) + '_' + str(department.id)
    job = None
    try:
        job = db.open().query(Job).filter(Job.pid_to_did == pid_to_did).one()
        if job.active != active:
            job.active = active
        db.update(job)
    except:
        job = Job()
        job.pid_to_did = pid_to_did
        job.person = person
        job.department = department
        job.active = active
        db.save(job)
    return job

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
            department = get_department(current_job_url)
            current_job = get_job(person, department, 1)

        for past_job_url in json_data['employment_history']:
            
            department = get_department(past_job_url)
            past_job = get_job(person, department, 0)

        current_address = json_data['current_address']
        if current_address:
            city = get_city_from_address(current_address)
            address = get_address(person, city, 1)

        for past_address in json_data['past_addresses']:
            city = get_city_from_address(past_address)
            address = get_address(person, city, 0)

    return person

def get_city_from_address(address):
    base_state_url = 'http://data.coding.kitchen/api/state/'
    state_url = base_state_url + address['state']
    state = get_state(state_url)
    city_name = address['city']
    zip_code = address['zip']
    city = None
    try:
        city = db.open().query(City).filter((City.name == city_name) & (City.state == state)).one()
    except:
        state_json = get_json(state_url)
        print(state_json['name'])
        for city_url in state_json['cities']:
            if get_json(city_url)['zipcode']==zip_code:
                print(city_name + city_url)
                city = get_city(city_url)
                return city

    return city

def get_address(person, city, active):
    pid_to_cid = str(person.id) + '_' + str(city.id)
    address = None
    try:
        address = db.open().query(Address).filter(Address.pid_to_cid == pid_to_cid).one()
        if address.active != active:
            address.active = active
        db.update(address)
    except:
        address = Address()
        address.pid_to_cid = pid_to_cid
        address.person = person
        address.city = city
        address.active = active
        db.save(address)
    return address
    

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

person_url = "http://data.coding.kitchen/api/person/3"
person = get_person(person_url)