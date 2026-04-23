import os
from pathlib import Path
import requests
import streamlit as st

BACKEND_URL = os.getenv("NOVALENSE_BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="NOVALENSE", layout="wide")
st.title("NOVALENSE")
st.caption("Hybrid transformer-based research originality and semantic forensics framework")

with st.sidebar:
    st.header("Configuration")
    top_k = st.slider("Top-K similar papers", min_value=1, max_value=10, value=5)
    semantic_threshold = st.slider("Sentence similarity threshold", min_value=0.50, max_value=0.95, value=0.72)
    uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])

if uploaded_file:
    if st.button("Run NOVALENSE Analysis", use_container_width=True):
        with st.spinner("Uploading file and running analysis..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type or "application/octet-stream")}
            upload_response = requests.post(f"{BACKEND_URL}/api/v1/upload", files=files, timeout=120)
            upload_response.raise_for_status()
            file_path = upload_response.json()["file_path"]

            analyze_payload = {
                "file_path": file_path,
                "top_k": top_k,
                "semantic_threshold": semantic_threshold,
            }
            analysis_response = requests.post(f"{BACKEND_URL}/api/v1/analyze", json=analyze_payload, timeout=240)
            analysis_response.raise_for_status()
            result = analysis_response.json()

        col1, col2, col3 = st.columns(3)
        col1.metric("Originality Score", result["originality_score"])
        col2.metric("Semantic Similarity", result["semantic_similarity_score"])
        col3.metric("AI Likelihood", result["ai_likelihood_score"])

        st.subheader("Top Similar Papers")
        st.dataframe(result["top_similar_papers"], use_container_width=True)

        st.subheader("Flagged Sentences")
        if result["flagged_sentences"]:
            for item in result["flagged_sentences"]:
                with st.container(border=True):
                    st.markdown(f"**Input sentence:** {item['input_sentence']}")
                    st.markdown(f"**Matched sentence:** {item['matched_sentence']}")
                    st.markdown(f"**Matched paper:** {item['matched_paper_title']}")
                    st.markdown(f"**Similarity:** {item['similarity']} | **Paraphrase probability:** {item['paraphrase_probability']}")
                    st.markdown(f"**Explanation:** {item['explanation']}")
        else:
            st.info("No sentence-level matches crossed the current threshold.")

        st.subheader("AI Detection Explanations")
        for note in result["ai_explanations"]:
            st.write(f"- {note}")

        st.subheader("Generated Reports")
        st.code(result["report_json_path"], language="text")
        st.code(result["report_html_path"], language="text")
else:
    st.info("Upload a paper to start analysis.")
