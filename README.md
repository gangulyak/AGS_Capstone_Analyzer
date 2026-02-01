# AGS_Capstone_Analyzer
Data Analyzer for Clean Sales Data
AGS_Data_Analyzer: AI-Powered Business Intelligence Assistant

1. Project Overview
AGS_Data_Analyzer is an interactive Business Intelligence (BI) assistant built using Streamlit, Pandas, Seaborn/Matplotlib, and LangChain. It enables users to upload clean business datasets, dynamically select relevant columns, visualize key insights, and query the data using a Large Language Model (LLM).

2. Folder Structure
AGS_Captone/
 ├── ags_UI.py
 ├── analytical/
 │   ├── analytics.py
 │   ├── stats_retriever.py
 │   └── visualizer.py
 ├── llm/
 │   ├── prompts.py
 │   └── insight_chain.py
 └── requirements.txt

3. Execution Flow
User uploads data → selects columns → analytics computed → dashboard rendered → structured stats retrieved → LLM generates insights.

4. Core Components
- ags_UI.py: Main Streamlit controller
- analytics.py: Deterministic analytics engine
- visualizer.py: Seaborn dashboards
- stats_retriever.py: LLM-ready statistics
- insight_chain.py: LangChain-based insight generation

5. Why LangChain
LangChain cleanly separates prompts, data payloads, and model execution, making the system extensible and robust.

6. Conclusion
The system cleanly integrates classical analytics, visualization, and LLM reasoning in a modular architecture suitable for academic evaluation.

