
from fastapi import APIRouter, Request
from service.movies import MovieService
from models.response.award_response import AwardResponse
from utils.logging import logger

api = APIRouter(prefix='/awards')


@api.get(path='/get-awards-interval', response_model=AwardResponse)
def get_awards_interval(request: Request):
    logger.debug("Executando busca dos produtores premiados.")
    
    movie_service = MovieService(request.state.engine)
    ret = movie_service.get_award_intervals()
    
    logger.debug("Busca dos produtores premiados executada com sucesso!")
    
    return ret
