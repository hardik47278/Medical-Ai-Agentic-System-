import streamlit as st
import os
import io
from PIL import Image
from datetime import datetime
import json
import base64

# Import enhanced medical analysis functions
from utils import (
    process_file, 
    analyze_image, 
    generate_heatmap, 
    save_analysis,
    get_latest_analyses, 
    generate_report,
    search_pubmed,
    generate_statistics_report
)

# Import chat system for collaboration (Fixed typo)
from chat_sustem import render_chat_interface, create_manual_chat_room

# Import QA system
from repo import ReportQASystem, ReportQAChat
from qa_interface import render_qa_chat_interface

# Set page configuration
st.set_page_config(
    page_title="Medical Image Analysis Platform",
    page_icon="🏥",
    layout="wide"
)

# Initialize session states
for key, default in [
    ("openai_key", ""),
    ("file_data", None),
    ("analysis_results", None),
    ("file_name", None),
    ("file_type", None),
    ("OPENAI_API_KEY", None)
]:
    if key not in st.session_state:
        st.session_state[key] = default

# Main app header
st.title("🏥 Advanced Medical Image Analysis")
st.markdown("Upload medical images for AI-powered analysis and collaborate with colleagues")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")

    api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_key, type="password", key="api_key_input")
    user_input = st.text_input("Enter your question", key="user_input_key")

    if api_key:
        st.session_state.openai_key = api_key
        st.session_state.OPENAI_API_KEY = api_key

    st.subheader("Analysis Options")
    enable_xai = st.checkbox("Enable Explainable AI", value=True)
    include_references = st.checkbox("Include Medical References", value=True)

    st.subheader("Recent Analyses")
    recent_analyses = get_latest_analyses(limit=5)
    for analysis in recent_analyses:
        st.caption(f"{analysis.get('filename', 'Unknown')} - {analysis.get('date', '')[:10]}")

    if st.button("Generate Statistics Report"):
        try:
            stats_report = generate_statistics_report()
            if stats_report:
                b64_pdf = base64.b64encode(stats_report.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="statistics_report.pdf">Download Statistics Report</a>'
                st.markdown(href, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["Image Upload & Analysis", "Collaboration", "Report Q&A", "Reports"])

with tab1:
    uploaded_file = st.file_uploader("Upload a medical image (JPEG, PNG, DICOM, NIfTI)", type=["jpg", "jpeg", "png", "dcm", "nii", "nii.gz"])
    if uploaded_file:
        try:
            file_data = process_file(uploaded_file)
            if file_data:
                st.session_state.file_data = file_data
                st.session_state.file_name = uploaded_file.name
                st.session_state.file_type = file_data["type"]

                st.image(file_data["data"], caption=f"Uploaded {file_data['type']} image", use_column_width=True)

                if st.button("Analyze Image") and st.session_state.openai_key:
                    with st.spinner("Analyzing image..."):
                        try:
                            analysis_results = analyze_image(file_data["data"], st.session_state.openai_key, enable_xai=enable_xai)
                            analysis_results = save_analysis(analysis_results, filename=uploaded_file.name)
                            st.session_state.analysis_results = analysis_results
                            st.session_state.findings = analysis_results.get("findings", [])

                            st.subheader("Analysis Results")
                            st.markdown(analysis_results["analysis"])

                            if analysis_results.get("findings"):
                                st.subheader("Key Findings")
                                for idx, finding in enumerate(analysis_results["findings"], 1):
                                    st.markdown(f"{idx}. {finding}")

                            if analysis_results.get("keywords"):
                                st.subheader("Keywords")
                                st.markdown(f"{', '.join(analysis_results['keywords'])}")

                            if enable_xai:
                                st.subheader("Explainable AI Visualization")
                                overlay, heatmap = generate_heatmap(file_data["array"])
                                col1, col2 = st.columns(2)
                                col1.image(overlay, caption="Heatmap Overlay", use_column_width=True)
                                col2.image(heatmap, caption="Raw Heatmap", use_column_width=True)

                            if include_references and analysis_results.get("keywords"):
                                st.subheader("Relevant Medical Literature")
                                references = search_pubmed(analysis_results["keywords"], max_results=3)
                                for ref in references:
                                    st.markdown(f"- *{ref['title']}*  \n{ref['journal']}, {ref['year']} (PMID: {ref['id']})")

                        except Exception as e:
                            st.error(f"Error during analysis: {str(e)}")

                elif not st.session_state.openai_key:
                    st.warning("Please enter your OpenAI API key in the sidebar to enable analysis")
            else:
                st.error("Unable to process the uploaded file")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

with tab2:
    try:
        render_chat_interface()
    except Exception as e:
        st.error(f"Error in chat interface: {str(e)}")
        st.subheader("Create Discussion Without Image")
        manual_creator = st.text_input("Your Name", value="Dr. Anonymous", key="creator_key")
        manual_description = st.text_input("Case Description", key="description_key")
        if st.button("Create Manual Discussion") and manual_description:
            try:
                case_id = create_manual_chat_room(manual_creator, manual_description)
                st.session_state.current_case_id = case_id
                st.rerun()
            except Exception as e:
                st.error(f"Error creating discussion: {str(e)}")

with tab3:
    render_qa_chat_interface()

with tab4:
    st.subheader("Medical Reports & Analytics")
    st.markdown("### Analysis History")
    recent_analyses = get_latest_analyses(limit=10)
    
    if recent_analyses:
        for idx, analysis in enumerate(recent_analyses, 1):
            with st.expander(f"{idx}. {analysis.get('filename', 'Unknown')} - {analysis.get('date', '')[:10]}"):
                st.markdown(analysis.get("analysis", "No analysis available"))
                
                if analysis.get("findings"):
                    st.markdown("*Key Findings:*")
                    for finding_idx, finding in enumerate(analysis["findings"], 1):
                        st.markdown(f"{finding_idx}. {finding}")
                
                col1, col2 = st.columns(2)
                
                # Generate individual report
                with col1:
                    if st.button(f"Generate Report #{idx}"):
                        pdf_buffer = generate_report(analysis, include_references=include_references)
                        
                        # Create download link
                        b64_pdf = base64.b64encode(pdf_buffer.read()).decode()
                        report_name = f"report_{analysis.get('id', 'unknown')[:8]}.pdf"
                        href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{report_name}">Download Report</a>'
                        st.markdown(href, unsafe_allow_html=True)
                
                # Ask questions about this report
                with col2:
                    if st.button(f"Q&A on Report #{idx}"):
                        # Create a QA room specifically for this report
                        if "qa_chat" not in st.session_state:
                            st.session_state.qa_chat = ReportQAChat()
                        
                        report_name = f"Q&A for {analysis.get('filename', 'Unknown')}"
                        created_qa_id = st.session_state.qa_chat.create_qa_room("Dr. Anonymous", report_name)
                        st.session_state.current_qa_id = created_qa_id
                        
                        # Switch to QA tab
                        st.rerun()
    else:
        st.info("No previous analyses found. Upload and analyze an image to get started.")
    
    # Statistics section
    st.markdown("### Statistics")
    
    # Generate statistics report
    if st.button("Generate Comprehensive Statistics"):
        stats_report = generate_statistics_report()
        if stats_report:
            # Create download link
            b64_pdf = base64.b64encode(stats_report.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="statistics_report.pdf">Download Statistics Report</a>'
            st.markdown(href, unsafe_allow_html=True)
