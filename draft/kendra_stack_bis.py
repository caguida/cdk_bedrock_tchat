from aws_cdk import (
    Stack)
from aws_cdk import aws_kendra as kendra
from aws_cdk import aws_s3 as s3 
from aws_cdk import aws_iam as iam
from constructs import Construct

class KendraSearchToolStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
      # Création du compartiment S3 pour les données
        # s3_bucket_for_data_source = s3.Bucket(
        #     self, 's3BucketForDataSource' #,removal_policy=Construct.RemovalPolicy.RETAIN
        # )

        # Création du rôle IAM pour l'index Kendra
        kendra_index_role = iam.Role(
            self, 'kendraIndexRole',
            assumed_by=iam.ServicePrincipal('kendra.amazonaws.com'),
        )

        # Attachement de la politique par défaut au rôle Kendra Index
        kendra_index_role.add_to_policy(
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                effect=iam.Effect.ALLOW,
                resources=["*"]
            )
        )

        kendra_index_role.add_to_policy(
            iam.PolicyStatement(
                actions=["logs:DescribeLogGroups", "logs:CreateLogGroup", "logs:DescribeLogStreams", "logs:CreateLogStream", "logs:PutLogEvents"],
                effect=iam.Effect.ALLOW,
                resources=["*"]
            )
        )

        # Création du rôle IAM pour la source de données Kendra
        kendra_data_source_role = iam.Role(
            self, 'kendraDataSourceRole',
            assumed_by=iam.ServicePrincipal('kendra.amazonaws.com'),
        )

        # Attachement de la politique par défaut au rôle Kendra Data Source
        kendra_data_source_role.add_to_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                effect=iam.Effect.ALLOW,
                resources=[s3_bucket_for_data_source.bucket_arn + '/*']
            )
        )

        kendra_data_source_role.add_to_policy(
            iam.PolicyStatement(
                actions=["s3:ListBucket"],
                effect=iam.Effect.ALLOW,
                resources=[s3_bucket_for_data_source.bucket_arn]
            )
        )

        kendra_data_source_role.add_to_policy(
            iam.PolicyStatement(
                actions=["kendra:BatchPutDocument", "kendra:BatchDeleteDocument"],
                effect=iam.Effect.ALLOW,
                resources=["*"]
            )
        )

        # Création de l'index Kendra
        kendra_index = kendra.CfnIndex(
            self, 'kendraIndex',
            edition='ENTERPRISE_EDITION',
            name=s3_bucket_for_data_source.bucket_name,
            role_arn=kendra_index_role.role_arn,
            description='Kendra index for search tool'
        )

        # Création de la source de données Kendra
        kendra_data_source = kendra.CfnDataSource(
            self, 'kendraDataSource',
            index_id=kendra_index.ref,
            name=s3_bucket_for_data_source.bucket_name,
            type='S3',
            data_source_configuration={
                's3Configuration': {
                    'bucketName': s3_bucket_for_data_source.bucket_name
                }
            },
            description='S3 data source for search tool',
            role_arn=kendra_data_source_role.role_arn
            # ,schedule='cron(0/2 * * * ? *)'
        )

      