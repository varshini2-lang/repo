from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field



app = FastAPI()

# Define a feedback model
class FeedbackItem(BaseModel):
    modelName: str
    image: str  # Assuming the image is a base64-encoded string
    result: str
class Config:
        arbitrary_types_allowed = True


# Endpoint to receive feedback via HTTP-Post
@app.post("/feedback")
async def submit_feedback(feedback: FeedbackItem = Body(...)):
    # Assuming feedback is stored or processed here
    # You can add your logic to handle the feedback data as needed
    
    # For demonstration, let's just echo the received feedback
    return {"message": "Feedback received", "feedback": feedback}
