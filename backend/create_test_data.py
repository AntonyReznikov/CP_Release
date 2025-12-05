# Скрипт для создания тестовых данных в системе бронирования

import requests
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"

# Создание тестовых сотрудников
def create_employees():    
    employees = [
        {"full_name": "Иванов Иван Иванович", "email": "ivanov@company.com"},
        {"full_name": "Петрова Мария Сергеевна", "email": "petrova@company.com"},
        {"full_name": "Сидоров Петр Александрович", "email": "sidorov@company.com"},
        {"full_name": "Козлова Анна Дмитриевна", "email": "kozlova@company.com"},
    ]

    created = []
    for emp in employees:
        response = requests.post(f"{BASE_URL}/employees/", json=emp)
        if response.status_code == 201:
            created.append(response.json())
            print(f"[OK] Создан сотрудник: {emp['full_name']}")
        else:
            print(f"[ERROR] Ошибка создания сотрудника {emp['full_name']}: {response.text}")

    return created

# Создание тестовых ресурсов
def create_resources(): 
    resources = [
        {"name": "Переговорная №1 (10 этаж)", "type": "комната", "capacity": 8},
        {"name": "Переговорная №2 (11 этаж)", "type": "комната", "capacity": 12},
        {"name": "Переговорная №3 (12 этаж)", "type": "комната", "capacity": 6},
        {"name": "Проектор №1", "type": "проектор", "capacity": None},
        {"name": "Проектор №2", "type": "проектор", "capacity": None},
    ]

    created = []
    for res in resources:
        response = requests.post(f"{BASE_URL}/resources/", json=res)
        if response.status_code == 201:
            created.append(response.json())
            print(f"[OK] Создан ресурс: {res['name']}")
        else:
            print(f"[ERROR] Ошибка создания ресурса {res['name']}: {response.text}")

    return created

# Создание тестовых бронирований
def create_bookings(employees, resources):    
    today = date.today()

    bookings = [
        # Сегодняшние бронирования
        {
            "resource_id": resources[0]["id"],
            "employee_id": employees[0]["id"],
            "date": str(today),
            "start_time": "10:00",
            "end_time": "11:30",
        },
        {
            "resource_id": resources[1]["id"],
            "employee_id": employees[1]["id"],
            "date": str(today),
            "start_time": "14:00",
            "end_time": "15:00",
        },
        # Завтрашние бронирования
        {
            "resource_id": resources[0]["id"],
            "employee_id": employees[2]["id"],
            "date": str(today + timedelta(days=1)),
            "start_time": "09:00",
            "end_time": "10:00",
        },
        {
            "resource_id": resources[2]["id"],
            "employee_id": employees[3]["id"],
            "date": str(today + timedelta(days=1)),
            "start_time": "11:00",
            "end_time": "12:30",
        },
        # Бронирования на следующую неделю
        {
            "resource_id": resources[1]["id"],
            "employee_id": employees[0]["id"],
            "date": str(today + timedelta(days=7)),
            "start_time": "13:00",
            "end_time": "14:00",
        },
    ]

    created = []
    for booking in bookings:
        response = requests.post(f"{BASE_URL}/bookings/", json=booking)
        if response.status_code == 201:
            created.append(response.json())
            print(
                f"[OK] Создано бронирование: {booking['date']} {booking['start_time']}-{booking['end_time']}"
            )
        else:
            print(f"[ERROR] Ошибка создания бронирования: {response.text}")

    return created


def main():
    print("=" * 60)
    print("Создание тестовых данных для системы бронирования")
    print("=" * 60)
    print()

    # Проверка доступности сервера
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"[OK] Сервер доступен: {response.json()['message']}")
        print()
    except Exception as e:
        print(f"[ERROR] Ошибка подключения к серверу: {e}")
        print("Убедитесь, что backend запущен на http://127.0.0.1:8000")
        return

    # Создание данных
    print("--- Создание сотрудников ---")
    employees = create_employees()
    print()

    print("--- Создание ресурсов ---")
    resources = create_resources()
    print()

    print("--- Создание бронирований ---")
    bookings = create_bookings(employees, resources)
    print()

    print("=" * 60)
    print("Результаты:")
    print(f"  Создано сотрудников: {len(employees)}")
    print(f"  Создано ресурсов: {len(resources)}")
    print(f"  Создано бронирований: {len(bookings)}")
    print("=" * 60)
    print()
    print("Тестовые данные успешно созданы!")
    print("Откройте frontend (index.html) для просмотра.")
    print("Swagger UI доступен по адресу: http://127.0.0.1:8000/docs")


if __name__ == "__main__":
    main()
