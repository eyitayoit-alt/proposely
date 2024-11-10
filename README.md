# Proposely
  A Job proposal and Cover letter generator App.

## Introduction
Need a cover letter or job proposal on the fly? Proposely is here for you. Upload your CV and Proposely start generating Cover letter and Job. Proposely is built using Ollama LLM, Postgres, pgvector, pgai and pgvector scale.


## Setup
### On linux

Open a new terminal and run ` chmod +777 ./install.sh`

Then run `./install.sh`

After successful installation
Run ollama serve
Run ollama pull 'nomic-embed-text'
Run ollama pull  'llama3.2'

Change the `example.env` to `.env` add the Database credentials in the  `pginstallation.sh` to the `.env` file.

Run `streamlit run app` 

### On Mac and Windows
Download Docker if not installed

Run 

