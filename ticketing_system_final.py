import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import qrcode
from PIL import ImageTk, Image

# ---------------- DATABASE ----------------

conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
ticket_id INTEGER,
name TEXT
)
""")

TOTAL_TICKETS = 50


# ---------------- BASIC FUNCTIONS ----------------

def login():
    messagebox.showinfo("Login", "Login Successful")


def register():
    messagebox.showinfo("Register", "Registration Successful")


def view_tickets():

    cursor.execute("SELECT COUNT(*) FROM bookings")
    booked = cursor.fetchone()[0]

    available = TOTAL_TICKETS - booked

    messagebox.showinfo("Tickets", f"Available Tickets: {available}")


# ---------------- DIGITAL TICKET WINDOW ----------------

def show_ticket(ticket_id, name):

    data = f"Ticket ID: {ticket_id}\nPassenger: {name}"

    qr = qrcode.make(data)
    qr.save("ticket_qr.png")

    ticket = tk.Toplevel()
    ticket.title("Digital Ticket")
    ticket.geometry("350x420")
    ticket.configure(bg="white")

    tk.Label(
        ticket,
        text="AUTOMATED TICKETING SYSTEM",
        font=("Arial",16,"bold"),
        bg="#1f4e79",
        fg="white",
        pady=5
    ).pack(fill="x")

    frame = tk.Frame(ticket, bg="white")
    frame.pack(pady=20)

    tk.Label(frame, text="Passenger:", font=("Arial",12), bg="white").grid(row=0,column=0,sticky="w")
    tk.Label(frame, text=name, font=("Arial",12,"bold"), bg="white").grid(row=0,column=1)

    tk.Label(frame, text="Ticket ID:", font=("Arial",12), bg="white").grid(row=1,column=0,sticky="w")
    tk.Label(frame, text=ticket_id, font=("Arial",12,"bold"), bg="white").grid(row=1,column=1)

    tk.Label(frame, text="Status:", font=("Arial",12), bg="white").grid(row=2,column=0,sticky="w")
    tk.Label(frame, text="CONFIRMED", font=("Arial",12,"bold"), fg="green", bg="white").grid(row=2,column=1)

    img = Image.open("ticket_qr.png")
    img = img.resize((180,180))

    qr_img = ImageTk.PhotoImage(img)

    qr_label = tk.Label(ticket, image=qr_img, bg="white")
    qr_label.image = qr_img
    qr_label.pack(pady=10)


# ---------------- BOOK TICKET ----------------

def book_ticket():

    name = name_entry.get()

    if name == "":
        messagebox.showerror("Error", "Enter Passenger Name")
        return

    cursor.execute("SELECT COUNT(*) FROM bookings")
    booked = cursor.fetchone()[0]

    if booked >= TOTAL_TICKETS:
        messagebox.showerror("Error", "No Tickets Available")
        return

    ticket_id = random.randint(100000,999999)

    cursor.execute(
        "INSERT INTO bookings VALUES (?,?)",
        (ticket_id,name)
    )

    conn.commit()

    messagebox.showinfo("Success","Ticket Booked Successfully")

    show_ticket(ticket_id,name)


# ---------------- CANCEL TICKET ----------------

def cancel_ticket():

    ticket = cancel_entry.get()

    if ticket == "":
        messagebox.showerror("Error","Enter Ticket ID")
        return

    cursor.execute(
        "DELETE FROM bookings WHERE ticket_id=?",
        (ticket,)
    )

    conn.commit()

    messagebox.showinfo("Cancelled","Ticket Cancelled")


# ---------------- BOOKING HISTORY ----------------

def show_history():

    cursor.execute("SELECT * FROM bookings")

    records = cursor.fetchall()

    history = tk.Toplevel()
    history.title("Booking History")
    history.geometry("350x300")

    tk.Label(
        history,
        text="Booking History",
        font=("Arial",16,"bold")
    ).pack(pady=10)

    for record in records:

        tk.Label(
            history,
            text=f"Ticket ID: {record[0]} | Name: {record[1]}",
            font=("Arial",11)
        ).pack()


# ---------------- ADMIN DASHBOARD ----------------

def admin_dashboard():

    dashboard = tk.Toplevel()
    dashboard.title("Admin Dashboard")
    dashboard.geometry("350x250")
    dashboard.configure(bg="white")

    cursor.execute("SELECT COUNT(*) FROM bookings")
    booked = cursor.fetchone()[0]

    available = TOTAL_TICKETS - booked

    tk.Label(
        dashboard,
        text="ADMIN DASHBOARD",
        font=("Arial",16,"bold"),
        bg="#2f5597",
        fg="white",
        pady=5
    ).pack(fill="x")

    tk.Label(
        dashboard,
        text=f"Total Tickets : {TOTAL_TICKETS}",
        font=("Arial",12),
        bg="white"
    ).pack(pady=10)

    tk.Label(
        dashboard,
        text=f"Booked Tickets : {booked}",
        font=("Arial",12),
        bg="white"
    ).pack()

    tk.Label(
        dashboard,
        text=f"Available Tickets : {available}",
        font=("Arial",12),
        bg="white"
    ).pack()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Automated Ticketing System")
root.geometry("750x500")
root.configure(bg="white")


title = tk.Label(
    root,
    text="AUTOMATED TICKETING SYSTEM",
    font=("Arial",20,"bold"),
    bg="#1f4e79",
    fg="white",
    pady=10
)

title.pack(fill="x")


# ---------------- MENU ----------------

menu = tk.Frame(root,bg="#2f5597",width=200)
menu.pack(side="left",fill="y")

content = tk.Frame(root,bg="white")
content.pack(side="right",expand=True,fill="both",padx=20,pady=20)


# ---------------- INPUTS ----------------

tk.Label(content,text="Passenger Name:",font=("Arial",12),bg="white").pack(pady=5)
name_entry = tk.Entry(content,width=30)
name_entry.pack()

tk.Label(content,text="Ticket ID to Cancel:",font=("Arial",12),bg="white").pack(pady=5)
cancel_entry = tk.Entry(content,width=30)
cancel_entry.pack()


# ---------------- MENU BUTTON FUNCTION ----------------

def menu_button(text,command):

    return tk.Button(
        menu,
        text=text,
        command=command,
        width=20,
        bg="#4f81bd",
        fg="white",
        font=("Arial",11),
        pady=8
    )


menu_button("Login",login).pack(pady=5)
menu_button("Register",register).pack(pady=5)
menu_button("View Tickets",view_tickets).pack(pady=5)
menu_button("Book Ticket",book_ticket).pack(pady=5)
menu_button("Cancel Ticket",cancel_ticket).pack(pady=5)
menu_button("Booking History",show_history).pack(pady=5)
menu_button("Admin Dashboard",admin_dashboard).pack(pady=5)
menu_button("Exit",root.quit).pack(pady=20)


root.mainloop()