import customtkinter as ctk
from tkinter import messagebox
from db import load_hospital, save_hospital
from factory import Hospital, Department, Patient, Staff

# --- 1. LIGHT THEME CONFIGURATION ---
ctk.set_appearance_mode("light")  # Set to Light Mode
ctk.set_default_color_theme("blue")

class HospitalApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.hospital = load_hospital()
        # Ensure at least one department exists
        if not self.hospital.departments:
            self.hospital.add_department("General")

        self.title(f"Admin Portal | {self.hospital.hospital_name}")
        self.geometry("1100x700") # Adjusted default size for better window management

        # Configure Grid Layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- 2. SIDEBAR (Light Gray Palette) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#ebebeb")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CITY HOSPITAL", 
                                       font=ctk.CTkFont(size=20, weight="bold"), text_color="#1f538d")
        self.logo_label.pack(pady=30, padx=20)

        self.home_btn = self.create_nav_btn("Dashboard", self.show_dashboard)
        self.dep_btn = self.create_nav_btn("Departments", self.show_departments)
        self.pat_btn = self.create_nav_btn("Patients", self.show_patients)
        self.staff_btn = self.create_nav_btn("Staff Registry", self.show_staff)
        
        self.save_btn = ctk.CTkButton(self.sidebar_frame, text="Save Data", fg_color="transparent", 
                                      border_width=1, text_color="#1f538d", command=self.save_data)
        self.save_btn.pack(side="bottom", pady=20, padx=20)

        # --- 3. MAIN CONTENT AREA (Pure White) ---
        self.main_view = ctk.CTkFrame(self, corner_radius=15, fg_color="#ffffff")
        self.main_view.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_view.grid_columnconfigure(0, weight=1)
        self.main_view.grid_rowconfigure(0, weight=1)

        # Initialize Screens
        self.show_dashboard()

    def create_nav_btn(self, text, command):
        # Adjusted text_color to black for light mode visibility
        btn = ctk.CTkButton(self.sidebar_frame, text=text, font=ctk.CTkFont(size=14), 
                            height=40, anchor="w", fg_color="transparent", 
                            text_color="black", hover_color="#d1d1d1", command=command)
        btn.pack(fill="x", padx=20, pady=5)
        return btn

    def clear_main_view(self):
        for widget in self.main_view.winfo_children():
            widget.destroy()

    # ------------------ SCREENS ------------------

    def show_dashboard(self):
        self.clear_main_view()
        
        # Header (Dark text for light background)
        header = ctk.CTkLabel(self.main_view, text=f"Welcome, Administrator", 
                              font=ctk.CTkFont(size=28, weight="bold"), text_color="#1a1a1a")
        header.pack(pady=(0, 30), anchor="w", padx=20)

        # Stats Row
        stats_frame = ctk.CTkFrame(self.main_view, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10, padx=20)

        total_p = sum(len(d.patients) for d in self.hospital.departments)
        total_s = sum(len(d.staff) for d in self.hospital.departments)
        
        # Vibrant but light-friendly colors
        self.create_stat_card(stats_frame, "Total Patients", str(total_p), "#3b82f6").grid(row=0, column=0, padx=10)
        self.create_stat_card(stats_frame, "Medical Staff", str(total_s), "#10b981").grid(row=0, column=1, padx=10)
        self.create_stat_card(stats_frame, "Departments", str(len(self.hospital.departments)), "#f59e0b").grid(row=0, column=2, padx=10)

        # Information Box
        info_box = ctk.CTkTextbox(self.main_view, height=200, fg_color="#f9fafb", 
                                  border_width=1, border_color="#e5e7eb", text_color="black")
        info_box.pack(fill="both", expand=True, pady=20, padx=20)
        info_box.insert("0.0", f"Hospital Status: Operational\nLocation: {self.hospital.location}\n\nQuick Tips:\n1. Use the sidebar to navigate.\n2. Don't forget to save before exiting.")

    def create_stat_card(self, master, title, value, color):
        # Card with subtle border and light gray background
        card = ctk.CTkFrame(master, width=200, height=120, fg_color="#f9fafb", 
                            border_width=1, border_color="#e5e7eb")
        card.grid_propagate(False)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color="gray").pack(pady=(15, 0))
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=32, weight="bold"), text_color=color).pack(pady=5)
        return card

    def show_departments(self):
        self.clear_main_view()
        
        top_bar = ctk.CTkFrame(self.main_view, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 20), padx=20)
        ctk.CTkLabel(top_bar, text="Departments Management", font=ctk.CTkFont(size=22, weight="bold"), text_color="black").pack(side="left")
        ctk.CTkButton(top_bar, text="+ Add Dept", width=100, command=self.add_dep_popup).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.main_view, fg_color="#ffffff")
        scroll.pack(fill="both", expand=True, padx=20)

        for dep in self.hospital.departments:
            item = ctk.CTkFrame(scroll, height=60, fg_color="#f3f4f6")
            item.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(item, text=f"ID: {dep.id}", width=100, text_color="black").pack(side="left", padx=10)
            ctk.CTkLabel(item, text=dep.name, font=ctk.CTkFont(weight="bold"), text_color="black").pack(side="left", padx=20)
            ctk.CTkLabel(item, text=f"Patients: {len(dep.patients)} | Staff: {len(dep.staff)}", text_color="#4b5563").pack(side="right", padx=20)

    def show_patients(self):
        self.clear_main_view()
        
        top_bar = ctk.CTkFrame(self.main_view, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 20), padx=20)
        ctk.CTkLabel(top_bar, text="Patient Registry", font=ctk.CTkFont(size=22, weight="bold"), text_color="black").pack(side="left")
        ctk.CTkButton(top_bar, text="+ Register Patient", width=100, command=self.add_patient_popup).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.main_view, fg_color="#ffffff")
        scroll.pack(fill="both", expand=True, padx=20)

        for dep in self.hospital.departments:
            if dep.patients:
                ctk.CTkLabel(scroll, text=f"Department: {dep.name}", font=ctk.CTkFont(weight="bold"), text_color="#3b82f6").pack(pady=(10, 5), anchor="w")
                for pat in dep.patients:
                    item = ctk.CTkFrame(scroll, fg_color="#f3f4f6")
                    item.pack(fill="x", pady=2, padx=10)
                    ctk.CTkLabel(item, text=f"{pat.id} | {pat.name.title()}", font=ctk.CTkFont(size=13), text_color="black").pack(side="left", padx=10, pady=5)
                    ctk.CTkLabel(item, text=f"Age: {pat.age} | Diagnosis: {pat.medical_record}", text_color="#4b5563").pack(side="right", padx=10)

    def show_staff(self):
        self.clear_main_view()
        
        top_bar = ctk.CTkFrame(self.main_view, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 20), padx=20)
        ctk.CTkLabel(top_bar, text="Staff Directory", font=ctk.CTkFont(size=22, weight="bold"), text_color="black").pack(side="left")
        ctk.CTkButton(top_bar, text="+ Recruit Staff", width=100, command=self.add_staff_popup).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.main_view, fg_color="#ffffff")
        scroll.pack(fill="both", expand=True, padx=20)

        for dep in self.hospital.departments:
            if dep.staff:
                ctk.CTkLabel(scroll, text=f"Department: {dep.name}", font=ctk.CTkFont(weight="bold"), text_color="#10b981").pack(pady=(10, 5), anchor="w")
                for emp in dep.staff:
                    item = ctk.CTkFrame(scroll, fg_color="#f3f4f6")
                    item.pack(fill="x", pady=2, padx=10)
                    ctk.CTkLabel(item, text=f"{emp.id} | {emp.name.title()}", font=ctk.CTkFont(size=13), text_color="black").pack(side="left", padx=10, pady=5)
                    ctk.CTkLabel(item, text=f"Role: {emp.position}", text_color="#4b5563").pack(side="right", padx=10)

    # ------------------ POPUPS (Inherit Light Mode) ------------------

    def add_dep_popup(self):
        dialog = ctk.CTkInputDialog(text="Enter Department Name:", title="New Department")
        name = dialog.get_input()
        if name:
            self.hospital.add_department(name)
            self.show_departments()
            messagebox.showinfo("Success", f"Department {name} created.")

    def add_patient_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Patient Registration")
        popup.geometry("400x450")
        popup.attributes('-topmost', True)

        ctk.CTkLabel(popup, text="Register New Patient", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        dep_names = [d.name for d in self.hospital.departments]
        dep_var = ctk.StringVar(value=dep_names[0])
        
        ctk.CTkOptionMenu(popup, variable=dep_var, values=dep_names, width=250).pack(pady=10)
        name_ent = ctk.CTkEntry(popup, placeholder_text="Full Name", width=250)
        name_ent.pack(pady=10)
        age_ent = ctk.CTkEntry(popup, placeholder_text="Age", width=250)
        age_ent.pack(pady=10)
        rec_ent = ctk.CTkEntry(popup, placeholder_text="Medical History / Record", width=250)
        rec_ent.pack(pady=10)

        def save():
            try:
                n, a, r = name_ent.get(), int(age_ent.get()), rec_ent.get()
                for d in self.hospital.departments:
                    if d.name == dep_var.get():
                        d.add_patient(n, a, r)
                        break
                self.show_patients()
                popup.destroy()
            except: messagebox.showerror("Error", "Check input fields")

        ctk.CTkButton(popup, text="Confirm Registration", command=save, fg_color="#1f538d").pack(pady=30)

    def add_staff_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Staff Recruitment")
        popup.geometry("400x450")
        popup.attributes('-topmost', True)

        ctk.CTkLabel(popup, text="Recruit New Staff", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        dep_names = [d.name for d in self.hospital.departments]
        dep_var = ctk.StringVar(value=dep_names[0])
        
        ctk.CTkOptionMenu(popup, variable=dep_var, values=dep_names, width=250).pack(pady=10)
        name_ent = ctk.CTkEntry(popup, placeholder_text="Full Name", width=250)
        name_ent.pack(pady=10)
        age_ent = ctk.CTkEntry(popup, placeholder_text="Age", width=250)
        age_ent.pack(pady=10)
        pos_ent = ctk.CTkEntry(popup, placeholder_text="Position (e.g. Surgeon)", width=250)
        pos_ent.pack(pady=10)

        def save():
            try:
                n, a, p = name_ent.get(), int(age_ent.get()), pos_ent.get()
                for d in self.hospital.departments:
                    if d.name == dep_var.get():
                        d.add_staff(n, a, p)
                        break
                self.show_staff()
                popup.destroy()
            except: messagebox.showerror("Error", "Check input fields")

        ctk.CTkButton(popup, text="Add to Staff List", command=save, fg_color="#2b9348").pack(pady=30)

    def save_data(self):
        save_hospital(self.hospital)
        messagebox.showinfo("Saved", "All hospital data has been synchronized to storage.")

if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()