from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,
)
from .pipeline_stage import WorkshopPipelineStage

class ClearLambdaStoragePipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cls_repo = codecommit.Repository(
            self, 'clear_lambda_storage_repo',
            repository_name= "clear_lambda_storage"
        )
        
        cls_pipeline = pipelines.CodePipeline(
            self,"clear_lambda_storage_pipeline",
            synth=pipelines.ShellStep(
                "synth",
                input=pipelines.CodePipelineSource.code_commit(cls_repo, "master"),
                commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    "pip install -r requirements.txt",  # Instructs Codebuild to install required packages
                    "cdk synth",
                ]
            ),
        )
        
        # deploy = WorkshopPipelineStage(self, "Deploy")
        # deploy_stage = pipeline.add_stage(deploy)
        
        # deploy = WorkshopPipelineStage(self, "Deploy")
        # deploy_stage = pipeline.add_stage(deploy)
        # deploy_stage.add_post(
        #     pipelines.ShellStep(
        #         "TestViewerEndpoint",
        #         env_from_cfn_outputs={
        #             "ENDPOINT_URL": deploy.hc_viewer_url
        #         },
        #         commands=["curl -Ssf $ENDPOINT_URL"],
        #     )
        # )
        # deploy_stage.add_post(
        #     pipelines.ShellStep(
        #         "TestAPIGatewayEndpoint",
        #         env_from_cfn_outputs={
        #             "ENDPOINT_URL": deploy.hc_endpoint
        #         },
        #         commands=[
        #             "curl -Ssf $ENDPOINT_URL",
        #             "curl -Ssf $ENDPOINT_URL/hello",
        #             "curl -Ssf $ENDPOINT_URL/test",
        #         ],
        #     )
        # )