import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import hashlib
import csv
from datetime import datetime

# ---------------------------------------------------------
# CAMPUS COMPLAINT MANAGEMENT SYSTEM
# Built with Python Tkinter only - no extra installation.
# Demo admin login: 400 | Password: asdf
# ---------------------------------------------------------

ADMIN_ID = "400"
ADMIN_PASSWORD = "asdf"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(BASE_DIR, "students.json")
COMPLAINTS_FILE = os.path.join(BASE_DIR, "complaints.json")

NAVY = "#142B4A"
BLUE = "#2463A6"
LIGHT_BLUE = "#EAF2FB"
TEAL = "#0F9D8A"
GREEN = "#218838"
ORANGE = "#D97706"
RED = "#C0392B"
BG = "#F3F6FA"
WHITE = "#FFFFFF"
TEXT = "#1E293B"
MUTED = "#64748B"
BORDER = "#DCE4EE"


def load_data(filename, default):
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def save_data(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except OSError as error:
        messagebox.showerror("Save error", f"Could not save data:\n{error}")


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class CampusComplaintSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("CampusCare | Campus Complaint Management System")
        self.root.configure(bg=BG)
        self.root.minsize(950, 650)

        # Open a large, presentation-friendly window on Windows/IDLE.
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.geometry("1200x760")

        self.students = load_data(STUDENTS_FILE, {})
        self.complaints = load_data(COMPLAINTS_FILE, [])
        self.current_student = None
        self.setup_styles()
        self.show_role_screen()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Treeview", background=WHITE, foreground=TEXT,
                        fieldbackground=WHITE, rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=NAVY, foreground=WHITE,
                        font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Treeview", background=[("selected", "#CFE3FA")],
                  foreground=[("selected", TEXT)])
        style.configure("TCombobox", padding=6, font=("Segoe UI", 10))
        style.configure("TEntry", padding=7, font=("Segoe UI", 10))

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_button(self, parent, text, command, color=BLUE, width=None):
        button = tk.Button(
            parent, text=text, command=command,
            bg=color, fg=WHITE, activebackground=NAVY, activeforeground=WHITE,
            font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
            padx=16, pady=9, cursor="hand2"
        )
        if width:
            button.configure(width=width)
        return button

    def heading(self, parent, title, subtitle=""):
        tk.Label(parent, text=title, bg=parent.cget("bg"), fg=NAVY,
                 font=("Segoe UI", 25, "bold")).pack(pady=(8, 5))
        if subtitle:
            tk.Label(parent, text=subtitle, bg=parent.cget("bg"), fg=MUTED,
                     font=("Segoe UI", 11)).pack(pady=(0, 16))

    def top_banner(self, title, subtitle, show_home=True):
        banner = tk.Frame(self.root, bg=NAVY, padx=26, pady=17)
        banner.pack(fill="x")
        left = tk.Frame(banner, bg=NAVY)
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text="CAMPUSCARE", bg=NAVY, fg="#70D6C5",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(left, text=title, bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(2, 1))
        tk.Label(left, text=subtitle, bg=NAVY, fg="#D7E3F2",
                 font=("Segoe UI", 10)).pack(anchor="w")
        if show_home:
            self.make_button(banner, "Logout / Home", self.logout, "#38516F").pack(side="right", padx=(12, 0))
        return banner

    def logout(self):
        self.current_student = None
        self.show_role_screen()

    def show_role_screen(self):
        self.clear_screen()
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True)

        hero = tk.Frame(outer, bg=NAVY, height=250)
        hero.pack(fill="x")
        hero.pack_propagate(False)
        tk.Label(hero, text="CAMPUSCARE", bg=NAVY, fg="#70D6C5",
                 font=("Segoe UI", 13, "bold")).pack(pady=(35, 8))
        tk.Label(hero, text="Campus Complaint Management System", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 28, "bold")).pack(pady=4)
        tk.Label(hero, text="A smarter way to report, manage and resolve campus issues",
                 bg=NAVY, fg="#D7E3F2", font=("Segoe UI", 12)).pack(pady=7)

        content = tk.Frame(outer, bg=BG)
        content.pack(expand=True, fill="both", padx=20, pady=20)
        tk.Label(content, text="WELCOME", bg=BG, fg=BLUE,
                 font=("Segoe UI", 11, "bold")).pack(pady=(4, 3))
        tk.Label(content, text="Choose how you want to continue", bg=BG, fg=NAVY,
                 font=("Segoe UI", 18, "bold")).pack(pady=(0, 16))

        cards = tk.Frame(content, bg=BG)
        cards.pack()
        student_card = tk.Frame(cards, bg=WHITE, highlightbackground=BORDER,
                                highlightthickness=1, padx=28, pady=22)
        student_card.grid(row=0, column=0, padx=12, sticky="n")
        tk.Label(student_card, text="🎓", bg=WHITE, fg=BLUE,
                 font=("Segoe UI Emoji", 30)).pack()
        tk.Label(student_card, text="STUDENT PORTAL", bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 14, "bold")).pack(pady=(8, 5))
        tk.Label(student_card, text="Submit a complaint and track its status.",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 10), wraplength=260).pack(pady=(0, 14))
        self.make_button(student_card, "Continue as Student", self.show_student_login, BLUE, 23).pack()

        admin_card = tk.Frame(cards, bg=WHITE, highlightbackground=BORDER,
                              highlightthickness=1, padx=28, pady=22)
        admin_card.grid(row=0, column=1, padx=12, sticky="n")
        tk.Label(admin_card, text="🛡", bg=WHITE, fg=TEAL,
                 font=("Segoe UI Emoji", 30)).pack()
        tk.Label(admin_card, text="ADMIN PORTAL", bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 14, "bold")).pack(pady=(8, 5))
        tk.Label(admin_card, text="Review complaints and update their progress.",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 10), wraplength=260).pack(pady=(0, 14))
        self.make_button(admin_card, "Continue as Admin", self.show_admin_login, TEAL, 23).pack()

        tk.Label(content, text="Simple • Organized • Transparent • Student-focused",
                 bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(pady=22)
        tk.Label(outer, text="CampusCare Demo  |  Data is stored locally on this computer",
                 bg="#E7EDF5", fg=MUTED, font=("Segoe UI", 9), pady=8).pack(fill="x", side="bottom")

    def login_panel(self, title, subtitle, fields, submit_command, back_command):
        self.clear_screen()
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)
        self.top_banner(title, subtitle, show_home=False)

        card = tk.Frame(body, bg=WHITE, padx=38, pady=30,
                        highlightbackground=BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.48, anchor="center")
        tk.Label(card, text=title, bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 21, "bold")).pack(pady=(0, 5))
        tk.Label(card, text=subtitle, bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 10)).pack(pady=(0, 20))

        entries = {}
        for label, secret in fields:
            tk.Label(card, text=label, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(7, 4))
            entry = ttk.Entry(card, width=38, show="*" if secret else "")
            entry.pack(fill="x", ipady=3)
            entries[label] = entry

        def submit():
            submit_command(entries)

        self.make_button(card, "Login", submit, BLUE).pack(fill="x", pady=(20, 8))
        self.make_button(card, "Back to Home", back_command, "#64748B").pack(fill="x")
        for entry in entries.values():
            entry.bind("<Return>", lambda event: submit())
        if entries:
            next(iter(entries.values())).focus_set()
        return entries

    def show_student_login(self):
        def login(entries):
            sid = entries["Student ID"].get().strip()
            pwd = entries["Password"].get()
            if not sid or not pwd:
                messagebox.showerror("Missing details", "Enter your student ID and password.")
                return
            student = self.students.get(sid)
            if not student or student.get("password") != hash_password(pwd):
                messagebox.showerror("Login failed", "Incorrect student ID or password.")
                return
            self.current_student = sid
            self.show_student_dashboard()

        # Add a registration option below the login panel.
        entries = self.login_panel("Student Login", "Sign in to submit and track campus complaints.",
                                   [("Student ID", False), ("Password", True)], login, self.show_role_screen)
        card = entries["Student ID"].master
        self.make_button(card, "Create a Student Account", self.show_student_register, TEAL).pack(fill="x", pady=(8, 0))

    def show_student_register(self):
        self.clear_screen()
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)
        self.top_banner("Student Registration", "Create an account to access CampusCare", show_home=False)
        card = tk.Frame(body, bg=WHITE, padx=35, pady=25,
                        highlightbackground=BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(card, text="Create Student Account", bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 20, "bold")).pack(pady=(0, 15))

        fields = {}
        for label, secret in [("Student ID", False), ("Full Name", False),
                              ("Password", True), ("Confirm Password", True)]:
            tk.Label(card, text=label, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(6, 3))
            entry = ttk.Entry(card, width=40, show="*" if secret else "")
            entry.pack(fill="x", ipady=3)
            fields[label] = entry

        def register():
            sid = fields["Student ID"].get().strip()
            name = fields["Full Name"].get().strip()
            pwd = fields["Password"].get()
            confirm = fields["Confirm Password"].get()
            if not all([sid, name, pwd, confirm]):
                messagebox.showerror("Missing details", "Please fill in all fields.")
                return
            if sid.lower() == ADMIN_ID.lower():
                messagebox.showerror("Invalid ID", "This ID is reserved for the admin.")
                return
            if sid in self.students:
                messagebox.showerror("Account exists", "This student ID is already registered.")
                return
            if len(pwd) < 4:
                messagebox.showerror("Password too short", "Use at least 4 characters.")
                return
            if pwd != confirm:
                messagebox.showerror("Password mismatch", "The passwords do not match.")
                return
            self.students[sid] = {"name": name, "password": hash_password(pwd)}
            save_data(STUDENTS_FILE, self.students)
            messagebox.showinfo("Registration successful", "Your account has been created. Please log in.")
            self.show_student_login()

        self.make_button(card, "Register", register, TEAL).pack(fill="x", pady=(18, 8))
        self.make_button(card, "Back to Student Login", self.show_student_login, "#64748B").pack(fill="x")

    def create_tree(self, parent, columns, headings, widths):
        wrap = tk.Frame(parent, bg=WHITE)
        wrap.pack(fill="both", expand=True)
        tree = ttk.Treeview(wrap, columns=columns, show="headings", selectmode="browse")
        yscroll = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        xscroll = ttk.Scrollbar(wrap, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, width=widths[col], minwidth=70, anchor="w")
        tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)
        tree.tag_configure("Pending", foreground=ORANGE)
        tree.tag_configure("In Progress", foreground=BLUE)
        tree.tag_configure("Resolved", foreground=GREEN)
        return tree

    def stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=WHITE, padx=18, pady=12,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=5)
        tk.Label(card, text=title.upper(), bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        label = tk.Label(card, text=str(value), bg=WHITE, fg=color,
                         font=("Segoe UI", 23, "bold"))
        label.pack(anchor="w", pady=(4, 0))
        return label

    def show_student_dashboard(self):
        self.clear_screen()
        student = self.students.get(self.current_student, {})
        name = student.get("name", self.current_student)
        self.top_banner(f"Welcome, {name}", "Student portal  |  Submit a new issue or follow your existing complaints")

        body = tk.Frame(self.root, bg=BG, padx=18, pady=14)
        body.pack(fill="both", expand=True)

        form = tk.LabelFrame(body, text="  SUBMIT A COMPLAINT  ", bg=WHITE, fg=NAVY,
                             font=("Segoe UI", 11, "bold"), padx=14, pady=12,
                             highlightbackground=BORDER, highlightthickness=1)
        form.pack(fill="x", pady=(0, 12))

        tk.Label(form, text="Category", bg=WHITE, fg=TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        category = ttk.Combobox(form, values=[
            "Classroom", "Hostel", "Library", "Canteen", "Cleanliness",
            "Water Supply", "Electricity", "Wi-Fi / Internet", "Transport", "Washroom", "Other"
        ], state="readonly", width=25)
        category.set("Classroom")
        category.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(form, text="Subject", bg=WHITE, fg=TEXT, font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        subject = ttk.Entry(form)
        subject.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        tk.Label(form, text="Problem Location / Address * (Required)", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        address = ttk.Entry(form)
        address.insert(0, "e.g. Block A, Room 204")
        address.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        address.bind("<FocusIn>", lambda event: address.delete(0, "end")
                     if address.get() == "e.g. Block A, Room 204" else None)

        tk.Label(form, text="Description", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        description = tk.Text(form, height=3, wrap="word", font=("Segoe UI", 10),
                              bg="#FBFDFF", fg=TEXT, relief="solid", bd=1,
                              highlightthickness=1, highlightbackground=BORDER)
        description.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=2)

        def submit_complaint():
            cat = category.get().strip()
            sub = subject.get().strip()
            loc = address.get().strip()
            desc = description.get("1.0", "end").strip()
            if loc == "e.g. Block A, Room 204":
                loc = ""
            if not cat or not sub or not loc or not desc:
                messagebox.showwarning(
                    "Missing details",
                    "Problem location/address is compulsory. Please also enter the subject and description."
                )
                return
            complaint_id = max([c.get("id", 0) for c in self.complaints], default=0) + 1
            self.complaints.append({
                "id": complaint_id,
                "student": self.current_student,
                "student_name": name,
                "category": cat,
                "subject": sub,
                "address": loc,
                "description": desc,
                "status": "Pending",
                "created_at": datetime.now().strftime("%d-%m-%Y %I:%M %p")
            })
            save_data(COMPLAINTS_FILE, self.complaints)
            subject.delete(0, "end")
            address.delete(0, "end")
            description.delete("1.0", "end")
            refresh_complaints()
            messagebox.showinfo("Complaint submitted", f"Complaint submitted successfully!\nYour complaint ID is CC-{complaint_id:04d}.")

        self.make_button(form, "＋ Submit Complaint", submit_complaint, TEAL).grid(row=2, column=3, sticky="e", padx=5, pady=(8, 0))

        list_frame = tk.LabelFrame(body, text="  MY COMPLAINT HISTORY  ", bg=WHITE, fg=NAVY,
                                   font=("Segoe UI", 11, "bold"), padx=10, pady=10)
        list_frame.pack(fill="both", expand=True)
        columns = ("id", "category", "subject", "status", "date")
        tree = self.create_tree(list_frame, columns,
                                {"id": "Complaint ID", "category": "Category", "subject": "Subject",
                                 "status": "Current Status", "date": "Submitted On"},
                                {"id": 105, "category": 150, "subject": 350, "status": 145, "date": 180})

        def refresh_complaints():
            for item in tree.get_children():
                tree.delete(item)
            for complaint in self.complaints:
                if complaint.get("student") == self.current_student:
                    cid = complaint.get("id", "")
                    tree.insert("", "end", iid=str(cid), values=(
                        f"CC-{cid:04d}" if isinstance(cid, int) else cid,
                        complaint.get("category", ""),
                        complaint.get("subject", ""),
                        complaint.get("status", "Pending"),
                        complaint.get("created_at", "")
                    ), tags=(complaint.get("status", "Pending"),))

        def view_my_details(event=None):
            selected = tree.selection()
            if not selected:
                return
            cid = selected[0]
            for complaint in self.complaints:
                if str(complaint.get("id")) == cid and complaint.get("student") == self.current_student:
                    self.show_complaint_details(complaint)
                    break

        tree.bind("<Double-1>", view_my_details)
        tk.Label(body, text="Tip: Double-click a complaint to view its full details.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(6, 0))
        refresh_complaints()

    def show_admin_login(self):
        """Display the administrator login screen."""
        def login(entries):
            admin_id = entries["Admin ID"].get().strip()
            password = entries["Password"].get()
            if admin_id == ADMIN_ID and password == ADMIN_PASSWORD:
                self.show_admin_dashboard()
            else:
                messagebox.showerror("Login failed", "Incorrect admin ID or password.")

        self.login_panel(
            "Admin Login",
            "Authorized administrator access to CampusCare.",
            [("Admin ID", False), ("Password", True)],
            login,
            self.show_role_screen
        )

    def show_admin_dashboard(self):
        self.clear_screen()
        self.top_banner("Administrator Dashboard", "Monitor, review and manage all campus complaints")

        body = tk.Frame(self.root, bg=BG, padx=16, pady=12)
        body.pack(fill="both", expand=True)

        stats = tk.Frame(body, bg=BG)
        stats.pack(fill="x", pady=(0, 12))
        total_label = self.stat_card(stats, "Total Complaints", 0, NAVY)
        pending_label = self.stat_card(stats, "Pending", 0, ORANGE)
        progress_label = self.stat_card(stats, "In Progress", 0, BLUE)
        resolved_label = self.stat_card(stats, "Resolved", 0, GREEN)

        panel = tk.LabelFrame(body, text="  COMPLAINT REGISTER  ", bg=WHITE, fg=NAVY,
                              font=("Segoe UI", 11, "bold"), padx=10, pady=10)
        panel.pack(fill="both", expand=True)

        filterbar = tk.Frame(panel, bg=WHITE)
        filterbar.pack(fill="x", pady=(0, 9))
        tk.Label(filterbar, text="Search:", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 6))
        search_var = tk.StringVar()
        search_entry = ttk.Entry(filterbar, textvariable=search_var, width=28)
        search_entry.pack(side="left", padx=(0, 12))
        tk.Label(filterbar, text="Status:", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 6))
        status_filter = ttk.Combobox(filterbar, values=["All", "Pending", "In Progress", "Resolved"],
                                     state="readonly", width=15)
        status_filter.set("All")
        status_filter.pack(side="left", padx=(0, 12))

        columns = ("id", "student", "name", "category", "subject", "address", "status", "date")
        tree = self.create_tree(panel, columns,
                                {"id": "ID", "student": "Student ID", "name": "Student Name",
                                 "category": "Category", "subject": "Subject", "address": "Problem Location / Address",
                                 "status": "Status", "date": "Submitted On"},
                                {"id": 85, "student": 115, "name": 155, "category": 135,
                                 "subject": 220, "address": 220, "status": 125, "date": 165})

        def refresh_complaints():
            for item in tree.get_children():
                tree.delete(item)
            query = search_var.get().strip().lower()
            chosen_status = status_filter.get()
            for complaint in self.complaints:
                status = complaint.get("status", "Pending")
                searchable = " ".join(str(complaint.get(k, "")) for k in
                                       ("id", "student", "student_name", "category", "subject", "address", "description")).lower()
                if query and query not in searchable:
                    continue
                if chosen_status != "All" and status != chosen_status:
                    continue
                cid = complaint.get("id", "")
                tree.insert("", "end", iid=str(cid), values=(
                    f"CC-{cid:04d}" if isinstance(cid, int) else cid,
                    complaint.get("student", ""),
                    complaint.get("student_name", ""),
                    complaint.get("category", ""),
                    complaint.get("subject", ""),
                    complaint.get("address", "Not provided (older complaint)"),
                    status,
                    complaint.get("created_at", "")
                ), tags=(status,))

            total = len(self.complaints)
            pending = sum(1 for c in self.complaints if c.get("status", "Pending") == "Pending")
            progress = sum(1 for c in self.complaints if c.get("status") == "In Progress")
            resolved = sum(1 for c in self.complaints if c.get("status") == "Resolved")
            total_label.config(text=str(total))
            pending_label.config(text=str(pending))
            progress_label.config(text=str(progress))
            resolved_label.config(text=str(resolved))

        def selected_complaint():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select complaint", "Please select a complaint from the table first.")
                return None
            for complaint in self.complaints:
                if str(complaint.get("id")) == selected[0]:
                    return complaint
            return None

        def update_status():
            complaint = selected_complaint()
            if complaint is None:
                return
            new_status = status_choice.get()
            if not new_status:
                messagebox.showwarning("Choose status", "Please choose a status.")
                return
            complaint["status"] = new_status
            complaint["updated_at"] = datetime.now().strftime("%d-%m-%Y %I:%M %p")
            save_data(COMPLAINTS_FILE, self.complaints)
            refresh_complaints()
            messagebox.showinfo("Status updated",
                                f"Complaint CC-{complaint.get('id', 0):04d} is now '{new_status}'.")

        def view_details(event=None):
            complaint = selected_complaint()
            if complaint is not None:
                self.show_complaint_details(complaint)

        def export_csv():
            if not self.complaints:
                messagebox.showinfo("No data", "There are no complaints to export yet.")
                return
            filename = filedialog.asksaveasfilename(
                title="Export complaint register",
                defaultextension=".csv",
                filetypes=[("CSV file", "*.csv")],
                initialfile="campus_complaints_report.csv"
            )
            if not filename:
                return
            fields = ["id", "student", "student_name", "category", "subject", "address",
                      "description", "status", "created_at", "updated_at"]
            try:
                with open(filename, "w", newline="", encoding="utf-8-sig") as file:
                    writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
                    writer.writeheader()
                    for complaint in self.complaints:
                        writer.writerow(complaint)
                messagebox.showinfo("Export complete", f"Report saved successfully:\n{filename}")
            except OSError as error:
                messagebox.showerror("Export failed", f"Could not export report:\n{error}")

        controls = tk.Frame(body, bg=BG, pady=10)
        controls.pack(fill="x")
        tk.Label(controls, text="Set selected complaint to:", bg=BG, fg=TEXT,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
        status_choice = ttk.Combobox(controls, values=["Pending", "In Progress", "Resolved"],
                                     state="readonly", width=15)
        status_choice.set("In Progress")
        status_choice.pack(side="left")
        self.make_button(controls, "Update Status", update_status, TEAL).pack(side="left", padx=8)
        self.make_button(controls, "View Full Details", view_details, BLUE).pack(side="left", padx=4)
        self.make_button(controls, "Export CSV Report", export_csv, "#6D4AA2").pack(side="left", padx=4)
        self.make_button(controls, "Refresh", refresh_complaints, "#64748B").pack(side="right")

        search_var.trace_add("write", lambda *_: refresh_complaints())
        status_filter.bind("<<ComboboxSelected>>", lambda event: refresh_complaints())
        tree.bind("<Double-1>", view_details)
        refresh_complaints()

    def show_complaint_details(self, complaint):
        popup = tk.Toplevel(self.root)
        cid = complaint.get("id", "")
        popup.title(f"Complaint CC-{cid:04d} | Details" if isinstance(cid, int) else "Complaint Details")
        popup.configure(bg=WHITE)
        popup.geometry("620x500")
        popup.transient(self.root)
        popup.grab_set()

        header = tk.Frame(popup, bg=NAVY, padx=20, pady=15)
        header.pack(fill="x")
        tk.Label(header, text=f"COMPLAINT CC-{cid:04d}" if isinstance(cid, int) else "COMPLAINT DETAILS",
                 bg=NAVY, fg=WHITE, font=("Segoe UI", 17, "bold")).pack(anchor="w")
        tk.Label(header, text=f"Status: {complaint.get('status', 'Pending')}",
                 bg=NAVY, fg="#70D6C5", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(4, 0))

        content = tk.Frame(popup, bg=WHITE, padx=22, pady=18)
        content.pack(fill="both", expand=True)
        details = [
            ("Student", f"{complaint.get('student_name', '')} ({complaint.get('student', '')})"),
            ("Category", complaint.get("category", "")),
            ("Subject", complaint.get("subject", "")),
            ("Problem Location / Address", complaint.get("address", "Not provided (older complaint)")),
            ("Submitted", complaint.get("created_at", "")),
            ("Last Updated", complaint.get("updated_at", "Not updated yet")),
        ]
        for label, value in details:
            line = tk.Frame(content, bg=WHITE)
            line.pack(fill="x", pady=4)
            tk.Label(line, text=label + ":", width=14, anchor="w", bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(line, text=value, anchor="w", justify="left", wraplength=420,
                     bg=WHITE, fg=TEXT, font=("Segoe UI", 10)).pack(side="left", fill="x", expand=True)

        tk.Label(content, text="DESCRIPTION", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(12, 5))
        description = tk.Text(content, height=5, wrap="word", font=("Segoe UI", 10),
                              bg=LIGHT_BLUE, fg=TEXT, relief="flat", padx=10, pady=8)
        description.pack(fill="both", expand=True)
        description.insert("1.0", complaint.get("description", ""))
        description.configure(state="disabled")
        self.make_button(content, "Close", popup.destroy, BLUE).pack(anchor="e", pady=(12, 0))


if __name__ == "__main__":
    root = tk.Tk()
    app = CampusComplaintSystem(root)
    root.mainloop()