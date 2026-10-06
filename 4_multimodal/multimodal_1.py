from dotenv import load_dotenv
import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b",temperature=0)


agent = create_agent(
    tools=[],
    model=llm,
    system_prompt=(
        "You are an image agent"
    )
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Which bird is this in the photo ? print only the name of the bird: " #provide the link of the bird
                ),
            }
        ]
    }
)

print(result["messages"][-1].content)