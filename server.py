import socket


def find_employee_current_salary(employee_id):
    for employee in employees:
        if employee.get("id") == employee_id:
            return f"Current Salary: {employee.get('current_salary')}"


def find_employee_total_salary(employee_id, chosen_year):
    for employee in employees:
        if employee.get("id") == employee_id:
            for year in employee.get("salary_history"):
                if year.get("year") == chosen_year:
                    return f"Total Salary for {chosen_year}: {year.get('salary')}"
            return "Year not found"


def find_employee_current_leave(employee_id):
    for employee in employees:
        if employee.get("id") == employee_id:
            return f"Current Leave Entitlement: {employee.get('current_leave_entitlement')}"


def find_employee_year_leave(employee_id, chosen_year):
    for employee in employees:
        if employee.get("id") == employee_id:
            for year in employee.get("leave_history"):
                if year.get("year") == chosen_year:
                    return f"Total Leave Taken for {chosen_year}: {year.get('days')}"
            return "Year not found"


HOST = "localhost"
PORT = 64900

employees = [
    {
        "id": "E001",
        "name": "Alex Johnson",
        "current_salary": "25000",
        "salary_history": [
            {
                "year": "2018",
                "salary": "22000"
            },
            {
                "year": "2019",
                "salary": "23000"
            },
            {
                "year": "2020",
                "salary": "24000"
            },
            {
                "year": "2021",
                "salary": "25000"
            }
        ],
        "current_leave_entitlement": "20",
        "leave_history": [
            {
                "year": "2019",
                "days": "15"
            },
            {
                "year": "2020",
                "days": "9"
            },
            {
                "year": "2021",
                "days": "7"
            }
        ]
    },
    {
        "id": "E002",
        "name": "David Atten",
        "current_salary": "49000",
        "salary_history": [
            {
                "year": "2015",
                "salary": "35000"
            },
            {
                "year": "2016",
                "salary": "38000"
            },
            {
                "year": "2017",
                "salary": "39000"
            },
            {
                "year": "2018",
                "salary": "40000"
            },
            {
                "year": "2019",
                "salary": "43000"
            },
            {
                "year": "2020",
                "salary": "47000"
            },
            {
                "year": "2021",
                "salary": "49000"
            }
        ],
        "current_leave_entitlement": "30",
        "leave_history": [
            {
                "year": "2015",
                "days": "4"
            },
            {
                "year": "2016",
                "days": "9"
            },
            {
                "year": "2017",
                "days": "13"
            },
            {
                "year": "2018",
                "days": "14"
            },
            {
                "year": "2019",
                "days": "9"
            },
            {
                "year": "2020",
                "days": "23"
            },
            {
                "year": "2021",
                "days": "4"
            }
        ]
    }
]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    conn, addr = sock.accept()
    employee_locked = False
    employee_id = ""
    while True:
        print("Connected from: ", addr)
        # if not data:
        #     break
        if not employee_locked:
            data = conn.recv(512).decode()
            for employee in employees:
                if data == employee.get("id"):
                    reply = "True".encode()
                    employee_locked = True
                    employee_id = data
                    break
            if not employee_locked:
                print("Employee is false")
                reply = "False".encode()
            conn.send(reply)

        else:
            menu_choice = conn.recv(512).decode()

            if menu_choice == "S":
                reply = "True".encode()
                conn.send(reply)
                sal_choice = conn.recv(512).decode()
                if sal_choice == "C":
                    reply = find_employee_current_salary(employee_id).encode()
                elif sal_choice == "T":
                    reply = "continue".encode()
                    conn.send(reply)
                    year = conn.recv(512).decode()
                    reply = f"{find_employee_total_salary(employee_id, year)}".encode()
                else:
                    reply = "False".encode()
                conn.send(reply)

            elif menu_choice == "L":
                reply = "True".encode()
                conn.send(reply)
                leave_choice = conn.recv(512).decode()
                if leave_choice == "C":
                    reply = find_employee_current_leave(employee_id).encode()
                elif leave_choice == "Y":
                    reply = "continue".encode()
                    conn.send(reply)
                    year = conn.recv(512).decode()
                    reply = f"{find_employee_year_leave(employee_id, year)}".encode()
                else:
                    reply = "False".encode()
                conn.send(reply)

            else:
                reply = "False".encode()
                conn.send(reply)


