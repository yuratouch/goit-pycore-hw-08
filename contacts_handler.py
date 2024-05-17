import pickle
from datetime import datetime
from error_handler import input_error
from flie_handler import Record, Phone, Birthday, PhoneVerificationError

@input_error
def add_contact(args:list, book) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
        
    if phone:
        record.add_phone(phone)
    
    return message


@input_error
def change_contact(args:list, book) -> str:
    name, old, new = args
    record = book.find(name)

    if record:
        for index in range(len(record.phones)):
            if record.phones[index].phone == old:
                try:
                    record.phones[index] = Phone(new)
                    return "Contact updated."
                except PhoneVerificationError as e:
                    return e.message

        return f"Contact {name} does not have entered phone number."
    
    return "Contact not found."

def show_phone(args:list, book) -> str:
    name = args[0]
    record = book.find(name)

    if record:
        return ', '.join(p.value for p in record.phones)
    
    return "Contact not found."

def show_all(filename="addressbook.pkl") -> str:
    with open(filename, "rb") as file:
            book = pickle.load(file)
            return book
    
def add_birthday(args:list, book) -> str:
    name, date = args
    record = book.find(name)

    if record:
        try:
            record.birthday = Birthday(date)
            return f"Birthday added for {name}."
        except ValueError:
            return "Invalid date format. Please enter date in format DD.MM.YYYY"
    else: 
        return "Contact not found."

def show_birthday(args:list, book) -> str:
    name = args[0]
    record = book.find(name)

    if record:
        try:
            return f"{name}'s birthday is {datetime.strftime(record.birthday.birthday, "%d.%m.%Y")}"
        except AttributeError:
            return f"No record about {name}'s birthday."
        
    return "Contact not found."

def show_upcoming_birthdays(book) -> list:
    return book.get_upcoming_birthdays()
