from aws_mock.lib import get_aws_mock_db, aws_response
from aws_mock.predefined import MASTER_REGION_NAME, MASTER_REGION_BASE_IMAGE


@aws_response
def describe_images(region_name: str, image_id: str | None = None) -> dict:
    if region_name == MASTER_REGION_NAME and image_id == MASTER_REGION_BASE_IMAGE["id"]:
        return {"items": [MASTER_REGION_BASE_IMAGE]}
    filters = {"region_name": region_name}
    if image_id is not None:
        filters["id"] = image_id
    return {"items": list(get_aws_mock_db()["ami"].find(filters))}
