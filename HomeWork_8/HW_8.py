import datetime

def get_birthdays_per_week(users):
    # Визначаємо поточний день тижня (понеділок - 0, неділя - 6).
    current_day_of_week = datetime.datetime.now().weekday()

    # Створюємо словник для зберігання іменинників на кожний день тижня.
    birthdays_by_weekday = {i: [] for i in range(7)}

    for user in users:
        # Отримуємо день народження користувача з об'єкту datetime.
        birthday = user["birthday"].date()

        # Визначаємо день тижня, на який припадає день народження (понеділок - 0, неділя - 6).
        birthday_day_of_week = birthday.weekday()

        # Перевіряємо, чи є день тижня вихідним (субота або неділя).
        if birthday_day_of_week >= 5:  # 5 і 6 - вихідні дні (субота, неділя).
            # Знаходимо, скільки днів потрібно додати до дня народження, щоб перенести його на понеділок (якщо субота - додаємо 2 дні, якщо неділя - додаємо 1 день).
            days_to_add = 2 if birthday_day_of_week == 5 else 1
            # Знаходимо новий день народження, перенесений на понеділок.
            birthday = birthday + datetime.timedelta(days=days_to_add)

        # Додаємо ім'я користувача до списку іменинників на відповідний день тижня.
        birthdays_by_weekday[birthday.weekday()].append(user["name"])

    # Виводимо іменинників на тиждень вперед.
    for i in range(7):
        # Визначаємо день тижня.
        day_name = datetime.date(2000, 1, 3 + i).strftime('%A')  # 2000-01-03 - це понеділок.
        # Виводимо іменинників для даного дня тижня, якщо вони є.
        if birthdays_by_weekday[i]:
            print(f"{day_name}: {', '.join(birthdays_by_weekday[i])}")

# тестовий список users:
users = [
    {"name": "Alex", "birthday": datetime.datetime(2023, 7, 25)}, #вівторок
    {"name": "Anna", "birthday": datetime.datetime(2022, 1, 2)}, #неділя
    {"name": "Мах", "birthday": datetime.datetime(2022, 1, 1)}, #суббота
    {"name": "Bob", "birthday": datetime.datetime(2023, 7, 27)},  # Четвер
    {"name": "Mike", "birthday": datetime.datetime(2023, 7, 28)},  # П'ятниця
    {"name": "Ivan", "birthday": datetime.datetime(2023, 7, 30)},  # Неділя
    {"name": "Nick", "birthday": datetime.datetime(2023, 7, 26)},   #середа
]

get_birthdays_per_week(users)
