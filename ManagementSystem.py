from tkinter import *
from tkinter import ttk, messagebox
import pymysql


class ManagementSystem():
    def __init__(self, root):
        self.root = root
        self.root.title("Management System")
        self.root.geometry("1370x700+0+0")

        title = Label(self.root, text="Management System", bd=9, relief=GROOVE,
                      font=("Times New Roman", 50, "bold"), bg="#00FFCC", fg="black")
        title.pack(side=TOP, fill=X)

        self.nr_var = StringVar()
        self.first_name_var = StringVar()
        self.last_name_var = StringVar()
        self.email_var = StringVar()
        self.contact_var = StringVar()
        self.field_of_study_var = StringVar()
        self.address_var = StringVar()

        self.search_by = StringVar()
        self.search_txt = StringVar()

        Manage_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="#00FFCC")
        Manage_Frame.place(x=20, y=100, width=450, height=585)

        # Titlu:
        m_title = Label(Manage_Frame, text="Details", bg="#00FFCC", fg="black",
                        font=("Times New Roman", 40, "bold"))
        m_title.grid(row=0, columnspan=2, pady=20)

        # Etichete si campuri de intrare:
        labels_and_entries = [
            ("Nr:", self.nr_var),
            ("First Name:", self.first_name_var),
            ("Last Name:", self.last_name_var),
            ("Email:", self.email_var),
            ("Contact:", self.contact_var),
            ("College:", self.field_of_study_var)
        ]

        for row, (label_text, var) in enumerate(labels_and_entries, start=1):
            label = Label(Manage_Frame, text=label_text, bg="#00FFCC", fg="black", font=("Times New Roman", 20, "bold"))
            label.grid(row=row, column=0, pady=10, padx=20, sticky="w")

            entry = Entry(Manage_Frame, textvariable=var, font=("Times New Roman", 15, "bold"), bd=5, relief=GROOVE)
            entry.grid(row=row, column=1, pady=10, padx=20, sticky="w")

        # Adresă:
        address = Label(Manage_Frame, text="Address:", bg="#00FFCC", fg="black", font=("Times New Roman", 20, "bold"))
        address.grid(row=7, column=0, pady=10, padx=20, sticky="w")
        self.txt_address = Text(Manage_Frame, width=30, height=3, font=("Times New Roman", 10, "bold"),bd=5, relief=GROOVE)
        self.txt_address.grid(row=7, column=1, pady=10, padx=20, sticky="w")

        # Crearea butoanelor:

        btn_Frame = Frame(Manage_Frame, bd=3, bg="#00FFCC")
        btn_Frame.place(x=15, y=525, width=420)

        buttons = [
            ("Add", self.add_students),
            ("Update", self.update_data),
            ("Delete", self.delete_data),
            ("Clear", self.clear)
        ]

        for col, (button_text, command) in enumerate(buttons):
            Button(btn_Frame, text=button_text, width=10, command=command).grid(row=0, column=col, padx=10, pady=10)

        # Căutarea și afișarea datelor:
        Detials_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="#00FFCC")
        Detials_Frame.place(x=500, y=100, width=800, height=585)

        lbl_search = Label(Detials_Frame, text="Search By", bg="#00FFCC", fg="black", font=("Times New Roman", 20, "bold"))
        lbl_search.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        combo_search = ttk.Combobox(Detials_Frame, textvariable=self.search_by, width=10,
                                    font=("Times New Roman", 13, "bold"), state='readonly')
        combo_search['values'] = ("nr", "first_name", "last_name", "email", "contact")
        combo_search.grid(row=0, column=1, padx=20, pady=10)

        txt_search = Entry(Detials_Frame, textvariable=self.search_txt, width=20, font=("Times New Roman", 10, "bold"),
                           bd=5, relief=GROOVE)
        txt_search.grid(row=0, column=2, pady=10, padx=20, sticky="w")

        searchbtn = Button(Detials_Frame, text="Search", width=10, pady=5, command=self.search_data).grid(row=0,
                                                                                                          column=3,
                                                                                                          padx=10,
                                                                                                          pady=10)
        showallbtn = Button(Detials_Frame, text="Show All", width=10, pady=5, command=self.fetch_data).grid(row=0,
                                                                                                            column=4,
                                                                                                            padx=10,
                                                                                                            pady=10)

        # Crearea tabelei pentru studenți
        student_table_frame = Frame(Detials_Frame, bd=4, relief=RIDGE, bg="#f0f0f0")
        student_table_frame.place(x=10, y=70, width=760, height=500)

        # Barele de derulare orizontale și verticale
        scroll_x = Scrollbar(student_table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(student_table_frame, orient=VERTICAL)

        # Tabelul pentru studenți
        self.Student_table = ttk.Treeview(student_table_frame, column=("nr", "first_name", "last_name", "email", "contact", "field_of_study", "address"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        # Configurarea barelor de derulare
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)

        # Setarea antetelor coloanelor:
        self.Student_table.heading("nr", text="Nr")
        self.Student_table.heading("first_name", text="First Name")
        self.Student_table.heading("last_name", text="Last Name")
        self.Student_table.heading("email", text="Email")
        self.Student_table.heading("contact", text="Contact")
        self.Student_table.heading("field_of_study", text="College")
        self.Student_table.heading("address", text="Address")

        # Afișarea doar a antetelor coloanelor:
        self.Student_table['show'] = 'headings'

        # Setarea lățimii coloanelor:
        column_widths = {
            "nr": 20,
            "first_name": 80,
            "last_name": 80,
            "email": 120,
            "contact": 90,
            "field_of_study": 120,
            "address": 150
        }

        for col, width in column_widths.items():
            self.Student_table.column(col, width=width)

        # Plasarea tabelului:
        self.Student_table.pack(fill=BOTH, expand=1)
        self.Student_table.bind("<ButtonRelease-1>", self.get_cursor)

        # Încărcarea datelor în tabel:
        self.fetch_data()

    def add_students(self):
        if not self.nr_var.get() or not self.first_name_var.get():
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            con = pymysql.connect(host='localhost', user='root', password="***", database='managementsystem')
            cur = con.cursor()

            query = "INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (self.nr_var.get(), self.first_name_var.get(), self.last_name_var.get(),
                      self.email_var.get(), self.contact_var.get(), self.field_of_study_var.get(),
                      self.txt_address.get('1.0', END))

            cur.execute(query, values)
            con.commit()

            self.fetch_data()
            self.clear()
            con.close()

            messagebox.showinfo("Success", "Record has been inserted")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def fetch_data(self):
        try:
            with pymysql.connect(host='localhost', user='root', password="***", database='managementsystem') as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM students")
                rows = cur.fetchall()

                self.Student_table.delete(*self.Student_table.get_children())
                for row in rows:
                    self.Student_table.insert('', END, values=row)
                con.commit()
        except pymysql.Error as e:
            print(f"Error fetching data: {e}")

    def clear(self):
        self.nr_var.set("")
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.email_var.set("")
        self.contact_var.set("")
        self.field_of_study_var.set("")
        self.txt_address.delete("1.0", END)

    def get_cursor(self, ev):
        curosor_row = self.Student_table.focus()
        contents = self.Student_table.item(curosor_row)
        row = contents['values']
        self.nr_var.set(row[0])
        self.first_name_var.set(row[1])
        self.last_name_var.set(row[2])
        self.email_var.set(row[3])
        self.contact_var.set(row[4])
        self.field_of_study_var.set(row[5])
        self.txt_address.delete("1.0", END)
        self.txt_address.insert(END, row[6])

    def update_data(self):
        try:
            with pymysql.connect(host='localhost', user='root', password="***", database='managementsystem') as con:
                cur = con.cursor()
                query = "UPDATE students SET first_name=%s, last_name=%s, email=%s, contact=%s, field_of_study=%s, address=%s WHERE nr=%s"
                values = (
                    self.first_name_var.get(),
                    self.last_name_var.get(),
                    self.email_var.get(),
                    self.contact_var.get(),
                    self.field_of_study_var.get(),
                    self.txt_address.get('1.0', END),
                    self.nr_var.get()
                )
                cur.execute(query, values)
                con.commit()
                self.fetch_data()
                self.clear()
        except pymysql.Error as e:
            print(f"Error updating data: {e}")

    def delete_data(self):
        con = pymysql.connect(host='localhost', user='root', password="***", database='managementsystem')
        cur = con.cursor()
        cur.execute("delete from students where nr=%s", self.nr_var.get())
        con.commit()
        con.close()
        self.fetch_data()
        self.clear()

    def search_data(self):
        try:
            with pymysql.connect(host='localhost', user='root', password="***", database='managementsystem') as con:
                cur = con.cursor()
                query = f"SELECT * FROM students WHERE {self.search_by.get()} LIKE '%{self.search_txt.get()}%'"
                cur.execute(query)
                rows = cur.fetchall()

                self.Student_table.delete(*self.Student_table.get_children())
                for row in rows:
                    self.Student_table.insert('', END, values=row)
                con.commit()
        except pymysql.Error as e:
            print(f"Error searching data: {e}")


class ManagementSystem():
    pass

    root = Tk()
    ob = ManagementSystem(root)
    root.mainloop()
