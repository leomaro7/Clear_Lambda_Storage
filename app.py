#!/usr/bin/env python3

import aws_cdk as cdk
from clear_lambda_storage.pipeline_stack import ClearLambdaStoragePipelineStack

app = cdk.App()
ClearLambdaStoragePipelineStack(app, "clearlambdastoragepipelinestack")

app.synth()