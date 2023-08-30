from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, authentication, votes
from .config import settings


from fastapi.middleware.cors import CORSMiddleware

print(settings.database_password)

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message:": "Do self-assesment and admit things about yourself."}

