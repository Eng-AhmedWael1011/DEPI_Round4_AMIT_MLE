from abc import ABC, abstractmethod

# Creating the Abstract class, Person

class Person(ABC):
    """An abstract base class representing a person.

    Attributes:
        name: A string representing the person's name.
        age: An integer representing the person's age.
    """

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def view_info(self):
        """The Inhertied class will adjust the function"""
        pass




# Inherit the Patient and Staff Classes

class Patient(Person):

    """Represents a patient in the hospital in a specific Department.

    param:_id_counter: used for intializing the patient ID  

    Attributes:
        name: Patient's name.
        age: Patient's age.
        medical_record: A string containing the medical history.
        patient_id: A unique string identifier (e.g., PAT12345).
    """

    _id_counter = 1

    def __init__(self, name, age, medical_record, ID=None):
        if ID is None:
            self.id = f"PAT{10000 + Patient._id_counter}"
            Patient._id_counter += 1
        else:
            self.id = ID
            numeric_part = int(ID.replace("PAT", ""))
            Patient._id_counter = max(Patient._id_counter, numeric_part - 9999 + 1)
        super().__init__(name, age)
        self.medical_record = medical_record


    def view_info(self):
        return f"|{self.id} | {self.name} | age {self.age} | "
        
    
    def view_record(self):
        return f"Patient's medical Record: {self.medical_record}"



class Staff(Person):

    """A class to represent a staff member, inheriting from Person.

    Attributes:
        name: Staff member's name.
        age: Staff member's age.
        id: Unique identifier for the staff member.
    """

    _id_counter = 1

    def __init__(self, name, age, position, ID=None):
        if ID is None:
            self.id = f"EMP{10000 + Staff._id_counter}"
            Staff._id_counter += 1
        else:
            self.id = ID
            numeric_part = int(ID.replace("EMP", ""))
            Staff._id_counter = max(Staff._id_counter, numeric_part - 9999 + 1)
        super().__init__(name, age)
        self.position = position
    
    def view_info(self):
        return f"|{self.id} | {self.name} | age {self.age} | {self.position} | "



# Department instance

class Department:
    """Represents a hospital department containing patients and staff.

    Attributes:
        dep_ID: Unique identifier for the department.
        name: Name of the department.
        patients: List of Patient objects.
        staff: List of Staff objects.
    """
    _id_counter = 1

    def __init__(self, name, ID=None):
        if ID is None:
            self.id = f"DEP{100 + Department._id_counter}"
            Department._id_counter += 1
        else:
            self.id = ID
            numeric = int(ID.replace("DEP", ""))
            Department._id_counter = max(Department._id_counter, numeric - 100 + 1)
        self.name = name
        self.patients = []
        self.staff = []


    def add_patient(self, name, age, medical_record, ID=None):
        """Creates and adds a new patient to the department.
        
        Returns:
            A new Patient instance
        """

        patient = Patient(name, age, medical_record, ID)
        self.patients.append(patient)
        return patient
        
    def add_staff(self, name, age, position, ID=None):
        """Creates and adds a new staff to the department.

        Returns:
            A new Staff instance
        """
        staff = Staff(name, age, position, ID)
        self.staff.append(staff)
        return staff



# Hospital Class

class Hospital:

    def __init__(self, name,location):
        """Represents a hospital containing multiple departments.

        Attributes:
            hospital_name: The name of the hospital.
            departments: List of Department objects.
        """
        self.hospital_name = name
        self.location = location
        self.departments = []


    def add_department(self, name,ID=None):
        """Creates and adds a new department to the hospital.
        
        Returns:
            A new Department instance
        """
        department = Department(name, ID)
        self.departments.append(department)
        return department
