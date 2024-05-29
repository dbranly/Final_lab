from fastapi import FastAPI, HTTPException, status
from pymongo import MongoClient
from neo4j import GraphDatabase
from dotenv import dotenv_values
from routes import router as movies_router

# Load configuration from .env file
config = dotenv_values(".env")

# Initialize the FastAPI app
app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    # Connect to MongoDB using the URI from the .env file
    app.mongodb_client = MongoClient(config["MONGO_URI"])
    # Select the database specified in the .env file
    app.database = app.mongodb_client[config["DB_NAME"]]

    # Connect to Neo4j using credentials from the .env file
    neo4j_uri = config['NEO4J_URI']
    neo4j_user = config['NEO4J_USER']
    neo4j_password = config['NEO4J_PASSWORD']
    app.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

@app.get("/")
async def root():
    # Simple root endpoint to check if the API is running
    return {"message": "Final Lab - MongoDB & Neo4j"}

# Function to fetch movie titles from MongoDB
def get_mongodb_movie_titles():
    # Fetch titles from the 'movies' collection, excluding the '_id' field
    movies = app.database["movies"].find({}, {"title": 1, "_id": 0})
    # Return a set of titles
    return {movie["title"] for movie in movies if "title" in movie}

# Function to fetch movie titles from Neo4j
def get_neo4j_movie_titles():
    query = "MATCH (m:Movie) RETURN m.title AS title"
    with app.neo4j_driver.session() as session:
        result = session.run(query)
        # Return a set of titles
        return {record["title"] for record in result}

@movies_router.get("/common_movies", response_description="Get the number of common movies between MongoDB and Neo4j", tags=["MongoDB & Neo4j"])
def get_common_movies():
    try:
        # Fetch movie titles from MongoDB
        mongodb_titles = get_mongodb_movie_titles()

        # Fetch movie titles from Neo4j
        neo4j_titles = get_neo4j_movie_titles()

        # Find the common titles between the two sets
        common_titles = mongodb_titles.intersection(neo4j_titles)

        # Return the count of common movies and the titles
        return {"common_movies_count": len(common_titles)}, common_titles

    except Exception as e:
        # Handle any errors and return a 500 status code
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Function to fetch people who rated a specific movie from Neo4j
def get_people_who_rated_movie(m_title: str):
    query = """
    MATCH (u:Person)-[r:REVIEWED]->(m:Movie {title: $title})
    RETURN u.name AS user_name
    """
    with app.neo4j_driver.session() as session:
        result = session.run(query, title=m_title)
        # Return a list of user names
        return [record["user_name"] for record in result]

@movies_router.get("/reviewers-who-rated", response_description="Get users who rated a specific movie", tags=["Neo4j"])
def people_who_rated_movie(title: str):
    try:
        # Fetch the users who rated the specified movie
        users = get_people_who_rated_movie(title)
        if users:
            # Return the list of users
            return {"users": users}
        # If no users found, return a 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No person reviewed the movie titled '{title}'")
    except Exception as e:
        # Handle any errors and return a 500 status code
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Function to fetch reviewers details by their name from Neo4j
def get_reviewer_details(user_name: str):
    query = """
    MATCH (u:Person {name: $name})-[r:REVIEWED]->(m:Movie)
    RETURN u.name AS user_name, count(m) AS rated_movies_count, collect(m.title) AS rated_movies
    """
    with app.neo4j_driver.session() as session:
        result = session.run(query, name=user_name)
        record = result.single()
        if record:
            # Return reviewers details including the count of rated movies and their titles
            return {
                "user_name": record["user_name"],
                "rated_movies_count": record["rated_movies_count"],
                "rated_movies": record["rated_movies"]
            }
        return None

@movies_router.get("/reviewers-ratings", response_description="Get user details with the number of movies rated and the list of rated movies", tags=["Neo4j"])
def reviewer_ratings(name: str):
    try:
        # Fetch the details of the user
        user_details = get_reviewer_details(name)
        if user_details:
            # Return the user details
            return user_details
        # If user not found, return a 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User named '{name}' not found")
    except Exception as e:
        # Handle any errors and return a 500 status code
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Include the movies router with the prefix /movies
app.include_router(movies_router, prefix="/movies")

@app.on_event("shutdown")
def shutdown_db_client():
    # Close the MongoDB client
    app.mongodb_client.close()
    # Close the Neo4j driver
    app.neo4j_driver.close()
