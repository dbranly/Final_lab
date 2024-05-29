from fastapi import APIRouter, Body, Request, HTTPException, status, Query
from typing import List, Optional
from models import Movie, MovieUpdate

# Create a new router instance
router = APIRouter()

@router.get("/", response_description="List all movies [MongoDB]", response_model=List[Movie], tags=["MongoDB"])
def list_all_movies(request: Request):
    """
    Retrieve and return a list of the first 4 movies from the MongoDB collection.
    """
    movies = list(request.app.database["movies"].find({}, {"_id": 0}).limit(4))
    return movies

@router.get("/search", response_description="Get movies by title or actor", response_model=List[Movie], tags=["MongoDB"])
def find_movies_by_title_or_actor_name(request: Request, title: Optional[str] = Query(None), actor: Optional[str] = Query(None)):
    """
    Search for movies in the MongoDB collection by title or actor name.
    If no parameters are provided, return all movies.
    """
    query = []
    if title:
        query.append({"title": title})
    if actor:
        query.append({"cast": actor})

    if query:
        movies = list(request.app.database["movies"].find({"$or": query}, {"_id": 0}))
    else:
        movies = list(request.app.database["movies"].find({}, {"_id": 0}))

    if movies:
        return movies
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No movies found with the given criteria")

@router.put("/update", response_description="Update specific information on a Movie", response_model=Movie, tags=["MongoDB"])
def update_movie_info(title: str, request: Request, movie: MovieUpdate = Body(...)):
    """
    Update specific information for a movie in the MongoDB collection by its title.
    """
    movie_data = {k: v for k, v in movie.dict().items() if v is not None}
    
    if movie_data:
        update_result = request.app.database["movies"].update_one(
            {"title": title}, {"$set": movie_data}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title {title} not found")

    if (existing_movie := request.app.database["movies"].find_one({"title": title},{"_id": 0})) is not None:
        return existing_movie

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title {title} not found")
