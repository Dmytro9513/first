from datetime import datetime
from collections import UserDict
import json
import os

class Field:
    def __init__(self, value = None):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self,instance, value):
        self.value = value

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Name):
            return obj.__json_encode__()
        return super().default(obj)


class Phone(Field):
    def __set__(self, instance, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError("Невірний номер")
        
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __json_encode__(self):
        return self.value

    @classmethod
    def __json_decode__(cls, value):
        return cls(value)

class Birthday(Field):
    def __set__(self, instance, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Невірний формат дати народження. Введи YYYY-MM-DD")
        self.value = value
    
    def __init__(self, value):
        super().__init__(value)


    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __json_encode__(self):
        return self.value

    @classmethod
    def __json_decode__(cls, value):
        return cls(value)

class Name(Field):
    def __set__(self, instance, value):
        if not value:
            raise ValueError("Поле з імʼям не може бути пустим")
        self.value = value

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __json_encode__(self):
        return self.value

    @classmethod
    def __json_decode__(cls, value):
        return cls(value)


class Record:

    def __init__(self, name, phone):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.birthday = None

    
    def __json_encode__(self):
        data = {
            "name": self.name,
            "phones": [phone.__json_encode__() for phone in self.phones],
            "birthday": self.birthday.__json_encode__() if isinstance(self.birthday, Birthday) else self.birthday
        }
        return data

    

    @classmethod
    def __json_decode__(cls, data):
        record = cls(data["name"], data["phones"][0])
        record.birthday = Birthday.__json_decode__(data.get("birthday")) if data.get("birthday") else None
        for phone_data in data.get("phones")[1:]:
            record.add_phone(Phone.__json_decode__(phone_data))
        return record

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            self.phones.remove(old_phone)
            self.add_phone(new_phone)

    def edit_birthday(self, new_birthday):
        try:
            datetime.strptime(new_birthday, "%Y-%m-%d")
            self.birthday = Birthday(new_birthday)
        except ValueError:
            print("Невірний формат дати народження. Введи YYYY-MM-DD")

    def show_phones(self):
        return [phone.value for phone in self.phones]

    def days_to_birthday(self):
        if isinstance(self.birthday, Birthday):
            today = datetime.today().date()
            birthday_date = datetime.strptime(self.birthday.value, "%Y-%m-%d").date()
            
            next_birthday = birthday_date.replace(year=today.year)
            if today > next_birthday:
                next_birthday = birthday_date.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None
    """def days_to_birthday(self):
        if self.birthday and isinstance(self.birthday, Birthday):
            today = datetime.today()
            birthday_date = datetime.strptime(self.birthday.value, "%Y-%m-%d")
            
            next_birthday = datetime(today.year, birthday_date.month, birthday_date.day)

            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left
        return None"""

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index >= len(self.data):
            raise StopIteration
        record = list(self.data.values())[self._iter_index]
        self._iter_index += 1
        return record

    def search_by_name(self, name):
        results = []
        for record in self.data.values():
            if name.lower() in record.name.value.lower():
                results.append(record)
        return results

    def search_by_phone(self, phone):
        results = []
        for record in self.data.values():
            if any(phone in p.value for p in record.phones):
                results.append(record)
        return results
    
    def __json_encode__(self):
        data = {
            "contacts": [record.__json_encode__() for record in self.data.values()]
        }
        return data

    @classmethod
    def __json_decode__(cls, data):
        address_book = cls()
        for contact_data in data.get("contacts", []):
            record = Record(contact_data["name"]["value"], contact_data["phones"][0])
            record.birthday = Birthday.__json_decode__(contact_data.get("birthday")) if contact_data.get("birthday") else None
            for phone_data in contact_data.get("phones"):
                record.add_phone(Phone.__json_decode__(phone_data))
            address_book.add_record(record)
        return address_book

def save_address_book(address_book, filename):
    data = {
        "contacts": [record.__json_encode__() for record in address_book.data.values()]
    }
    with open(filename, "w") as file:
        json.dump(data, file, indent=4, cls=CustomJSONEncoder)



def load_address_book(filename):
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не існує. Створюю нову адресну книгу.")
        return AddressBook()

    try:
        with open(filename, "r") as file:
            data = json.load(file)
            print("Завантажені дані:", data)
            address_book = AddressBook()
            for contact_data in data.get("contacts", []):
                if contact_data is None:
                    print("Зустрічено None в contact_data")
                    continue
                if "name" in contact_data and "phones" in contact_data:
                    record = Record(contact_data["name"], contact_data["phones"][0])
                    birthday_str = contact_data.get("birthday")
                    if birthday_str is not None:
                        record.birthday = datetime.strptime(birthday_str, '%Y-%m-%d')
                    for phone in contact_data.get("phones")[1:]:
                        record.add_phone(phone)
                    address_book.add_record(record)
                else:
                    print("Недійсні дані контакту:", contact_data)
            return address_book
    except json.JSONDecodeError as e:
        print(f"Невірний JSON у файлі '{filename}': {e}")
        return AddressBook()
    

if __name__ == "__main__":
    filename = "address_book.json"
    book = load_address_book(filename)


    while True:
        command = input(">").lower()

        if command in ["bye", "good bye", "exit", "бувай", "до побачення"]:
            save_address_book(book, filename)
            print("До побачення,повертайся!")
            break
        elif command in ["hi", "hello", "привіт"]:
            print("Вітаю,друже!")
        elif command in ["add", "додати"]:
            name = input("Введи Імʼя: ").lower()
            phone = input("Введи номер телефону(10цифр): ")
            while not phone.isdigit() or len(phone) != 10:
                print("Цей номер не є дійсний.Введи 10 цифр.")
                phone = input("Введи номер(10 цифр): ")
            if name.lower() in book.data:
                print("Контакт з цим імʼям вже створений!")
            else:
                record = Record(name, phone)
                book.add_record(record)
                print("Контакт доданий.")
        elif command == "add_birthday":
            name = input("Введи імʼя: ")
            if name in book.data:
                birthday = input("Введи дату народження (YYYY-MM-DD): ")
                try:
                    datetime.strptime(birthday, "%Y-%m-%d")
                    book.data[name].birthday = Birthday(birthday)  # Викликаємо конструктор з одним аргументом
                    print("Дата народження додана.")
                except ValueError:
                    print("Невірний формат дати. Використовуйте YYYY-MM-DD.")
            else:
                print("Контакт з таким іменем ще не доданий.")
            """name = input("Введи імʼя: ")
            if name.lower() in book.data:
                birthday_input = input("Введи дату народження (YYYY-MM-DD): ")
                try:
                    datetime.strptime(birthday_input, "%Y-%m-%d")
                    record = book.data[name.lower()]
                    record.birthday = Birthday(birthday_input)
                    print("Дата народження додана.")
                except ValueError:
                    print("Невірний формат дати народження. Введи YYYY-MM-DD")
            else:
                print("Контакт з таким іменем ще не доданий.")"""
        elif command.startswith("edit_phone"):
            try:
                name = input("Введи імʼя: ")
                record = book.get(name)
                if record:
                    print(f"Current phone(s):")
                    phone_to_edit = input("Введи номер для зміни: ")
                    new_phone = input("Введи новий номер: ")
                    for phone in record.phones:
                        if phone.value == phone_to_edit:
                            phone.value = new_phone
                            print("Номер змінено.")
                            break
                    else:
                        print("Номер не знайдений.")
                else:
                    print(f"Контакт '{name}' не знайдено.")
            except Exception as e:
                print(f"Error: {e}")
        elif command == "edit_birthday":
            name = input("Введи імʼя: ")
            if name.lower() in book.data:
                record = book.data[name.lower()]
                new_birthday = input("Введи нову дату народження (YYYY-MM-DD): ")
                record.edit_birthday(new_birthday)
            else:
                print("Контакт не знайдений.")
        elif command == "show all":
            for record in book.data.values():
                print(f"Імʼя: {record.name.value}, Телефон: {record.show_phones()}")
                
                if record.birthday is not None:
                    days_left = record.days_to_birthday()
                    if days_left is not None:
                        days_str = f"{days_left} днів"
                    else:
                        days_str = "Сьогодні!"
                    print(f"Днів до дня народження: {days_str}")
                else:
                    print("Днів до дня народження: Немає дати")
                
                print("-" * 20)


        elif command == "search name":
            name_query = input("Введи частину імені для пошуку: ").lower()
            search_results = book.search_by_name(name_query)
            if search_results:
                print("Результат пошуку:")
                for result in search_results:
                    print(f"Ім'я: {result.name.value}, Телефон: {result.show_phones()}")
                    if hasattr(result, 'birthday'):
                        print(f"Днів до дня народження: {result.days_to_birthday()} днів")
                    print("-" * 20)
            else:
                print("Контакт не знайдений.")
        elif command == "search phone":
            phone_query = input("Введи частину номера для пошуку: ")
            search_results = book.search_by_phone(phone_query)
            if search_results:
                print("Результат пошуку:")
                for result in search_results:
                    print(f"Ім'я: {result.name.value}, Телефон: {result.show_phones()}")
                    if hasattr(result, 'birthday'):
                        print(f"Днів до дня народження: {result.days_to_birthday()} днів")
                    print("-" * 20)
            else:
                print("Контакт не знайдений.")

        elif command == "delete":
            name = input("Введи імʼя до видалення: ")
            if name.lower() in book.data:
                del book.data[name.lower()]
                print(f"Контакт '{name}' видалений.")
            else:
                print(f"Контакт '{name}' не знайдений.")
        else:
            print("Невірна команда.")

        save_address_book(book, filename)
