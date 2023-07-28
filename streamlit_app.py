import streamlit as st
import pandas as pd
import io
import csv
import os
import shutil

class DataCleanserApp:

    def __init__(self):
        self.AcademyUserData = None
        self.ExpiredUserIDs = None
        self.ExpiredUserEmailAddresses = None
        self.data_deleted = False

    def uploadAcademyUserData(self):
        uploaded_file = st.file_uploader("Upload Academy User Data", type="csv")
        if uploaded_file is not None:
            self.AcademyUserData = pd.read_csv(uploaded_file)
            st.write("Academy User Data Uploaded")
        else:
            st.write("Please Upload a File")

    def uploadExpiredUserIDs(self):
        uploaded_file = st.file_uploader("Upload Expired User IDs", type="csv")
        if uploaded_file is not None:
            self.ExpiredUserIDs = pd.read_csv(uploaded_file)
            st.write("Expired User IDs Uploaded")
        else:
            st.write("Please Upload a File")

    def uploadExpiredUserEmailAddresses(self):
        uploaded_file = st.file_uploader("Upload Expired User Email Addresses", type="csv")
        if uploaded_file is not None:
            self.ExpiredUserEmailAddresses = pd.read_csv(uploaded_file)
            st.write("Expired User Email Addresses Uploaded")
        else:
            st.write("Please Upload a File")

    def deleteExpiredUserIDs(self):
        if st.button("Delete Expired User IDs"):
            self.AcademyUserData = self.deleteExpiredUsers(self.AcademyUserData, self.ExpiredUserIDs, 'User ID')
            self.data_deleted = True
            self.check_export_status()
            st.write("Expired User IDs Deleted")

    def deleteExpiredUserEmailAddresses(self):
        if st.button("Delete Expired User Email Addresses"):
            self.AcademyUserData = self.deleteExpiredUsers(self.AcademyUserData, self.ExpiredUserEmailAddresses, 'Email Address')
            self.data_deleted = True
            self.check_export_status()
            st.write("Expired User Email Addresses Deleted")

    def deleteExpiredUsers(self, user_data, expired_users, column_name):
        user_data = user_data[~user_data[column_name].isin(expired_users[column_name])]
        return user_data

    def exportCleansedAcademyUserData(self):
        if st.button("Export Cleansed Academy User Data"):
            csv = self.AcademyUserData.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/csv;base64,{b64}" download="CleansedAcademyUserData.csv">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)

    def check_export_status(self):
        if self.data_deleted:
            self.export_button.config(state=tk.NORMAL)

def main():
    st.title("Data Cleansing")
    app = DataCleanserApp()
    app.uploadAcademyUserData()
    app.uploadExpiredUserIDs()
    app.uploadExpiredUserEmailAddresses()
    app.deleteExpiredUserIDs()
    app.deleteExpiredUserEmailAddresses()
    app.exportCleansedAcademyUserData()

if __name__ == "__main__":
    main()
