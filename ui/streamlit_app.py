import os
import streamlit as st
import pandas as pd
import requests
import tempfile
import time

# Set wide layout
st.set_page_config(page_title="📊 AI Analytics Agent", layout="wide")

# ======= CONFIG =======
API_URL = st.secrets["api_url"]
SECRET_ID = st.secrets["secret_id"]
SECRET_KEY = st.secrets["secret_key"]

# ======= SESSION STATE SETUP =======
for key in ["bearer_token", "token_expiry"]:
    if key not in st.session_state:
        st.session_state[key] = None

TOKEN_EXPIRE_SECONDS = 360
TOKEN_REFRESH_BUFFER = 30

# ======= TOKEN HANDLING =======
def get_token(secret_id, secret_key):
    try:
        res = requests.post(
            f"{API_URL}/auth/token",
            json={"secret_id": secret_id, "secret_key": secret_key},
        )
        if res.status_code == 200:
            token_info = res.json()
            st.session_state.bearer_token = token_info["access_token"]
            st.session_state.token_expiry = time.time() + token_info.get("expires_in", 3600) - 30
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Token request failed: {e}")
        return False

def ensure_token():
    token_expiry = st.session_state.get("token_expiry")
    if (
            "bearer_token" not in st.session_state
            or token_expiry is None
            or time.time() >= token_expiry
    ):
        # Try to refresh if credentials are available
        if "secret_id" in st.session_state and "secret_key" in st.session_state:
            return get_token(st.session_state.secret_id, st.session_state.secret_key)
        else:
            return False
    return True

# ======= AUTH UI =======
with st.sidebar:
    st.header("🔐 Login (One-time only)")
    st.session_state.secret_id = st.text_input("Secret ID", type="password")
    st.session_state.secret_key = st.text_input("Secret Key", type="password")
    if st.button("Generate Token"):
        if get_token(st.session_state.secret_id, st.session_state.secret_key):
            st.success("Token generated and stored successfully.")

# ======= API CALL FUNCTION =======
def send_authenticated_request(endpoint, payload):
    if not ensure_token():
        st.warning("⚠️ Could not authenticate. Please check your credentials.")
        return None

    headers = {"Authorization": f"Bearer {st.session_state.bearer_token}"}
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

# ======= Initialize chat states =======
for key in ["df_chat_history", "context_chat_history", "sql_chat_history"]:
    if key not in st.session_state:
        st.session_state[key] = []

