from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup

from aws_mock.predefined import MASTER_REGION_BASE_IMAGE, MASTER_REGION_NAME
from tests.conftest import REGION_NAME

if TYPE_CHECKING:
    from unittest.mock import Mock

    from mypy_boto3_ec2 import EC2Client, EC2ServiceResource

    from tests.conftest import RunQueryFunc


IMAGE_ID = "ami-12345"


def test_describe_images(run_query: RunQueryFunc, mongo: Mock) -> None:
    mongo().aws_mock["ami"].find.return_value = [{
        "_id": "MOCKED_ID",
        "id": IMAGE_ID,
        "tags": {},
    }]
    response = run_query({
        "Action": "DescribeImages",
        "Version": "2016-11-15",
        "ImageId.1": IMAGE_ID,
    })
    mongo().aws_mock["ami"].find.assert_called_once()
    assert IMAGE_ID in response.data.decode()


def test_master_region_base_image(run_query: RunQueryFunc, mongo: Mock) -> None:
    with patch("aws_mock.main.get_region_name_from_hostname") as mock:
        mock.return_value = MASTER_REGION_NAME
        response = run_query({
            "Action": "DescribeImages",
            "Version": "2016-11-15",
            "ImageId.1": MASTER_REGION_BASE_IMAGE["id"],
        })
        mongo().aws_mock["ami"].find.assert_not_called()

        assert MASTER_REGION_BASE_IMAGE["id"] in response.data.decode()


@pytest.mark.integration
def test_describe_images_boto3(ec2_client: EC2Client) -> None:
    ...
