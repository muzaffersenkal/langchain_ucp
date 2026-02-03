"""A2UI Agent Example: Create a shopping agent with rich UI rendering.

This example demonstrates how to use langchain-ucp with A2UI support
to render rich, interactive UIs for shopping experiences.

A2UI is NOT a tool - the LLM generates A2UI JSON directly in its response
using a delimiter pattern. The agent validates and parses the A2UI JSON.

Prerequisites:
- pip install langchain-ucp[a2ui] langchain-openai langgraph
- Set OPENAI_API_KEY environment variable
- UCP merchant server running at http://localhost:8000

Usage:
    python a2ui_agent.py              # Normal mode
    python a2ui_agent.py --verbose    # Verbose mode with debug logs
    python a2ui_agent.py -i           # Interactive mode
"""

import asyncio
import json
import os
import sys

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage

from langchain_ucp import UCPToolkit, Product
from langchain_ucp.a2ui import (
    get_a2ui_system_prompt,
    parse_a2ui_response,
    create_product_list,
    A2UI_DELIMITER,
)


# Define your product catalog
PRODUCTS = [
    Product(id="bouquet_roses", title="Bouquet of Red Roses"),
    Product(id="bouquet_sunflowers", title="Sunflower Bundle"),
    Product(id="bouquet_tulips", title="Spring Tulips"),
    Product(id="orchid_white", title="White Orchid"),
    Product(id="pot_ceramic", title="Ceramic Pot"),
    Product(id="gardenias", title="Gardenias"),
]


def get_system_prompt() -> str:
    """Build system prompt with A2UI instructions."""
    base_prompt = """You are a helpful shopping assistant for a flower shop.

You can help users:
1. Search for products in our catalog
2. Add items to their cart
3. View and manage their checkout
4. Complete purchases

Use the available tools to fulfill user requests.

IMPORTANT: When showing products to users, you MUST generate A2UI JSON
to render rich UI cards with images, prices, and interactive buttons.
This provides a much better shopping experience than plain text.
"""
    return base_prompt + get_a2ui_system_prompt(
        include_schema=True,
        include_commerce_examples=True,
    )


async def main():
    """Run a simple demonstration of the A2UI agent."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        return

    # Check for verbose flag
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    # Create toolkit
    toolkit = UCPToolkit(
        merchant_url="http://localhost:8000",
        products=PRODUCTS,
        verbose=verbose,
    )

    # Create agent with system prompt
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    agent = create_react_agent(
        llm,
        toolkit.get_tools(),
    )

    print("=" * 60)
    print("A2UI Shopping Agent")
    print("=" * 60)
    print("\nThis agent renders rich UIs using A2UI format.")
    print(f"A2UI delimiter: {A2UI_DELIMITER}")
    print("\nTry asking: 'Show me the roses' or 'Search for flowers'\n")

    # Example: Show products with A2UI
    print("Example: Requesting product display...")
    result = await agent.ainvoke({
        "messages": [
            SystemMessage(content=get_system_prompt()),
            HumanMessage(content="Show me available flowers")
        ]
    })

    response = result["messages"][-1].content
    print("\nRaw LLM response:")
    print("-" * 40)
    print(response[:500] + "..." if len(response) > 500 else response)
    print("-" * 40)

    # Parse A2UI from response
    text_content, a2ui_messages = parse_a2ui_response(response)

    print("\nParsed content:")
    print(f"  Text: {text_content[:200]}..." if text_content else "  Text: (none)")
    
    if a2ui_messages:
        print(f"\n  A2UI: {len(a2ui_messages)} messages")
        print("=" * 60)
        print("A2UI Payload:")
        print("=" * 60)
        print(json.dumps(a2ui_messages, indent=2))
    else:
        print("\n  A2UI: (none generated)")

    print("\n" + "=" * 60)

    # Example 2: Create a product list programmatically
    print("\nExample 2: Creating product list programmatically...")
    
    products_data = [
        {"id": "roses", "name": "Red Roses", "price": "$29.99", "imageUrl": "https://example.com/roses.jpg"},
        {"id": "tulips", "name": "Spring Tulips", "price": "$19.99", "imageUrl": "https://example.com/tulips.jpg"},
        {"id": "orchid", "name": "White Orchid", "price": "$39.99", "imageUrl": "https://example.com/orchid.jpg"},
    ]
    
    a2ui_payload = create_product_list(
        title="Featured Flowers",
        products=products_data,
        primary_color="#E91E63",
    )
    
    print("\nProgrammatically generated A2UI:")
    print(json.dumps(a2ui_payload, indent=2))

    # Cleanup
    await toolkit.close()


async def interactive_mode():
    """Run in interactive chat mode."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        return

    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    toolkit = UCPToolkit(
        merchant_url="http://localhost:8000",
        products=PRODUCTS,
        verbose=verbose,
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    agent = create_react_agent(llm, toolkit.get_tools())

    print("=" * 60)
    print("A2UI Shopping Agent - Interactive Mode")
    print("=" * 60)
    print(f"A2UI delimiter: {A2UI_DELIMITER}")
    print("Type 'quit' to exit\n")

    messages = [SystemMessage(content=get_system_prompt())]
    last_a2ui = None

    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                break
            
            if user_input.lower() == 'a2ui':
                if last_a2ui:
                    print("\nLast A2UI Payload:")
                    print(json.dumps(last_a2ui, indent=2))
                else:
                    print("\nNo A2UI payload generated yet.")
                continue

            messages.append(HumanMessage(content=user_input))
            
            result = await agent.ainvoke({"messages": messages})
            
            response = result["messages"][-1].content
            
            # Parse A2UI from response
            text_content, a2ui_messages = parse_a2ui_response(response)
            
            if text_content:
                print(f"\nAssistant: {text_content}\n")
            
            if a2ui_messages:
                last_a2ui = a2ui_messages
                print(f"[A2UI UI rendered - {len(a2ui_messages)} messages - type 'a2ui' to see payload]\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    await toolkit.close()
    print("\nGoodbye!")


if __name__ == "__main__":
    if "--interactive" in sys.argv or "-i" in sys.argv:
        asyncio.run(interactive_mode())
    else:
        asyncio.run(main())
