"""A2UI system prompt helpers for langchain-ucp.

This module provides system prompt generation for A2UI output formatting.
A2UI is NOT a tool - it's a standardization for output formats. The LLM
generates A2UI JSON directly in its response using a delimiter pattern.

Usage:
    >>> from langchain_ucp.a2ui import get_a2ui_system_prompt
    >>> 
    >>> # Add to your agent's system prompt
    >>> system_prompt = base_prompt + get_a2ui_system_prompt(
    ...     include_schema=True,
    ...     include_commerce_examples=True,
    ... )
"""

import json
import logging
from typing import Any

from langchain_ucp.a2ui.schema import A2UI_MESSAGE_SCHEMA, wrap_as_json_array

logger = logging.getLogger(__name__)

# The delimiter used to separate text content from A2UI JSON in responses
A2UI_DELIMITER = "---a2ui_JSON---"


def _get_commerce_examples() -> str:
    """Generate commerce UI examples using templates.
    
    Uses the helper functions from templates.py to generate consistent examples.
    """
    # Import here to avoid circular imports
    from langchain_ucp.a2ui.templates import (
        create_product_card,
        create_product_list,
        create_checkout_ui,
        create_order_confirmation,
    )
    
    examples = []
    
    # Product Card Example
    product_card = create_product_card(
        product_id="product-123",
        name="Red Roses",
        price="$29.99",
        image_url="https://example.com/roses.jpg",
        description="Beautiful red roses bouquet",
    )
    examples.append(f"""
=== PRODUCT CARD ===
A single product card with image, name, price, and add to cart button:

{A2UI_DELIMITER}
{json.dumps(product_card, indent=2)}
""")
    
    # Product List Example - Show multiple products to demonstrate list capability
    products = [
        {"id": "roses", "name": "Red Roses", "price": "$29.99", "imageUrl": "https://example.com/roses.jpg"},
        {"id": "tulips", "name": "Tulips", "price": "$19.99", "imageUrl": "https://example.com/tulips.jpg"},
        {"id": "sunflowers", "name": "Sunflowers", "price": "$24.99", "imageUrl": "https://example.com/sunflowers.jpg"},
        {"id": "lilies", "name": "White Lilies", "price": "$34.99", "imageUrl": "https://example.com/lilies.jpg"},
        {"id": "orchids", "name": "Orchids", "price": "$49.99", "imageUrl": "https://example.com/orchids.jpg"},
    ]
    product_list = create_product_list(
        title="Available Products",
        products=products,
    )
    examples.append(f"""
=== PRODUCT LIST ===
A list of products for search results. IMPORTANT: Include ALL products from search results, not just one or two:

{A2UI_DELIMITER}
{json.dumps(product_list, indent=2)}
""")
    
    # Checkout Example
    items = [
        {"title": "Red Roses", "quantity": 2, "total": "$59.98"},
    ]
    checkout = create_checkout_ui(
        checkout_id="checkout-123",
        items=items,
        total="$59.98",
    )
    examples.append(f"""
=== CHECKOUT FORM ===
A checkout form with order summary and shipping fields:

{A2UI_DELIMITER}
{json.dumps(checkout, indent=2)}
""")
    
    # Order Confirmation Example
    confirmation = create_order_confirmation(
        order_id="ORD-12345",
        items_summary="2x Red Roses",
        total="$59.98",
        shipping_address="123 Main St, New York, NY 10001",
        primary_color="#4CAF50",  # Green for success
    )
    examples.append(f"""
=== ORDER CONFIRMATION ===
An order confirmation card after successful purchase:

{A2UI_DELIMITER}
{json.dumps(confirmation, indent=2)}
""")
    
    return "\nCOMMERCE UI EXAMPLES:\n" + "\n".join(examples)


