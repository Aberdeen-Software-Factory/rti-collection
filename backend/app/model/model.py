from typing import Optional

from pydantic import BaseModel, HttpUrl


class Metadata(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    creator: Optional[str] = None
    date: Optional[str] = None
    copyright: Optional[str] = None


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
    title: str
    description: str
    creator: str
    date: str
    copyright: str
    thumbnailURL: Optional[HttpUrl]

class ArtifactsResponse(BaseModel):
    artifacts: list[ArtifactPreview]
