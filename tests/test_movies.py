import pytest
from httpx import ASGITransport, AsyncClient
from main import app, engine
from sqlmodel import SQLModel
from service.movies import MovieService
from models.response.award_response import AwardResponse


@pytest.fixture(autouse=True)
def setup_database():
    SQLModel.metadata.create_all(engine)
    
    service = MovieService(engine)
    data = service.read_data_from_csv()
    service.persist_data_on_database(data)
    
    yield
    

@pytest.mark.asyncio
async def test_award_intervals_integration():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as ac:
        response = await ac.get("/awards/get-awards-interval")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "min" in data, "A resposta deve conter a chave 'min'"
        assert "max" in data, "A resposta deve conter a chave 'max'"
        
        for category in ["min", "max"]:
            for item in data[category]:
                assert "producer" in item
                assert "interval" in item
                assert "previousWin" in item
                assert "followingWin" in item
                
                calculated_interval = item["followingWin"] - item["previousWin"]
                assert item["interval"] == calculated_interval, \
                    f"Intervalo incorreto para o produtor {item['producer']}"

        if data["min"] and data["max"]:
            min_val = data["min"][0]["interval"]
            max_val = data["max"][0]["interval"]
            assert min_val <= max_val, "O intervalo mínimo não pode ser maior que o máximo"

        assert len(data["min"]) > 0, "Deveria haver ao menos um produtor no intervalo mínimo"
        assert len(data["max"]) > 0, "Deveria haver ao menos um produtor no intervalo máximo"