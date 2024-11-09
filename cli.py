from database import (
    insert_cv_content, get_latest_cv, generate_proposal,
    update_cv_content, generate_ollama_embedding,get_name
)
from cvreader import read_cv
import json

def main():
    
        # Ask the user to provide CV file and job description
    print("Welcome! Enter your full name to begin or type 'exit' to quit.")
    fullname = input("Please Enter your name: ").strip()
        
        # Check if the user wants to exit
    if fullname.lower() == "exit":
        print("Exiting program. Goodbye!")
        return
    
    while True:
        user_data = get_name(fullname)
        if user_data:
                print(user_data[0])
                print("Do you want to generate a cover letter/proposal or update your CV?")
                choices = input("Press 1 to generate cover letter, 2 to generate proposal, 3 to update CV: ").strip()
                    
                if choices == "1":
                    job_description = input("Please enter the job description: ").strip("< > / ./")
                    job_embedding = generate_ollama_embedding(job_description)
                    content,similarity = get_latest_cv(job_embedding)
                    prompt = (
                        f"You're a respectful and honest assistant. Create a cover letter "
                        f"based on the job description: {job_description} and using this CV: {content}. "
                        f"If you cannot write the proposal, please say so."
                    )
                    cover_letter = generate_proposal(prompt)
                    print(cover_letter['response'])
                elif choices == "2":
                    job_description = input("Please enter the job description: ").strip()
                    job_embedding = generate_ollama_embedding(job_description)
                    content,similarity = get_latest_cv(job_embedding)
                    prompt = (
                        f"You're a respectful and honest assistant. Create a job proposal "
                        f"based on the job description: {job_description} and using this CV: {content}. "
                        f"If you cannot write the proposal, please say so."
                    )
                    proposal = generate_proposal(prompt)
                    print(proposal['response'])
                elif choices == "3":
                    file_path = input("Enter the path to your CV file (PDF format): ")
                    print("Updating CV")
                    cv = read_cv(file_path)
                        
                    if not cv:
                        print("Failed to read CV. Please check the file path and try again.")
                        return
                        
                    embeddings = generate_ollama_embedding(cv)
                    update_cv = update_cv_content(cv, embeddings, fullname)
                        
                    if update_cv:
                        print("Successfully updated CV.")

                    else:
                        print("Invalid choice. Please try again.")    
        else:
            file_path = input("Enter the path to your CV file (PDF format): ")
            print("Uploading CV")
            cv = read_cv(file_path)
                
            if not cv:
                print("Failed to read CV. Please check the file path and try again.")
                return   
            embeddings = generate_ollama_embedding(cv)
            metadata = json.dumps({
                "author": fullname,
                "source": "user_cv"
            }, indent=2)
                
            insert_cv = insert_cv_content(cv, fullname, metadata, embeddings)
                
            if insert_cv:
                print("Successfully uploaded CV.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting the App")
        SystemExit(0)
