from aws_cdk import (
    Stack)
from aws_cdk import aws_kendra as kendra
from aws_cdk import aws_s3 as s3 
from aws_cdk import aws_iam as iam
from constructs import Construct

class KendraS3Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Créez un bucket S3
        kendra_s3_bucket = s3.Bucket(
            self, "KendraS3Bucket", 
            bucket_name = "data-kendra-cdk" # pas obligatoire, Default: - Assigned by CloudFormation (recommended).
        )

        # Créez un rôle IAM pour Kendra
        kendra_role = iam.Role(
            self, "KendraRole",
            assumed_by=iam.ServicePrincipal("kendra.amazonaws.com")
        )

        # Attachez une stratégie Kendra au rôle
        kendra_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKendraFullAccess"))
        kendra_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchLogsFullAccess')
        )

        # Créez une stratégie personnalisée pour les autorisations Kendra spécifiques
        kendra_custom_policy = iam.PolicyStatement(
            actions=[
                "cloudwatch:PutMetricData",
                "logs:DescribeLogGroups",
                "logs:CreateLogGroup",
                "logs:DescribeLogStreams",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "s3:GetObject",        # Autorisation pour lire les objets S3
                "s3:ListBucket"        # Autorisation pour lister les objets dans le compartiment S3
            ],
            resources=["*"]  # ressources plus restrictives si nécessaire
        )

        # Ajoutez la stratégie personnalisée au rôle Kendra
        kendra_role.add_to_policy(kendra_custom_policy)

        # Créez une ressource Kendra Index

        kendra_index = kendra.CfnIndex(
            self, "KendraIndex",
            edition="DEVELOPER_EDITION",  # Vous pouvez ajuster cela en fonction de vos besoins
            name="my-kendra-index",  # Remplacez par le nom souhaité de l'index Kendra
            role_arn=kendra_role.role_arn,
            description='Kendra index for search tool in bedrock'
        )

        s3_configuration = kendra.CfnDataSource.S3DataSourceConfigurationProperty(
            bucket_name=kendra_s3_bucket.bucket_name
        )

        kendra_data_source = kendra.CfnDataSource(
            self, "KendraDataSource",
            index_id=kendra_index.attr_id,
            name="S3-DataSource",
            type="S3",
            data_source_configuration={
                "s3Configuration": s3_configuration
            },
            role_arn=kendra_role.role_arn
        )

        self.kendra_index = kendra_index.attr_id
