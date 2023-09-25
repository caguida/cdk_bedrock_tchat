#!/usr/bin/env python3
import aws_cdk as cdk

from stack.vpc_network_stack import VpcNetworkStack
from stack.web_app_stack import WepAppStack
from stack.chat_user_stack import ChatUserStack
from stack.kendra_stack import KendraS3Stack
import boto3

region_name = boto3.Session().region_name
role_arn = "arn:aws:iam::743456971407:role/BedrockDataFR"
env={"region": region_name}
print("env")
print(env)

app = cdk.App()

kendra_index_id = KendraS3Stack(app,"KendraS3StackID",env=env)
network_stack = VpcNetworkStack(app, "VpcNetworkStack", env=env)
ChatUserStack(app, "ChatUserStack",vpc=network_stack.vpc,role_arn = role_arn,kendra_index_id=kendra_index_id,env=env)
WepAppStack(app, "WepAppStack", vpc=network_stack.vpc, env=env)

app.synth()
