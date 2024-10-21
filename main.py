from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import httpx  

from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# Pydantic model to receive the base64 image
class ImageData(BaseModel):
    base64_image: str

# @app.post("/upload")
# async def upload_image(image_data: ImageData):
#     try:
#         from db import initialize_counter, insert_url_document      
#         # Prepare the request to Freeimage.host
#         response = requests.post(
#             "https://freeimage.host/api/1/upload",
#             data={
#                 "key": "6d207e02198a847aa98d0a2a901485a5",  # Replace with your Freeimage.host API key
#                 "source": image_data.base64_image,
#                 "format": "json",
#             },
#         )

#         # Check if the response was successful
#         if response.status_code == 200:
#             initialize_counter()
#             id=insert_url_document(response.json()['image']['url'])
#             return id
#         else:
#             raise HTTPException(status_code=response.status_code, detail=response.text)
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# Instead of requests

@app.post("/upload")
async def upload_image(image_data: ImageData):
    try:
        from db import initialize_counter, insert_url_document
        # Prepare the request using httpx for async operations
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://freeimage.host/api/1/upload",
                data={
                    "key": "6d207e02198a847aa98d0a2a901485a5",  # Replace with your Freeimage.host API key
                    "source": image_data.base64_image,
                    "format": "json",
                }
            )

        # Check if the response was successful
        if response.status_code == 200:
            initialize_counter()
            id = insert_url_document(response.json()['image']['url'])
            return id
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the FastAPI app, use the command: uvicorn filename:app --reload

@app.get("/")
async def root():
      return {"message": "Deployed Succesfully!"}