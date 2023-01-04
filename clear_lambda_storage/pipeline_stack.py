from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,
)
from .pipeline_stage import ClearLambdaStoragePipelineStage

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
                    # "python lambda/clear_lambda_storage.py",
                ]
            ),
        )
        
        cls_deploy = ClearLambdaStoragePipelineStage(self, "deploy")
        cls_deploy_stage = cls_pipeline.add_stage(cls_deploy)
        # cls_deploy_stage.add_post(
        #     pipelines.ShellStep(
        #         "test",
        #         commands=["curl -Ssf $ENDPOINT_URL"],
        #     )
        # )