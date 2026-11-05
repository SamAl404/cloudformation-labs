import json, os, boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])

def resp(code, body):
    # default=str: DynamoDB returns numbers as Decimal, which json can't serialize
    return {"statusCode": code, "body": json.dumps(body, default=str)}

def handler(event, context):
    route, method = event["resource"], event["httpMethod"]
    if route == "/items" and method == "POST":
        item = json.loads(event["body"])
        table.put_item(Item=item)
        return resp(201, item)
    if route == "/items" and method == "GET":
        # ponytail: scan reads the whole table, 1MB per call; paginate when the table grows
        return resp(200, table.scan()["Items"])
    if route == "/items/{id}" and method == "GET":
        item = table.get_item(Key={"id": event["pathParameters"]["id"]}).get("Item")
        return resp(200 if item else 404, item)
    return resp(404, {"error": "route not found"})