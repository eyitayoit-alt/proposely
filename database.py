import psycopg2
from config import POSTGRES_DB, HOST, POSTGRES_PASSWORD, PORT, POSTGRES_USER

# Function to establish a database connection
def db_conn():
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            host=HOST,
            password=POSTGRES_PASSWORD,
            port=PORT,
            user=POSTGRES_USER
        )
        return conn
    except psycopg2.Error as e:
        raise ConnectionError(f"Database connection error: {e}")
# Function to retrieve name of user
def get_name(data):
    conn = db_conn()
    try:
        with conn.cursor() as cur:
            
            cur.execute("""
                SELECT 
                        fullname
                FROM cvtable
                WHERE fullname = %s
                LIMIT 1
            """, (data,))
            name = cur.fetchone()
            return name if name else None
    except Exception as e:
        print(f"Failed to retrieve CV: {e}")
    finally:
        conn.close()

# Function to insert CV content into the database
def insert_cv_content(contents: str,fullname:str, metadata: dict,embedding):
    conn = db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO cvtable (content,fullname, metadata,embedding) VALUES (%s, %s, %s,%s)",
                (contents, fullname,str(metadata),embedding)  
            )
        conn.commit()
        return True
    except Exception as e:
        print(f"Failed to insert content: {e}")
    finally:
        conn.close()

# Function to insert CV content into the database
def update_cv_content(contents: str, embedding,fullname:str,):

    conn = db_conn()
    try:
        with conn.cursor() as cur:
           cur.execute(
               "UPDATE cvtable SET content = %s, embedding = %s WHERE fullname = %s",
               (contents, embedding, fullname)
               )
        conn.commit()
        return True
    except Exception as e:
        print(f"Failed to insert content: {e}")
    finally:
        conn.close()



# Function to retrieve the most recent CV content
def get_latest_cv(data,fullname):
    conn = db_conn()
    try:
        with conn.cursor() as cur:
            
            cur.execute("""
                SELECT 
                        content,
                        embedding <=> %s as distance
                FROM cvtable
                WHERE fullname= %s
                ORDER BY distance
                LIMIT 1
            """, (data,fullname))
            cv_content = cur.fetchone()
            return cv_content if cv_content else None
    except Exception as e:
        print(f"Failed to retrieve CV: {e}")
    finally:
        conn.close()

def generate_ollama_embedding(content: str):
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            host=HOST,
            password=POSTGRES_PASSWORD,
            port=PORT,
            user=POSTGRES_USER
        )

        with conn.cursor() as cur:
            cur.execute("""
                SELECT ai.ollama_embed('nomic-embed-text', %s) AS embedding
            """, (content,))
            embedding = cur.fetchone()
            return embedding[0] if embedding else None
    except Exception as e:
        print(f"Error generating Ollama embedding: {e}")
        return None
    finally:
        if conn:
            conn.close()

def generate_proposal(prompt):
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            host=HOST,
            password=POSTGRES_PASSWORD,
            port=PORT,
            user=POSTGRES_USER
        )

        with conn.cursor() as cur:
            cur.execute("""
                SELECT ai.ollama_generate
                ( 'llama3.2', %s ,host=>'http://ollama:11434/api/generate)
            """, (prompt,))
            proposal = cur.fetchone()
            return proposal[0] if proposal else None
    except Exception as e:
        print(f"Error generating proposal: {e}")
        return None
    finally:
        if conn:
            conn.close()


