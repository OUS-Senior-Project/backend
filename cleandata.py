import streamlit as st
import pandas as pd
import json
import openpyxl
from openpyxl.utils import get_column_letter

# ------------------------------------------------------------
# REQUIRED COLUMNS (REAL COLUMN NAMES IN EXCEL)
# ------------------------------------------------------------

REQUIRED_COLS = {
    "Academic Level": "Academic Level",
    "Primary Program of Study": "Primary Program of Study",
    "Cumulative GPA": "Cumulative GPA",
    "Gender": "Gender",
    "FTIC Cohort": "FTIC Cohort"
}

NORMALIZATION_MAP = {
    "Overall Registration Status": {
        "First Time in College": "FTIC",
        "FTIC": "FTIC",
        "First Time Transfer": "TR",
        "Transfer": "TR",
    },
    "Gender": {
        "Male": "M",
        "Female": "F"
    }
}

# ------------------------------------------------------------
# 1. Extract Excel AutoFilters using openpyxl
# ------------------------------------------------------------

def extract_filters(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active

    if not ws.auto_filter or not ws.auto_filter.ref:
        return {}

    filters_dict = {}

    for flt in ws.auto_filter.filterColumn:
        col_letter = get_column_letter(flt.colId + 1)
        allowed = []

        for f in flt.filters:
            if hasattr(f, "val"):
                allowed.append(f.val)

        filters_dict[col_letter] = allowed

    return filters_dict


# ------------------------------------------------------------
# 2. Cleaning function
# ------------------------------------------------------------
def clean_data(file_path):
    # ------------------------------------------------------------
    # Skip first 20 rows, row 21 becomes the header
    # ------------------------------------------------------------
    df = pd.read_excel(file_path, engine="openpyxl", skiprows=20)
    
    # Clean column names - remove any extra whitespace
    df.columns = df.columns.str.strip()

    # ------------------------------------------------------------
    # Check if required columns exist
    # ------------------------------------------------------------
    missing = []
    for excel_col in REQUIRED_COLS.keys():
        if excel_col not in df.columns:
            missing.append(excel_col)

    if missing:
        st.warning(f"Available columns: {list(df.columns)}")
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    # Select only required columns
    df = df[list(REQUIRED_COLS.keys())].copy()

    # ------------------------------------------------------------
    # Normalize values
    # ------------------------------------------------------------
    for col, mapping in NORMALIZATION_MAP.items():
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip().replace(mapping)

    # ------------------------------------------------------------
    # Convert numeric columns
    # ------------------------------------------------------------
    df["Cumulative GPA"] = pd.to_numeric(df["Cumulative GPA"], errors="coerce")

    # ------------------------------------------------------------
    # Remove invalid rows
    # ------------------------------------------------------------
    df = df.dropna(subset=["Academic Level"], how="any")
    
    # Remove empty string rows
    df = df[(df["Academic Level"].astype(str).str.strip() != "")]
    
    # Reset index starting from 1
    df = df.reset_index(drop=True)
    df.index = df.index + 1

    return df


# ------------------------------------------------------------
# STREAMLIT UI
# ------------------------------------------------------------

st.title("📊 Excel Data Cleaner + Filter Extractor")
st.write("Upload your Excel file. The system will clean it and save its filters.")
st.info("The first 20 rows (metadata) will be skipped. Row 21 is treated as the header.")

uploaded = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])

if uploaded:
    st.success("✅ File uploaded successfully!")

    # Save temp file
    temp_path = "temp.xlsx"
    with open(temp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    # -----------------------------
    # EXTRACT FILTERS
    # -----------------------------
    try:
        filters = extract_filters(temp_path)
        
        if filters:
            st.subheader("📘 Extracted Excel Filters")
            st.json(filters)

            with open("excel_filters.json", "w") as f:
                json.dump(filters, f, indent=4)

            st.success("✅ Excel filters saved as excel_filters.json")
        else:
            st.info("ℹ️ No filters found in the Excel file.")
    except Exception as e:
        st.warning(f"⚠️ Could not extract filters: {str(e)}")

    # -----------------------------
    # CLEAN DATA
    # -----------------------------
    try:
        st.subheader("🔄 Processing Data...")
        
        # Clean the data
        cleaned_df = clean_data(temp_path)

        st.subheader("✅ Cleaned Data - Each Row is One Student")
        st.dataframe(cleaned_df)
        
        st.success(f"📊 Total students after cleaning: **{len(cleaned_df)}**")

        # Save to CSV
        csv_path = "cleaned_output.csv"
        cleaned_df.to_csv(csv_path, index=True, index_label="Student #")

        with open(csv_path, "rb") as f:
            st.download_button(
                label="📥 Download Cleaned CSV",
                data=f,
                file_name="cleaned_output.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")
        
        # Show raw preview for debugging
        st.subheader("🔍 Raw File Preview (First 25 Rows)")
        try:
            raw_preview = pd.read_excel(temp_path, engine="openpyxl", header=None, nrows=25)
            st.dataframe(raw_preview)
        except:
            st.error("Could not load raw preview")