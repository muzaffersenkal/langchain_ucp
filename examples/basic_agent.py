"""Basic example: Create a shopping agent with UCPToolkit.

Prerequisites:
- pip install langchain-ucp langchain-openai langgraph
- Set OPENAI_API_KEY environment variable
- UCP merchant server running at http://localhost:8000
"""

import asyncio
import os

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from langchain_ucp import UCPToolkit


async def main():
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        return

    # Create toolkit
    toolkit = UCPToolkit(merchant_url="http://localhost:8000")

    # Create agent
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    agent = create_react_agent(llm, toolkit.get_tools())

    # Run agent
    result = await agent.ainvoke({
        "messages": [HumanMessage(content="Search for roses and add them to my cart")]
    })

    # Print response
    print(result["messages"][-1].content)

    # Cleanup
    await toolkit.close()


if __name__ == "__main__":
    asyncio.run(main())
