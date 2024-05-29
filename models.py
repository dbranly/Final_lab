from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class IMDb(BaseModel):
    rating: Optional[float] = None
    votes: Optional[int] = None
    id: Optional[int] = None

class Awards(BaseModel):
    wins: Optional[int] = None
    nominations: Optional[int] = None
    text: Optional[str] = None

class Viewer(BaseModel):
    rating: Optional[float]
    numReviews: Optional[int]
    meter: Optional[int]

class Critic(BaseModel):
    rating: float
    numReviews: int
    meter: int

class Tomatoes(BaseModel):
    viewer: Optional[Viewer] = None
    fresh: Optional[int] = None
    critic: Optional[Critic] = None
    rotten: Optional[int] = None
    lastUpdated: Optional[datetime] = None


class IMDb(BaseModel):
    rating: Optional[float] = None
    votes: Optional[int] = None
    id: Optional[int] = None

class Awards(BaseModel):
    wins: Optional[int] = None
    nominations: Optional[int] = None
    text: Optional[str] = None

class Viewer(BaseModel):
    rating: Optional[float] = None
    numReviews: Optional[int] = None
    meter: Optional[int] = None

class Critic(BaseModel):
    rating: Optional[float] = None
    numReviews: Optional[int] = None
    meter: Optional[int] = None

class Tomatoes(BaseModel):
    viewer: Optional[Viewer] = None
    fresh: Optional[int] = None
    critic: Optional[Critic] = None
    rotten: Optional[int] = None
    lastUpdated: Optional[datetime] = None


class Movie(BaseModel):
    ## We voluntarily ommited id. We got many problems integrating ObjectId to pydantic basemodel 
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    runtime: Optional[int] = None
    cast: Optional[List[str]] = None
    poster: Optional[str] = None
    title: Optional[str] = None
    fullplot: Optional[str] = None
    languages: Optional[List[str]] = None
    released: Optional[datetime] = None
    directors: Optional[List[str]] = None
    rated: Optional[str] = None
    awards: Optional[Awards] = None
    lastupdated: Optional[str] = None
    year: Optional[int] = None
    imdb: Optional[IMDb] = None
    countries: Optional[List[str]] = None
    type: Optional[str] = None
    tomatoes: Optional[Tomatoes] = None
    num_mflix_comments: Optional[int] = None
    writers: Optional[List[str]] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MovieUpdate(BaseModel):
    plot: Optional[str]
    genres: Optional[List[str]]
    runtime: Optional[int]
    cast: Optional[List[str]]
    poster: Optional[str]
    title: Optional[str]
    fullplot: Optional[str]
    languages: Optional[List[str]]
    released: Optional[datetime]
    directors: Optional[List[str]]
    rated: Optional[str]
    awards: Optional[Awards]
    lastupdated: Optional[datetime]
    year: Optional[int]
    imdb: Optional[IMDb]
    countries: Optional[List[str]]
    type: Optional[str]
    tomatoes: Optional[Tomatoes]
    num_mflix_comments: Optional[int]
    writers: Optional[List[str]]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }