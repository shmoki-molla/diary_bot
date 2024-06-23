from app.database.models import User

months = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12"
}

year = "2024"

def convert_date(input_string):
    parts = input_string.split()
    date = parts[0]
    month = parts[1].lower()

    if month in months:
        month_number = months[month]
        return f"{year}:{month_number}:{date}"



