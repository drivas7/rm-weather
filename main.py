from fastapi import FastAPI
from app.api import app as weather_api_app

app = FastAPI()

# Mount the weather API app under the root URL "/"
app.mount("/", weather_api_app)

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)