from functions import *

if __name__ == '__main__':
    master()
    while True:
        operation_list()
        user_choice = input('Your choice: ')

        if user_choice == '1':
            save_password()
        elif user_choice == '2':
            retrieve_password()
        elif user_choice == '3':
            sys.exit()
        else:
            print('Invalid choice!')
