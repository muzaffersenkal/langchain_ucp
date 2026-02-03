"""A2UI type definitions using Pydantic models."""

from typing import Any, Literal, Union
from pydantic import BaseModel, Field


# -----------------------------------------------------------------------------
# Value Types - for data binding
# -----------------------------------------------------------------------------


class LiteralValue(BaseModel):
    """Represents a literal value."""
    literal_string: str | None = Field(default=None, alias="literalString")
    literal_number: float | None = Field(default=None, alias="literalNumber")
    literal_boolean: bool | None = Field(default=None, alias="literalBoolean")

    model_config = {"populate_by_name": True}


class PathValue(BaseModel):
    """Represents a path reference to data model."""
    path: str


class TextValue(BaseModel):
    """Text value - literal or path reference."""
    literal_string: str | None = Field(default=None, alias="literalString")
    path: str | None = None

    model_config = {"populate_by_name": True}


class NumberValue(BaseModel):
    """Number value - literal or path reference."""
    literal_number: float | None = Field(default=None, alias="literalNumber")
    path: str | None = None

    model_config = {"populate_by_name": True}


class BooleanValue(BaseModel):
    """Boolean value - literal or path reference."""
    literal_boolean: bool | None = Field(default=None, alias="literalBoolean")
    path: str | None = None

    model_config = {"populate_by_name": True}


# -----------------------------------------------------------------------------
# Data Model Types
# -----------------------------------------------------------------------------


class DataEntry(BaseModel):
    """A single data entry in the data model."""
    key: str
    value_string: str | None = Field(default=None, alias="valueString")
    value_number: float | None = Field(default=None, alias="valueNumber")
    value_boolean: bool | None = Field(default=None, alias="valueBoolean")
    value_map: list["DataEntry"] | None = Field(default=None, alias="valueMap")

    model_config = {"populate_by_name": True}

    @classmethod
    def string(cls, key: str, value: str) -> "DataEntry":
        """Create a string data entry."""
        return cls(key=key, value_string=value)

    @classmethod
    def number(cls, key: str, value: float) -> "DataEntry":
        """Create a number data entry."""
        return cls(key=key, value_number=value)

    @classmethod
    def boolean(cls, key: str, value: bool) -> "DataEntry":
        """Create a boolean data entry."""
        return cls(key=key, value_boolean=value)

    @classmethod
    def map(cls, key: str, entries: list["DataEntry"]) -> "DataEntry":
        """Create a map data entry."""
        return cls(key=key, value_map=entries)


# -----------------------------------------------------------------------------
# Component Types
# -----------------------------------------------------------------------------


class ExplicitChildren(BaseModel):
    """Explicit list of child component IDs."""
    explicit_list: list[str] = Field(alias="explicitList")

    model_config = {"populate_by_name": True}


class TemplateChildren(BaseModel):
    """Template-based children from data binding."""
    component_id: str = Field(alias="componentId")
    data_binding: str = Field(alias="dataBinding")

    model_config = {"populate_by_name": True}


class Children(BaseModel):
    """Children definition for container components."""
    explicit_list: list[str] | None = Field(default=None, alias="explicitList")
    template: TemplateChildren | None = None

    model_config = {"populate_by_name": True}


class ActionContext(BaseModel):
    """Context item for button actions."""
    key: str
    value: dict[str, Any]


class ButtonAction(BaseModel):
    """Action configuration for buttons."""
    name: str
    context: list[ActionContext] | None = None


# -----------------------------------------------------------------------------
# Component Definitions
# -----------------------------------------------------------------------------


class TextComponent(BaseModel):
    """Text component."""
    text: TextValue
    usage_hint: Literal["h1", "h2", "h3", "h4", "h5", "caption", "body"] | None = Field(
        default=None, alias="usageHint"
    )

    model_config = {"populate_by_name": True}


class ImageComponent(BaseModel):
    """Image component."""
    url: TextValue
    fit: Literal["contain", "cover", "fill", "none", "scale-down"] | None = None
    usage_hint: Literal[
        "icon", "avatar", "smallFeature", "mediumFeature", "largeFeature", "header"
    ] | None = Field(default=None, alias="usageHint")

    model_config = {"populate_by_name": True}


class IconComponent(BaseModel):
    """Icon component."""
    name: TextValue


class ButtonComponent(BaseModel):
    """Button component."""
    child: str
    primary: bool | None = None
    action: ButtonAction


class CardComponent(BaseModel):
    """Card component."""
    child: str


