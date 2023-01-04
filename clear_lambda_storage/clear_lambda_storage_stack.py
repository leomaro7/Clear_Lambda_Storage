from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_events_targets as _targets,
    Duration,
    aws_iam as iam,
)

from aws_cdk.aws_events import Rule, Schedule

class ClearLambdaStorageStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cls_lambda = _lambda.Function(
            self, 'clear_lambda_storage_handler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='handler.clear_lambda_storage',
            timeout=Duration.seconds(120)
        )

        cls_rule = Rule(self, "clear_lambda_storage_schedulerule",
            schedule=Schedule.cron(minute="0", hour="16", day="L"),
            targets=[_targets.LambdaFunction(cls_lambda)]
        )
        
        cls_lambda_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW, 
            resources=['*'], 
            actions=[
                    "lambda:ListFunctions",
                    "lambda:ListVersionsByFunction",
                    "lambda:DeleteFunction"
            ]
        )
        cls_lambda.add_to_role_policy(cls_lambda_policy)