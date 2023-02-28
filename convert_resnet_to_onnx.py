import pathlib

import torch
import torchvision


def export_model_to_onnx(model, dummy_tensor_shape, onnx_file_path):
    model.eval()
    dummy_tensor = torch.ones(
        dummy_tensor_shape, dtype=torch.float32, requires_grad=True
    )

    torch.onnx.export(
        model,
        dummy_tensor,
        onnx_file_path,
        export_params=True,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
    )


if __name__ == "__main__":
    onnx_path = pathlib.Path("./onnx_model")
    if not onnx_path.exists():
        onnx_path.mkdir()

    weights = torchvision.models.ResNet50_Weights.DEFAULT
    model = torchvision.models.resnet50(weights)
    export_model_to_onnx(
        model,
        dummy_tensor_shape=(1, 3, 224, 224),
        onnx_file_path=onnx_path / "resnet50.onnx",
    )
