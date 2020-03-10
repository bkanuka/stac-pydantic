from enum import auto
from typing import List, Optional, Tuple, Union

from pydantic import BaseModel, Field

from .utils import AutoValueEnum

NumType = Union[float, int]
BBox = Union[
    Tuple[NumType, NumType, NumType, NumType],  # 2D bbox
    Tuple[NumType, NumType, NumType, NumType, NumType, NumType],  # 3D bbox
]


class ExtensionTypes(str, AutoValueEnum):
    """
    https://github.com/radiantearth/stac-spec/blob/v0.9.0/extensions/README.md#list-of-content-extensions
    """

    asset = auto()
    checksum = auto()
    commons = auto()
    context = auto()
    cube = auto()
    eo = auto()
    label = auto()
    pc = auto()
    proj = auto()
    sar = auto()
    sat = auto()
    sci = auto()
    version = auto()
    view = auto()


class AssetRoles(str, AutoValueEnum):
    """
    https://github.com/radiantearth/stac-spec/blob/v0.9.0/extensions/asset/README.md
    """

    thumbnail = auto()
    overview = auto()
    data = auto()
    metadata = auto()


class Link(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v0.9.0/collection-spec/collection-spec.md#link-object
    """

    href: str
    rel: str
    type: Optional[str]
    title: Optional[str]
    # Label extension
    label: Optional[str] = Field(None, alias="label:assets")

    class Config:
        use_enum_values = True


class Asset(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v0.9.0/item-spec/item-spec.md#asset-object
    """

    href: str
    type: Optional[str]
    title: Optional[str]
    description: Optional[str]
    roles: Optional[List[AssetRoles]]
    # EO extension
    bands: Optional[List[int]] = Field(None, alias="eo:bands")
    # SAR extension
    polarizations: Optional[List[str]] = Field(None, alias="sar:polarizations")
    # Checksum extension
    multihash: Optional[str] = Field(None, alias="checksum:multihash")

    class Config:
        allow_population_by_fieldname = True
        use_enum_values = True