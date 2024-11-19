import streamlit as st
from database import (
    insert_cv_content, get_latest_cv,
    update_cv_content, get_name
)
from llmodel import create_embeddings,generate_response
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
                    job_embedding = create_embeddings(job_description)
                    #print(job_embedding)
                    content = get_latest_cv(job_embedding,user_data[0])
                    prompt = (
                        f"You're a respectful and honest assistant. Create a cover letter "
                        f"based on the job description: {job_description} and using this CV: {content}. "
                        f"If you cannot write the proposal, please say so."
                    )
                    cover_letter = generate_response(prompt)
                    st.write(cover_letter['response'])

            elif choices == "Generate Proposal":
                job_description = st.text_area("Please enter the job description:")
                if st.button("Generate Proposal"):
                    job_embedding = create_embeddings(job_description)
                    content = get_latest_cv(job_embedding,user_data[0])
                    prompt = (
                        f"You're a respectful and honest assistant. Create a job proposal "
                        f"based on the job description: {job_description} and using this CV: {content}. "
                        f"If you cannot write the proposal, please say so."
                    )
                    proposal = generate_response(prompt)
                    st.write(proposal['response'])

            elif choices == "Update CV":
                file = st.file_uploader("Upload your CV (PDF format)", type="pdf")
                if file and st.button("Update CV"):
                    cv = read_cv(file)
                    if cv:
                        embeddings = create_embeddings(cv)
                        update_cv = update_cv_content(cv, user_data[0],embeddings)
                        if update_cv:
                            st.success("Successfully updated CV.")
                    else:
                        st.error("Failed to read CV. Please check the file and try again.")

        else:
            file = st.file_uploader("Upload your CV (PDF format)", type="pdf")
            if file and st.button("Upload CV"):
                cv = read_cv(file)
                if cv:
                    embeddings = create_embeddings(cv)
                    print(embeddings)
                    metadata = json.dumps({"author": fullname, "source": "user_cv"}, indent=2)
                    insert_cv = insert_cv_content(cv, fullname, metadata,embeddings)
                    if insert_cv:
                        st.success("Successfully uploaded CV.")
                else:
                    st.error("Failed to read CV. Please check the file and try again.")

if __name__ == "__main__":
    main()
