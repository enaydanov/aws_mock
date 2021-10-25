import logging
from uuid import uuid4
from flask import Flask, request, render_template
from werkzeug.datastructures import ImmutableMultiDict
from aws_mock.lib import get_collection_name, get_aws_mock_db


app = Flask(__name__)
LOGGER = logging.getLogger(__name__)


def describe_instances(request_data: ImmutableMultiDict[str, str]) -> str:
    """
        Action=DescribeInstances&Version=2016-11-15&InstanceId.1=i-08cafe5e67f1a0bd2
        Doc: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstances.html
    """
    instance_ids = [request_data[key] for key in request_data if key.startswith("InstanceId")]
    if not instance_ids:  # no instances provided return empty list
        return render_template("responses/describe_instances.xml", instances=[], request_id=str(uuid4()))
    LOGGER.debug(f"Looking for instances with ids: %s ...", instance_ids)
    db = get_aws_mock_db()
    collection = db[get_collection_name(instance_ids[0])]
    found_instances = list(collection.find({"id": {"$in":  instance_ids}}))
    LOGGER.debug("Found instances: %s", found_instances)
    items = []
    for instance_id in [doc["id"] for doc in found_instances]:
        items.append(render_template("responses/describe_instances_item.xml", instance_id=instance_id))
    return render_template("responses/describe_instances.xml", instances=items,  request_id=str(uuid4()))


@app.route("/", methods=['POST'])
def index():
    action = request.form["Action"]
    match request.form["Action"]:
        case "DescribeInstances":
            return describe_instances(request_data=request.form)
        case _:
            return f"Unknown action: {action}", 400
