import json
import pandas as pd
from pyarrow import json_
import streamlit as st


# Column names (adjust if your Excel has different column names)
COL_ACADEMIC_LEVEL = "Academic Level"
COL_LOAD_STATUS = "Load Status"
COL_STUDENT_TYPE = "Student Type"

# Expected values (adjust if your data uses different values)
VALUE_UNDERGRADUATE = "Undergraduate"
VALUE_FTIC = "First Time in College (FTIC)"
VALUE_FTIT = "First Time in Transfer (FTIT)"
VALUE_FULL_TIME = "Full-time"
VALUE_PART_TIME = "Part-time"


def load_data(file_path: str) -> pd.DataFrame:
    """Load the cleaned Excel file into a pandas DataFrame."""
    try:
        df = pd.read_excel(file_path, index_col=0)  # index_col=0 to preserve Student # index
        return df
    except FileNotFoundError:
        st.error(f"❌ File '{file_path}' not found. Please run cleandata-algo.py first to generate it.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        st.stop()


def calculate_total_enrollment(df: pd.DataFrame) -> int:
    """
    Calculate Total Enrollment.
    Count students where Current Academic Record Status = 'Active'
    """
    # Total enrollment = total number of rows (students)
    return len(df)


def calculate_undergraduate_enrollment(df: pd.DataFrame) -> dict:
    """
    Calculate Total Undergraduate Enrollment with Full-time/Part-time breakdown.
    Count students where Academic Level = 'Undergraduate'
    """
    if COL_ACADEMIC_LEVEL not in df.columns:
        return {"total": 0, "full_time": 0, "part_time": 0}
    
    # Filter for Undergraduate students
    undergrad_df = df[df[COL_ACADEMIC_LEVEL].str.strip().str.lower() == VALUE_UNDERGRADUATE.lower()]
    total = len(undergrad_df)
    
    # Break down by Load Status
    if COL_LOAD_STATUS not in df.columns:
        return {"total": total, "full_time": 0, "part_time": 0}
    
    full_time = len(undergrad_df[
        undergrad_df[COL_LOAD_STATUS].str.strip().str.lower() == VALUE_FULL_TIME.lower()
    ])
    part_time = len(undergrad_df[
        undergrad_df[COL_LOAD_STATUS].str.strip().str.lower() == VALUE_PART_TIME.lower()
    ])
    
    return {
        "total": total,
        "full_time": full_time,
        "part_time": part_time
    }


def calculate_ftic_enrollment(df: pd.DataFrame) -> dict:
    """
    Calculate FTIC Enrollment with Full-time/Part-time breakdown.
    Count students where Student Type = 'First Time in College (FTIC)'
    """
    if COL_STUDENT_TYPE not in df.columns:
        return {"total": 0, "full_time": 0, "part_time": 0}
    
    # Filter for FTIC students
    ftic_df = df[df[COL_STUDENT_TYPE].str.strip().str.lower() == VALUE_FTIC.lower()]
    total = len(ftic_df)
    
    # Break down by Load Status
    if COL_LOAD_STATUS not in df.columns:
        return {"total": total, "full_time": 0, "part_time": 0}
    
    full_time = len(ftic_df[
        ftic_df[COL_LOAD_STATUS].str.strip().str.lower() == VALUE_FULL_TIME.lower()
    ])
    part_time = len(ftic_df[
        ftic_df[COL_LOAD_STATUS].str.strip().str.lower() == VALUE_PART_TIME.lower()
    ])
    
    return {
        "total": total,
        "full_time": full_time,
        "part_time": part_time
    }


def calculate_transfer_enrollment(df: pd.DataFrame) -> dict:
    """
    Calculate Transfer Enrollment with Full-time/Part-time breakdown.
    Count students where Student Type = 'First Time in Transfer (FTIT)'
    """
    if COL_STUDENT_TYPE not in df.columns:
        return {"total": 0, "full_time": 0, "part_time": 0}
    
    # Filter for FTIT students
    ftit_df = df[df[COL_STUDENT_TYPE].str.strip().str.lower() == VALUE_FTIT.lower()]
    total = len(ftit_df)
    
    # Break down by Load Status
    if COL_LOAD_STATUS not in df.columns:
        return {"total": total, "full_time": 0, "part_time": 0}
    
    full_time = len(ftit_df[
        ftit_df[COL_LOAD_STATUS].str.strip().str.lower() == VALUE_FULL_TIME.lower()
    ])
    part_time = len(ftit_df[
        ftit_df[COL_LOAD_STATUS].str.strip().str.lower() == VALUE_PART_TIME.lower()
    ])
    
    return {
        "total": total,
        "full_time": full_time,
        "part_time": part_time
    }

def collect_all_metrics(df: pd.DataFrame) -> dict:
    """
    Collect all enrollment metrics into a structured dictionary.
    Returns a dictionary that can be easily converted to JSON.
    """
    total_enrollment = calculate_total_enrollment(df)
    undergrad_metrics = calculate_undergraduate_enrollment(df)
    ftic_metrics = calculate_ftic_enrollment(df)
    transfer_metrics = calculate_transfer_enrollment(df)
    
    # Structure the data as a nested dictionary
    metrics_dict = {
        "total_enrollment": total_enrollment,
        "undergraduate_enrollment": {
            "total": undergrad_metrics["total"],
            "full_time": undergrad_metrics["full_time"],
            "part_time": undergrad_metrics["part_time"],
        },
        "ftic_enrollment": {
            "total": ftic_metrics["total"],
            "full_time": ftic_metrics["full_time"],
            "part_time": ftic_metrics["part_time"]
        },
        "transfer_enrollment": {
            "total": transfer_metrics["total"],
            "full_time": transfer_metrics["full_time"],
            "part_time": transfer_metrics["part_time"]
        }
    }
    
    return metrics_dict

def export_metrics_to_json(metrics_dict: dict, filename: str = "enrollment_metrics.json") -> str:
    """
    Convert metrics dictionary to JSON string and save to file.
    Returns the JSON string for download.
    """
    # Convert dictionary to JSON string with nice formatting (indent=4)
    json_string = json.dumps(metrics_dict, indent=4)
    
    # Optionally save to disk
    with open(filename, "w") as f:
        f.write(json_string)
    
    return json_string


def display_metrics(df: pd.DataFrame) -> dict:
    """Calculate and display all enrollment metrics."""
    
    st.header("📊 Enrollment Metrics")
    
    # Calculate all metrics
    total_enrollment = calculate_total_enrollment(df)
    undergrad_metrics = calculate_undergraduate_enrollment(df)
    ftic_metrics = calculate_ftic_enrollment(df)
    transfer_metrics = calculate_transfer_enrollment(df)
    
    # Display Total Enrollment
    st.subheader("1️⃣ Total Enrollment")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Total Active Students",
            value=total_enrollment
        )
    with col2:
        st.info(f"Criteria: Total Number of Students'")
    
    st.divider()
    
    # Display Undergraduate Enrollment
    st.subheader("2️⃣ Total Undergraduate Enrollment")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Total Undergraduate",
            value=undergrad_metrics["total"]
        )
    with col2:
        st.metric(
            label="Full-time",
            value=undergrad_metrics["full_time"]
        )
    with col3:
        st.metric(
            label="Part-time",
            value=undergrad_metrics["part_time"]
        )
    st.info(f"Criteria: {COL_ACADEMIC_LEVEL} = '{VALUE_UNDERGRADUATE}'")
    
    st.divider()
    
    # Display FTIC Enrollment
    st.subheader("3️⃣ FTIC Enrollment")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Total FTIC",
            value=ftic_metrics["total"]
        )
    with col2:
        st.metric(
            label="Full-time",
            value=ftic_metrics["full_time"]
        )
    with col3:
        st.metric(
            label="Part-time",
            value=ftic_metrics["part_time"]
        )
    st.info(f"Criteria: {COL_STUDENT_TYPE} = '{VALUE_FTIC}'")
    
    st.divider()
    
    # Display Transfer Enrollment
    st.subheader("4️⃣ Transfer Enrollment")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Total Transfer (FTIT)",
            value=transfer_metrics["total"]
        )
    with col2:
        st.metric(
            label="Full-time",
            value=transfer_metrics["full_time"]
        )
    with col3:
        st.metric(
            label="Part-time",
            value=transfer_metrics["part_time"]
        )
    st.info(f"Criteria: {COL_STUDENT_TYPE} = '{VALUE_FTIT}'")
    
    st.divider()
    
    # Summary Table
    st.subheader("📋 Summary Table")
    summary_data = {
        "Metric": [
            "Total Enrollment",
            "Undergraduate Enrollment",
            "Undergraduate - Full-time",
            "Undergraduate - Part-time",
            "FTIC Enrollment",
            "FTIC - Full-time",
            "FTIC - Part-time",
            "Transfer Enrollment (FTIT)",
            "Transfer - Full-time",
            "Transfer - Part-time"
        ],
        "Count": [
            total_enrollment,
            undergrad_metrics["total"],
            undergrad_metrics["full_time"],
            undergrad_metrics["part_time"],
            ftic_metrics["total"],
            ftic_metrics["full_time"],
            ftic_metrics["part_time"],
            transfer_metrics["total"],
            transfer_metrics["full_time"],
            transfer_metrics["part_time"]
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, width='stretch', hide_index=True)
    
    # Return metrics as dictionary
    return {
        "total_enrollment": total_enrollment,
        "undergraduate_enrollment": undergrad_metrics,
        "ftic_enrollment": ftic_metrics,
        "transfer_enrollment": transfer_metrics
    }


# ==================== STREAMLIT UI ====================
st.title("🎓 Enrollment Metrics Calculator")
st.write("Calculate core enrollment metrics from cleaned enrollment data.")

# File upload (required)
st.sidebar.header("📁 Upload File")
uploaded_file = st.sidebar.file_uploader(
    "Upload cleaned Excel file (.xlsx)",
    type=["xlsx"],
    help="Please upload your cleaned enrollment Excel file"
)

if not uploaded_file:
    st.warning("⚠️ Please upload an Excel file to continue.")
    st.info("💡 Upload your cleaned enrollment roster file (e.g., cleaned_output.xlsx)")
    st.stop()
    
# Save uploaded file temporarily
file_path = "temp_metrics.xlsx"
with open(file_path, "wb") as f:
    f.write(uploaded_file.getbuffer())
st.success(f"✅ File uploaded: `{uploaded_file.name}`")

# Load data
df = load_data(file_path)

# Display data info
st.sidebar.subheader("📊 Data Info")
st.sidebar.write(f"**Total rows:** {len(df)}")
st.sidebar.write(f"**Total columns:** {len(df.columns)}")

# Show available columns (for debugging)
with st.expander("🔍 View Available Columns"):
    st.write("Columns in the dataset:")
    st.code(", ".join(df.columns.tolist()))

# Show sample data
with st.expander("👀 View Sample Data (first 10 rows)"):
    st.dataframe(df.head(10), width='stretch')

# Calculate and display metrics
metrics_dict = display_metrics(df)

# Export to JSON
st.divider()
st.subheader("💾 Export Metrics")

# Convert to JSON string with nice formatting
json_string = json.dumps(metrics_dict, indent=4)

# Display JSON preview
with st.expander("Preview JSON"):
    st.code(json_string, language="json")

# Download button
st.download_button(
    label="Download Metrics as JSON",
    data=json_string,
    file_name="enrollment_metrics.json",
    mime="application/json",
    help="Download all calculated metrics as a JSON file"
)

# Optionally save to disk
with open("enrollment_metrics.json", "w") as f:
    f.write(json_string)
st.success("✅ Metrics saved to `enrollment_metrics.json`")