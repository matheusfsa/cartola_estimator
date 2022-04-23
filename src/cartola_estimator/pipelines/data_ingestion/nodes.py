"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 0.18.0
"""
from distutils.log import error
import re
import json
from typing import List
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

_TEAMS = {
        '373': "Atlético-GO", '293': 'Athlético-PR', '282': 'Atlético-MG',
        '284': 'Grêmio', '276':'São Paulo', '265': 'Bahia', '266': 'Fluminense',
        '356': 'Fortaleza', '264': 'Corinthians','354': 'Ceará',
        '267': 'Vasco', '263': 'Botafogo', '290': 'Goiás', '292': 'Sport',
        '285': 'Internacional' , '275': 'Palmeiras', '280': 'Bragantino', '262': 'Flamengo',
        '1371': 'Cuiabá', '315':'Chapecoense', '327':'América-MG', '286':'Juventude', '277': 'Santos'
    }

def load_cartola_data(years: List[int]) -> pd.DataFrame:
    """
    This node load data with information about
    rounds of Cartola app to a DataFrame.
    """
    cartola_data = pd.DataFrame()
    for year in years:
        if year == 2021:
            files_iter = CartolaFiles(year, f_prefix="Mercado_", f_ext="txt")
            for rodada, url in tqdm(files_iter, total=len(files_iter)):
                rodada_df = _process_mercado(year, rodada, url)
                cartola_data = pd.concat((cartola_data, rodada_df), ignore_index=True)

        else:
            files_iter = CartolaFiles(year, f_prefix="rodada-", f_ext="csv")
            for rodada, url in tqdm(files_iter, total=len(files_iter)):
                rodada_df = _process_round(year, rodada, url)
                cartola_data = pd.concat((cartola_data, rodada_df), ignore_index=True)
    id_cols = [
        "atletas.atleta_id",
        "atletas.rodada_id",
        "atletas.clube_id",
        "atletas.posicao_id",
        "atletas.status_id",
    ]
    cartola_data[id_cols] = cartola_data[id_cols].astype("str")

    unused_cols = ["athletes$atletas$scout"]
    cartola_data = cartola_data.drop(columns=unused_cols, errors="ignore")
    cartola_data["atletas.clube.id.full.name"] = cartola_data["atletas.clube.id.full.name"].astype(str).replace(_TEAMS)
    cartola_data = cartola_data.rename(columns=replace_sep)
    return cartola_data

def replace_sep(x):
    """This function remove prefix with '.'"""
    return x.replace(".", "_")

class CartolaFiles:
    """
    This class is a iterator that get urls of the files
    with information about rounds of Cartola app. The data
    can be found at this link: https://github.com/henriquepgomide/caRtola
    """

    def __init__(self, year, f_prefix="rodada-", f_ext="txt"):
        self._f_prefix = f_prefix
        self._f_ext = f_ext
        self._year = year
        url = "https://github.com/henriquepgomide/caRtola/tree/master/data/{}".format(
            year
        )
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "lxml")
        self._files_tags = soup.find_all(
            "a", attrs={"href": re.compile(f"{f_prefix}([0-9]|[0-9][0-9])\.{f_ext}")}
        )
        self._n_files = len(self._files_tags)

    def __len__(self):
        return self._n_files

    def __iter__(self):
        for tag in self._files_tags:
            href_str = tag.get("href")
            round_id = re.search(f"{self._f_prefix}(.*?)\.\w*", href_str).group(1)
            file_name = href_str.split("/")[-1]
            url = (
                "https://raw.githubusercontent.com/"
                + f"henriquepgomide/caRtola/master/data/{self._year}/{file_name}"
            )
            yield round_id, url


def _process_round(ano, rodada, url):
    df = pd.read_csv(url)
    df = df.drop(columns=["Unnamed: 0"])
    df["rodada"] = rodada
    df["ano"] = ano
    return df


def _process_mercado(ano, rodada, url):

    response = urlopen(url)
    mercado = json.loads(response.read().decode("latin1"))
    atletas = mercado["atletas"]
    rodada_df = pd.DataFrame()
    for at in atletas:
        atleta_data = {}
        for k, v in at.items():
            if k == "scout":
                for k_scout, v_scout in v.items():
                    atleta_data[k_scout] = [v_scout]
            else:
                atleta_data[f"atletas.{k}"] = [v]

        rodada_df = pd.concat((rodada_df, pd.DataFrame(atleta_data)), ignore_index=True)
    rodada_df["atletas.clube.id.full.name"] = rodada_df["atletas.clube_id"].replace(_TEAMS)
    rodada_df["rodada"] = rodada
    rodada_df["ano"] = ano

    return rodada_df
