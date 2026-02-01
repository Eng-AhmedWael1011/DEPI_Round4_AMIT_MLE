from database import DataBase


DATABASE = DataBase()

class BankAccount():

    """
    Handles basic bank account operations for users.

    This class manages user creation, authentication,
    balance operations, and interaction with the database.
    """

    def __init__(self):
        """Initializes the BankAccount instance.

        Attributes:
            active_user (dict): Currently logged-in user data.
            users (list): List of all users loaded from the database.
            currentErrors (int): Error flag (0 = no error, 1 = error).
        """

        self.active_user = {}
        self.users = DATABASE.users
        self.currentErrors = 0

    def adduser(self , username , password):
        """Creates a new user account.

        Args:
            username (str): The username for the new account.
            password (int): The PIN password for the account.

        Returns:
            None
        """
        DATABASE.add_user(username=username , PinPassword = password)
        print("User Created Successfully")
        self.currentErrors = 0


    def get_user_info(self , username: str):

        """Retrieves user information based on username.

        Args:
            username (str): The username to search for.

        Returns:
            dict: The matched user data if found, otherwise an empty dict.
        """

        print(self.users)
        self.active_user = {}
        for user in self.users:
            if user['UserName'] == username:
                self.active_user = user
                print(self.active_user)
                break
        self.currentErrors = 0
        return self.active_user
    
    def determine_userID(self):
        """Displays the active user's ID.

        Returns:
            None
        """
        print(f"Your user ID is: {self.active_user['UserID']}")
        self.currentErrors = 0
    
    def deposit(self, amount: int):
        """Deposits money into the active user's account.

        Args:
            amount (int): Amount of money to deposit.

        Returns:
            dict: Updated active user data.
        """

        prev_balance = self.active_user["Balance"]

        self.active_user['Balance'] += amount
        print(f"Previous Balance: {prev_balance}\nAmount Deposited: {amount}\nCurrent Balance: {self.active_user['Balance']}")
        DATABASE.update_user(self.active_user)
        self.currentErrors = 0
        return self.active_user
    
    def withdraw(self, amount: int):
        """Withdraws money from the active user's account.

        Args:
            amount (int): Amount of money to withdraw.

        Returns:
            None
        """
        if self.active_user['Balance'] < amount:
            print("Amount exceeded the existing balance")
            self.currentErrors = 1
        else:
            prev_balance = self.active_user["Balance"]
            self.active_user['Balance'] -= amount
            print(f"Previous Balance: {prev_balance}\nAmount withdrawn: {amount}\nCurrent Balance: {self.active_user['Balance']}")
            DATABASE.update_user(self.active_user)
            self.currentErrors = 0
    
    def check_balance(self):
        """Displays the active user's current balance.

        Returns:
            None
        """
        print(f"Total Balance: {self.active_user['Balance']}")
        self.currentErrors = 0