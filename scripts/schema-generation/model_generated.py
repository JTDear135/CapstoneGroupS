# type: ignore

# generated usings steps in model-generation.md
# generated by datamodel-codegen:
#   filename:  schema.json
#   timestamp: 2025-02-20T21:35:14+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Extra, Field 


class AdditionalGeometryData(BaseModel):
    pass

    class Config:
        extra = Extra.forbid


class HeightInformation(BaseModel):
    class Config:
        extra = Extra.forbid

    upperLevel: int
    uomUpperLevel: str
    lowerLevel: int
    uomLowerLevel: str


class NotamEvent(BaseModel):
    class Config:
        extra = Extra.forbid

    scenario: int


class Coordinate(BaseModel):
    __root__: Union[List[List[float]], float] = Field(..., title='Coordinate')


class PurpleType(Enum):
    Polygon = 'Polygon'
    Point = 'Point'


class FluffyType(Enum):
    GeometryCollection = 'GeometryCollection'


class AffectedFIR(Enum):
    KZJX = 'KZJX'
    KZDC = 'KZDC'
    KZTL = 'KZTL'
    ZJX = 'ZJX'


class Classification(Enum):
    FDC = 'FDC'
    INTL = 'INTL'
    DOM = 'DOM'


class EffectiveEndEnum(Enum):
    PERM = 'PERM'


class Series(Enum):
    A = 'A'


class NotamType(Enum):
    N = 'N'


class NotamTranslationType(Enum):
    LOCAL_FORMAT = 'LOCAL_FORMAT'
    ICAO = 'ICAO'


class ItemType(Enum):
    Feature = 'Feature'


class GeometryElement(BaseModel):
    class Config:
        extra = Extra.forbid

    type: PurpleType
    heightInformation: Optional[HeightInformation] = None
    coordinates: List[Coordinate]
    additionalGeometryData: Optional[AdditionalGeometryData] = None


class NotamTranslation(BaseModel):
    class Config:
        extra = Extra.forbid

    type: NotamTranslationType
    simpleText: Optional[str] = None
    formattedText: Optional[str] = None


class EffectiveEndUnion(BaseModel):
    __root__: Union[datetime, EffectiveEndEnum] = Field(..., title='EffectiveEndUnion')


class ItemGeometry(BaseModel):
    class Config:
        extra = Extra.forbid

    type: FluffyType
    geometries: Optional[List[GeometryElement]] = None


class Notam(BaseModel):
    class Config:
        extra = Extra.forbid

    id: str
    number: str
    type: NotamType
    issued: datetime
    selectionCode: Optional[str] = None
    location: str
    effectiveStart: datetime
    effectiveEnd: EffectiveEndUnion
    text: str
    classification: Classification
    accountId: str
    lastUpdated: datetime
    icaoLocation: str
    series: Optional[Series] = None
    affectedFIR: Optional[AffectedFIR] = None
    minimumFL: Optional[str] = None
    maximumFL: Optional[str] = None
    coordinates: Optional[str] = None
    radius: Optional[str] = None
    lowerLimit: Optional[str] = None
    upperLimit: Optional[str] = None


class CoreNOTAMData(BaseModel):
    class Config:
        extra = Extra.forbid

    notamEvent: NotamEvent
    notam: Notam
    notamTranslation: List[NotamTranslation]


class Properties(BaseModel):
    class Config:
        extra = Extra.forbid

    coreNOTAMData: CoreNOTAMData


class Item(BaseModel):
    class Config:
        extra = Extra.forbid

    type: ItemType
    properties: Properties
    geometry: ItemGeometry


class Schema(BaseModel):
    class Config:
        extra = Extra.forbid

    pageSize: int
    pageNum: int
    totalCount: int
    totalPages: int
    items: List[Item]


class Model(BaseModel):
    __root__: Schema
