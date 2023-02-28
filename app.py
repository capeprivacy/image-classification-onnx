import numpy as np
import onnxruntime


onnx_sess = onnxruntime.InferenceSession("./onnx_model/resnet50.onnx")


def cape_handler(input_bytes: bytes):
    input = np.frombuffer(input_bytes, dtype=np.float32).reshape(1, 3, 224, 224)
    ort_inputs = {onnx_sess.get_inputs()[0].name: input}
    ort_outs = onnx_sess.run(None, ort_inputs)
    return ort_outs[0].tobytes()


from torchvision.io import read_image
from torchvision.models import ResNet50_Weights
import torch


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
    input_bytes = process_image("./images_sample/dog.jpeg")
    onnx_output = cape_handler(input_bytes)
    category_name, score = process_onnx_output(onnx_output)
    print(f"{category_name}: {100 * score:.1f}%")