# ======= UI Styling =======
st.markdown("""
    <style>
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] {
        display: flex;
        align-items: center;
    }
    div[data-testid="stRadio"] p {
        margin-right: 30px;
        font-size: 28px !important;
        color: #1a73e8 !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# ======= Option Selection =======
option = st.radio("Choose an option:", ("DataFrame Agent", "Context Agent", "SQL Agent"), horizontal=True)

# ======= DataFrame Agent =======
if option == "DataFrame Agent":
    st.header("📊 Analytics Dataframe Chatbot")

    @st.cache_data
    def load_default_data():
        return pd.read_csv("data/retail_transactions_dataset.csv")

    if "df" not in st.session_state:
        st.session_state.df = load_default_data()

    uploaded_file = st.file_uploader("Upload your data file", type=["csv", "xlsx", "xls"])
    if uploaded_file:
        prev_file_name = st.session_state.get("last_df_file")
        if uploaded_file.name != prev_file_name:
            # New file detected
            if uploaded_file.name.endswith(".csv"):
                st.session_state.df = pd.read_csv(uploaded_file)
            else:
                st.session_state.df = pd.read_excel(uploaded_file)

            st.session_state.last_df_file = uploaded_file.name
            st.session_state.df_chat_history = []  # Only reset on new upload

            df_json = st.session_state.df.to_json(orient="split")
            result = send_authenticated_request("update-df", {"data": df_json})
            if result:
                st.success("✅ LLM Data (Tabular) updated successfully!")
            else:
                st.error("❌ Failed to update LLM Data (Tabular).")

    st.write("#### 📄 Data Preview (Used by LLM Agent):")
    st.dataframe(st.session_state.df.head(25), height=200)

    for msg in st.session_state.df_chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question about the DataFrame:")
    if user_input:
        st.session_state.df_chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            loading = st.empty()
            loading.markdown("...")

        messages = [{"role": "system", "content": "You are a helpful assistant"}] + st.session_state.df_chat_history[-5:]
        result = send_authenticated_request("chat", {"messages": messages})
        assistant_reply = result["response"] if result else "❌ Error retrieving response."

        loading.markdown(assistant_reply)
        st.session_state.df_chat_history.append({"role": "assistant", "content": assistant_reply})

# ======= Context Agent =======
elif option == "Context Agent":
    st.header("📚 Analytics Context Chatbot")

    @st.cache_data
    def load_default_context():
        with open("data/retail_transactions_description.txt", "r", encoding="utf-8") as file:
            return file.read()

    if "context_text" not in st.session_state:
        st.session_state.context_text = load_default_context()

    context_file = st.file_uploader("Upload a context file (.txt)", type=["txt"])
    if context_file:
        prev_context_file = st.session_state.get("last_context_file")
        if context_file.name != prev_context_file:
            st.session_state.context_text = context_file.read().decode("utf-8")
            st.session_state.last_context_file = context_file.name

            result = send_authenticated_request("update-context", {"text": st.session_state.context_text})
            if result:
                st.success("✅ RAG context updated successfully!")
                st.session_state.context_chat_history = []  # Only clear if new file
            else:
                st.error("❌ Failed to update RAG context.")
    else:
        send_authenticated_request("update-context", {"text": st.session_state.context_text})

    st.write("#### 📄 Context File Preview (Used by RAG Agent):")
    st.text_area("Context Preview", st.session_state.context_text, height=150, disabled=True)

    for msg in st.session_state.context_chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    context_input = st.chat_input("Ask a question about the Dataset Documentation:")
    if context_input:
        st.session_state.context_chat_history.append({"role": "user", "content": context_input})

        with st.chat_message("user"):
            st.markdown(context_input)

        with st.chat_message("assistant"):
            loading = st.empty()
            loading.markdown("...")

        messages = [{"role": "system", "content": "You are a helpful assistant"}] + st.session_state.context_chat_history[-5:]
        result = send_authenticated_request("context", {"messages": messages})
        reply = result["response"] if result else "❌ Error retrieving response."

        loading.markdown(reply)
        st.session_state.context_chat_history.append({"role": "assistant", "content": reply})

# ======= SQL Agent =======
elif option == "SQL Agent":
    st.header("🗄️ SQL Agent Chatbot")

    DEFAULT_DB_FILE = "data/retail_transactions_data.db"
    DEFAULT_DB_URI = f"sqlite:///{DEFAULT_DB_FILE}"

    if "sql_db_uri" not in st.session_state:
        st.session_state.sql_db_uri = DEFAULT_DB_URI

    uploaded_db = st.file_uploader("Upload a new SQLite DB file (.db)", type=["db", "sqlite"])
    if uploaded_db:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
            tmp.write(uploaded_db.getbuffer())
            tmp_path = tmp.name

        new_db_uri = f"sqlite:///{tmp_path}"
        st.session_state.sql_db_uri = new_db_uri
        result = send_authenticated_request("update-sql", {"db_uri": new_db_uri})

        if result:
            st.success(f"✅ SQL DB updated: {uploaded_db.name}")
            st.session_state.sql_chat_history = []
        else:
            st.error("❌ Failed to update SQL DB.")

    st.write(f"#### Current DB: `{st.session_state.sql_db_uri}`")

    for msg in st.session_state.sql_chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    sql_input = st.chat_input("Ask a question about the SQL database:")
    if sql_input:
        st.session_state.sql_chat_history.append({"role": "user", "content": sql_input})

        with st.chat_message("user"):
            st.markdown(sql_input)

        with st.chat_message("assistant"):
            loading = st.empty()
            loading.markdown("...")

        messages = [{"role": "system", "content": "You are an expert SQL assistant."}] + st.session_state.sql_chat_history[-5:]
        result = send_authenticated_request("sql", {"messages": messages})
        reply = result["response"] if result else "❌ Error retrieving response."

        loading.markdown(reply)
        st.session_state.sql_chat_history.append({"role": "assistant", "content": reply})

# ======= Footer =======
st.markdown("""
    <script>
    setTimeout(function() {
        var container = window.parent.document.querySelector('.main, body, html');
        if (container) {
            container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
        }
    }, 1000);
    </script>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .bottom-right-credit {
        position: fixed;
        bottom: 10px;
        left: 30%;
        font-weight: bold;
        font-size: 16px;
        color: black;
        background-color: rgba(255, 255, 255, 0.85);
        padding: 6px 12px;
        border-radius: 8px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        z-index: 100;
        font-family: Arial, sans-serif;
    }
    .bottom-right-credit a {
        color: black;
        text-decoration: none;
        font-weight: 600;
        margin-left: 4px;
        margin-right: 8px;
    }
    .bottom-right-credit a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="bottom-right-credit">
        Created by - Sagar Maru (
        <a href="https://www.kaggle.com/marusagar" target="_blank">kaggle.com/marusagar</a>,
        || <a href="https://github.com/sagar-maru/" target="_blank">github.com/sagar-maru</a>,
        || <a href="https://www.linkedin.com/in/sagarmaru" target="_blank">linkedin.com/in/sagarmaru</a>
        )
    </div>
""", unsafe_allow_html=True)
