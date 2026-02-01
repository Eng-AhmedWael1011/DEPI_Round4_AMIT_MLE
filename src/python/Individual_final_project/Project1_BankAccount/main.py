from server import BankAccount

OPERATIONS = BankAccount()


def user_interface():

    """Runs the command-line interface for the bank system.

    This function handles all user interactions including:
    - User login and authentication
    - Account creation for new users
    - Performing banking operations such as:
        - Checking balance
        - Withdrawing money
        - Depositing money
        - Displaying user ID

    The function enforces a maximum of three password attempts
    before terminating the session and persists changes
    through the BankAccount service layer.

    Returns:
        None
    """
    
    print("************************************\n" \
          "        Welcome to Bank ABC         ")
    
    username = input("Please kindley enter your username: ")

    OPERATIONS.get_user_info(username)
    
    if OPERATIONS.active_user != {}:
        trys = 3
        while trys != 0:
            try:
                password = int(input("please enter your ATM Pin: "))
            except ValueError:
                print("PIN must be numbers only")
                continue
            if OPERATIONS.active_user['PinPassword'] != password:
                trys -= 1
                print('Password Incorrect!! Please try again')
                if trys == 0:
                    print("please Try again later!!! GoodBye!")
                    return

            else:
                print(f"Hello, {OPERATIONS.active_user['UserName']}")
                while True:
                    x = int(input("Select from the following options\n1- Check Balance\n2- Withdraw\n3- Deposit\n4- Identify UserID\n\n"))
                    
                    if x == 1:
                        OPERATIONS.check_balance()
                        y = int(input("Would you like to continue? 1-YES , 0-NO: "))
                        if y == 0:
                            break
                        
                    elif x == 2:

                        
                        print(f"Balance Available: {OPERATIONS.active_user['Balance']}")
                        amount = int(input("Enter the Amount of Withdrawel: "))
                        OPERATIONS.withdraw(amount)
                        y = int(input("Would you like to continue? 1-YES , 0-NO: "))
                        if y == 0:
                            print('Thank You, Have a wonderful Day!')
                            return

                    elif x == 3:

                        amount = int(input("Enter the Amount of Deposit: "))
                        OPERATIONS.deposit(amount)
                    
                        y = int(input("Would you like to continue? 1-YES , 0-NO: "))
                        if y == 0:
                            print('Thank You, Have a wonderful Day!')
                            return

                    elif x == 4:

                        OPERATIONS.determine_userID()
                        y = int(input("Would you like to continue? 1-YES , 0-NO: "))
                        if y == 0:
                            print('Thank You, Have a wonderful Day!')
                            return
                    else:
                        print("Please Select the right option!!")

    else:
        print("We gonna Create a Bank Account for you")
        a = input("Please Enter a username: ")
        OPERATIONS.get_user_info(a)
        while True:
            if OPERATIONS.active_user != {}:
                a = input("please enter another username: ")
                OPERATIONS.get_user_info(a)
            else:
                b = int(input("setup a PinPassword: "))
                OPERATIONS.adduser(a , b)
                return



user_interface()