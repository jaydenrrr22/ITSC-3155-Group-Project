import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from sqlalchemy import text
from .dependencies.database import engine


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Resets the increment on tables to start from one
#order_details does not start at 1 in the DB
@app.on_event("startup")
def reset_auto_increment():
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE customers AUTO_INCREMENT = 1"))
        conn.execute(text("ALTER TABLE orders AUTO_INCREMENT = 1"))
        conn.execute(text("ALTER TABLE order_details AUTO_INCREMENT = 1"))
        conn.commit()

model_loader.index()
indexRoute.load_routes(app)

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)