def get_a2ui_system_prompt(
    include_schema: bool = True,
    include_commerce_examples: bool = True,
) -> str:
    """Generate A2UI system prompt for the LLM.

    This function generates instructions for the LLM to output A2UI JSON
    as part of its response, using a delimiter pattern. The LLM should NOT
    call a tool - instead it directly generates the A2UI JSON.

    Args:
        include_schema: Whether to include the full A2UI schema.
        include_commerce_examples: Whether to include commerce-specific examples.

    Returns:
        System prompt string with A2UI instructions.
    """
    prompt_parts = [
        f"""
You can generate rich UIs using the A2UI (Agent-to-User Interface) format.

When you need to show products, checkout information, or order details to the user,
generate A2UI JSON in your response using the following format:

A2UI MESSAGE TYPES:
- beginRendering: Start a new UI surface with root component and styles
- surfaceUpdate: Define the component tree for a surface
- dataModelUpdate: Update data values that components reference
- deleteSurface: Remove a surface

IMPORTANT:
- Each UI must have a beginRendering, surfaceUpdate, and dataModelUpdate message
- The JSON must be a valid array of A2UI messages
- Do NOT wrap the JSON in markdown code blocks after the delimiter
- Only include the delimiter and JSON when you want to render a UI
- Component IDs must be unique and should NOT match data path names (e.g., use "product-name" not "name")
- When displaying product lists, include ALL products from the data source, not just one or two

RESPONSE FORMAT:
1. Your response MUST be in two parts, separated by the delimiter: `{A2UI_DELIMITER}`
2. The first part is your conversational text response.
3. The second part is a raw JSON array of A2UI messages (no markdown code blocks).

Example response structure:
Here are the flowers you requested!

{A2UI_DELIMITER}
[{{"beginRendering": ...}}, {{"surfaceUpdate": ...}}, {{"dataModelUpdate": ...}}]

"""
    ]

    if include_commerce_examples:
        prompt_parts.append(_get_commerce_examples())

    if include_schema:
        prompt_parts.append(f"""
---BEGIN A2UI JSON SCHEMA---
{json.dumps(wrap_as_json_array(A2UI_MESSAGE_SCHEMA), indent=2)}
---END A2UI JSON SCHEMA---
""")

    return "\n".join(prompt_parts)


def validate_a2ui_json(json_string: str, schema: dict[str, Any] | None = None) -> tuple[bool, list[dict[str, Any]] | None, str | None]:
    """Validate A2UI JSON string against the schema.

    Args:
        json_string: The JSON string to validate.
        schema: Optional custom schema. Uses default A2UI schema if not provided.

    Returns:
        Tuple of (is_valid, parsed_data, error_message).
    """
    if schema is None:
        schema = wrap_as_json_array(A2UI_MESSAGE_SCHEMA)

    try:
        # Clean the JSON string (remove markdown code blocks if present)
        cleaned = json_string.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.lstrip("```json").lstrip("```").rstrip("```").strip()

        # Parse JSON
        parsed = json.loads(cleaned)

        # Auto-wrap single object in list
        if isinstance(parsed, dict):
            parsed = [parsed]

        if not isinstance(parsed, list):
            return False, None, "A2UI JSON must be a list of messages"

        # Validate against schema
        try:
            import jsonschema
            jsonschema.validate(instance=parsed, schema=schema)
        except ImportError:
            logger.warning("jsonschema not installed, skipping validation")
        except jsonschema.exceptions.ValidationError as e:
            return False, None, f"Schema validation failed: {e.message}"

        return True, parsed, None

    except json.JSONDecodeError as e:
        return False, None, f"Invalid JSON: {e}"


def parse_a2ui_response(response: str) -> tuple[str, list[dict[str, Any]] | None]:
    """Parse an LLM response that may contain A2UI JSON.

    Looks for the A2UI_DELIMITER in the response and splits it into
    text content and A2UI JSON.

    Args:
        response: The full LLM response string.

    Returns:
        Tuple of (text_content, a2ui_messages).
        a2ui_messages is None if no A2UI JSON found or if parsing failed.
    """
    if A2UI_DELIMITER not in response:
        return response, None

    parts = response.split(A2UI_DELIMITER, 1)
    text_content = parts[0].strip()
    json_string = parts[1].strip() if len(parts) > 1 else ""

    if not json_string:
        return text_content, None

    is_valid, parsed, error = validate_a2ui_json(json_string)
    if not is_valid:
        logger.warning(f"A2UI JSON validation failed: {error}")
        return text_content, None

    return text_content, parsed


def get_a2ui_schema() -> dict[str, Any]:
    """Get the A2UI message schema wrapped for array validation.

    Returns:
        The A2UI schema as a Python dict, ready for jsonschema validation.
    """
    return wrap_as_json_array(A2UI_MESSAGE_SCHEMA)
