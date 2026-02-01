import random as rd
import json
import os
# DATABASE
PATH = r'C:\Users\Ahmed\Desktop\DEPI\DEPI Round 4\MLE SESSION TASKS\DEPI_Round4_AMIT_MLE\src\python\Individual_final_project\Project1_BankAccount'

class DataBase():
    """
    DataBase class to manage user information for a Bank Account project.

    This class handles storing, retrieving, and updating user data in a JSON file. 
    It ensures that each user has a unique UserID and prevents duplicate usernames.

    """
    def __init__(self , json_file=os.path.join( PATH , 'users.json')):
        '''
        Docstring for __init__
        
        Attributes:
        users (list): A list of dictionaries, each representing a user with keys:
                      'UserID', 'UserName', 'PinPassword', and 'Balance'.
        json_file (str): Path to the JSON file where user data is stored.

        '''
        self.users = []
        self.json_file = json_file
        # Load users at startup
        try:
            with open(self.json_file, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = []

    def save_to_file(self):
        '''
        save_to_file():
        Saves the current `users` list to the JSON file in a formatted way.
        '''
        with open(self.json_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def add_user(self, username: str, PinPassword: int):

        ''' 
        add_user(username: str, PinPassword: int):
            Adds a new user with a unique UserID and PIN password.
            Checks for duplicate usernames before adding.
            Initializes the user's balance to 0.
            Returns the newly created user dictionary if successful, otherwise None.
        '''

        for user in self.users:
            if user['UserName'] == username:
                print(f"Username '{username}' already exists.")
                return None

        while True:
            current_ID = rd.randrange(10000, 1000000)
            if all(u['UserID'] != current_ID for u in self.users):
                break

        new_user = {
            "UserID": current_ID,
            "UserName": username,
            "PinPassword": PinPassword,
            "Balance": 0
        }

        self.users.append(new_user)
        self.save_to_file()
        print(f"User '{username}' added successfully!")
        return new_user
        
    def update_user(self, user):
        '''
        update_user(user: dict):
            Updates an existing user's information in the users list.
            Matches the user based on 'UserID' and saves the updated list to the file.
        '''
        for i in range(len(self.users)):
            if self.users[i]['UserID'] == user['UserID']:
                self.users[i] = user
                self.save_to_file()
                break



