# Write your answer

class TextFileReader:
    """
    Encapsulates functionality for reading a text file
    and performing basic text analysis.
    """

    def __init__(self, file_path):
        # Initialize the file path
        self.file_path = file_path
        self.content = ""

    def read_file(self):
        # Open the file and read its content
        with open(self.file_path) as file:
            self.content = file.read()

    def count_lines(self):
        # Return number of lines in the file
        print(len(self.content.splitlines()))
        return len(self.content.splitlines())

    def count_words(self):
        # Return number of words in the file
        print(len(self.content.split()))
        return len(self.content.split())

    def count_characters(self):
        # Return number of characters in the file
        print(len(self.content))
        return len(self.content)

    def display_content(self):
        # Print file content
        print(self.content)



path = r'C:\Users\Ahmed\Desktop\DEPI\DEPI Round 4\MLE SESSION TASKS\DEPI_Round4_AMIT_MLE\src\python\Individual_final_project\file.txt'

file1 = TextFileReader(path)

file1.read_file()
file1.count_lines()
file1.count_words()
file1.display_content()
file1.count_characters()
