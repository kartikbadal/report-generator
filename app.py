import streamlit as st
import logging
import os
from modules import(
    load_file,
    clean_data,
    get_summary,
    save_bar_chart,
    save_line_chart,
    save_correlation_heatmap,
    generate_pdf,
    send_report,
    get_usd_to_inr
)

# Configure logging for entire app

logging.basicConfig(
    level= logging.INFO,
    format ="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Output folder for charts and PDF

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok= True)

# App Title

st.set_page_config(
    page_title= "Report Generator",
    page_icon= "📊",
    layout= "wide"
)

st.title("📊 Automated Business Report Generator")
st.markdown(
    "Upload a CSV or Excel file to generate." 
    "A professional PDF report with chart."
    )

# Sidebar

st.sidebar.header("⚙️ Settings")
recipient_email = st.sidebar.text_input("Recipient Email Address")
send_email_option = st.sidebar.checkbox("Send Report via email")

# File Upload
st.subheader("Step 1 - Upload your Data")

uploaded_file =st.file_uploader("Choose a CSV or Excel file",type = ["csv", "xlsx","xls"])


# Data Processing

if uploaded_file is not None:
    st.subheader("Step 2 - Data Preview")

    # Load and clean data
    with st.spinner("Loading and cleaning data"):
        df = load_file(uploaded_file)
        df = clean_data(df)
        summary = get_summary(df)

    # Show summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", summary["rows"])

    with col2:
        st.metric("Total Columns", summary["columns"])

    with col3:
        null_total = sum(summary["null_counts"].values())
        st.metric("Total Nulls", null_total)

    # Show null counts
    st.subheader("Missing values per Column")
    st.json(summary["dtypes"])

    # Chart Selection
    st.subheader("Step 3 - Select Charts")

    numeric_cols = df.select_dtypes(include = "number").columns.tolist()
    all_cols = df.columns.tolist()

    chart_paths = []

    # Bar chart options

    st.markdown("** Bar Chart")
    bar_x = st.selectbox("X axis(categories)", all_cols , key = "bar_x")
    bar_y = st.selectbox("Y axis (values)", numeric_cols,  key = "bar_y")

    # Line chart options

    st.markdown ("**Line Chart**")
    line_x = st.selectbox("X axis(time/order)", all_cols, key = "line_x")
    line_y = st.selectbox("Y axis(values)", numeric_cols, key = "line_y")

    # Heatmap - no selection needed, auto uses numeric cols

    show_heatmap = st.checkbox("Include corelation Heatmap")

    # Generate Report

    st.subheader("Step 4- Generate Report")

    if st.button("Generate PDF Report"):
        with st.spinner("Generating Charts"):
            
            # Save bar chart
            bar_path = os.path.join(OUTPUT_DIR, "bar_chart.png")
            save_bar_chart(df, bar_x, bar_y, bar_path)
            chart_paths.append(bar_path)

            # Save Line Chart
            line_path = os.path.join(OUTPUT_DIR, "line_chart.png")
            save_line_chart(df, line_x, line_y, line_path)
            chart_paths.append(line_path)

            # Save Heatmap if selected

            if show_heatmap:
                heat_path = os.path.join(OUTPUT_DIR, "heatmap.png")
                save_correlation_heatmap(df, heat_path)
                chart_paths.append(heat_path)
        
        with st.spinner("Generating PDF"):
            pdf_path = os.path.join(OUTPUT_DIR, "report.pdf")
            generate_pdf(summary, chart_paths, pdf_path)
        
        st.success("PDF report generated successfully!")

        # Download Button
        with open(pdf_path, "rb") as f:
            st.download_button(label= "Download PDF Report", data = f, file_name= "business_report.pdf", mime = "application/pdf")

        # Email Section
        if send_email_option and recipient_email:
            with st.spinner("Sending Email...."):
                send_report(
                    recipient_email= recipient_email,
                    subject= "Your Business Report",
                    body=(
                        "Please find attached your "
                        "automated business report"
                    ),
                    pdf_path= pdf_path
                )
            st.success(f"Report sent to {recipient_email}!")
        
        # Live Exchange Rate
        st.subheader("Live USD to INR rate")
        with st.spinner("Fetching the exchange rate"):
            try:
                rate = get_usd_to_inr()
                st.metric("1 USD = ", f"RS{rate}")
            except Exception as e:
                st.warning("Cound not fetch exchange rate. Check Internet Connection")
