from fastapi import FastAPI, Body, HTTPException, status
from base64 import b64decode
from PIL import Image 
import io

app = FastAPI()

@app.post("/feedback")
async def receive_feedback(data: dict = Body(...), modelName: str = None, image: str = None, result: str = None):
    

    if not all([modelName, image, result]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required fields: modelName, image, and result")

    try:
        # Validate and decode base64 image (assuming binary image format)
        image_data = b64decode(image)
        image = Image.open(io.BytesIO(image_data))  # Assuming binary image format

        return {"message": "Feedback received successfully!", "modelName": modelName, "result": result}

    except (ValueError, IOError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid image data: {str(e)}")

# ... other app routes and configuration

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
