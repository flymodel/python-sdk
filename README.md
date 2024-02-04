# Flymodel Python

This repo contains source code for the python client for `flymodel`.



### Usage


```python
from flymodel import Client, models
from flymodel.experiment import Experiment

async def main():
    client = Client(base_url="http://localhost:9009")

    model = models.create_model.CreateModelVariables(name="test_model", namespace=1)
    model = await client.create_model(model)

    version = models.create_model_version.CreateModelVersionVariables(
        model_id=model.create_model.id, version_tag="v1.0.0rc1"
    )
    version = await client.create_model_version(version)

    new = models.create_experiment.CreateExperimentVariables(
        experiment_name="my-experiment",
        model_version_id=version.create_model_version.id,
    )

    resp = await client.create_experiment(new)
    async with Experiment(client) as test:
        args = UploadExperimentArgs(
            experiment=exp.id,
            params=UploadRequestParams(
                artifact_name="abctest",
                format=None,
                encode=None,
            ),
        )

        resp = await test.save_artifact(args, b"okok")
```