import socket

HOST = 'localhost'
PORT = 64900

employee_locked = False
menu_locked = False
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    print("HR System 1.0")
    while not employee_locked:
        emp_id = input("What is the employee ID? ")
        emp_id = emp_id.encode()
        sock.sendall(emp_id)
        data = sock.recv(512).decode()
        if eval(data):
            employee_locked = True
            print("Employee is locked")
            break
        else:
            print("Employee not recognised")

    # =================
    # Menu
    # =================
    while True:
        menu_choice = input("Salary (S) or Annual Leave (L) Query?: ")
        sock.sendall(menu_choice.encode())
        data = sock.recv(512).decode()
        if data == "False":
            print("Invalid Command")
            continue

        if menu_choice == "S":
            sub_choice = input("Current salary (C) or total salary (T) for year? ")

        elif menu_choice == "L":
            sub_choice = input("Current Entitlement (C) or Leave taken for year (Y)? ")

        sock.send(sub_choice.encode())
        data = sock.recv(512).decode()

        if data == "continue":
            year_choice = input("What year? ")
            sock.send(year_choice.encode())
            data = sock.recv(512).decode()

        if data == "False":
            print("Invalid Command")
            continue
        print(data)







