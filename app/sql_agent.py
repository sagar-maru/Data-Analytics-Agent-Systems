import os
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.base import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType

# === Constants ===
DEFAULT_DB_PATH = "data/retail_transactions_data.db"
DEFAULT_DB_URI = f"sqlite:///{DEFAULT_DB_PATH}"

# === Initialize LLM ===
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

# === Create initial SQL DB connection ===
db = SQLDatabase.from_uri(DEFAULT_DB_URI)

# === Build agent ===
sql_agent = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS
)

# === SQL Agent Query Handler ===
def query_sql_data(question: str):
    print("\n[User Query]:", question)
    response = sql_agent.run(question)
    print("[SQL Agent Response]:", response)
    return response

# === Replace DB dynamically ===
def update_sql_database(new_db_uri: str):
    global db, sql_agent
    if not new_db_uri.startswith("sqlite:///"):
        raise ValueError("Only sqlite:/// URIs are supported in this example.")

    print(f"🔄 Switching to new DB: {new_db_uri}")
    db = SQLDatabase.from_uri(new_db_uri)

    sql_agent = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS
    )

# === Optional: Direct Test ===
# def main():
#     query_sql_data("What are the total sales by Customer Segment?")
#
# if __name__ == "__main__":
#     main()
