from kedro.config import ConfigLoader
import pandas as pd
import mlflow
if __name__ == "__main__":
    conf_loader = ConfigLoader('conf', 'local')
    conf_mlflow = conf_loader.get('**/mlflow.yml')
    client = mlflow.tracking.MlflowClient(tracking_uri=conf_mlflow["server"]["mlflow_tracking_uri"])
    experiment = client.get_experiment_by_name(conf_mlflow["tracking"]["experiment"]["name"])

    runs = client.search_runs(experiment_ids=[experiment.experiment_id])
    runs.sort(key=lambda x: x.info.start_time, reverse=True)

    metrics = pd.Series(runs[0].data.metrics, name="rmse").to_frame()
    tb_md = metrics.to_markdown()
    tb_md = "## Metrics \n" +  tb_md
    with open("data/08_reporting/metrics.md", "w", encoding="utf-8") as f:
        f.write(tb_md)