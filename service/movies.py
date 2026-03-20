import csv
from models.database.movie import Movie, Studio, Producer
from models.response.award_response import AwardResponse, ProducerIntervalResponse
from database.database import Database
from utils.logging import logger

class MovieService():
    def __init__(self, engine):
        self.csv_path = "./csv/movielist.csv"
        self.engine = engine
        self.database = Database(engine)
        self.cache_producers = {}
        self.cache_studios = {}
        
        
    def get_studio(self, studio_str: str) -> list[Studio]:
        studio_list = studio_str.split(",")
        ret: list[Studio] = []
        for studio in studio_list:
            if studio:
                studio = studio.strip()
                if studio in self.cache_studios:
                    ret.append(self.cache_studios[studio])
                else:
                    self.cache_studios[studio] = Studio(name=studio)
                    ret.append(self.cache_studios[studio])
        
        return ret
    
    def get_producer(self, producer_str: str) -> list[Producer]:
        producer_list = producer_str.replace(" and ", ",").split(',')
        ret: list[Producer] = []
        for producer in producer_list:
            if producer:
                producer = producer.strip()
                if producer in self.cache_producers:
                    ret.append(self.cache_producers[producer])
                else:
                    self.cache_producers[producer] = Producer(name=producer)
                    ret.append(self.cache_producers[producer])
        return ret
    
    def read_data_from_csv(self) -> list[Movie]:
        logger.debug(f"Iniciando processo de leitura do arquivo: {self.csv_path}")
       
        movies: list[Movie] = []
        with open(self.csv_path, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                winner = True if row["winner"].lower() == "yes" else False
                
                studios = self.get_studio(row["studios"])
                producers = self.get_producer(row["producers"])
                
                movie = Movie(
                    year=int(row["year"]),
                    title=row["title"],
                    studios=studios,
                    producers=producers,
                    winner=winner
                )
                movies.append(movie)
                
        logger.debug(f"Total de itens Lidos: {len(movies)}")
        
        return movies
        
    def persist_data_on_database(self, movies: list[Movie]):
        logger.debug("Iniciando persistência do Banco de dados!")
        
        movies = self.database.persist_itens(movies)
        
        logger.debug(f"Sucesso na persistência de: {len(movies)} no Banco de dados!")
        
    def get_award_intervals(self) -> AwardResponse:
        items = self.database.get_award_intervals()
        
        ret = AwardResponse(min=[], max=[])
        for item in items:
            data = ProducerIntervalResponse(**item)
            if item.is_from == 'min':
                ret.min.append(data)
            else:
                ret.max.append(data)
                
        return ret