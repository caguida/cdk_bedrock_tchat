from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_kendra as kendra
from constructs import Construct
from aws_cdk import (
    Stack)

class KendraCdkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create IAM role for Kendra within the scope of the stack
        kendra_role = iam.Role(
            self, "kendra-role",
            assumed_by=iam.ServicePrincipal("kendra.amazonaws.com"),
        )
        print("aaaaaa")
        # Create IAM policy for enabling Kendra to access CloudWatch Logs
        kendra_cwl_access_policy = iam.Policy(
            self, "kendra-cwl-access-policy",
            policy_name="kendra-cwl-access-policy",
            statements=[
                # IAM policy statements for CloudWatch Logs
            ]
        )
        print("bbbbbbb")
        # Create IAM policy for enabling Kendra to access and index S3
        kendra_s3_access_policy = iam.Policy(
            self, "iam-kendra-access-s3-access-policy",
            policy_name="iam-kendra-access-s3-access-policy",
            statements=[
                # IAM policy statements for S3 access
            ]
        )
        print("cccccc")
        # Attach policies to the Kendra role
        kendra_role.add_managed_policy(kendra_cwl_access_policy)
        kendra_role.add_managed_policy(kendra_s3_access_policy)


        # Create S3 bucket
        s3_docs_bucket = s3.Bucket(
            self, "s3-docs",
            bucket_name=self.node.try_get_context('s3_bucket_name')
        )
        print("mmmmmmmmmmmmmmm")
        # Upload private docs to S3
        s3.Object(
            self, "docs",
            bucket=s3_docs_bucket,
            key="NET-Microservices-Architecture-for-Containerized-NET-Applications",
            source="docs/NET-Microservices-Architecture-for-Containerized-NET-Applications.pdf"
        )

        # Create Kendra Index
        kendra_index = kendra.Index(
            self, "kendra-docs-index",
            index_name=self.node.try_get_context('kendra_index_name'),
            edition=self.node.try_get_context('kendra_index_edition'),
            role=kendra_role
        )

        # Create Kendra Index S3 connector
        kendra.S3DataSource(
            self, "kendra-docs-s3-connector",
            index=kendra_index,
            name="s3-docs-connector",
            type="S3",
            role=kendra_role,
            schedule="cron(0/5 * * * ? *)",
            bucket_name=s3_docs_bucket.bucket_name
        )










# from aws_cdk import (
#     Stack)
# from aws_cdk import aws_kendra as kendra
# from aws_cdk import aws_s3 as s3 
# from aws_cdk import aws_iam as iam
# from constructs import Construct

# class KendraStackBis(Stack):

#     def __init__(self, scope: Construct, id: str, **kwargs) -> None:
#         super().__init__(scope, id, **kwargs)
        
#         # Créez un compartiment S3
#         kendra_s3_bucket = s3.Bucket(
#             self, "KendraS3BucketTest", 
#             bucket_name = "data-kendra-cdk-test" # pas obligatoire, Default: - Assigned by CloudFormation (recommended).
#         )

#         # Créez un rôle IAM pour Kendra
#         kendra_role = iam.Role(
#             self, "KendraRole",
#             assumed_by=iam.ServicePrincipal("kendra.amazonaws.com")
#         )

#         # Attachez une stratégie Kendra au rôle
#         kendra_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKendraFullAccess"))
#         kendra_role.add_managed_policy(
#             iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchLogsFullAccess')
#         )

#         # Créez une stratégie personnalisée pour les autorisations Kendra spécifiques
#         kendra_custom_policy = iam.PolicyStatement(
#             actions=[
#                 "cloudwatch:PutMetricData",
#                 "logs:DescribeLogGroups",
#                 "logs:CreateLogGroup",
#                 "logs:DescribeLogStreams",
#                 "logs:CreateLogStream",
#                 "logs:PutLogEvents",
#                 "s3:GetObject",        # Autorisation pour lire les objets S3
#                 "s3:ListBucket"        # Autorisation pour lister les objets dans le compartiment S3
#             ],
#             resources=["*"]  # Vous pouvez spécifier des ressources plus restrictives si nécessaire
#         )

#         # Ajoutez la stratégie personnalisée au rôle Kendra
#         kendra_role.add_to_policy(kendra_custom_policy)

#         field_mappings = [
#         {
#             "dataSourceFieldName": "s3_document_id",  # Champ dans votre source de données S3
#             "dateFieldFormat": "STRING",  # Format du champ de date
#             "indexFieldName": "s3_document_id",  # Champ d'index Kendra
#             "dataSourceFieldType": "S3_PATH",  # Type de champ dans votre source de données S3
#         }
#         ]
#         # Créez une ressource Kendra Index
#         kendra_index = kendra.CfnIndex(
#             self, "KendraIndexBis",
#             edition="DEVELOPER_EDITION",  # Vous pouvez ajuster cela en fonction de vos besoins
#             name="my-kendra-index-bis",  # Remplacez par le nom souhaité de l'index Kendra
#             role_arn=kendra_role.role_arn
#         )

#         # Créez une source de données Kendra pour S3
#         kendra_data_source = kendra.CfnDataSource(
#             self, "KendraDataSource",
#             index_id=kendra_index.attr_id,
#             name="S3-DataSource",
#             type="S3",
#             data_source_configuration={
#                 "s3Configuration": {
#                     "bucketName": kendra_s3_bucket.bucket_name,
#                     "language_code": 'fr',
#                     "fieldMappings": field_mappings  # Ajoutez le champ de mappage ici
#                 }
#             },
#             role_arn=kendra_role.role_arn
#         )


#         self.kendra_index = kendra_index.attr_id
