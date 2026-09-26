# 🛡️ CodeSentinel

A web-based code plagiarism detection system that analyzes and compares source code files to identify similarities.

🌐 Live Demo

(https://codesentinel12.streamlit.app/)

 ✨ Features

- 🐍 Supports Python, C, C++, and Java
- 🔍 Text and AST-based similarity analysis
- 🌐 Winnowing-based detection
- 📁 Multiple file comparison
- 📊 Similarity percentage and risk classification
- 🚨 Threshold-based plagiarism alerts
- 📋 Suspicious pairs ranking
- 📄 PDF report generation
- 🕒 Comparison history

 🛠️ Technologies Used

- Python
- Streamlit
- Plotly
- SQLite
- AST
- Winnowing Algorithm

 🚀 How to Run Locally

1. Clone the repository
   ```bash
  git clone https://github.com/chaboo12/CodeSentinel.git
  cd CodeSentinel

3. Install dependencies
   pip install -r requirements.txt

4. Run the application
   streamlit run app.py

📁 Project Structure

CodeSentinel/
├── app.py
├── database.py
├── style.css
├── requirements.txt
└── modules/
    ├── ast_analyzer.py
    ├── report.py
    ├── similarity.py
    ├── tokenizer.py
    └── winnowing.py
