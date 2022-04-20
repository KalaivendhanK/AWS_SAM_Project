Steps :

--------------------------------------------------------------------------------------------------------------
2. Work with SAM
--------------------------------------------------------------------------------------------------------------
- Build and test Serverless applications locally and deploy to AWS using Cloudformation
    Deploy command:
    - sam init
    - sam build
    - sam deploy --stack-name my-test-stack --s3-bucket "yext-sample-json" --profile dev --region us-east-1 --capabilities CAPABILITY_NAMED_IAM