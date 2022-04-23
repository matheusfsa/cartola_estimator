"""
This is a boilerplate test file for pipeline 'preprocessing'
generated using Kedro 0.18.0.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""
from cartola_estimator.pipelines.preprocessing.nodes import add_match_info

def test_add_match_info(cartola_raw_data, cb_data):
    cartola_info = add_match_info(cartola_raw_data, cb_data)
    print(cartola_info)
    assert (cartola_info.clube.unique() == ["Sao Paulo", "Athletico-PR"]).all()
    assert (cartola_info.resultado == ["D", "V", "D", "D", "V", "V"]).all()