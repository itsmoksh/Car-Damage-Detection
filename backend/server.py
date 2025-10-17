from fastapi import FastAPI,File,UploadFile
from ..prediction import predict
app = FastAPI()

@app.post("/predict")
async def get_predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image_path = '../temp.jpg'
        with open(image_path, 'wb') as f:
            f.write(image_bytes)
        result = predict(image_path)
        return result
    except Exception as e:
        return {"error":str(e)}