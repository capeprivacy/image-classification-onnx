import os

import torch
from torchvision.io import read_image
from torchvision.models import ResNet50_Weights

from pycape import Cape

token_env = os.environ.get("TOKEN")
function_id_env = os.environ.get("FUNCTION_ID")


def process_image(file):
    img = read_image(file)
    weights = ResNet50_Weights.DEFAULT
    preprocess = weights.transforms()
    batch = preprocess(img).unsqueeze(0)
    batch_numpy = batch.detach().numpy()
    batch_numpy_bytes = batch_numpy.tobytes()
    return batch_numpy_bytes


def process_onnx_output(onnx_output):
    onnx_prediction = torch.from_numpy(
        np.frombuffer(onnx_output, dtype=np.float32).reshape(1, 1000)
    )
    prediction = onnx_prediction.squeeze(0).softmax(0)
    class_id = prediction.argmax().item()
    score = prediction[class_id].item()
    category_name = ResNet50_Weights.DEFAULT.meta["categories"][class_id]
    return category_name, score


if __name__ == "__main__":
    cape = Cape()
    f = cape.function(function_id_env)
    t = cape.token(token_env)

    input_bytes = process_image("./images_sample/dog.jpeg")

    onnx_output = cape.run(f, t, input_bytes)

    category_name, score = process_onnx_output(onnx_output)
    print(f"{category_name}: {100 * score:.1f}%")