class RowComponent(BaseModel):
    """Row layout component."""
    children: Children
    distribution: Literal[
        "center", "end", "spaceAround", "spaceBetween", "spaceEvenly", "start"
    ] | None = None
    alignment: Literal["start", "center", "end", "stretch"] | None = None


class ColumnComponent(BaseModel):
    """Column layout component."""
    children: Children
    distribution: Literal[
        "start", "center", "end", "spaceBetween", "spaceAround", "spaceEvenly"
    ] | None = None
    alignment: Literal["start", "center", "end", "stretch"] | None = None


class ListComponent(BaseModel):
    """List component."""
    children: Children
    direction: Literal["vertical", "horizontal"] | None = None
    alignment: Literal["start", "center", "end", "stretch"] | None = None


class DividerComponent(BaseModel):
    """Divider component."""
    axis: Literal["horizontal", "vertical"] | None = None


class TextFieldComponent(BaseModel):
    """Text field input component."""
    label: TextValue
    text: TextValue | None = None
    text_field_type: Literal[
        "date", "longText", "number", "shortText", "obscured"
    ] | None = Field(default=None, alias="textFieldType")
    validation_regexp: str | None = Field(default=None, alias="validationRegexp")

    model_config = {"populate_by_name": True}


# -----------------------------------------------------------------------------
# Component Wrapper
# -----------------------------------------------------------------------------


class Component(BaseModel):
    """A UI component with ID and component definition."""
    id: str
    weight: float | None = None
    component: dict[str, Any]  # {"Text": {...}, "Image": {...}, etc.}


# -----------------------------------------------------------------------------
# Message Types
# -----------------------------------------------------------------------------


class Styles(BaseModel):
    """UI styling configuration."""
    primary_color: str | None = Field(default=None, alias="primaryColor")
    font: str | None = None

    model_config = {"populate_by_name": True}


class BeginRendering(BaseModel):
    """Begin rendering message."""
    surface_id: str = Field(alias="surfaceId")
    root: str
    catalog_id: str | None = Field(default=None, alias="catalogId")
    styles: Styles | None = None

    model_config = {"populate_by_name": True}


class SurfaceUpdate(BaseModel):
    """Surface update message."""
    surface_id: str = Field(alias="surfaceId")
    components: list[Component]

    model_config = {"populate_by_name": True}


class DataModelUpdate(BaseModel):
    """Data model update message."""
    surface_id: str = Field(alias="surfaceId")
    path: str | None = None
    contents: list[DataEntry]

    model_config = {"populate_by_name": True}


class DeleteSurface(BaseModel):
    """Delete surface message."""
    surface_id: str = Field(alias="surfaceId")

    model_config = {"populate_by_name": True}


# -----------------------------------------------------------------------------
# A2UI Message
# -----------------------------------------------------------------------------


class A2UIMessage(BaseModel):
    """A2UI message - contains exactly one of the action types."""
    begin_rendering: BeginRendering | None = Field(default=None, alias="beginRendering")
    surface_update: SurfaceUpdate | None = Field(default=None, alias="surfaceUpdate")
    data_model_update: DataModelUpdate | None = Field(default=None, alias="dataModelUpdate")
    delete_surface: DeleteSurface | None = Field(default=None, alias="deleteSurface")

    model_config = {"populate_by_name": True}

    @classmethod
    def begin(
        cls,
        surface_id: str,
        root: str,
        primary_color: str | None = None,
        font: str | None = None,
    ) -> "A2UIMessage":
        """Create a begin rendering message."""
        styles = None
        if primary_color or font:
            styles = Styles(primary_color=primary_color, font=font)
        return cls(
            begin_rendering=BeginRendering(
                surface_id=surface_id,
                root=root,
                styles=styles,
            )
        )

    @classmethod
    def update_surface(
        cls,
        surface_id: str,
        components: list[Component],
    ) -> "A2UIMessage":
        """Create a surface update message."""
        return cls(
            surface_update=SurfaceUpdate(
                surface_id=surface_id,
                components=components,
            )
        )

    @classmethod
    def update_data(
        cls,
        surface_id: str,
        contents: list[DataEntry],
        path: str = "/",
    ) -> "A2UIMessage":
        """Create a data model update message."""
        return cls(
            data_model_update=DataModelUpdate(
                surface_id=surface_id,
                path=path,
                contents=contents,
            )
        )

    @classmethod
    def delete(cls, surface_id: str) -> "A2UIMessage":
        """Create a delete surface message."""
        return cls(delete_surface=DeleteSurface(surface_id=surface_id))

    def to_dict(self) -> dict[str, Any]:
        """Convert message to dictionary for JSON serialization."""
        return self.model_dump(by_alias=True, exclude_none=True)
