import json
import os
import boto3
import botocore
import uuid
from langchain.chains import ConversationalRetrievalChain
from langchain import SagemakerEndpoint
from langchain.prompts.prompt import PromptTemplate
from langchain.embeddings import SagemakerEndpointEmbeddings
from langchain.embeddings.sagemaker_endpoint import EmbeddingsContentHandler
from langchain.llms.bedrock import Bedrock
from langchain.embeddings import BedrockEmbeddings

from langchain.llms.sagemaker_endpoint import ContentHandlerBase, LLMContentHandler
from langchain.memory import ConversationBufferWindowMemory
from langchain import PromptTemplate, LLMChain
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.retrievers import AmazonKendraRetriever



REGION = os.environ.get('REGION')
KENDRA_INDEX_ID = os.environ.get('KENDRA_INDEX_ID')


#############Bedrock##############

session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()

aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
aws_session_token= credentials.token

base_session = boto3.Session(
    aws_access_key_id= aws_access_key_id, #your access key
    aws_secret_access_key= aws_secret_access_key,#your secret acces key 
    aws_session_token= aws_session_token
)
base_sts = base_session.client('sts')
bedrock_credentials = base_sts.assume_role(RoleArn = 'arn:aws:iam::743456971407:role/BedrockDataFR', RoleSessionName = str(uuid.uuid4()))['Credentials']
bedrock_session = boto3.Session(
    aws_access_key_id = bedrock_credentials['AccessKeyId'],
    aws_secret_access_key = bedrock_credentials['SecretAccessKey'],
    aws_session_token = bedrock_credentials['SessionToken']
)

bedrock_client = bedrock_session.client('bedrock', region_name = REGION)
##################################
kendra_client = boto3.client("kendra", REGION, 
                                 aws_access_key_id= aws_access_key_id, #your access key
                                 aws_secret_access_key= aws_secret_access_key,#your secret acces key 
                                 aws_session_token= aws_session_token)

llm = Bedrock(client = bedrock_client, 
            model_kwargs={"max_tokens_to_sample": 1000},
            model_id = "anthropic.claude-v2")



_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language. 

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""


CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)


def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    print(body)
    query = body['query']
    uuid = body['uuid']
    print(query)
    print(uuid)

    message_history = DynamoDBChatMessageHistory(table_name="MemoryTable", session_id=uuid)
    memory = ConversationBufferWindowMemory(memory_key="chat_history", chat_memory=message_history, return_messages=True, k=3)

    retriever = AmazonKendraRetriever(index_id=KENDRA_INDEX_ID, top_k=3, client=kendra_client, attribute_filter={
    'EqualsTo': {
        'Key': '_language_code',
        'Value': {'StringValue': 'fr'}
    }
    })
    qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory, condense_question_prompt=CONDENSE_QUESTION_PROMPT, verbose=True)


    response = qa.run(query)   

    return {
            'statusCode': 200,
            'body': json.dumps(response)
        }