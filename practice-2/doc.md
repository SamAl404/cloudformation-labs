# Practice 2: Lambda + DynamoDB

A Lambda function that writes items to a DynamoDB table and reads them back. It's split into two stacks: one holds the bucket for the Lambda code, and one holds the app.

## What I built

### `bucket.yaml`: code artifact bucket

- An S3 bucket where `aws cloudformation package` uploads the zipped Lambda code.
- A lifecycle rule deletes objects after 7 days, so old code uploads don't pile up.
- It's a separate stack so the bucket exists before the app is packaged, and so it can be managed on its own.

### `main.yaml`: the app

- **DynamoDB table**: partition key `id` (string), on-demand billing (`PAY_PER_REQUEST`).
- **IAM role**: Lambda can assume it. It allows CRUD + Scan on *only this table* (`!GetAtt DynamoDBTable.Arn`), plus `AWSLambdaBasicExecutionRole` for CloudWatch logs.
- **Lambda function** (Python 3.13): `Code: src/` points at a local folder. `package` uploads that folder to S3 and rewrites the path to an S3 location in `packaged.yaml`. The table name reaches the code through the `TABLE_NAME` environment variable.

### `src/index.py`: handler

- `POST`: saves the JSON body as an item and returns `201`.
- Otherwise: reads the item whose `id` is in the query string, and returns `200`, or `404` if it isn't there.

## Deploy

1. Create the code bucket:

   ```bash
   aws cloudformation deploy --template-file bucket.yaml --stack-name practice-2-bucket --parameter-overrides BucketName=<unique-bucket-name>
   ```

2. Package: zip `src/`, upload it, and write `packaged.yaml`:

   ```bash
   aws cloudformation package --template-file main.yaml --s3-bucket <unique-bucket-name> --output-template-file packaged.yaml
   ```

3. Deploy the app. `CAPABILITY_IAM` is required because the stack creates an IAM role:

   ```bash
   aws cloudformation deploy --template-file packaged.yaml --stack-name practice-2 --parameter-overrides TableName=<table-name> --capabilities CAPABILITY_IAM
   ```

## Test

Invoke the function with a fake API Gateway POST event:

```bash
aws lambda invoke --function-name <function-name-from-outputs> --cli-binary-format raw-in-base64-out --payload '{"httpMethod":"POST","body":"{\"id\":\"1\",\"msg\":\"hello\"}"}' out.json
```

`out.json` should contain:

```json
{"statusCode": 201, "body": "{\"id\": \"1\", \"msg\": \"hello\"}"}
```

## Clean up

```bash
aws cloudformation delete-stack --stack-name practice-2
```

```bash
aws s3 rm s3://<unique-bucket-name> --recursive
```

```bash
aws cloudformation delete-stack --stack-name practice-2-bucket
```

## What I learned

- `aws cloudformation package` turns local code paths into S3 references.
- IAM permissions can be limited to a single resource with `!GetAtt ... .Arn`.
- Stacks that create IAM resources need `--capabilities CAPABILITY_IAM`.
- <!-- add your own notes -->
