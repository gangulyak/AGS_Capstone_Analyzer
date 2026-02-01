import streamlit as st
import pandas as pd

st.set_page_config(page_title="AGS Data Analyzer", layout="wide")

st.title("📊 AGS_Data_Analyzer – Step 1")
st.write("Upload a clean CSV or Excel file for analysis.")

uploaded_file = st.file_uploader(
    "Upload file",
    type=["csv", "xlsx"]
)

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File loaded successfully!")

    st.subheader("Dataset Overview")
    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")

    st.subheader("Column Names")
    st.write(list(df.columns))

    st.subheader("Preview")
    st.dataframe(df.head())
