# Final_lab
Exercise on Neo4j and MongoDB by Branly DJIME and Emmanuel LAWAIGE

﻿On Windows
1. Prerequisites
- Python 3.11+, Neo4j Sandbox, MongoDB Compass

2. 
- Create virtual enviromment
python -m venv env
- Activate virtual enviroment
.\env\Scripts\activate

3. Install Dependencies
pip install fastapi uvicorn pymongo neo4j python-dotenv

4. Setting up MongoDB
Load  "movies.json" to a collection you'll name 'movies' to a database of your choice on MongoDB Compass

5. Create a .env file
- Place it in the root directory of your project
- Add the following to the file

MONGO_URI=mongodb://localhost:27017 
DB_NAME="movies_db"
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="your_password"

Don't forget to adjust the values to your context

6. Add the files to your project
main.py, models.py, route.py

7. Run the FastAPI application (After having activated your env)
- uvicorn main:app --reload (on cmd)
- http://127.0.0.1:8000:docs (on a browser) to access the app

8. Shutting Down (on cmd)
- Press 'Ctrl+C' to stop the server 
- deactivate 

