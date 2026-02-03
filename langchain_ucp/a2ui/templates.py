"""Commerce-specific A2UI UI templates for langchain-ucp.

This module provides pre-built templates for common commerce UIs:
- Product cards and lists
- Checkout forms
- Order confirmations
- Shopping cart

These templates can be used by LLM agents to render rich UIs.
"""

from typing import Any

from langchain_ucp.a2ui.constants import (
    DEFAULT_FONT,
    DEFAULT_PRIMARY_COLOR,
    SURFACE_ID_CHECKOUT,
    SURFACE_ID_ORDER_CONFIRMATION,
    SURFACE_ID_PRODUCT_DETAIL,
    SURFACE_ID_PRODUCTS,
)
from langchain_ucp.a2ui.types import (
    A2UIMessage,
    Component,
    DataEntry,
)


# -----------------------------------------------------------------------------
# Template Classes
# -----------------------------------------------------------------------------


class ProductCardTemplate:
    """Template for a single product card.

    Creates a card with image, name, price, description, and add to cart button.
    """

    SURFACE_ID = SURFACE_ID_PRODUCT_DETAIL

    @staticmethod
    def get_components() -> list[dict[str, Any]]:
        """Get component definitions for product card."""
        return [
            {"id": "card", "component": {"Card": {"child": "card-content"}}},
            {"id": "card-content", "component": {"Column": {
                "children": {"explicitList": [
                    "product-image",
                    "product-info",
                    "product-actions"
                ]}
            }}},
            {"id": "product-image", "component": {"Image": {
                "url": {"path": "imageUrl"},
                "usageHint": "largeFeature",
                "fit": "cover"
            }}},
            {"id": "product-info", "component": {"Column": {
                "children": {"explicitList": [
                    "product-name",
                    "product-price",
                    "product-description"
                ]}
            }}},
            {"id": "product-name", "component": {"Text": {
                "text": {"path": "name"},
                "usageHint": "h2"
            }}},
            {"id": "product-price", "component": {"Text": {
                "text": {"path": "price"},
                "usageHint": "h3"
            }}},
            {"id": "product-description", "component": {"Text": {
                "text": {"path": "description"},
                "usageHint": "body"
            }}},
            {"id": "product-actions", "component": {"Row": {
                "children": {"explicitList": ["add-to-cart-btn"]},
                "distribution": "end"
            }}},
            {"id": "add-to-cart-btn", "component": {"Button": {
                "child": "add-btn-text",
                "primary": True,
                "action": {
                    "name": "add_to_cart",
                    "context": [
                        {"key": "productId", "value": {"path": "id"}},
                        {"key": "quantity", "value": {"literalNumber": 1}}
                    ]
                }
            }}},
            {"id": "add-btn-text", "component": {"Text": {
                "text": {"literalString": "Add to Cart"}
            }}}
        ]


class ProductListTemplate:
    """Template for a list of products.

    Creates a scrollable list of product cards with images, names, and prices.
    """

    SURFACE_ID = SURFACE_ID_PRODUCTS

    @staticmethod
    def get_components() -> list[dict[str, Any]]:
        """Get component definitions for product list."""
        return [
            {"id": "root", "component": {"Column": {
                "children": {"explicitList": ["page-title", "product-list"]}
            }}},
            {"id": "page-title", "component": {"Text": {
                "text": {"path": "title"},
                "usageHint": "h1"
            }}},
            {"id": "product-list", "component": {"List": {
                "direction": "vertical",
                "children": {"template": {
                    "componentId": "product-item",
                    "dataBinding": "/products"
                }}
            }}},
            {"id": "product-item", "component": {"Card": {"child": "item-content"}}},
            {"id": "item-content", "component": {"Row": {
                "children": {"explicitList": ["item-image", "item-details"]},
                "alignment": "center"
            }}},
            {"id": "item-image", "weight": 1, "component": {"Image": {
                "url": {"path": "imageUrl"},
                "usageHint": "mediumFeature"
            }}},
            {"id": "item-details", "weight": 2, "component": {"Column": {
                "children": {"explicitList": [
                    "item-name",
                    "item-price",
                    "item-add-btn"
                ]}
            }}},
            {"id": "item-name", "component": {"Text": {
                "text": {"path": "name"},
                "usageHint": "h3"
            }}},
            {"id": "item-price", "component": {"Text": {
                "text": {"path": "price"},
                "usageHint": "body"
            }}},
            {"id": "item-add-btn", "component": {"Button": {
                "child": "item-btn-text",
                "primary": True,
                "action": {
                    "name": "add_to_cart",
                    "context": [
                        {"key": "productId", "value": {"path": "id"}}
                    ]
                }
            }}},
            {"id": "item-btn-text", "component": {"Text": {
                "text": {"literalString": "Add to Cart"}
            }}}
        ]


