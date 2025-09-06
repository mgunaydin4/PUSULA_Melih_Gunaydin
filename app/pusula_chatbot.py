from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv
import os
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

load_dotenv()

df = pd.read_excel("../data/Talent_Academy_Case_DT_2025.xlsx")
api_key = os.getenv("OPENAI_API_KEY")


def pusula_advisor(question):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        allow_dangerous_code=True,
        max_iterations=10,
        max_execution_time=60
    )

    response = agent_executor.invoke({"input": question})
    print(response['output'])
    return response['output']


if __name__ == "__main__":
    print(pusula_advisor("Kaç tane hasta vardır ?"))