from datetime import datetime
from collections import UserDict

class Field:
    def __init__(self, value = None):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self,instance, value):
        self.value = value


class Phone(Field):
    def __set__(self, instance, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError("Невірний номер")

class Birthday(Field):
    def __set__(self, instance, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Невірний формат дати народження. Введи YYYY-MM-DD")
        self.value = value

class Name(Field):
    def __set__(self,instance, value):
        if not value:
            raise ValueError("Поле з імʼям не може бути пустим")
        self.value = value

class Record:
    def __init__(self, name, phone):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.birthday = None

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
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, int(self.birthday.value[5:7]), int(self.birthday.value[8:10]))
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left
        return None

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

if __name__ == "__main__":
    book = AddressBook()

    while True:
        command = input(">").lower()

        if command in ["bye", "good bye", "exit", "бувай", "до побачення"]:
            print("До побачення,повертайся!")
            break
        elif command in ["hi", "hello", "привіт", "вітаю"]:
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
                print("Контакт з таким іменем ще не доданий.")
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
                if hasattr(record, 'birthday'):
                    print(f"Днів до дня народження: {record.days_to_birthday()} днів")
                print("-" * 20)
        elif command == "search name":
            name_query = input("Введи імʼя для пошуку: ")
            search_results = book.search_by_name(name_query.lower())
            if search_results:
                print("Результат пошуку:")
                for result in search_results:
                    print(f"Імʼя: {result.name.value}, Телефон: {result.show_phones()}")
                    if hasattr(result, 'birthday'):
                        print(f"Днів до дня народження: {result.days_to_birthday()} днів")
                    print("-" * 20)
            else:
                print("Контакт не знайдений.")
        elif command == "search phone":
            phone_query = input("Введи телефон для пошуку: ")
            search_results = book.search_by_phone(phone_query)
            if search_results:
                print("Search results:")
                for result in search_results:
                    print(f"Імʼя: {result.name.value}, Телефон: {result.show_phones()}")
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

    if __name__ == "__main__":
        book = AddressBook()

        record1 = Record("Dmytro", "1234567890")
        record2 = Record("Mila", "9876543210")
        book.add_record(record1)
        book.add_record(record2)

        for contact in book:
            print(f"Ім'я: {contact.name.value}, Телефон: {contact.show_phones()}")