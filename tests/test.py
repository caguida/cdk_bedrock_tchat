import aws_cdk as core
import aws_cdk.assertions as assertions

from stack.web_app_stack import GenerativeAiDemoWebStack

# example tests. To run these tests, uncomment this file along with the example
# resource in generative_ai_sagemaker_cdk_demo/generative_ai_sagemaker_cdk_demo_stack.py
def test_sqs_queue_created():
    app = core.App()