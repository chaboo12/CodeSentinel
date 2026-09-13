import streamlit as st
import pandas as pd
import plotly.express as px
import os

from modules.similarity import hybrid_similarity
from modules.winnowing import winnowing_similarity
from modules.report import generate_report

from database import (
    init_db,
    insert_result,
    insert_history,
    get_history
)


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="CPDS V2",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ================= HIDE DEFAULT STREAMLIT UI =================

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        display:none;
    }

    div[data-testid="stToolbar"] {
        display:none;
    }

    div.block-container {
        padding-top:1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ================= LOAD CSS =================

def load_css():

    if os.path.exists("style.css"):

        with open(
            "style.css",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


load_css()


# ================= DATABASE =================

init_db()


# ================= SESSION STATE =================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


if "report_results" not in st.session_state:
    st.session_state.report_results = None


if "report_generated" not in st.session_state:
    st.session_state.report_generated = False


if "pdf_filename" not in st.session_state:
    st.session_state.pdf_filename = None



# ================= SIDEBAR =================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;">
            <h3>🔍 CPDS</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "📊 Dashboard",
        use_container_width=True
    ):
        st.session_state.page = "Dashboard"


    if st.button(
        "📄 Reports",
        use_container_width=True
    ):
        st.session_state.page = "Reports"


    if st.button(
        "🕒 History",
        use_container_width=True
    ):
        st.session_state.page = "History"


    if st.button(
        "⚙ Settings",
        use_container_width=True
    ):
        st.session_state.page = "Settings"


    if st.button(
        "ℹ About",
        use_container_width=True
    ):
        st.session_state.page = "About"



    st.divider()


    threshold = st.slider(
        "Detection Threshold (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=5
    )


    st.caption(
        f"Current Threshold: {threshold}%"
    )



page = st.session_state.page



# ================= HISTORY PAGE =================

if page == "History":

    st.title("🕒 Analysis History")


    history = get_history()


    if history:

        history_df = pd.DataFrame(
            history,
            columns=[
                "Run ID",
                "Files",
                "Comparisons",
                "Highest Similarity",
                "Date"
            ]
        )


        st.dataframe(
            history_df,
            use_container_width=True
        )


    else:

        st.info(
            "No analysis history available."
        )


    st.stop()



# ================= REPORT PAGE =================

if page == "Reports":

    st.title("📄 Reports")


    filename = f"report_{threshold}.pdf"
    

    

    if filename and os.path.exists(filename):

        with open(
            filename,
            "rb"
        ) as pdf_file:

            pdf_data = pdf_file.read()



        st.download_button(
            label="📥 Download Latest Report",
            data=pdf_data,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True
        )


    else:

        st.warning(
            "No report generated yet."
        )


    st.stop()



# ================= SETTINGS PAGE =================

if page == "Settings":

    st.title("⚙ Settings")


    st.info(
        f"Similarity Threshold: {threshold}%"
    )


    st.success(
        "Theme: Dark"
    )


    st.stop()



# ================= ABOUT PAGE =================

if page == "About":

    st.title("ℹ About CPDS")


    st.markdown(
        """
        ### Supported Languages

        ✅ Python (.py)

        ✅ C (.c)

        ✅ C++ (.cpp)

        ✅ Java (.java)

        ✅ JavaScript (.js)


        ### Detection Engines

        - AST Analysis
        - Text Similarity
        - Winnowing Fingerprinting
        - PDF Reporting
        - History Tracking
        """
    )


    st.stop()
# ================= DASHBOARD =================

st.markdown(
    "<div style='margin-top:-20px'></div>",
    unsafe_allow_html=True
)


if not st.session_state.report_generated:

    st.title(
        "🔍 Code Plagiarism Detection System"
    )

    st.caption(
        "AI-Powered Source Code Similarity Analysis"
    )

else:

    st.title(
        "📊 Analysis Report"
    )


    if st.button(
        "← Back to Upload"
    ):

        st.session_state.report_generated = False
        st.session_state.report_results = None
        st.rerun()



# ================= SHOW REPORT =================

if st.session_state.report_generated:

    results = st.session_state.report_results


    names = results["names"]
    matrix = results["matrix"]
    report_data = results["report_data"]
    highest_similarity = results["highest_similarity"]



    filename = f"report_{threshold}.pdf"
    generate_report(report_data,threshold)



    # Generate metrics

    high_risk_matches = len(
        [
            r for r in report_data
            if r[2] >= threshold
        ]
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:
        st.metric(
            "Files",
            len(names)
        )


    with c2:
        st.metric(
            "Comparisons",
            len(report_data)
        )


    with c3:
        st.metric(
            "Highest Similarity",
            f"{highest_similarity}%"
        )


    with c4:
        st.metric(
            "High Risk Matches",
            high_risk_matches
        )



    # ================= CHARTS =================


    left, right = st.columns(
        [1.2, 1]
    )



    with left:

        st.subheader(
            "📈 Similarity Distribution"
        )


        high = 0
        medium = 0
        low = 0


        for _, _, score in report_data:

            if score >= threshold:
                high += 1

            elif score >= threshold / 2:
                medium += 1

            else:
                low += 1



        distribution = pd.DataFrame(
            {
                "Category":
                    [
                        "Low",
                        "Medium",
                        "High"
                    ],

                "Count":
                    [
                        low,
                        medium,
                        high
                    ]
            }
        )


        fig = px.pie(
            distribution,
            names="Category",
            values="Count",
            hole=0.55
        )


        fig.update_traces(
            textinfo="label+percent"
        )


        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20) 
            
            
        )
        fig.update_traces(
            domain=dict(
                x=[0.20,0.80],
                y=[0.15,0.85]
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True,
            height=300
        )



    with right:

        st.subheader(
            "🏆 Top Suspicious Pairs"
        )


        rows = []


        for a, b, score in sorted(
            report_data,
            key=lambda x: x[2],
            reverse=True
        ):


            if score >= threshold:

                risk = "🔴 High"


            elif score >= threshold / 2:

                risk = "🟠 Medium"


            else:

                risk = "🟢 Low"



            rows.append(
                [
                    a,
                    b,
                    score,
                    risk
                ]
            )



        if rows:

            top_df = pd.DataFrame(
                rows,
                columns=[
                    "File 1",
                    "File 2",
                    "Similarity %",
                    "Risk"
                ]
            )


            top_df.insert(
                0,
                "Rank",
                range(
                    1,
                    len(top_df)+1
                )
            )


            st.dataframe(
                top_df,
                hide_index=True,
                use_container_width=True,
                height=300
            )


        else:

            st.info(
                "No suspicious matches."
            )



    # ================= ALERTS =================


    st.subheader(
        "🚨 Threshold Alerts"
    )


    found = False

    high_alerts = []

    for i in range(len(names)):

        for j in range(i + 1, len(names)):

            score = matrix[i][j]

            if score >= threshold:
                high_alerts.append(
                    (names[i], names[j], score)
                )

    # Sort highest similarity first
    high_alerts.sort(
        key=lambda x: x[2],
        reverse=True
    )

    for file1, file2, score in high_alerts:

        st.markdown(
            f"""
        <div style="
        background: rgba(8, 32, 65, 0.75);
        border: 1px solid #1d5fa7;
        border-left: 4px solid #ff4b5c;
        border-radius: 8px;
        padding: 6px 12px;
        margin: 4px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        ">
        <div>
        <span style="
            color:#ff4b5c;
            font-weight:700;
            font-size:10px;
        ">
        🚨 HIGH SIMILARITY
        </span>
        <br>
        <span style="
            color:white;
            font-size:12px;
        ">
        {file1} &nbsp; ↔ &nbsp; {file2}
        </span>
        </div>

        <div style="
        background:rgba(255,75,92,0.15);
        color:#ff6675;
        padding:4px 9px;
        border-radius:7px;
        font-weight:700;
        font-size:12px;
        flex-shrink:0;
        ">
        {score:.1f}%
        </div>
        </div>
        """,
            unsafe_allow_html=True
        )

        found = True

    if not found:
        st.success(
            "No files exceeded the threshold."
        )

    # ================= DOWNLOAD =================

    generate_report(report_data,threshold)
    if filename and os.path.exists(filename):
        

        with open(
            filename,
            "rb"
        ) as pdf:
            st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf.read(),
                file_name=filename,
                mime="application/pdf",
                use_container_width=True
            )
            st.markdown("<div style='height:30px'></div>",unsafe_allow_html=True)



    st.stop()



