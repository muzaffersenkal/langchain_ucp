"""UCP Toolkit for LangChain agents."""

import logging
from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, ConfigDict, Field

from langchain_ucp.client import UCPClient
from langchain_ucp.store import Product, UCPStore
from langchain_ucp.tools import (
    AddToCheckoutTool,
    CancelCheckoutTool,
    CompleteCheckoutTool,
    GetCheckoutTool,
    GetOrderTool,
    RemoveFromCheckoutTool,
    SearchCatalogTool,
    StartPaymentTool,
    UpdateCheckoutTool,
    UpdateCustomerDetailsTool,
)

logger = logging.getLogger(__name__)


class UCPToolkit(BaseModel):
    """Toolkit for UCP (Universal Commerce Protocol) operations.

    This toolkit provides tools for:
    - Searching product catalogs
    - Managing checkout sessions (add/remove/update items)
    - Updating customer details and shipping info
    - Completing purchases and tracking orders

    For A2UI (rich UI) support, use the separate a2ui module functions
    to build system prompts and parse responses. A2UI is an output format
    standardization, not a tool.

    Example:
        >>> from langchain_ucp import UCPToolkit, Product
        >>> from langchain_openai import ChatOpenAI
        >>> from langgraph.prebuilt import create_react_agent
        >>>
        >>> products = [
        ...     Product(id="roses", title="Red Roses"),
        ...     Product(id="tulips", title="Tulips"),
        ... ]
        >>> toolkit = UCPToolkit(
        ...     merchant_url="http://localhost:8000",
        ...     products=products,
        ... )
        >>> llm = ChatOpenAI(model="gpt-4o")
        >>> agent = create_react_agent(llm, toolkit.get_tools())

    With A2UI support (add to system prompt):
        >>> from langchain_ucp.a2ui import get_a2ui_system_prompt, parse_a2ui_response
        >>>
        >>> # Build system prompt with A2UI instructions
        >>> base_prompt = "You are a helpful shopping assistant..."
        >>> system_prompt = base_prompt + get_a2ui_system_prompt()
        >>>
        >>> # After getting LLM response, parse A2UI
        >>> text, a2ui_messages = parse_a2ui_response(response)
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    merchant_url: str = Field(description="URL of the UCP merchant server")
    agent_name: str = Field(
        default="langchain-ucp-agent",
        description="Name of this agent for UCP-Agent header",
    )
    products: list[Product] = Field(description="Product catalog for the store")
    verbose: bool = Field(
        default=False,
        description="Enable verbose logging",
    )

    _client: UCPClient | None = None
    _store: UCPStore | None = None

    def model_post_init(self, __context) -> None:
        """Initialize client and store after model creation."""
        if self.verbose:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            )
            logger.debug(f"[UCPToolkit] Initializing with merchant_url={self.merchant_url}")

        self._client = UCPClient(
            merchant_url=self.merchant_url,
            agent_name=self.agent_name,
            verbose=self.verbose,
        )
        self._store = UCPStore(
            client=self._client,
            products=self.products,
            verbose=self.verbose,
        )

        if self.verbose:
            logger.debug(f"[UCPToolkit] Loaded {len(self._store.products)} products")

    @property
    def client(self) -> UCPClient:
        """Get the UCP client."""
        if self._client is None:
            self._client = UCPClient(
                merchant_url=self.merchant_url,
                agent_name=self.agent_name,
                verbose=self.verbose,
            )
        return self._client

    @property
    def store(self) -> UCPStore:
        """Get the UCP store."""
        if self._store is None:
            self._store = UCPStore(
                client=self.client,
                products=self.products,
                verbose=self.verbose,
            )
        return self._store

    def get_tools(self) -> list[BaseTool]:
        """Get all UCP tools.
        
        Returns commerce operation tools for:
        - search_shopping_catalog: Search products
        - add_to_checkout: Add items to cart
        - remove_from_checkout: Remove items from cart
        - update_checkout: Update item quantities
        - get_checkout: View current cart
        - update_customer_details: Set shipping address
        - start_payment: Prepare for payment
        - complete_checkout: Place order
        - cancel_checkout: Cancel checkout
        - get_order: Get order status
        """
        tool_classes = [
            SearchCatalogTool,
            AddToCheckoutTool,
            RemoveFromCheckoutTool,
            UpdateCheckoutTool,
            GetCheckoutTool,
            UpdateCustomerDetailsTool,
            StartPaymentTool,
            CompleteCheckoutTool,
            CancelCheckoutTool,
            GetOrderTool,
        ]

        tools = [
            tool_class(store=self.store, verbose=self.verbose)
            for tool_class in tool_classes
        ]

        if self.verbose:
            logger.debug(f"[UCPToolkit] Created {len(tools)} tools")

        return tools

    async def close(self) -> None:
        """Close the toolkit and release resources."""
        if self._client is not None:
            await self._client.close()

    def clear_session(self) -> None:
        """Clear the current checkout session."""
        if self._store is not None:
            self._store.clear_session()
            if self.verbose:
                logger.debug("[UCPToolkit] Session cleared")
