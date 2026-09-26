import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# 1
from langchain_community.document_loaders import PyPDFDirectoryLoader
loader = PyPDFDirectoryLoader("documents")
docs = loader.load()

#2
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

chunks = text_splitter.split_documents(docs)

# 3.
from langchain_huggingface import HuggingFaceEmbeddings
embedding_model = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

# 4.
from langchain_community.vectorstores import FAISS

vector = FAISS.from_documents(chunks, embedding_model)

from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="groq"
)

def lords_bot(ques):
    result = vector.similarity_search(ques)
    
    context = ""
    for res in result:
        context += res.page_content + "\n\n"
        
    prompt = f"""
        You are an Lords College AI Assistant. Answer the user's question only using given context.
       
        context: {context}
        question: {ques}
    """
    response = model.invoke(prompt)
    return response.content



import streamlit as st
import time

st.set_page_config(
    page_title="Lords College AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(0, 255, 255, 0.15), transparent 25%),
        radial-gradient(circle at 90% 80%, rgba(138, 43, 226, 0.18), transparent 25%),
        linear-gradient(135deg, #050816, #0b1026, #080b18);
    color: white;
    overflow-x: hidden;
}

/* Animated background */
.stApp::before {
    content: "";
    position: fixed;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: rgba(0, 255, 255, 0.08);
    filter: blur(100px);
    top: -150px;
    left: -150px;
    animation: floatOrb 8s ease-in-out infinite alternate;
    z-index: -1;
}

.stApp::after {
    content: "";
    position: fixed;
    width: 450px;
    height: 450px;
    border-radius: 50%;
    background: rgba(150, 0, 255, 0.08);
    filter: blur(100px);
    bottom: -150px;
    right: -100px;
    animation: floatOrb2 10s ease-in-out infinite alternate;
    z-index: -1;
}

@keyframes floatOrb {
    from {
        transform: translate(0, 0);
    }
    to {
        transform: translate(150px, 100px);
    }
}

@keyframes floatOrb2 {
    from {
        transform: translate(0, 0);
    }
    to {
        transform: translate(-120px, -80px);
    }
}

/* Main title */
.hero {
    text-align: center;
    padding: 40px 10px 20px;
    animation: fadeDown 1s ease;
}

.hero-icon {
    font-size: 70px;
    animation: robotFloat 3s ease-in-out infinite;
    filter: drop-shadow(0 0 25px #00ffff);
}

.hero h1 {
    font-size: 48px;
    font-weight: 800;
    margin: 5px 0;
    background: linear-gradient(
        90deg,
        #00ffff,
        #ffffff,
        #9d4edd,
        #00ffff
    );
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 5s linear infinite;
}

.hero p {
    color: #aeb8d4;
    font-size: 17px;
}

@keyframes robotFloat {
    0%, 100% {
        transform: translateY(0) rotate(0deg);
    }
    50% {
        transform: translateY(-15px) rotate(3deg);
    }
}

@keyframes gradientMove {
    0% { background-position: 0%; }
    100% { background-position: 300%; }
}

@keyframes fadeDown {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Glass card */
.glass-card {
    max-width: 900px;
    margin: 20px auto;
    padding: 30px;
    border-radius: 25px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(20px);
    box-shadow:
        0 0 30px rgba(0,255,255,0.08),
        inset 0 0 30px rgba(255,255,255,0.02);
    animation: cardAppear 1s ease;
}

@keyframes cardAppear {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* Text area */
textarea {
    background: rgba(0,0,0,0.35) !important;
    color: white !important;
    border: 1px solid rgba(0,255,255,0.25) !important;
    border-radius: 18px !important;
    transition: all 0.3s ease !important;
}

textarea:focus {
    border: 1px solid #00ffff !important;
    box-shadow: 0 0 20px rgba(0,255,255,0.25) !important;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 55px;
    border: none;
    border-radius: 16px;
    color: white;
    font-size: 17px;
    font-weight: 700;

    background: linear-gradient(
        90deg,
        #00bcd4,
        #007bff,
        #8e2de2,
        #00bcd4
    );

    background-size: 300%;
    animation: buttonGradient 4s linear infinite;

    box-shadow:
        0 0 15px rgba(0,255,255,0.35);

    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow:
        0 0 25px rgba(0,255,255,0.7),
        0 0 50px rgba(140,0,255,0.3);
}

@keyframes buttonGradient {
    0% { background-position: 0%; }
    100% { background-position: 300%; }
}

/* Response box */
.response-box {
    margin-top: 30px;
    padding: 25px;
    border-radius: 20px;

    background: linear-gradient(
        135deg,
        rgba(0,255,255,0.08),
        rgba(140,0,255,0.08)
    );

    border: 1px solid rgba(0,255,255,0.2);

    box-shadow:
        0 0 25px rgba(0,255,255,0.08);

    animation: responseAppear 0.7s ease;
}

@keyframes responseAppear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.response-title {
    color: #00ffff;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* Status */
.status {
    text-align: center;
    color: #7fffd4;
    font-size: 14px;
    margin-top: 20px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%,100% {
        opacity: 0.4;
    }
    50% {
        opacity: 1;
    }
}

/* Footer */
.footer {
    text-align: center;
    color: #66708f;
    margin-top: 40px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="hero-icon">🤖</div>
    <h1>Lords College AI Assistant</h1>
    <p>Your intelligent academic companion ✨</p>
</div>
""", unsafe_allow_html=True)


# ---------- MAIN CARD ----------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

st.markdown(
    "<h3 style='color:#ffffff;'>💬 Ask your AI assistant</h3>",
    unsafe_allow_html=True
)

que = st.text_area(
    "Enter your query",
    placeholder="✨ Ask anything about Lords College...",
    height=140,
    label_visibility="collapsed"
)

ask = st.button("🚀  ASK AI")

st.markdown('</div>', unsafe_allow_html=True)


# ---------- AI RESPONSE ----------
if ask:

    if not que.strip():

        st.warning("⚠️ Please enter a query first.")

    else:

        # Animated loading
        loading = st.empty()

        messages = [
            "🔮 Understanding your question...",
            "🧠 Processing information...",
            "⚡ Generating intelligent response...",
            "✨ Almost ready..."
        ]

        for msg in messages:
            loading.markdown(
                f"<div class='status'>{msg}</div>",
                unsafe_allow_html=True
            )
            time.sleep(0.45)

        loading.empty()

        # Your AI function
        response = lords_bot(que)

        # Response container
        st.markdown("""
        <div class="response-box">
            <div class="response-title">
                🤖 Lords AI Response
            </div>
        """, unsafe_allow_html=True)

        st.write(response)

        st.markdown("</div>", unsafe_allow_html=True)


# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    ⚡ Powered by Lords College AI • Intelligent • Fast • Helpful
</div>
""", unsafe_allow_html=True)
