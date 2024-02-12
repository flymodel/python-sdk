import zlib
from io import BytesIO

import pytest
from polars import DataFrame

from flymodel.client import PartialUploadExperimentArgs, UploadRequestParams
from flymodel.experiment import Experiment
from flymodel.models.enums import ArchiveCompression, ArchiveFormat

from .fixture import client
from .test_create_experiment import create_experiment_variables as initial_experiment


def get_some_df():
    return DataFrame(
        {
            "a": [1, 2, 3],
            "b": [4, 5, 6],
        }
    )


@pytest.mark.asyncio
async def test_it(client):
    exp = await initial_experiment(client)

    async with Experiment(client, args=exp) as test:
        args = PartialUploadExperimentArgs(
            UploadRequestParams(
                artifact_name="abc.txt",
                format=ArchiveFormat("txt"),
                encode=None,
            ),
        )

        resp = await test.save_artifact(args, b"okok")

        assert resp.name == "abc.txt"
        assert resp.experiment_id == test.id
        assert resp.version_id == test.experiment.version_id

        fits = get_some_df()
        bts = BytesIO()
        fits.write_ipc(bts)

        args = PartialUploadExperimentArgs(
            UploadRequestParams(
                artifact_name="abc.arrow",
                format=ArchiveFormat("arrow"),
                encode=ArchiveCompression("gzip"),
            ),
        )
        resp = await test.save_artifact(args, zlib.compress(bts.getvalue()))
