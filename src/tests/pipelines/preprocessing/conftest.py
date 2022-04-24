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
            "atletas_clube_id_full_name": [
                "São Paulo",
                "Sao Paulo",
                "Sao Paulo",
                "Athletico-PR",
                "Athletico-PR",
                "Athletico-PR",
            ],
            "G": [0, 1, 1, 0, 0, 1],
            "A": [0, 0, 1, 0, 2, 3],
        }
    )
    return df


@pytest.fixture(scope="module")
def cb_data():
    df = pd.DataFrame(
        {
            "data": [
                "2020-03-27",
                "2020-03-28",
                "2020-03-29",
                "2020-03-27",
                "2020-03-28",
                "2020-03-29",
            ],
            "rodada": ["1", "2", "3", "1", "2", "3"],
            "mandante": [
                "Sao Paulo",
                "Coritiba",
                "Sao Paulo",
                "Athletico-PR",
                "Athletico-PR",
                "Bahia",
            ],
            "visitante": [
                "Gremio",
                "Sao Paulo",
                "Cruzeiro",
                "Vasco",
                "Internacional",
                "Athletico-PR",
            ],
            "vencedor": [
                "Gremio",
                "Sao Paulo",
                "-",
                "Vasco",
                "Athletico-PR",
                "Athletico-PR",
            ],
        }
    )
    return df


@pytest.fixture(scope="module")
def cartola_hist_data():
    df = pd.DataFrame(
        {
            "rodada": [1, 2, 3, 1, 2, 3],
            "ano": [2020, 2020, 2020, 2020, 2020, 2020],
            "atletas_slug": ["pablo", "pablo", "pablo", "nikao", "nikao", "nikao"],
            "atletas_posicao_id": ["ata", "ata", "ata", "mei", "mei", "mei"],
            "clube": [
                "Sao Paulo",
                "Sao Paulo",
                "Sao Paulo",
                "Athletico-PR",
                "Athletico-PR",
                "Athletico-PR",
            ],
            "G": [0, 1, 1, 0, 0, 1],
            "A": [0, 0, 1, 0, 2, 3],
        }
    )
    return df


@pytest.fixture(scope="module")
def cartola_data():
    df = pd.DataFrame(
        {
            "time_idx": [1, 2, 1, 2],
            "rodada": [1, 2, 1, 2],
            "ano": [2020, 2020, 2020, 2020],
            "atletas_slug": ["pablo", "pablo", "nikao", "nikao"],
            "atletas_posicao_id": ["ata", "ata", "ata", "ata"],
            "clube": ["Sao Paulo", "Sao Paulo", "Athletico-PR", "Athletico-PR"],
            "oponente": ["Gremio", "Cruzeiro", "Vasco", "Internacional"],
            "G": [1, 0, 0, 1],
            "A": [0, 1, 2, 1],
        }
    )
    return df


@pytest.fixture(scope="module")
def stats_dict():
    return {
        "assistencias": {"id": "A", "pos": ["mei", "ata"]},
        "gols": {"id": "G", "pos": ["mei", "ata"]},
    }


@pytest.fixture(scope="module")
def columns():
    return ["atletas_posicao_id"]


@pytest.fixture(scope="module")
def id_cols():
    return [
        "time_idx",
        "rodada",
        "ano",
        "clube",
        "atletas_slug",
        "oponente",
        "atletas_posicao_id",
    ]
