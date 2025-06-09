import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI

# # Load CSV on server start (default)
DEFAULT_DATA_PATH = "data/retail_transactions_dataset.csv"
df = pd.read_csv(DEFAULT_DATA_PATH)

# Initialize LLM
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

# Create agent
pandas_agent = create_pandas_dataframe_agent(
    llm=llm,
    df=df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True
)

# Agent Query Handler
def query_data_analytics(question: str):
    print("\n[User Query]:", question)
    response = pandas_agent.run(question)
    print("[Agent Response]:", response)
    return response

# Allow dynamic replacement of the dataframe
def update_dataframe(new_df: pd.DataFrame):
    global df, pandas_agent
    df = new_df
    pandas_agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True
    )

# def main():
#     # Your code goes here
#     print("Hello from the main function!")
#
# if __name__ == "__main__":
#     main()