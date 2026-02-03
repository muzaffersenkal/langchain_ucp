"""A2UI JSON Schema definitions."""

from typing import Any

# A2UI Message Schema - based on v0.8 specification
A2UI_MESSAGE_SCHEMA: dict[str, Any] = {
    "title": "A2UI Message Schema",
    "description": "Describes a JSON payload for an A2UI (Agent to UI) message.",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "beginRendering": {
            "type": "object",
            "description": "Signals the client to begin rendering a surface.",
            "additionalProperties": False,
            "properties": {
                "surfaceId": {
                    "type": "string",
                    "description": "The unique identifier for the UI surface."
                },
                "catalogId": {
                    "type": "string",
                    "description": "The identifier of the component catalog to use."
                },
                "root": {
                    "type": "string",
                    "description": "The ID of the root component to render."
                },
                "styles": {
                    "type": "object",
                    "description": "Styling information for the UI.",
                    "additionalProperties": True
                }
            },
            "required": ["root", "surfaceId"]
        },
        "surfaceUpdate": {
            "type": "object",
            "description": "Updates a surface with a new set of components.",
            "additionalProperties": False,
            "properties": {
                "surfaceId": {
                    "type": "string",
                    "description": "The unique identifier for the UI surface."
                },
                "components": {
                    "type": "array",
                    "description": "A list of UI components.",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "The unique identifier for this component."
                            },
                            "weight": {
                                "type": "number",
                                "description": "Relative weight in Row or Column."
                            },
                            "component": {
                                "type": "object",
                                "description": "Component type and properties.",
                                "additionalProperties": True
                            }
                        },
                        "required": ["id", "component"]
                    }
                }
            },
            "required": ["surfaceId", "components"]
        },
        "dataModelUpdate": {
            "type": "object",
            "description": "Updates the data model for a surface.",
            "additionalProperties": False,
            "properties": {
                "surfaceId": {
                    "type": "string",
                    "description": "The surface this data model update applies to."
                },
                "path": {
                    "type": "string",
                    "description": "Path within the data model (e.g., '/user/name')."
                },
                "contents": {
                    "type": "array",
                    "description": "Array of data entries.",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "key": {"type": "string"},
                            "valueString": {"type": "string"},
                            "valueNumber": {"type": "number"},
                            "valueBoolean": {"type": "boolean"},
                            "valueMap": {
                                "type": "array",
                                "description": "Represents a map as an adjacency list. Can contain nested valueMap for complex structures.",
                                "items": {
                                    "type": "object",
                                    "description": "One entry in the map. Exactly one 'value*' property should be provided alongside the key.",
                                    "properties": {
                                        "key": {"type": "string"},
                                        "valueString": {"type": "string"},
                                        "valueNumber": {"type": "number"},
                                        "valueBoolean": {"type": "boolean"},
                                        "valueMap": {
                                            "type": "array",
                                            "description": "Nested map for complex data structures like lists of objects."
                                        }
                                    },
                                    "required": ["key"]
                                }
                            }
                        },
                        "required": ["key"]
                    }
                }
            },
            "required": ["contents", "surfaceId"]
        },
        "deleteSurface": {
            "type": "object",
            "description": "Signals the client to delete a surface.",
            "additionalProperties": False,
            "properties": {
                "surfaceId": {
                    "type": "string",
                    "description": "The surface to delete."
                }
            },
            "required": ["surfaceId"]
        }
    }
}

# Standard catalog components supported
A2UI_STANDARD_CATALOG: dict[str, Any] = {
    "components": [
        "Text",
        "Image",
        "Icon",
        "Video",
        "AudioPlayer",
        "Row",
        "Column",
        "List",
        "Card",
        "Tabs",
        "Divider",
        "Modal",
        "Button",
        "CheckBox",
        "TextField",
        "DateTimeInput",
        "MultipleChoice",
        "Slider",
    ],
    "usageHints": {
        "text": ["h1", "h2", "h3", "h4", "h5", "caption", "body"],
        "image": ["icon", "avatar", "smallFeature", "mediumFeature", "largeFeature", "header"],
    },
    "icons": [
        "accountCircle", "add", "arrowBack", "arrowForward", "attachFile",
        "calendarToday", "call", "camera", "check", "close", "delete",
        "download", "edit", "event", "error", "favorite", "favoriteOff",
        "folder", "help", "home", "info", "locationOn", "lock", "lockOpen",
        "mail", "menu", "moreVert", "moreHoriz", "notificationsOff",
        "notifications", "payment", "person", "phone", "photo", "print",
        "refresh", "search", "send", "settings", "share", "shoppingCart",
        "star", "starHalf", "starOff", "upload", "visibility", "visibilityOff",
        "warning"
    ]
}


def wrap_as_json_array(schema: dict[str, Any]) -> dict[str, Any]:
    """Wraps the A2UI schema in an array to support multiple messages.

    Args:
        schema: The A2UI schema to wrap.

    Returns:
        The wrapped schema as an array type.

    Raises:
        ValueError: If the schema is empty.
    """
    if not schema:
        raise ValueError("A2UI schema is empty")
    return {"type": "array", "items": schema}
