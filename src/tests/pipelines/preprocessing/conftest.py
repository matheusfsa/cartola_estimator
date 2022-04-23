import pytest
import pandas as pd

@pytest.fixture(scope="module")
def cartola_raw_data():
    df = pd.DataFrame(
        {
            "rodada": ["1", "2", "3", "1", "2", "3"],
            "ano": [2020, 2020, 2020, 2020, 2020, 2020],
            "atletas_slug": ["pablo", "pablo", "pablo", "nikao", "nikao", "nikao"],
            "atletas_posicao_id": ["ata", "ata", "ata", "gol", "gol", "gol"],
            "atletas_clube_id_full_name": ["São Paulo", "Sao Paulo", "Sao Paulo", "Athletico-PR", "Athletico-PR", "Athletico-PR"],
            "G": [0, 1, 1, 0, 0, 1],
            "A": [0, 0, 1, 0, 2, 3],
        }
    )
    return df

@pytest.fixture(scope="module")
def cb_data():
    df = pd.DataFrame(
        {
            "data": ["2020-03-27", "2020-03-28", "2020-03-29", "2020-03-27", "2020-03-28", "2020-03-29"],
            "rodada": ["1", "2", "3", "1", "2", "3"],
            "mandante": ["Sao Paulo", "Sao Paulo", "Sao Paulo", "Athletico-PR", "Athletico-PR", "Athletico-PR"],
            "visitante": ["Gremio", "Coritiba", "Cruzeiro", "Vasco", "Internacional", "Bahia"],
            "vencedor": ["Gremio", "Sao Paulo", "Cruzeiro", "Vasco", "Athletico-PR", "Athletico-PR"],
        }
    )
    return df

@pytest.fixture(scope="module")
def cartola_hist_data():
    df = pd.DataFrame(
        {
            "rodada": ["1", "2", "3", "1", "2", "3"],
            "ano": [2020, 2020, 2020, 2020, 2020, 2020],
            "atletas_slug": ["pablo", "pablo", "pablo", "nikao", "nikao", "nikao"],
            "atletas_posicao_id": ["ata", "ata", "gol", "gol"],
            "atletas_clube_id_full_name": ["São Paulo", "Sao Paulo", "Athletico-PR", "Athletico-PR"],
            "G": [0, 1, 1, 0, 0, 1],
            "A": [0, 0, 1, 0, 2, 3],
        }
    )
    return df