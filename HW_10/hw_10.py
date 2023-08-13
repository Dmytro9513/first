from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name: str, phones: list, email: list):
        self.name = name
        self.phones = [Phone(phone) for phone in phones]
        self.emails = email

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number.value not in [phone.value for phone in self.phones]:
            self.phones.append(phone_number)
            
    def find_phone(self, value):
        pass

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, value):
        return self.data.get(value)