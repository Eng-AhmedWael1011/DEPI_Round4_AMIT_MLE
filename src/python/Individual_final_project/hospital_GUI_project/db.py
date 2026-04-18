import json
from  factory import Hospital , Department

DB_FILE = r'src\python\Individual_final_project\hospital_GUI_project\hospital_data.json'

def hospital_to_dict(hospital: Hospital):
    return {
        "hospital": hospital.hospital_name,
        "location": hospital.location,
        "departments": [
            {
                "id" : dep.id,
                "name": dep.name,
                "patients" : [
                    {
                        "id" : pat.id,
                        "name" : pat.name,
                        "age" : pat.age,
                        "medical_record" : pat.medical_record,
                    }
                    for pat in dep.patients
                ],
                "staff": [
                    {
                        "id": emp.id,
                        "name": emp.name,
                        "age": emp.age,
                        "position": emp.position,
                    }
                    for emp in dep.staff
                ]
            }
            for dep in hospital.departments
        ]

    }

def dict_to_hospital(data):
    hosp = Hospital(data["hospital"], data["location"])

    for dep_data in data["departments"]:

        dep = hosp.add_department(dep_data["name"])

        for pat_data in dep_data.get("patients", []):
            dep.add_patient(
                pat_data["name"],
                pat_data["age"],
                pat_data["medical_record"],
                pat_data["id"]
            )
            
        for emp_data in dep_data.get("staff", []):
            dep.add_staff(
                emp_data["name"],
                emp_data["age"],
                emp_data["position"],
                emp_data["id"]
            )
    return hosp

    
def save_hospital(hospital):

    data = hospital_to_dict(hospital)

    with open(DB_FILE, "w" , encoding="utf-8") as file:
        json.dump(data , file , indent=4)

def load_hospital():
    """Load hospital data from JSON"""
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                raise FileNotFoundError  # Treat empty file like missing file
            data = json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        # First run or empty/corrupted file: create a new hospital
        print("No saved data found or file is empty. Creating new hospital...")
        return Hospital("City Hospital", "Cairo")

    # Build hospital from data
    hosp = Hospital(data["hospital"], data["location"])

    for dep_data in data.get("departments", []):
        dep = hosp.add_department(dep_data["name"], dep_data.get("id"))

        for pat_data in dep_data.get("patients", []):
            dep.add_patient(
                pat_data["name"],
                pat_data["age"],
                pat_data["medical_record"],
                pat_data["id"]
            )

        for emp_data in dep_data.get("staff", []):
            dep.add_staff(
                emp_data["name"],
                emp_data["age"],
                emp_data["position"],
                emp_data["id"]
            )

    print("Hospital loaded successfully!")
    return hosp
