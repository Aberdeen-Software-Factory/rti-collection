from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl, Field

class CCLicenseType(str, Enum):
    """Creative Commons License options as described at:
    https://creativecommons.org/share-your-work/cclicenses/
    """
    CC_BY = "CC BY"
    CC_BY_SA = "CC BY-SA"
    CC_BY_NC = "CC BY-NC"
    CC_BY_NC_SA = "CC BY-NC-SA"
    CC_BY_ND = "CC BY-ND"
    CC_BY_NC_ND = "CC BY-NC_ND"


class Metadata(BaseModel):
    """Metadata describing an artifact."""
    name: str | None = None
    language: list[str] = Field(default_factory=list)
    script: list[str] = Field(default_factory=list)
    provenance: list[str] = Field(default_factory=list)
    location: list[str] = Field(default_factory=list)
    photographer: list[str] = Field(default_factory=list)
    date: str | None = None
    bibliography: str | None = None
    notes: str | None = None
    keywords: list[str] = Field(default_factory=list)
    copyright: CCLicenseType = CCLicenseType.CC_BY


class RelightWebMedia(BaseModel):
    id: str
    url: HttpUrl
    files: list[HttpUrl]


class Rtis(BaseModel):
    web: list[RelightWebMedia]

class Artifact(BaseModel):
    id: str
    metadata: Metadata
    images: list[HttpUrl]
    rtis: Rtis

class ArtifactResponse(BaseModel):
    artifact: Artifact

class ArtifactPreview(BaseModel):
    id: str
    metadata: Metadata
    thumbnailURL: Optional[HttpUrl]

class ArtifactsResponse(BaseModel):
    artifacts: list[ArtifactPreview]
