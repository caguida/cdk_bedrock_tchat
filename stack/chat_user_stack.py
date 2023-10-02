from aws_cdk import (
    Duration,
    Stack,
    aws_ssm as ssm,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda
)
from constructs import Construct
import aws_cdk.aws_iam as iam
from aws_cdk.aws_lambda import Function, Code, Runtime
import   aws_cdk.aws_apigateway as apigw
import os

class ChatUserStack(Stack):

    def __init__(self, scope: Construct, id: str,vpc: ec2.IVpc,role_arn,kendra_index_id,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        # Crée la fonction Lambda
        lambda_handler_path_entry = os.path.join(os.getcwd(), "lambda")
        lambda_function_entry = Function(self, "LambdaFunctionEntry",
            runtime=Runtime.PYTHON_3_8,
            handler="lambda_entry.handler",
            timeout=Duration.seconds(180),
            code=Code.from_asset(lambda_handler_path_entry),
        )

        # add policy for invoking
        lambda_function_entry.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "lambda:InvokeFunction",
                ],
                resources=["*"]
            )
        )

        # Crée la fonction Lambda
        
        lambda_handler_path = os.path.join(os.getcwd(), "lambda_chat_dock")
        lambda_function = _lambda.DockerImageFunction(
            self, f"lambda-chat-dock",
            description="lambda for chat api",
            function_name=f"lambda-chat-dock",
            code=_lambda.DockerImageCode.from_image_asset(lambda_handler_path),
            timeout=Duration.seconds(180),
            environment={
                "KENDRA_INDEX_ID": str(kendra_index_id.kendra_index)
            },
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            vpc=vpc
        )


        # add policy for invoking
        lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "sagemaker:InvokeEndpoint",
                ],
                resources=["*"]
            )
        )


        # Ajoutez une autorisation DynamoDB à votre rôle
        dynamodb_policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "dynamodb:Scan",
                "dynamodb:Query",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem"
            ],
            resources=["*"]  # Vous pouvez spécifier les ressources DynamoDB spécifiques si nécessaire
        )

        # Ajoutez une autorisation Kendra à votre rôle
        kendra_policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "kendra:Query",
                "kendra:BatchGetDocumentStatus",
                "kendra:Retrieve"
            ],
            resources=["*"]  # Vous pouvez spécifier les ressources Kendra spécifiques si nécessaire
        )
        assume_role_policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["sts:AssumeRole"],
            resources=[role_arn]
        )


        # Créez une stratégie IAM pour CloudWatch Logs
        cloudwatch_logs_policy = iam.PolicyStatement(
            actions=[
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            resources=["arn:aws:logs:*:*:*"]
        )



        # Attachez les autorisations au rôle
        lambda_function.add_to_role_policy(dynamodb_policy_statement)
        lambda_function.add_to_role_policy(kendra_policy_statement)
        lambda_function.add_to_role_policy(assume_role_policy_statement)
        lambda_function.add_to_role_policy(cloudwatch_logs_policy)
        
        # Defines an Amazon API Gateway endpoint 
        apigw_endpoint_chat = apigw.LambdaRestApi(
            self, "apigw_endpoint_chat",
            handler=lambda_function_entry
        )  

    #    DynamoDB Table
        memory_table = dynamodb.Table(
            self, "MemoryTableChat",
            table_name="MemoryTableChat",
            partition_key={"name": "SessionId", "type": dynamodb.AttributeType.STRING},
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        ssm.StringParameter(self, "txt_apigw_endpoint_chat", parameter_name="txt_apigw_endpoint_chat", string_value=apigw_endpoint_chat.url)
