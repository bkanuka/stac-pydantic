from enum import auto
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field, validator
import geojson

from .utils import AutoValueEnum
from .shared import BBox, NumType

Coordinate = Tuple[NumType, NumType]


class GeoJSONType(str, AutoValueEnum):
    GeometryCollection = auto()
    Point = auto()
    MultiPoint = auto()
    LineString = auto()
    MultiLineString = auto()
    Polygon = auto()
    MultiPolygon = auto()
    Feature = auto()
    FeatureCollection = auto()


class _GeometryBase(BaseModel):
    coordinates: Any  # will be constrained in child classes

    @validator("coordinates")
    def check_coordinates(cls, coords):
        try:
            geojson_instance = getattr(geojson, cls.__name__)(coordinates=coords)
        except AttributeError as e:
            raise ValueError(str(e))

        if geojson_instance.is_valid:
            return coords
        else:
            raise ValueError(geojson_instance.errors())

    @property
    def __geo_interface__(self):
        return self.dict()


class Point(_GeometryBase):
    type: str = Field("Point", const=True)
    coordinates: Coordinate


class MultiPoint(_GeometryBase):
    type: str = Field("MultiPoint", const=True)
    coordinates: List[Coordinate]


class LineString(_GeometryBase):
    type: str = Field("LineString", const=True)
    coordinates: List[Coordinate]


class MultiLineString(_GeometryBase):
    type: str = Field("MultiLineString", const=True)
    coordinates: List[List[Coordinate]]


class Polygon(_GeometryBase):
    type: str = Field("Polygon", const=True)
    coordinates: List[List[Coordinate]]


class MultiPolygon(_GeometryBase):
    type: str = Field("MultiPolygon", const=True)
    coordinates: List[List[List[Coordinate]]]


class Feature(BaseModel):
    type: str = Field("Feature", const=True)
    geometry: Union[
        Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon
    ]
    properties: Optional[Dict[Any, Any]]
    id: Optional[str]
    bbox: Optional[BBox]

    class Config:
        use_enum_values = True

    @validator("geometry", pre=True, always=True)
    def set_geometry(cls, v):
        if hasattr(v, "__geo_interface__"):
            return v.__geo_interface__
        return v

    @property
    def __geo_interface__(self):
        return self.dict()


class FeatureCollection(BaseModel):
    type: str = Field("FeatureCollection", const=True)
    features: List[Feature]
    bbox: Optional[BBox]