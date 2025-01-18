# rehab_tagging

`python3 -m venv tagenv`
`source tagenv/bin/activate`
`pip3 install -r requirements.txt`

## For AWS SAM
- [Install AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Test locally
    - [Test locally in vscode](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/sam-get-started.html#serverless-apps-create)
    - [Testing with SAM local invoke](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-local-invoke.html)

### To get started with AWS SAM and test locally
Create a new env.json file with the PINECONE_API_KEY
- sam init
- sam build
- sam build && sam local invoke RETagLambdaFunction --event event.json --env-vars env.json

### To deploy to AWS
- sam init
- sam build
- sam deploy --guided

Note:
- To delete the stack
   `aws cloudformation delete-stack --stack-name retagstack`