class CheckoutTemplate:
    """Template for checkout form.

    Creates a form with shipping address fields and order summary.
    """

    SURFACE_ID = SURFACE_ID_CHECKOUT

    @staticmethod
    def get_components() -> list[dict[str, Any]]:
        """Get component definitions for checkout form."""
        return [
            {"id": "checkout-root", "component": {"Column": {
                "children": {"explicitList": [
                    "checkout-title",
                    "checkout-divider",
                    "order-summary",
                    "shipping-section",
                    "checkout-actions"
                ]}
            }}},
            {"id": "checkout-title", "component": {"Text": {
                "text": {"literalString": "Checkout"},
                "usageHint": "h1"
            }}},
            {"id": "checkout-divider", "component": {"Divider": {}}},
            
            # Order Summary
            {"id": "order-summary", "component": {"Column": {
                "children": {"explicitList": [
                    "summary-title",
                    "items-list",
                    "total-row"
                ]}
            }}},
            {"id": "summary-title", "component": {"Text": {
                "text": {"literalString": "Order Summary"},
                "usageHint": "h3"
            }}},
            {"id": "items-list", "component": {"List": {
                "direction": "vertical",
                "children": {"template": {
                    "componentId": "checkout-item",
                    "dataBinding": "/items"
                }}
            }}},
            {"id": "checkout-item", "component": {"Row": {
                "children": {"explicitList": ["item-title", "item-qty", "item-total"]},
                "distribution": "spaceBetween"
            }}},
            {"id": "item-title", "component": {"Text": {"text": {"path": "title"}}}},
            {"id": "item-qty", "component": {"Text": {"text": {"path": "quantity"}}}},
            {"id": "item-total", "component": {"Text": {"text": {"path": "total"}}}},
            {"id": "total-row", "component": {"Row": {
                "children": {"explicitList": ["total-label", "total-value"]},
                "distribution": "spaceBetween"
            }}},
            {"id": "total-label", "component": {"Text": {
                "text": {"literalString": "Total:"},
                "usageHint": "h4"
            }}},
            {"id": "total-value", "component": {"Text": {
                "text": {"path": "total"},
                "usageHint": "h4"
            }}},
            
            # Shipping Section
            {"id": "shipping-section", "component": {"Column": {
                "children": {"explicitList": [
                    "shipping-title",
                    "name-row",
                    "address-field",
                    "city-row",
                    "email-field"
                ]}
            }}},
            {"id": "shipping-title", "component": {"Text": {
                "text": {"literalString": "Shipping Address"},
                "usageHint": "h3"
            }}},
            {"id": "name-row", "component": {"Row": {
                "children": {"explicitList": ["first-name-field", "last-name-field"]}
            }}},
            {"id": "first-name-field", "weight": 1, "component": {"TextField": {
                "label": {"literalString": "First Name"},
                "text": {"path": "firstName"}
            }}},
            {"id": "last-name-field", "weight": 1, "component": {"TextField": {
                "label": {"literalString": "Last Name"},
                "text": {"path": "lastName"}
            }}},
            {"id": "address-field", "component": {"TextField": {
                "label": {"literalString": "Street Address"},
                "text": {"path": "streetAddress"}
            }}},
            {"id": "city-row", "component": {"Row": {
                "children": {"explicitList": ["city-field", "state-field", "zip-field"]}
            }}},
            {"id": "city-field", "weight": 2, "component": {"TextField": {
                "label": {"literalString": "City"},
                "text": {"path": "city"}
            }}},
            {"id": "state-field", "weight": 1, "component": {"TextField": {
                "label": {"literalString": "State"},
                "text": {"path": "state"}
            }}},
            {"id": "zip-field", "weight": 1, "component": {"TextField": {
                "label": {"literalString": "ZIP Code"},
                "text": {"path": "zipCode"}
            }}},
            {"id": "email-field", "component": {"TextField": {
                "label": {"literalString": "Email"},
                "text": {"path": "email"}
            }}},
            
            # Actions
            {"id": "checkout-actions", "component": {"Row": {
                "children": {"explicitList": ["cancel-btn", "place-order-btn"]},
                "distribution": "spaceBetween"
            }}},
            {"id": "cancel-btn", "component": {"Button": {
                "child": "cancel-text",
                "action": {"name": "cancel_checkout"}
            }}},
            {"id": "cancel-text", "component": {"Text": {
                "text": {"literalString": "Cancel"}
            }}},
            {"id": "place-order-btn", "component": {"Button": {
                "child": "place-order-text",
                "primary": True,
                "action": {
                    "name": "place_order",
                    "context": [
                        {"key": "checkoutId", "value": {"path": "checkoutId"}}
                    ]
                }
            }}},
            {"id": "place-order-text", "component": {"Text": {
                "text": {"literalString": "Place Order"}
            }}}
        ]


