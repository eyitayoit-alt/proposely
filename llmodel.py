from ollama import Client
client = Client(host='http://localhost:11434')

def create_embeddings(docu):
    embeddings = client.embeddings(model='nomic-embed-text',prompt=docu)
    print(embeddings)
    return embeddings["embedding"]

def generate_response(prompt: str):
    output = client.generate(
        model="llama3.2",prompt=prompt
    )
    return output
