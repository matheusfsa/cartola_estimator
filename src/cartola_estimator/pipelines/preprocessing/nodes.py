"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.0
"""
from typing import List, Tuple, Any, Dict
from unidecode import unidecode
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def add_match_info(cartola_data: pd.DataFrame, cb_data: pd.DataFrame) -> pd.DataFrame:
    """
    This node add match info (opponent, results, ...) to data.
    """
    # Normalize clube name
    cartola_data["clube"] = cartola_data["atletas_clube_id_full_name"].apply(unidecode)
    cartola_data["clube"] = cartola_data["clube"].replace(
        {"Atletico-PR": "Athletico-PR"}
    )
    cartola_data = cartola_data.drop_duplicates(
        ["rodada", "ano", "atletas_slug", "clube"]
    )

    cartola_data["rodada"] = cartola_data["rodada"].astype(int)

    cb_data["rodada"] = cb_data["rodada"].astype(int)
    cb_data["data"] = pd.to_datetime(cb_data.data)
    cb_data["ano"] = cb_data.data.dt.year
    cb_data = cb_data[cb_data.data.dt.year >= cartola_data.ano.min()]
    mando = pd.melt(
        cb_data[["rodada", "ano", "mandante", "visitante", "vencedor"]],
        value_vars=["mandante", "visitante"],
        value_name="clube",
        var_name="mando",
        id_vars=["rodada", "ano", "vencedor"],
    )
    mandante = mando[mando.mando == "mandante"]
    visitante = mando[mando.mando == "visitante"]

    mandante = pd.merge(
        mandante,
        cb_data[["rodada", "ano", "mandante", "visitante"]],
        left_on=["rodada", "ano", "clube"],
        right_on=["rodada", "ano", "mandante"],
        how="left",
    )
    visitante = pd.merge(
        visitante,
        cb_data[["rodada", "ano", "mandante", "visitante"]],
        left_on=["rodada", "ano", "clube"],
        right_on=["rodada", "ano", "visitante"],
        how="left",
    )

    mando = pd.concat((mandante, visitante), ignore_index=True)
    mando["oponente"] = np.where(
        mando.mando == "mandante", mando.visitante, mando.mandante
    )
    mando["resultado"] = np.where(mando.clube == mando.vencedor, "V", mando.vencedor)
    mando["resultado"] = np.where(
        mando.resultado == mando.oponente, "D", mando.resultado
    )
    mando["resultado"] = np.where(mando.resultado == "-", "E", mando.resultado)
    return pd.merge(cartola_data, mando, on=["rodada", "ano", "clube"], how="left")


def create_target_data(
    data: pd.DataFrame,
    stats_dict: Dict[str, Any],
) -> pd.DataFrame:
    """This node create a data with stats by rounds"""
    target = pd.DataFrame()
    stats = [stat["id"] for k, stat in stats_dict.items()]
    atleta_acc = data[data["atletas_posicao_id"] != "tec"]
    for _, g_data in atleta_acc.groupby(["ano", "atletas_slug", "clube"], sort=False):
        players_stats = g_data.sort_values("rodada")
        players_stats[stats] = players_stats[stats].fillna(0).diff()
        target = pd.concat((target, players_stats), ignore_index=True)

    # As rodadas 37, 38, 10 e 11 de 2020 apresentaram dados "estranhos"
    target = target[~((target.rodada.isin([37, 38, 10, 11])) & (target.ano == 2020))]

    target["rodada"] = target["rodada"] - 1
    target = target[target.rodada > 0]
    target["time_idx"] = (target["ano"] - target["ano"].min()) * target[
        "rodada"
    ].max() + target["rodada"]
    return target


def create_hist_features(
    data: pd.DataFrame,
    columns: List[str],
    window: int,
    stats_dict: Dict[str, Any],
    id_cols: List[str],
) -> pd.DataFrame:
    """This node create historical features"""

    stats = [stat["id"] for k, stat in stats_dict.items()]
    data = data[id_cols + stats]

    for c in columns:
        data = _hist_features(data, c, window, stats)
    return data


def _hist_features(data, col, window, stats):

    group_stats = (
        data.groupby(["time_idx", "rodada", "ano", col]).mean()[stats].reset_index()
    )

    hist_stats = (
        group_stats.set_index("time_idx")
        .groupby([col])
        .rolling(window=window, min_periods=1)
        .mean()[stats]
        .reset_index()
    )
    hist_stats["time_idx"] += 1
    data = pd.merge(
        data, hist_stats, on=["time_idx", col], how="left", suffixes=("", f"_{col}")
    )
    return data


def split_test_val(
    data: pd.DataFrame, test_size: float, val_size: float, random_seed: int
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """This node split data in train/test."""
    train, test = train_test_split(data, test_size=test_size, random_state=random_seed)
    train, val = train_test_split(train, test_size=val_size, random_state=random_seed)
    return train, val, test