class OrderConfirmationTemplate:
    """Template for order confirmation.

    Creates a confirmation card with order details and status.
    """

    SURFACE_ID = SURFACE_ID_ORDER_CONFIRMATION

    @staticmethod
    def get_components() -> list[dict[str, Any]]:
        """Get component definitions for order confirmation."""
        return [
            {"id": "confirmation-root", "component": {"Card": {
                "child": "confirmation-content"
            }}},
            {"id": "confirmation-content", "component": {"Column": {
                "children": {"explicitList": [
                    "success-icon",
                    "confirmation-title",
                    "order-id",
                    "divider",
                    "items-summary",
                    "total-section",
                    "shipping-info"
                ]},
                "alignment": "center"
            }}},
            {"id": "success-icon", "component": {"Icon": {
                "name": {"literalString": "check"}
            }}},
            {"id": "confirmation-title", "component": {"Text": {
                "text": {"literalString": "Order Confirmed!"},
                "usageHint": "h1"
            }}},
            {"id": "order-id", "component": {"Text": {
                "text": {"path": "orderIdDisplay"},
                "usageHint": "body"
            }}},
            {"id": "divider", "component": {"Divider": {}}},
            {"id": "items-summary", "component": {"Text": {
                "text": {"path": "itemsSummary"},
                "usageHint": "body"
            }}},
            {"id": "total-section", "component": {"Text": {
                "text": {"path": "totalDisplay"},
                "usageHint": "h3"
            }}},
            {"id": "shipping-info", "component": {"Column": {
                "children": {"explicitList": ["shipping-label", "shipping-address"]}
            }}},
            {"id": "shipping-label", "component": {"Text": {
                "text": {"literalString": "Shipping to:"},
                "usageHint": "caption"
            }}},
            {"id": "shipping-address", "component": {"Text": {
                "text": {"path": "shippingAddress"},
                "usageHint": "body"
            }}}
        ]


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------


def create_product_card(
    product_id: str,
    name: str,
    price: str,
    image_url: str,
    description: str = "",
    primary_color: str = DEFAULT_PRIMARY_COLOR,
) -> list[dict[str, Any]]:
    """Create A2UI messages for a product card.

    Args:
        product_id: Unique product identifier.
        name: Product name.
        price: Formatted price string (e.g., "$29.99").
        image_url: URL to product image.
        description: Product description.
        primary_color: Primary color for styling.

    Returns:
        List of A2UI messages ready to be sent.
    """
    surface_id = ProductCardTemplate.SURFACE_ID

    return [
        {
            "beginRendering": {
                "surfaceId": surface_id,
                "root": "card",
                "styles": {"primaryColor": primary_color, "font": DEFAULT_FONT}
            }
        },
        {
            "surfaceUpdate": {
                "surfaceId": surface_id,
                "components": ProductCardTemplate.get_components()
            }
        },
        {
            "dataModelUpdate": {
                "surfaceId": surface_id,
                "path": "/",
                "contents": [
                    {"key": "id", "valueString": product_id},
                    {"key": "name", "valueString": name},
                    {"key": "price", "valueString": price},
                    {"key": "imageUrl", "valueString": image_url},
                    {"key": "description", "valueString": description},
                ]
            }
        }
    ]


