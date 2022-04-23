"""
This is a boilerplate test file for pipeline 'preprocessing'
generated using Kedro 0.18.0.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""
from cartola_estimator.pipelines.preprocessing.nodes import (add_match_info,
                                                             create_target_data,
                                                             create_hist_features)

def test_add_match_info(cartola_raw_data, cb_data):
    cartola_info = add_match_info(cartola_raw_data, cb_data)
    assert (cartola_info.clube.unique() == ["Sao Paulo", "Athletico-PR"]).all()
    assert (cartola_info.resultado == ["D", "V", "E", "D", "V", "V"]).all()
    assert (cartola_info.mando == ["mandante", "visitante", "mandante", "mandante", "mandante", "visitante"]).all()

def test_create_target_data(cartola_hist_data, stats_dict, cartola_data):
    cartola_data = create_target_data(cartola_hist_data, stats_dict)
    assert (cartola_data.G == [1, 0, 0, 1]).all()
    assert (cartola_data.A == [0, 1, 2, 1]).all()

def test_create_hist_features(cartola_data, columns, stats_dict, id_cols):
    hist_features = create_hist_features(cartola_data, columns, 1, stats_dict, id_cols)
    assert "G_atletas_posicao_id" in hist_features.columns
    assert hist_features[hist_features.rodada == 2]["A_atletas_posicao_id"].mean() == 1
    assert hist_features[hist_features.rodada == 2]["G_atletas_posicao_id"].mean() == 0.5