from fastapi import FastAPI, UploadFile, File
import pandas as pd
from io import StringIO

app = FastAPI()

# Dummy function to get movie titles from IDs (you would replace this with your actual logic)
def get_movie_titles_from_ids(ids):
    # For demonstration, this function just returns a string "Movie_" with the ID.
    # Replace this with actual logic to fetch movie titles.
    return [f"Movie_{id}" for id in ids]

@app.post("/process/")
async def process_file(file: UploadFile = File(...)):
    # Read the file into a string
    content = await file.read()
    string_io = StringIO(content.decode())

    # Convert string to DataFrame
    df = pd.read_csv(string_io)

    # Extract the 'PageVisited' column to get movie IDs
    movie_ids = df['PageVisited'].unique().tolist()

    # Convert movie IDs to titles
    movie_titles = get_movie_titles_from_ids(movie_ids)

    return {"movie_titles": movie_titles}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