def create_product_list(
    title: str,
    products: list[dict[str, Any]],
    primary_color: str = DEFAULT_PRIMARY_COLOR,
) -> list[dict[str, Any]]:
    """Create A2UI messages for a product list.

    Args:
        title: List title.
        products: List of product dicts with id, name, price, imageUrl.
        primary_color: Primary color for styling.

    Returns:
        List of A2UI messages ready to be sent.
    """
    surface_id = ProductListTemplate.SURFACE_ID

    # Convert products to data model format
    products_data = []
    for i, product in enumerate(products):
        product_entry = {
            "key": f"product_{i}",
            "valueMap": [
                {"key": "id", "valueString": product.get("id", "")},
                {"key": "name", "valueString": product.get("name", "")},
                {"key": "price", "valueString": product.get("price", "")},
                {"key": "imageUrl", "valueString": product.get("imageUrl", "")},
            ]
        }
        products_data.append(product_entry)

    return [
        {
            "beginRendering": {
                "surfaceId": surface_id,
                "root": "root",
                "styles": {"primaryColor": primary_color, "font": DEFAULT_FONT}
            }
        },
        {
            "surfaceUpdate": {
                "surfaceId": surface_id,
                "components": ProductListTemplate.get_components()
            }
        },
        {
            "dataModelUpdate": {
                "surfaceId": surface_id,
                "path": "/",
                "contents": [
                    {"key": "title", "valueString": title},
                    {"key": "products", "valueMap": products_data},
                ]
            }
        }
    ]


def create_checkout_ui(
    checkout_id: str,
    items: list[dict[str, Any]],
    total: str,
    primary_color: str = DEFAULT_PRIMARY_COLOR,
) -> list[dict[str, Any]]:
    """Create A2UI messages for checkout form.

    Args:
        checkout_id: Checkout session ID.
        items: List of item dicts with title, quantity, total.
        total: Formatted total string.
        primary_color: Primary color for styling.

    Returns:
        List of A2UI messages ready to be sent.
    """
    surface_id = CheckoutTemplate.SURFACE_ID

    # Convert items to data model format
    items_data = []
    for i, item in enumerate(items):
        item_entry = {
            "key": f"item_{i}",
            "valueMap": [
                {"key": "title", "valueString": item.get("title", "")},
                {"key": "quantity", "valueString": str(item.get("quantity", 1))},
                {"key": "total", "valueString": item.get("total", "")},
            ]
        }
        items_data.append(item_entry)

    return [
        {
            "beginRendering": {
                "surfaceId": surface_id,
                "root": "checkout-root",
                "styles": {"primaryColor": primary_color, "font": DEFAULT_FONT}
            }
        },
        {
            "surfaceUpdate": {
                "surfaceId": surface_id,
                "components": CheckoutTemplate.get_components()
            }
        },
        {
            "dataModelUpdate": {
                "surfaceId": surface_id,
                "path": "/",
                "contents": [
                    {"key": "checkoutId", "valueString": checkout_id},
                    {"key": "items", "valueMap": items_data},
                    {"key": "total", "valueString": total},
                    {"key": "firstName", "valueString": ""},
                    {"key": "lastName", "valueString": ""},
                    {"key": "streetAddress", "valueString": ""},
                    {"key": "city", "valueString": ""},
                    {"key": "state", "valueString": ""},
                    {"key": "zipCode", "valueString": ""},
                    {"key": "email", "valueString": ""},
                ]
            }
        }
    ]


def create_order_confirmation(
    order_id: str,
    items_summary: str,
    total: str,
    shipping_address: str,
    primary_color: str = DEFAULT_PRIMARY_COLOR,
) -> list[dict[str, Any]]:
    """Create A2UI messages for order confirmation.

    Args:
        order_id: Order ID.
        items_summary: Summary of items in order.
        total: Formatted total string.
        shipping_address: Formatted shipping address.
        primary_color: Primary color for styling.

    Returns:
        List of A2UI messages ready to be sent.
    """
    surface_id = OrderConfirmationTemplate.SURFACE_ID

    return [
        {
            "beginRendering": {
                "surfaceId": surface_id,
                "root": "confirmation-root",
                "styles": {"primaryColor": primary_color, "font": DEFAULT_FONT}
            }
        },
        {
            "surfaceUpdate": {
                "surfaceId": surface_id,
                "components": OrderConfirmationTemplate.get_components()
            }
        },
        {
            "dataModelUpdate": {
                "surfaceId": surface_id,
                "path": "/",
                "contents": [
                    {"key": "orderId", "valueString": order_id},
                    {"key": "orderIdDisplay", "valueString": f"Order #{order_id}"},
                    {"key": "itemsSummary", "valueString": items_summary},
                    {"key": "totalDisplay", "valueString": f"Total: {total}"},
                    {"key": "shippingAddress", "valueString": shipping_address},
                ]
            }
        }
    ]
