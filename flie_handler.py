import re
import pickle
from collections import UserDict
from datetime import datetime, timedelta

class PhoneVerificationError(Exception):
    def __init__(self, phone):
        self.phone = phone
        self.message = f"Invalid phone number: {phone}"
        super().__init__(self.message)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        self.name = Field(name)

class Phone(Field):
    pattern = r'\d{10}$'

    def __init__(self, phone):
        super().__init__(phone)
        if re.match(Phone.pattern, phone):
            self.phone = phone
        else:
             raise PhoneVerificationError(phone)

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.birthday = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except PhoneVerificationError as e: 
            print(e.message)

    def remove_phone(self, phone):
        self.phones.remove(self.find_phone(phone)) 

    def edit_phone(self, old, new):
        for index in range(len(self.phones)):
            if self.phones[index].phone == old:
                self.phones[index] = Phone(new)

    def find_phone(self, phone_input):
        for phone in self.phones:
            if phone_input == phone.phone:
                return phone
            
    def add_birthday(self, birthday):
            try:
                self.birthday = Birthday(birthday)
            except ValueError as e:
                print(e)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name] = record

    def find(self, name):
        for record_name, record in self.data.items():
            if name == record_name.name.value:
                return record
            
    def delete(self, name):
        for record_name, _ in self.data.items():
            if name == record_name.name.value:
                self.data.pop(record_name)
                break

    def get_upcoming_birthdays(self):
        current_date = datetime.today().date()
        congratulations = []

        for record_name, record in self.data.items():
            try:
                record_birthday = record.birthday.birthday.date()
                birthday_this_year = record_birthday.replace(year=current_date.year)

                if birthday_this_year < current_date:
                    continue

                if (birthday_this_year - current_date).days > 7:
                    continue

                if birthday_this_year.weekday() == 5:
                    congratulation_date = birthday_this_year + timedelta(days=2)
                elif birthday_this_year.weekday() == 6:
                    congratulation_date = birthday_this_year + timedelta(days=1)
                else:
                    congratulation_date = birthday_this_year

                congratulations.append({"name": record_name.name.value, "congratulation_date": congratulation_date.strftime("%d.%m.%Y")})
            except: AttributeError
        
        if len(congratulations) > 0:
            return congratulations
        else: 
            return "No birthdays in upcoming week"
        
    def __str__(self):
        book = "List of contacts:"
        for record_name, record in self.data.items():
            record_phones = ','.join(p.value for p in record.phones)
            try:
                record_birthday = datetime.strftime(record.birthday.birthday, "%d.%m.%Y")
            except AttributeError:
                record_birthday = ""
            book = book + "\n" + record_name.name.value + " [" + record_phones + "]" + " " + record_birthday
        return book

def save_to_file(book: AddressBook, filename="addressbook.pkl") -> None:  
    with open(filename, "wb") as file:
        pickle.dump(book, file)

def get_contacts(filename="addressbook.pkl") -> AddressBook:
    book = AddressBook()
    try:
        with open(filename, "rb") as file:
            book = pickle.load(file)
            return book
        
    except FileNotFoundError:
        return book