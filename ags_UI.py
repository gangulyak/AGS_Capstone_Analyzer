# ags_UI.py

import streamlit as st
import pandas as pd

from analytical.analytics import SalesAnalyzer
from analytical.visualizer import SalesVisualizer
from analytical.stats_retriever import StatsRetriever
from llm.insight_chain import InsightChain

# ------------------------------------------------------------------
# Streamlit config
# ------------------------------------------------------------------
st.set_page_config(page_title="AGS Data Analyzer", layout="wide")
st.title("📊 AGS Data Analyzer – Business Intelligence Dashboard")

# ------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------------------------------------------
if "analyzer" not in st.session_state:
    st.session_state.analyzer = None

if "schema_confirmed" not in st.session_state:
    st.session_state.schema_confirmed = False

if "last_file_id" not in st.session_state:
    st.session_state.last_file_id = None

if "llm_question" not in st.session_state:
    st.session_state.llm_question = ""

# ------------------------------------------------------------------
# FILE UPLOAD
# ------------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload CSV or XLSX file",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.stop()

# Detect new file upload → reset state
file_id = (uploaded_file.name, uploaded_file.size)

if st.session_state.last_file_id != file_id:
    st.session_state.last_file_id = file_id
    st.session_state.schema_confirmed = False
    st.session_state.analyzer = None
    st.session_state.llm_question = ""

# ------------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------------
try:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

st.subheader("📄 Data Preview")
st.dataframe(df.head())

# ------------------------------------------------------------------
# SCHEMA SELECTION FORM (ATOMIC)
# ------------------------------------------------------------------
st.subheader("🧭 Select Columns")

with st.form("schema_form"):
    columns = df.columns.tolist()

    sales_col = st.selectbox("Select Sales column", columns)
    region_col = st.selectbox("Select Region / Geography column", columns)
    product_col = st.selectbox("Select Product / Service column", columns)
    date_col = st.selectbox("Select Date column", columns)

    currency_choice = st.selectbox(
        "Currency (optional)",
        ["", "USD", "EUR", "GBP", "INR"]
    )

    submitted = st.form_submit_button("✅ Confirm selection")

if submitted:
    if len({sales_col, region_col, product_col, date_col}) < 4:
        st.error("Each selected column must be unique.")
        st.stop()

    schema = {
        "sales": sales_col,
        "region": region_col,
        "product": product_col,
        "date": date_col,
    }

    try:
        st.session_state.analyzer = SalesAnalyzer(df, schema=schema)
        st.session_state.schema_confirmed = True
        st.session_state.llm_question = ""  # reset old question
    except Exception as e:
        st.error(f"Analytics initialization failed: {e}")
        st.stop()

# ------------------------------------------------------------------
# STOP HERE UNTIL CONFIRMED
# ------------------------------------------------------------------
if not st.session_state.schema_confirmed:
    st.info("Select columns and click **Confirm selection** to proceed.")
    st.stop()

analyzer = st.session_state.analyzer
currency_label = currency_choice if currency_choice else None

# ------------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------------
st.subheader("📊 Executive Sales Dashboard")

fig = SalesVisualizer.plot_sales_dashboard(
    sales_over_time=analyzer.sales_over_time(),
    sales_by_year=analyzer.sales_by_year(),
    sales_by_product=analyzer.sales_by_product(),
    sales_by_region=analyzer.sales_by_region(),
    currency=currency_label,
)

st.pyplot(fig)

# ------------------------------------------------------------------
# SUMMARY TABLE
# ------------------------------------------------------------------
st.subheader("📋 Summary Statistics")

summary_df = (
    pd.DataFrame.from_dict(analyzer.basic_metrics(), orient="index", columns=["Value"])
    .reset_index()
    .rename(columns={"index": "Metric"})
)

st.table(summary_df)

# ------------------------------------------------------------------
# LLM SECTION (INDEPENDENT)
# ------------------------------------------------------------------
st.subheader("🧠 Ask the Data")

question = st.text_input(
    "Ask a business question",
    key="llm_question"
)

if question.strip():
    retriever = StatsRetriever(analyzer)
    payload = retriever.as_dict()

    chain = InsightChain()

    with st.spinner("Generating insight..."):
        answer = chain.run(payload, question)

    st.markdown("### 📌 Insight")
    st.write(answer)

