import os

def createfolder(path:str , n:int):
    """
    Docstring for createfolder
    
    :param path: takes a path from user to create folder
    :type path: str

    :param n: takes number of folder creations users wants to enter

    :return: str
    return: n of ordered folders based on the n entered
    """
    if not os.path.exists(path):
        os.makedirs(path)
        for i in range(n):
            inner_path = os.path.join(path , 'dir_' +  str(i))
            if not os.path.exists(inner_path):
                os.makedirs(inner_path)
        print('Files Created Successfully!')
    else:
        print("directory already exists: ", path)
