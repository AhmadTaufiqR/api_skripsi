from fastapi import APIRouter
from controller.predict_controller import get_predict

router = APIRouter()

@router.get("/predict")
def predict(height: float, age: int, gender: int, breastfeeding: int):
    return get_predict(height, age, gender, breastfeeding)

@router.get("/")
def root():
    return {"Hello" : "World"}
