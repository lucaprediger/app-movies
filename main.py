import uvicorn
import traceback
from fastapi import FastAPI, Request
from controller.award import api as awards_router
from sqlmodel import create_engine, SQLModel
from sqlalchemy.pool import StaticPool
from contextlib import asynccontextmanager
from service.movies import MovieService


sqlite_url = "sqlite:///:memory:"
engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        SQLModel.metadata.create_all(engine)
        movie_service = MovieService(engine)
        
        data = movie_service.read_data_from_csv()
        movie_service.persist_data_on_database(data)
    except Exception as e:
        msg = "Aplicação não pode iniciar: erro ao carregar dados para o banco de dados"
        raise Exception(f"{msg}: {traceback.format_exc()}")
        
    yield

app = FastAPI(lifespan=lifespan)
    
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.engine = engine 
    
    response = await call_next(request)
    return response


app.include_router(awards_router)
    

if __name__ == '__main__':
    uvicorn.run(
        app,
        port=8000,
        host='0.0.0.0'
    )