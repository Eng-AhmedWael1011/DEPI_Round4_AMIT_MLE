import mlflow

if __name__ == "__main__":

    try:
        experiment_id = mlflow.create_experiment(
            name='EXP 1',
            artifact_location= 'testing_artifact',
            tags={'env' : 'dev'}
        )
    except Exception as e:
        print(e)

    
    print(experiment_id)