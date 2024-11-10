# Job Proposal and Cover letter App

## Introduction
This app create cover letter and job proposal using users CV and Job description. The app is built using Ollama LLM, PGAI,PGVector Scale. It allows users to store the content of their cv in a database, input a job description and create a job proposal or cover letter from the CV and job description.

## System Requirement
- Minimum of 4 Gig RAM
- Dual Core Processor

## Getting Started
Run `curl -fsSL https://ollama.com/install.sh | sh` to install Ollama LLM on your local machine and make sure it is running.
Run:
  - ollama pull llama3.2
  - ollama pull nomic-embed-text
Install docker, after installation run  `docker compose up -d` to pull  `timescale/timescaledb-ha:pg16` image. Read more about Timescale here.

Install psql
Connect to the postgres database with the command below:
psql -h localhost -U postgres

In the postgres terminal, cope the the  `sql` statement in SQL.sql file and execute in the postgres terminal

Open a terminal run pip install -r requirement.txt
 
G