import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle
import os

class ContactBook:
    def __init__(self, master):
        self.master = master
        self.master.title("Contact Book")
        
        self.contacts = self.load_contacts()  

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Name").grid(row=0, column=0)
        tk.Entry(self.master, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(self.master, text="Email").grid(row=1, column=0)
        tk.Entry(self.master, textvariable=self.email_var).grid(row=1, column=1)

        tk.Label(self.master, text="Phone Number").grid(row=2, column=0)
        tk.Entry(self.master, textvariable=self.phone_var).grid(row=2, column=1)

        tk.Button(self.master, text="Add Contact", command=self.add_contact).grid(row=3, column=0)
        tk.Button(self.master, text="View Contacts", command=self.view_contacts).grid(row=3, column=1)
        tk.Button(self.master, text="Search Contact", command=self.search_contact).grid(row=4, column=0)
        tk.Button(self.master, text="Update Contact", command=self.update_contact).grid(row=4, column=1)
        tk.Button(self.master, text="Delete Contact", command=self.delete_contact).grid(row=5, column=0)

    def load_contacts(self):
        if os.path.exists("contacts.pkl"):
            with open("contacts.pkl", "rb") as f:
                contacts = pickle.load(f)
                if isinstance(contacts, list): 
                    return contacts
        return []  

    def save_contacts(self):
        with open("contacts.pkl", "wb") as f:
            pickle.dump(self.contacts, f)

    def add_contact(self):
        name = self.name_var.get()
        email = self.email_var.get()
        phone = self.phone_var.get()
        
        if name and email and phone:
            self.contacts.append({'name': name, 'email': email, 'phone': phone})
            self.contacts.sort(key=lambda x: x['name'])  # Sort by name
            self.save_contacts()
            messagebox.showinfo("Success", "Contact added successfully!")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def view_contacts(self):
        contacts = "\n".join(f"{contact['name']}: {contact['email']}, {contact['phone']}" for contact in self.contacts)
        messagebox.showinfo("Contacts", contacts if contacts else "No contacts available.")

    def search_contact(self):
        name = simpledialog.askstring("Search", "Enter name to search:")
        for contact in self.contacts:
            if contact['name'] == name:
                messagebox.showinfo("Contact Found", f"Email: {contact['email']}\nPhone: {contact['phone']}")
                return
        messagebox.showerror("Not Found", "Contact not found.")

    def update_contact(self):
        name = simpledialog.askstring("Update", "Enter name to update:")
        for contact in self.contacts:
            if contact['name'] == name:
                email = simpledialog.askstring("Update Email", "Enter new email:", initialvalue=contact['email'])
                phone = simpledialog.askstring("Update Phone", "Enter new phone number:", initialvalue=contact['phone'])
                contact['email'] = email
                contact['phone'] = phone
                self.save_contacts()
                messagebox.showinfo("Success", "Contact updated successfully!")
                return
        messagebox.showerror("Not Found", "Contact not found.")

    def delete_contact(self):
        name = simpledialog.askstring("Delete", "Enter name to delete:")
        for contact in self.contacts:
            if contact['name'] == name:
                self.contacts.remove(contact)
                self.save_contacts()
                messagebox.showinfo("Success", "Contact deleted successfully!")
                return
        messagebox.showerror("Not Found", "Contact not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
