import streamlit as st
from database import (
    insert_cv_content, get_latest_cv, generate_proposal,
    update_cv_content, generate_ollama_embedding, get_name
)
from cvreader import read_cv
import json

def main():
    st.title("Proposely: Job Proposal & Cover Letter Generator")
    st.write("Welcome! Enter your full name to begin or click 'Exit' to quit.")

    # Get user full name
    fullname = st.text_input("Enter your name:")
    if st.button("Exit"):
        st.stop()

    if fullname:
        user_data = get_name(fullname)
        
        if user_data:
            st.write(f"Hello, {user_data[0]}")
            st.write("Would you like to generate a cover letter/proposal or update your CV?")
            choices = st.radio(
                "Choose an option:", 
                ("Generate Cover Letter", "Generate Proposal", "Update CV")
            )

            if choices == "Generate Cover Letter":
                job_description = st.text_area("Please enter the job description:")
                if st.button("Generate Cover Letter"):
                    job_embedding = generate_ollama_embedding(job_description)
                    content, similarity = get_latest_cv(job_embedding,user_data[0])
                    prompt = (
                        f"You're a respectful and honest assistant. Create a cover letter "
                        f"based on the job description: {job_description} and using this CV: {content}. "
                        f"If you cannot write the proposal, please say so."
                    )
                    cover_letter = generate_proposal(prompt)
                    st.write(cover_letter['response'])

            elif choices == "Generate Proposal":
                job_description = st.text_area("Please enter the job description:")
                if st.button("Generate Proposal"):
                    job_embedding = generate_ollama_embedding(job_description)
                    content, similarity = get_latest_cv(job_embedding,user_data[0])
                    prompt = (
                        f"You're a respectful and honest assistant. Create a job proposal "
                        f"based on the job description: {job_description} and using this CV: {content}. "
                        f"If you cannot write the proposal, please say so."
                    )
                    proposal = generate_proposal(prompt)
                    st.write(proposal['response'])

            elif choices == "Update CV":
                file = st.file_uploader("Upload your CV (PDF format)", type="pdf")
                if file and st.button("Update CV"):
                    cv = read_cv(file)
                    if cv:
                        embeddings = generate_ollama_embedding(cv)
                        update_cv = update_cv_content(cv, embeddings, user_data[0])
                        if update_cv:
                            st.success("Successfully updated CV.")
                    else:
                        st.error("Failed to read CV. Please check the file and try again.")

        else:
            file = st.file_uploader("Upload your CV (PDF format)", type="pdf")
            if file and st.button("Upload CV"):
                cv = read_cv(file)
                if cv:
                    embeddings = generate_ollama_embedding(cv)
                    metadata = json.dumps({"author": fullname, "source": "user_cv"}, indent=2)
                    insert_cv = insert_cv_content(cv, fullname, metadata, embeddings)
                    if insert_cv:
                        st.success("Successfully uploaded CV.")
                else:
                    st.error("Failed to read CV. Please check the file and try again.")

if __name__ == "__main__":
    main()
