from sqlmodel import Session, text

from models.database.movie import Movie


class Database():
    def __init__(self, engine):
        self.engine = engine
        
    def persist_itens(self, movies: list[Movie]):
        with Session(self.engine) as session:
            session.add_all(movies)
            
            movies = [obj for obj in session.new if isinstance(obj, Movie)]
            session.commit()
            
            return movies

    def get_award_intervals(self):
        query = text("""
            WITH producer_wins AS (
                SELECT
                    p.name as producer,
                    m.year,
                    LAG(m.year) OVER (
                        PARTITION BY p.id
                        ORDER BY m.year
                    ) AS previous_year
                FROM movie m
                JOIN movieproducerlink link_m_p ON link_m_p.movie_id = m.id
                JOIN producer p ON p.id = link_m_p.producer_id
                WHERE m.winner = 1
            ),
            intervals AS (
                SELECT
                    producer AS producer,
                    year - previous_year AS interval,
                    previous_year AS previousWin,
                    year AS followingWin
                FROM producer_wins
                WHERE previous_year IS NOT NULL
            )
            SELECT a.*, 'min' AS is_from  FROM intervals a
            WHERE interval = (SELECT MIN(interval) FROM intervals)
            UNION ALL
            SELECT a.*, 'max' AS is_from FROM intervals a
            WHERE interval = (SELECT MAX(interval) FROM intervals)
        """)

        with Session(self.engine) as session:
            return session.exec(query).mappings().all()
