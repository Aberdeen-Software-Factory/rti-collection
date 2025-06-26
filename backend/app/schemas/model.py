from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from .cclicense import CCLicenseType


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


class RTIImageBundle(BaseModel):
    """Represents a relightable RTI image in the ["relight-web"](https://vcg.isti.cnr.it/vcgtools/relight/#format) format.

    This bundle includes all necessary files to view or process the RTI,
    such as an `info.json` file, multiple JPEG planes, and a thumbnail.
    """

    id: str
    url: HttpUrl
    thumbnail: HttpUrl | None
    filenames: list[str]


class Artifact(BaseModel):
    """Represents an artifact which contains relightable and still images and metadata."""

    id: str
    metadata: Metadata
    images: list[HttpUrl]
    rtis: list[RTIImageBundle]


class ArtifactPreview(BaseModel):
    """Represents a preview of the artifact.

    This is not as comprehensive as :class:`Artifact`, used for displaying a list of artifacts.
    """

    id: str
    metadata: Metadata
    thumbnailURL: Optional[HttpUrl]


class ArtifactResponse(BaseModel):
    artifact: Artifact


class ArtifactsResponse(BaseModel):
    page: int
    pages: int
    artifacts: list[ArtifactPreview]
