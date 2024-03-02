from fastapi import FastAPI, Query, HTTPException, status, Body
from pydantic import BaseModel
from base64 import b64decode
import requests

# Replace with the actual MAS service URL and API endpoint
MAS_SERVICE_URL = "https://cia-mas.cialabs.tech/"  # Replace with actual URL
MAS_SERVICE_ENDPOINT = "/upload/"  # Replace with actual endpoint

app = FastAPI()

@app.get("/test_model")
async def test_model(base64: str = Query(..., description="Base64-encoded image data"), model_name: str = Query(..., description="Name of the model to use")):
   

    if not all([base64, model_name]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required parameters: base64 and model_name")

    try:
        # Validate and decode base64 image data
        image_data = b64decode(base64)

        # Prepare request data for the MAS service
        data = {"image": ("image", image_data), "model_name": model_name}

        # Send request to the MAS service using the 'data' parameter
        response = requests.post(f"{MAS_SERVICE_URL}{MAS_SERVICE_ENDPOINT}", data=data)

        # Check for successful response
        if response.status_code == 200:
            # Return the response from the MAS service as JSON
            return response.json()
        else:
            # Raise an exception with the error details from the MAS service
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except (ValueError, requests.exceptions.RequestException) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error sending request to MAS service: {str(e)}")

class Feedback(BaseModel):
    modelName : str
    image: str
    result: str


@app.post("/feedback")
async def create_feedback(feedback: Feedback):
    feedback_id = collection.insert_one(feedback.dict()).inserted_id
    return {"message": "Feedback submitted successfully", "feedback_id": str(feedback_id)}


# ... other app routes and configuration

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("your_filename:app", host="0.0.0.0", port=8000, reload=True)
