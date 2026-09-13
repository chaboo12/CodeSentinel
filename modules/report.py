from fpdf import FPDF
from datetime import datetime

def generate_report(report_data, threshold=80):
    print("PDF Threshold:",threshold)
    

    report_data.sort(
        key=lambda x: x[2],
        reverse=True
    )

    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 18)
    pdf.cell(
        0,
        10,
        "Code Plagiarism Detection Report",
        ln=True,
        align="C"
    )

    pdf.set_font("Arial", "", 12)
    pdf.cell(
        0,
        10,
        "AI-Based Source Code Similarity Analysis",
        ln=True,
        align="C"
    )

    pdf.ln(5)

    pdf.cell(
        0,
        10,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ln=True
    )

    pdf.ln(5)

    # Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Summary", ln=True)

    pdf.set_font("Arial", "", 11)

    total = len(report_data)

    high_risk = [
        r for r in report_data
        if r[2] >= threshold
    ]

    highest = max(
        [r[2] for r in report_data],
        default=0
    )

    average = round(
        sum(r[2] for r in report_data) / total,
        2
    ) if total else 0

    pdf.cell(
        0,
        8,
        f"Total Comparisons: {total}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"High Risk Matches: {len(high_risk)}",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Highest Similarity: {highest}%",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Average Similarity: {average}%",
        ln=True
    )

    pdf.ln(5)

    # Top Pairs
    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        0,
        10,
        "Top Suspicious Pairs",
        ln=True
    )

    pdf.set_font("Arial", "", 11)

    for i, row in enumerate(
        report_data[:5],
        start=1
    ):
        pdf.cell(
            0,
            8,
            f"{i}. {row[0]} <-> {row[1]} = {row[2]}%",
            ln=True
        )

    pdf.ln(5)

    # Detailed Results
    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        0,
        10,
        "Detailed Results",
        ln=True
    )

    pdf.set_font("Arial", "", 11)

    for file1, file2, score in report_data:

        if score >= threshold:
            risk = "HIGH"
        elif score >= threshold / 2:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        pdf.cell(
            0,
            8,
            f"{file1} | {file2} | {score}% | {risk}",
            ln=True
        )

    pdf.ln(5)

    # Conclusion
    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        0,
        10,
        "Conclusion",
        ln=True
    )

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(
        0,
        8,
        f"The analysis detected "
        f"{len(high_risk)} file pairs "
        f"above the configured threshold "
        f"of {threshold}%. Manual "
        f"verification is recommended."
    )
    print("saving PDF:",f"report_{threshold}.pdf")
    pdf.output(f"report_{threshold}.pdf")



