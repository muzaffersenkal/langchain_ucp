# LangChain UCP

LangChain toolkit for Universal Commerce Protocol (UCP) with A2UI support.

### Basic Agent Demo

https://private-user-images.githubusercontent.com/22756941/545214874-602f31b8-2623-49b1-9217-2c67f8d43ae0.mp4?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzAyMzYzNDgsIm5iZiI6MTc3MDIzNjA0OCwicGF0aCI6Ii8yMjc1Njk0MS81NDUyMTQ4NzQtNjAyZjMxYjgtMjYyMy00OWIxLTkyMTctMmM2N2Y4ZDQzYWUwLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAyMDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMjA0VDIwMTQwOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWQ3ODIyYzRlMjUxYjZkYzEwMTc0OGE1ZmNiNjI5ZDVkNDA2NjI0YmUxZTY3ZTVmMzM4NWZhNDQzMjcxZGJlODkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.QYh7hqofZ4tFj_OLTRoum404Q5B2WVNa2sgDqE3M930





## Overview

`langchain-ucp` provides LangChain tools and toolkit for building AI agents that can interact with [UCP](https://ucp.dev)-compliant merchants. It includes **A2UI (Agent-to-User Interface)** support for rendering rich, interactive UIs.

## Features

- **Full UCP Support**: Complete checkout flow - search, cart, shipping, payment
- **A2UI Integration**: Render rich UIs with product cards, checkout forms, order confirmations
- **LangChain Native**: Works seamlessly with LangChain and LangGraph agents
- **Type-Safe**: Full Pydantic model support

## Installation

```bash
# Basic installation
pip install langchain-ucp

# With A2UI support (recommended)
pip install langchain-ucp[a2ui]

# All features
pip install langchain-ucp[all]
```

## Quick Start

### Basic Usage (Text Only)

```python
from langchain_ucp import UCPToolkit, Product
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Define your product catalog
products = [
    Product(id="roses", title="Red Roses"),
    Product(id="tulips", title="Spring Tulips"),
    Product(id="orchid", title="White Orchid"),
]

# Create toolkit with product catalog
toolkit = UCPToolkit(
    merchant_url="http://localhost:8000",
    products=products,
)

# Create agent
llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(llm, toolkit.get_tools())

# Run agent
result = await agent.ainvoke({
    "messages": [{"role": "user", "content": "I want to buy some red roses"}]
})
```

### With A2UI (Rich UI Rendering)

A2UI is **not a tool** - it's an output format standardization. The LLM generates A2UI JSON directly in its response using a delimiter pattern (`---a2ui_JSON---`).

```python
from langchain_ucp import UCPToolkit, Product
from langchain_ucp.a2ui import (
    get_a2ui_system_prompt,
    parse_a2ui_response,
    A2UI_DELIMITER,
)
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Create toolkit
toolkit = UCPToolkit(
    merchant_url="http://localhost:8000",
    products=products,
)

# Build system prompt with A2UI instructions
base_prompt = "You are a helpful shopping assistant for a flower shop."
system_prompt = base_prompt + get_a2ui_system_prompt(
    include_schema=True,
    include_commerce_examples=True,
)

# Create LLM and get response
llm = ChatOpenAI(model="gpt-4o")
response = await llm.ainvoke([
    SystemMessage(content=system_prompt),
    HumanMessage(content="Show me your products"),
])

# Parse response to extract text and A2UI JSON
text_content, a2ui_messages = parse_a2ui_response(response.content)

# text_content: "Here are our available products!"
# a2ui_messages: [{beginRendering...}, {surfaceUpdate...}, {dataModelUpdate...}]
```

## A2UI Architecture

### UCP with A2UI - Rich UI Shopping Experience

https://private-user-images.githubusercontent.com/22756941/545214895-340c8e12-9af1-4a01-a815-8c490fa03894.mp4?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzAyMzY2MTksIm5iZiI6MTc3MDIzNjMxOSwicGF0aCI6Ii8yMjc1Njk0MS81NDUyMTQ4OTUtMzQwYzhlMTItOWFmMS00YTAxLWE4MTUtOGM0OTBmYTAzODk0Lm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAyMDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMjA0VDIwMTgzOVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWRiZGU0MmIxZWY4NDYzZTUzOGY1ZDJhNDVkMjlkZTZiZjY0M2RhYTg3OWUxNWQ1YzdhYTk4OTlmZjkwYmM1ZTQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.yDO7o5nd42NsuU3joV3LPbg1yxlzqxpymylYbKQLKJg

A2UI works through a delimiter-based approach:

1. **System Prompt**: Use `get_a2ui_system_prompt()` to add A2UI instructions
2. **LLM Response**: LLM generates text + delimiter + A2UI JSON
3. **Parse Response**: Use `parse_a2ui_response()` to split text and A2UI

```
LLM Response Format:
┌─────────────────────────────────────────┐
│ Here are the products you requested!    │  ← Text content
│                                         │
│ ---a2ui_JSON---                         │  ← Delimiter
│ [{"beginRendering": ...},               │
│  {"surfaceUpdate": ...},                │  ← A2UI JSON array
│  {"dataModelUpdate": ...}]              │
└─────────────────────────────────────────┘
```

### A2UI Message Types

| Message Type | Description |
|--------------|-------------|
| `beginRendering` | Initialize a UI surface with root component and styles |
| `surfaceUpdate` | Define the component tree for a surface |
| `dataModelUpdate` | Update data values that components reference |
| `deleteSurface` | Remove a surface |

### Available A2UI Templates

| Template | Description |
|----------|-------------|
| `ProductCardTemplate` | Single product card with image, name, price, add to cart |
| `ProductListTemplate` | Scrollable list of products |
| `CheckoutTemplate` | Checkout form with shipping address |
| `OrderConfirmationTemplate` | Order confirmation with success status |

### A2UI Helper Functions

```python
from langchain_ucp.a2ui import (
    # Prompt helpers
    get_a2ui_system_prompt,
    parse_a2ui_response,
    validate_a2ui_json,
    get_a2ui_schema,
    A2UI_DELIMITER,
    
    # Template functions
    create_product_card,
    create_product_list,
    create_checkout_ui,
    create_order_confirmation,
)

# Create a product card
card = create_product_card(
    product_id="roses",
    name="Red Roses",
    price="$29.99",
    image_url="https://example.com/roses.jpg",
    description="Beautiful fresh red roses",
)

# Create a product list
products_list = create_product_list(
    title="Featured Products",
    products=[
        {"id": "roses", "name": "Red Roses", "price": "$29.99", "imageUrl": "..."},
        {"id": "tulips", "name": "Tulips", "price": "$19.99", "imageUrl": "..."},
    ],
)

# Create checkout UI
checkout = create_checkout_ui(
    checkout_id="chk_123",
    items=[{"title": "Red Roses", "quantity": 2, "total": "$59.98"}],
    total="$64.98",
)

# Create order confirmation
confirmation = create_order_confirmation(
    order_id="ord_456",
    items_summary="2x Red Roses",
    total="$64.98",
    shipping_address="123 Main St, City, ST 12345",
)
```

### Standard A2UI Components

The standard component catalog includes:

- **Layout**: Row, Column, List, Card, Tabs, Divider, Modal
- **Content**: Text, Image, Icon, Video, AudioPlayer
- **Input**: Button, CheckBox, TextField, DateTimeInput, MultipleChoice, Slider

## Product Catalog

The `Product` model is for agent-side discovery.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | str | Yes | Unique product identifier (must match merchant's product ID) |
| `title` | str | Yes | Product display name (used for search) |

> **Note:** When UCP product discovery is implemented, the full product catalog (pricing, categories, descriptions, images) will be fetched directly from the merchant.

## Available Tools

| Tool | Description |
|------|-------------|
| `search_shopping_catalog` | Search the product catalog |
| `add_to_checkout` | Add products to cart |
| `remove_from_checkout` | Remove products from cart |
| `update_checkout` | Update product quantities |
| `get_checkout` | View current cart |
| `update_customer_details` | Add buyer info and address |
| `start_payment` | Prepare checkout for payment |
| `complete_checkout` | Complete purchase |
| `cancel_checkout` | Cancel checkout |
| `get_order` | Get order details |

## Configuration

```python
toolkit = UCPToolkit(
    merchant_url="http://localhost:8000",  # UCP merchant URL
    products=products,                      # Product catalog
    agent_name="my-agent",                  # Agent name for headers
    verbose=False,                          # Enable debug logging
)
```

## Examples

See the [examples](./examples) directory:

- `basic_agent.py` - Simple agent that adds items to cart
- `interactive_chat.py` - Interactive chat with the shopping agent
- `a2ui_agent.py` - Agent with A2UI rich UI rendering




## License

Apache License 2.0
