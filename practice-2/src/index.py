import json, os, boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def handler(event, context):
    if event.get("httpMethod") == "POST":
        item = json.loads(event["body"])
        table.put_item(Item=item)
        return {"statusCode": 201, "body": json.dumps(item)}
    item = table.get_item(Key={"id": event["queryStringParameters"]["id"]}).get("Item")
    return {"statusCode": 200 if item else 404, "body": json.dumps(item)}