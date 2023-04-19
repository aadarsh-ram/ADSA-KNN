import pandas as pd
import uvicorn
from fastapi import FastAPI, status, Response, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from diabetes_classify import data_preprocessing, get_kd_tree

# Create KDTree KNN Classifier
data = pd.read_csv('diabetes.csv')
train_data, test_data = data_preprocessing(data)
kd_tree = get_kd_tree(train_data)

app = FastAPI()

# Allow anyone to call the API from their own apps
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
async def hello():
    return {"message": "Hello user! Tip: open /docs or /redoc for documentation"}

@app.post("/predict")
async def predict(request: Request, n_neighbors: int = 5):
    incoming_data = await request.json()
    pred_val = list(incoming_data.values())
    print (pred_val)
    neighbors = kd_tree.get_knn(pred_val, n_neighbors)
    outcomes = [neighbor[1][-1] for neighbor in neighbors]
    prediction = max(set(outcomes), key=outcomes.count)
    return {"prediction": prediction}

if __name__ == '__main__':
    uvicorn.run("app:app", reload=True)