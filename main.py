import tkinter as tk
from tkinter import messagebox as msg
import ttkbootstrap as ttk
import sqlite3
import re
import csv
from fpdf import FPDF

# Values
from values import *

class DataEntryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("DATA ENTRY SYSTEM")
        self.master.iconbitmap("users.ico")
        
        # Center the window on the screen
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        width = 1200
        height = 800
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.master.geometry(f"{width}x{height}+{x}+{y}")
        self.master.resizable(False, False)

        self.create_widgets()
        self.create_database()

    def create_widgets(self):
        # Parent Frame
        frame = ttk.Frame(self.master)
        frame.pack()

        self.create_user_info_frame(frame)
        self.create_courses_frame(frame)
        self.create_terms_frame(frame)
        self.create_crud_frame(frame)

        # Submit Button
        submit_button = ttk.Button(frame, text="SUBMIT", command=self.submit)
        submit_button.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)

        # Quit Button
        quit_button = ttk.Button(frame, text="QUIT", command=self.quit)
        quit_button.grid(row=5, column=0, sticky="nsew", padx=20, pady=20)

    def create_user_info_frame(self, parent):
        # USER INFO FRAME
        user_info_frame = ttk.LabelFrame(parent, text="USER INFORMATION")
        user_info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # User Frame Widgets
        ttk.Label(user_info_frame, text="Title").grid(row=0, column=0)
        ttk.Label(user_info_frame, text="First Name").grid(row=0, column=1)
        ttk.Label(user_info_frame, text="Last Name").grid(row=0, column=2)
        
        
        self.title_combo = ttk.Combobox(user_info_frame, values=title_options)
        self.title_combo.grid(row=1, column=0)

        self.first_name_entry = ttk.Entry(user_info_frame)
        self.first_name_entry.grid(row=1, column=1)

        self.last_name_entry = ttk.Entry(user_info_frame)
        self.last_name_entry.grid(row=1, column=2)


        # Adding Email Widget
        ttk.Label(user_info_frame, text="Email").grid(row=2, column=0)
        ttk.Label(user_info_frame, text="Age").grid(row=2, column=1)
        ttk.Label(user_info_frame, text="Nationality").grid(row=2, column=2)


        
        self.email_entry = ttk.Entry(user_info_frame)
        self.email_entry.grid(row=3, column=0)


        self.age_spinbox = ttk.Spinbox(user_info_frame, from_=14, to=100)
        self.age_spinbox.grid(row=3, column=1)

        self.nationality_combo = ttk.Combobox(user_info_frame, values=nationality_options)
        self.nationality_combo.grid(row=3, column=2)

        for child in user_info_frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

    def create_courses_frame(self, parent):
        # COURSES FRAME
        courses_frame = ttk.LabelFrame(parent, text="COURSES")
        courses_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        ttk.Label(courses_frame, text="Registration Status").grid(row=0, column=0)
        ttk.Label(courses_frame, text="Course Taken").grid(row=0, column=1)
        ttk.Label(courses_frame, text="Modules Completed").grid(row=0, column=2)

        self.status_var = tk.StringVar(value="Not Registered")
        registration_checkbox = ttk.Checkbutton(courses_frame, text="Registered", onvalue="Registered", offvalue="Not Registered", variable=self.status_var)
        registration_checkbox.grid(row=1, column=0)

        self.course_taken = ttk.Combobox(courses_frame, values=course_options)
        self.course_taken.grid(row=1, column=1)

        self.number_spinbox = ttk.Spinbox(courses_frame, from_=0, to=6)
        self.number_spinbox.grid(row=1, column=2)

        for child in courses_frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

    def create_terms_frame(self, parent):
        # TERMS FRAME
        terms_frame = ttk.LabelFrame(parent, text="TERMS")
        terms_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        ttk.Label(terms_frame, text="Terms and Conditions").grid(row=0, column=0, columnspan=3)

        self.terms_var = tk.BooleanVar(value=False)
        terms_checkbox = ttk.Checkbutton(terms_frame, text="I agree to the terms and conditions", variable=self.terms_var, onvalue=True, offvalue=False)
        terms_checkbox.grid(row=1, column=0, columnspan=3)

        for child in terms_frame.winfo_children():
            child.grid_configure(padx=10, pady=5)
            
            
    def create_crud_frame(self, parent):
        # CRUD FRAME
        crud_frame = ttk.LabelFrame(parent, text="CRUD")
        crud_frame.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")

        read_button = ttk.Button(crud_frame, text="READ", command=self.read_data)
        read_button.grid(row=0, column=0, padx=5)

        update_button = ttk.Button(crud_frame, text="UPDATE", command=self.update_data)
        update_button.grid(row=0, column=1, padx=5)

        delete_button = ttk.Button(crud_frame, text="DELETE", command=self.delete_data)
        delete_button.grid(row=0, column=2, padx=5)

        for child in crud_frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

    def create_database(self):
        """Connect to the database and create the table if it does not exist."""
        self.conn = sqlite3.connect("data.db")
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    registration_status TEXT, 
                    title TEXT, 
                    first_name TEXT, 
                    last_name TEXT, 
                    email TEXT,
                    course_taken TEXT, 
                    modules_completed INTEGER, 
                    age INTEGER, 
                    nationality TEXT
                )
            """)

    def clear(self):
        """Clear all the data from the form."""
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.title_combo.set("")
        self.email_entry.delete(0, tk.END) 
        self.age_spinbox.delete(0, tk.END)
        self.nationality_combo.set("")
        self.status_var.set("Not Registered")
        self.course_taken.set("")
        self.number_spinbox.delete(0, tk.END)
        self.terms_var.set(False)
        
        
    def is_valid_email(self, email):
        """Validate the email format."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def submit(self):
        """Submit all the data from the form."""
        if not self.terms_var.get():
            msg.showwarning(title="Warning", message="Please accept terms and conditions")
            return

        first = self.first_name_entry.get().strip().title()
        last = self.last_name_entry.get().strip().title()
        email = self.email_entry.get().strip()

        if not first or not last or not email:
            msg.showwarning(title="Warning", message="Please fill in all fields.")
            return
        
        if not self.is_valid_email(email):
            msg.showwarning(title="Warning", message="Please enter a valid email address.")
            return

        try:
            title = self.title_combo.get().title()
            age = int(self.age_spinbox.get())
            nationality = self.nationality_combo.get().title()
            registration_status = self.status_var.get().title()
            course = self.course_taken.get().title()
            number = int(self.number_spinbox.get())

            if age < 18 or number < 0 or course == "":
                msg.showwarning(title="Warning", message="Please ensure all values are valid.")
                return

            with self.conn:
                self.conn.execute("INSERT INTO students (registration_status, title, first_name, last_name, email, course_taken, modules_completed, age, nationality) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                  (registration_status, title, first, last, email, course, number, age, nationality))
                
            msg.showinfo("Submission Successful", 
                f"Title: {title.upper()}\n"
                f"Name: {first.upper()} {last.upper()}\n"
                f"Email: {email}\n"
                f"Age: {age}\n"
                f"Nationality: {nationality.upper()}\n"
                f"Course: {course.upper()}\n"
                f"Modules Completed: {number}\n"
                f"Registration Status: {registration_status}\n"
                f"Data Saved Successfully in (data.db)"
            )
            self.clear()

        except ValueError:
            msg.showerror(title="Error", message="Please enter valid numeric values for age and modules completed.")

    def read_data(self):
        """Read and display all records from the database."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM students")
            records = cursor.fetchall()

        if not records:
            msg.showinfo("No Records", "No records found in the database.")
            return
        
        # Create a new window to display the data
        data_window = tk.Toplevel(self.master)
        data_window.title("Student Records")
        data_window.geometry("1905x800+0+150")
        data_window.configure(bg='#2e2e2e')
        data_window.resizable(False, True)

        # Create a treeview to display the data
        tree = ttk.Treeview(data_window, columns=("ID", "Status", "Title", "First Name", "Last Name", "Email", "Course", "Modules", "Age", "Nationality"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Set column headings
        for col in tree["columns"]:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=column_widths[col])

        # Insert data into the treeview
        for row in records:
            tree.insert("", tk.END, values=row)



        #create a frame for buttons
        button_frame = ttk.Frame(data_window)
        button_frame.pack(side="bottom", pady=10, padx=10)


        #csv download button
        csv_button = ttk.Button(button_frame, text="Download CSV", command=lambda: self.download_csv(records))
        csv_button.pack(side="left", padx=10, ipadx=5)
        
        
        #pdf download button
        pdf_button = ttk.Button(button_frame, text="Download PDF", command=lambda: self.download_pdf(records))
        pdf_button.pack(side="left", padx=10, ipadx=5)
            
            
        # Quit Button 2
        quit_button = ttk.Button(button_frame, text="QUIT", command=data_window.destroy)
        quit_button.pack(side="left", pady=10, ipadx=10)
    
    def update_data(self):
        """Update an existing record in the database."""
        email = self.email_entry.get().strip()
        if not email:
            msg.showwarning("Warning", "Please enter an email to update the record.")
            return

        # Check if the record exists
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM students WHERE email = ?", (email,))
            existing_record = cursor.fetchone()

        if not existing_record:
            msg.showwarning("Warning", "No record found with the given email.")
            return

        # Prepare the update query and parameters
        update_fields = []
        update_values = []

        # Check each field and add to update list if changed
        fields = {
            "title": self.title_combo.get().strip().title(),
            "first_name": self.first_name_entry.get().strip().title(),
            "last_name": self.last_name_entry.get().strip().title(),
            "age": self.age_spinbox.get().strip(),
            "nationality": self.nationality_combo.get().strip().title(),
            "registration_status": self.status_var.get().strip().title(),
            "course_taken": self.course_taken.get().strip().title(),
            "modules_completed": self.number_spinbox.get().strip()
        }

        for field, value in fields.items():
            if value: 
                if field in ["age", "modules_completed"]:
                    try:
                        value = int(value)
                    except ValueError:
                        msg.showerror("Error", f"Please enter a valid numeric value for {field}.")
                        return
                update_fields.append(f"{field} = ?")
                update_values.append(value)
          
        # If no fields to update
        if not update_fields:
            msg.showinfo("No Changes", "No fields were changed. Nothing to update.")
            return

        # query
        query = f"UPDATE students SET {', '.join(update_fields)} WHERE email = ?"
        update_values.append(email)

        # Execute the update
        try:
            with self.conn:
                self.conn.execute(query, tuple(update_values))
            msg.showinfo("Update Successful", "Record updated successfully.")
            self.clear()
        except sqlite3.Error as e:
            msg.showerror("Database Error", f"An error occurred: {e}")


    
    def delete_data(self):
        """Delete a record from the database."""
        email = self.email_entry.get().strip()
        if not email:
            msg.showwarning("Warning", "Please enter an email to delete the record.")
            return

        # Check if the record exists
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM students WHERE email = ?", (email,))
            existing_record = cursor.fetchone()

        if not existing_record:
            msg.showwarning("Warning", "No record found with the given email.")
            return

        # Confirm deletion
        if msg.askyesno("Confirm Deletion", "Are you sure you want to delete this record?"):
            with self.conn:
                self.conn.execute("DELETE FROM students WHERE email = ?", (email,))
            msg.showinfo("Deletion Successful", "Record deleted successfully.")
            self.clear()


    def download_csv(self, records):
        """Save the data in a CSV file"""
        file_path = "data.csv"
        with open(file_path, "w", encoding = "UTF-8", newline = "") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Status", "Title", "First Name", "Last Name", "Email", "Course", "Modules", "Age", "Nationality"])
            writer.writerows(records)
        
        msg.showinfo("Success", f"Data saved to {file_path}")


    def download_pdf(self, records):
        """Save the data in a PDF file"""
        file_path = "data.pdf"

        # pdf class
        class PDF(FPDF):

            def header(self):
                self.set_font("Arial", "B", 10)
                self.cell(0, 10, "STUDENTS DATA", 0, 1, "C")

            def footer(self):
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0,10, f"Page {self.page_no()}", 0, 0, "C")
        # PDF
        page_width = 290
        page_height = 350
        students_pdf = PDF("P", "mm", (page_width, page_height))
        students_pdf.add_page()

        # add headers
        students_pdf.set_font("Arial", "B", 8)
        headers= ["ID", "Status", "Title", "First Name", "Last Name", "Email", "Course", "Modules", "Age", "Nationality"]
        widths = [15, 25, 15, 25, 25, 50, 50, 20, 15, 30]
        for i, header in enumerate(headers):
            students_pdf.cell(widths[i], 10, header, 1)

        students_pdf.ln()

        #add data
        students_pdf.set_font("Arial", "", 8)
        for row in records:
            for i, item in enumerate(row):
                students_pdf.cell(widths[i], 10, str(item), 1)
            students_pdf.ln()


        students_pdf.output(file_path)

        msg.showinfo("Success", f"Data saved to {file_path}")
               
    
    def quit(self):
        """Close the application."""
        if msg.askyesno("Quit", "Are you sure you want to quit?"):
            self.master.destroy()
     

    def __del__(self):
        """Close the database connection when the object is destroyed."""
        if hasattr(self, 'conn'):
            self.conn.close()


# Run the application
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = DataEntryApp(root)
    root.mainloop()
