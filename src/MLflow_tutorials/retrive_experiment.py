import mlflow
from mlflow_utils import get_mlflow_experiment

if __name__ == '__main__':

    experiment = get_mlflow_experiment(experiment_id = '1775746551630')

    print(f'exp name: {experiment.name}')
    