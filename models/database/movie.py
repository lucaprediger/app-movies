from sqlmodel import SQLModel, Field, Relationship


class MovieStudioLink(SQLModel, table=True):
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    studio_id: int = Field(foreign_key="studio.id", primary_key=True)


class MovieProducerLink(SQLModel, table=True):
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    producer_id: int = Field(foreign_key="producer.id", primary_key=True)
    

class Producer(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str

    movies: list["Movie"] = Relationship(back_populates="producers", link_model=MovieProducerLink)
    
    
class Studio(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str

    movies: list["Movie"] = Relationship(back_populates="studios", link_model=MovieStudioLink)


class Movie(SQLModel, table=True):
    id: int = Field(primary_key=True)

    year: int
    title: str
    winner: bool = False

    studios: list[Studio] = Relationship(back_populates="movies", link_model=MovieStudioLink)
    producers: list[Producer] = Relationship(back_populates="movies", link_model=MovieProducerLink)