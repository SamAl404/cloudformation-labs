# Practice 1: S3 Bucket

My first CloudFormation template. It creates one S3 bucket whose name is passed in as a parameter.

## What I built

- **Parameter** `BucketName`: the bucket name is supplied at deploy time instead of hardcoded.
- **Resource** `MyBucket` (`AWS::S3::Bucket`): uses `!Ref BucketName` to read the parameter.
- **Output** `BucketArn`: uses `!GetAtt MyBucket.Arn` to return the bucket's ARN after the stack is created.

## Deploy

S3 bucket names are global, so pick one nobody else has used.

```bash
aws cloudformation deploy --template-file template.yaml --stack-name practice-1 --parameter-overrides BucketName=<unique-bucket-name>
```

See the output:

```bash
aws cloudformation describe-stacks --stack-name practice-1 --query "Stacks[0].Outputs"
```

## Clean up

```bash
aws cloudformation delete-stack --stack-name practice-1
```

## What I learned

- A template's basic sections: `Parameters`, `Resources`, and `Outputs`.
- `!Ref` on a parameter returns its value. `!GetAtt` reads an attribute of a resource, like its ARN.
- <!-- add your own notes -->
