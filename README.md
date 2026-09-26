# RAG-based-Chatbot

steps:
0.  
pip install langchain langchain-community
pip install dotenv faiss-cpu
pip install langchain-groq langchain-google-genai 
pip install pypdf

hugging face:
pip install langchain-huggingface sentence-transformers

or

(pip install langchain langchain-community python-dotenv faiss-cpu langchain-groq langchain-google-genai
pip install pypdf
)


1. 
read and Load all the pdf documents

2.
split documents into chunks 

3.
Create embeeding model (hugging face)

4.
 save the embding into vector db faiss

5. initialize groq

6. do similarity search

7. Front-end (Streamlit)
	- app.py
	
