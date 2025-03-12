from fastapi import FastAPI
from router.route import router as predict_router

app = FastAPI()

# Daftarkan route
app.include_router(predict_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
