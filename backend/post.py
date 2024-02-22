from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
import base64

app = FastAPI()

# Replace 'YOUR_MAS_SERVICE_URL' with the actual URL of your MAS service
MAS_SERVICE_URL = "http://noobed-max/test_model"

@app.get("/test_model")
async def test_model(base64_data: str, model_name: str):
    try:
        # Your base64 decoding logic here if needed
        # decoded_data = base64.b64decode(base64_data)

        # Making a request to the MAS service
        async with httpx.AsyncClient() as client:
            response = await client.get(
                MAS_SERVICE_URL,
                params={"base64_data": base64_data, "model_name": model_name},
            )

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Assuming MAS service returns JSON response, you can return it
        return JSONResponse(content=response.json(), status_code=200)

    except httpx.HTTPError as e:
        # Handle HTTP errors from MAS service
        return JSONResponse(content={"error": f"MAS service error: {str(e)}"}, status_code=e.response.status_code)

    except Exception as e:
        # Handle other exceptions
        return JSONResponse(content={"error": f"Internal server error: {str(e)}"}, status_code=500)
