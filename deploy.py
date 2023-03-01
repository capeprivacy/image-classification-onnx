import pathlib
import pycape
from pycape.experimental import cli

cape = pycape.Cape()

function_ref = cli.deploy("onnx_resnet_deploy")

print(function_ref.id)