# ================= UPLOAD SECTION =================


st.subheader(
    "📂 Upload Source Files"
)


files = st.file_uploader(
    "Upload Python, C, C++, Java or JavaScript files",
    type=[
        "py",
        "c",
        "cpp",
        "java",
        "js"
    ],
    accept_multiple_files=True
)



codes = []
names = []



if files:


    for file in files:

        try:

            content = file.read().decode(
                "utf-8",
                errors="ignore"
            )

            codes.append(content)
            names.append(file.name)


        except Exception:

            st.error(
                f"Cannot read {file.name}"
            )




# ================= GENERATE REPORT =================


generate_clicked = st.button(
    "🚀 Generate Full Report",
    use_container_width=True
)



if generate_clicked:


    if len(codes) < 2:

        st.error(
            "Please upload at least 2 files."
        )

        st.stop()



    n = len(codes)


    matrix = [
        [0]*n
        for _ in range(n)
    ]


    report_data = []



    for i in range(n):

        for j in range(i+1, n):


            score1 = hybrid_similarity(
                codes[i],
                codes[j]
            )


            score2 = winnowing_similarity(
                codes[i],
                codes[j]
            )


            final_score = round(
                (score1 + score2) / 2,
                2
            )


            matrix[i][j] = final_score
            matrix[j][i] = final_score



            insert_result(
                names[i],
                names[j],
                final_score
            )


            report_data.append(
                (
                    names[i],
                    names[j],
                    final_score
                )
            )



    highest_similarity = max(
        [
            x[2]
            for x in report_data
        ]
    )



    insert_history(
        len(names),
        len(report_data),
        highest_similarity
    )



    # Save result


    st.session_state.report_results = {

        "names": names,

        "matrix": matrix,

        "report_data": report_data,

        "similarity_df":
            pd.DataFrame(
                matrix,
                index=names,
                columns=names
            ),

        "highest_similarity":
            highest_similarity
    }



    filename = f"report_{threshold}.pdf"
       
    generate_report(
        report_data,
        threshold
    )



    st.session_state.pdf_filename = filename



    st.session_state.report_generated = True



    st.success(
        "Analysis completed successfully."
    )


    st.rerun()
