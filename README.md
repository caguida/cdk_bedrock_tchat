
# Deploy Chatbot Bedrock models using the AWS CDK

The seeds of a machine learning (ML)

## Prerequisites

You must have the following prerequisites:

- An [AWS account](https://signin.aws.amazon.com/signin)
- The [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- Python 3.6 or later
- node.js 14.x or later
- The [AWS CDK v2](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
- Docker v20.10 or later

 You can deploy the infrastructure in this tutorial from your local computer or you can use [AWS Cloud9](https://aws.amazon.com/cloud9/) as your deployment workstation. AWS Cloud9 comes pre-loaded with AWS CLI, AWS CDK and Docker. If you opt for AWS Cloud9, [create the environment](https://docs.aws.amazon.com/cloud9/latest/user-guide/tutorial-create-environment.html) from the [AWS console](https://console.aws.amazon.com/cloud9).

The estimated cost to complete this post is $50, assuming you leave the resources running for 8 hours. Make sure you delete the resources you create in this post to avoid ongoing charges.


## Install the AWS CLI and AWS CDK on your local machine

If you don’t already have the AWS CLI on your local machine, refer to [Installing or updating the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Install the AWS CDK Toolkit globally using the following node package manager command:

```
npm install -g aws-cdk-lib@latest
```

Run the following command to verify the correct installation and print the version number of the AWS CDK:

```
cdk --version
```

Make sure you have Docker installed on your local machine. Issue the following command to verify the version:

```
docker --version
```

## Clone and set up the AWS CDK application

On your local machine, clone the AWS CDK application with the following command:

```
git clone https://github.com/caguida/cdk_bedrock_tchat.git
```

Navigate to the project folder:

```
cd chatbotPack
```

Before we deploy the application, let's review the directory structure:



The `stack` folder contains the code for each stack in the AWS CDK application. 

#### Setup a virtual environment

This project is set up like a standard Python project. Create a Python virtual environment using the following code:

```
python3 -m venv .venv
```

Use the following command to activate the virtual environment:

```
source .venv/bin/activate
```

If you’re on a Windows platform, activate the virtual environment as follows:

```
.venv\Scripts\activate.bat
```

After the virtual environment is activated, upgrade pip to the latest version:

```
python3 -m pip install --upgrade pip
```

Install the required dependencies:

```
pip install -r requirements.txt
```

Before you deploy any AWS CDK application, you need to bootstrap a space in your account and the Region you’re deploying into. To bootstrap in your default Region, issue the following command:

```
cdk bootstrap
```

If you want to deploy into a specific account and Region, issue the following command:

```
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

For more information about this setup, visit  [Getting started with the AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html).



#### AWS CDK application stack structure

The AWS CDK application contains multiple stacks as shown in the following diagram.

You can list stacks in your CDK application with the following command:

```bash
$ cdk list
```



Other useful AWS CDK commands:

 * `cdk ls`     - Lists all stacks in the app
 * `cdk synth`    - Emits the synthesized AWS CloudFormation template
 * `cdk deploy`    - Deploys this stack to your default AWS account and Region
 * `cdk diff`     - Compares the deployed stack with current state
 * `cdk docs`     - Opens the AWS CDK documentation

The next section shows you how to deploy the AWS CDK application.



## Deploy the AWS CDK application

The AWS CDK application will be deployed to the default Region based on your workstation configuration. If you want to force the deployment in a specific Region, set your `AWS_DEFAULT_REGION` environment variable accordingly.

If necessary, change the arn role to access bedrock `role_arn` in `app.py`.

At this point, you can deploy the AWS CDK application. First, launch the kendra stack:

```
cdk deploy KendraS3StackID
```
If you are prompted, enter `y` to proceed with the deployment. You should see a list of AWS resources that are being provisioned in the stack. 

In stack `KendraS3StackID`, we create a kendra stack whose index name is `KendraIndex` . We also create an S3 bucket named `KendraS3Bucket`, and then a datasource named `KendraDataSource`. Please load the S3 bucket with your documents to make them accessible to Kendra.

Now, launch the VPC Network stack:

```
cdk deploy VpcNetworkStack
```

After, launch your local docker application first and run the following command to build and deploy the lambda function image, and the link of API Gateway

```
cdk deploy ChatUserStack
```
You can collect the address of your API Gateway and test it with insomnia.

To finish, launch the streamlit web application stack:

```
cdk deploy WepAppStack
```

After execution, the link to your web application would be available.

You can delete the entire stack

```
cdk destroy --all 
```
or

```
cdk destroy WepAppStack
cdk destroy ChatUserStack
cdk destroy VpcNetworkStack
cdk destroy KendraS3StackID
```

## Pay attention:

Please note that bedrock may not have access to the file you've uploaded to the S3 bucket. This is due to the datasource. In this case, via the aws console, access Kendra, choose the kendra index `KendraIndex` and recreate a new datasource. You can use the same bucket `KendraS3Bucket`

## Note:

I've added a folder called **draft** which contains some draft functions for future.