import streamlit as st
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
import shutil

class DataCleanserApp:

    def __init__(self, window):
        self.window = window
        self.window.geometry("500x500")
        self.window.title("Data Cleansing")
        self.window.config(background="white")

        self.AcademyUserData = None
        self.ExpiredUserIDs = None
        self.ExpiredUserEmailAddresses = None
        self.data_deleted = False

        self.create_widgets()

    def create_widgets(self):
        # Upload Academy User Data
        self.upload_AcademyUserData_button = tk.Button(self.window, text="Upload Academy User Data", command=self.uploadAcademyUserData)
        self.upload_AcademyUserData_button.pack()
        self.academy_user_data_status = tk.Label(self.window, text="")
        self.academy_user_data_status.pack()

        # Upload Expired User IDs and Email Addresses
        self.upload_ExpiredUserIDs_button = tk.Button(self.window, text="Upload Expired User IDs", state=tk.DISABLED, command=self.uploadExpiredUserIDs)
        self.upload_ExpiredUserIDs_button.pack()
        self.expired_user_ids_status = tk.Label(self.window, text="")
        self.expired_user_ids_status.pack()

        self.upload_ExpiredEmails_button = tk.Button(self.window, text="Upload Expired User Email Addresses", state=tk.DISABLED, command=self.uploadExpiredUserEmailAddresses)
        self.upload_ExpiredEmails_button.pack()
        self.expired_user_emails_status = tk.Label(self.window, text="")
        self.expired_user_emails_status.pack()

        # Delete Expired User Data
        self.delete_expiredIDs_button = tk.Button(self.window, text="Delete Expired User IDs", state=tk.DISABLED, command=self.deleteExpiredUserIDs)
        self.delete_expiredIDs_button.pack()
        self.delete_expired_ids_status = tk.Label(self.window, text="")
        self.delete_expired_ids_status.pack()

        self.delete_expiredEmails_button = tk.Button(self.window, text="Delete Expired User Email Addresses", state=tk.DISABLED, command=self.deleteExpiredUserEmailAddresses)
        self.delete_expiredEmails_button.pack()
        self.delete_expired_emails_status = tk.Label(self.window, text="")
        self.delete_expired_emails_status.pack()

        # Export Cleansed Data
        self.export_button = tk.Button(self.window, text="Export Cleansed Academy User Data", state=tk.DISABLED, command=self.exportCleansedAcademyUserData)
        self.export_button.pack()
        self.export_status = tk.Label(self.window, text="")
        self.export_status.pack()

        # Exit Program
        self.exit_button = tk.Button(self.window, text="Exit Program", command=self.exitProgram)
        self.exit_button.pack()

    def uploadAcademyUserData(self):
        self.AcademyUserData = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("CSV Files", "*.csv*"), ("all files", "*.*")))
        if self.AcademyUserData:
            self.upload_ExpiredUserIDs_button.config(state=tk.NORMAL)
            self.upload_ExpiredEmails_button.config(state=tk.NORMAL)
            self.academy_user_data_status.config(text="Academy User Data Uploaded")
        else:
            self.academy_user_data_status.config(text="Please Upload a File")

    def uploadExpiredUserIDs(self):
        self.ExpiredUserIDs = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("CSV Files", "*.csv*"), ("all files", "*.*")))
        if self.ExpiredUserIDs:
            self.delete_expiredIDs_button.config(state=tk.NORMAL)
            self.expired_user_ids_status.config(text="Expired User IDs Uploaded")
        else:
            self.expired_user_ids_status.config(text="Please Upload a File")

    def uploadExpiredUserEmailAddresses(self):
        self.ExpiredUserEmailAddresses = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("CSV Files", "*.csv*"), ("all files", "*.*")))
        if self.ExpiredUserEmailAddresses:
            self.delete_expiredEmails_button.config(state=tk.NORMAL)
            self.expired_user_emails_status.config(text="Expired User Email Addresses Uploaded")
        else:
            self.expired_user_emails_status.config(text="Please Upload a File")

    def deleteExpiredUserIDs(self):
        self.AcademyUserData = self.deleteExpiredUsers(self.AcademyUserData, self.ExpiredUserIDs, 'User ID')
        self.data_deleted = True
        self.check_export_status()
        self.delete_expired_ids_status.config(text="Expired User IDs Deleted")

    def deleteExpiredUserEmailAddresses(self):
        self.AcademyUserData = self.deleteExpiredUsers(self.AcademyUserData, self.ExpiredUserEmailAddresses, 'Email Address')
        self.data_deleted = True
        self.check_export_status()
        self.delete_expired_emails_status.config(text="Expired User Email Addresses Deleted")

    def deleteExpiredUsers(self, user_data_file, expired_users_file, column_name):
        with open(user_data_file, "r") as f:
            reader = csv.reader(f)
            user_data = list(reader)
            id_index = user_data[0].index(column_name)

        with open(expired_users_file, "r") as f:
            reader = csv.reader(f)
            expired_users = list(reader)
            expired_id_index = expired_users[0].index(column_name)

        user_data = [row for row in user_data if row[id_index] not in [expired_row[expired_id_index] for expired_row in expired_users]]
        
        with open(user_data_file, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(user_data)
        
        return user_data_file

    def exportCleansedAcademyUserData(self):
        shutil.copy(self.AcademyUserData, "CleansedAcademyUserData.csv")
        self.export_status.config(text="Cleansed Academy User Data Exported")

    def check_export_status(self):
        if self.data_deleted:
            self.export_button.config(state=tk.NORMAL)

    def exitProgram(self):
        self.window.destroy()

def main():
    root = tk.Tk()
    app = DataCleanserApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
