# CloudFormation Practice

This is my personal repo for learning AWS CloudFormation. Each `practice-N/` folder is a self-contained lab. I'm documenting each one so anyone can follow along, understand what I built, and reuse the templates.

Feel free to use, copy, or adapt any lab.

## Labs

| Lab | What it builds | Concepts |
|-----|----------------|----------|
| [practice-1](practice-1/doc.md) | A single S3 bucket | Parameters, `!Ref`, `!GetAtt`, Outputs |
| [practice-2](practice-2/doc.md) | Lambda function that reads/writes DynamoDB, with a separate stack for the Lambda code bucket | Multiple stacks, IAM roles, `aws cloudformation package`, S3 lifecycle rules |

Each lab has its own `doc.md` explaining what I did, how to deploy it, and what I learned.

## Prerequisites

- An AWS account (labs create real resources, which may cost money)
- [AWS CLI](https://aws.amazon.com/cli/) configured with credentials

## Deploying a lab

```bash
aws cloudformation deploy --template-file practice-1/template.yaml --stack-name practice-1 --parameter-overrides BucketName=<unique-bucket-name>
```

## Cleaning up

Delete the stack when you're done so you don't get billed:

```bash
aws cloudformation delete-stack --stack-name practice-1
```

S3 buckets must be empty before the stack can delete them.
