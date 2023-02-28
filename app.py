import json
import numpy as np
import onnxruntime


onnx_sess = onnxruntime.InferenceSession("./onnx_model/resnet50.onnx")

with open("imagenet_classes.txt", "r") as f:
    imagenet_classes = [s.strip() for s in f.readlines()]


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def get_top5_classes(onnx_output, imagenet_classes):
    onnx_output = softmax(onnx_output.flatten())
    top5_cat_id = np.argsort(-onnx_output)[:5]
    top5_class_score = {
        imagenet_classes[class_id]: onnx_output[class_id].tolist()
        for class_id in top5_cat_id
    }
    return top5_class_score


def cape_handler(input_bytes: bytes):
    input = np.frombuffer(input_bytes, dtype=np.float32).reshape(1, 3, 224, 224)
    ort_inputs = {onnx_sess.get_inputs()[0].name: input}
    ort_outs = onnx_sess.run(None, ort_inputs)
    top5_classes = get_top5_classes(ort_outs[0], imagenet_classes)
    return json.dumps(top5_classes)
