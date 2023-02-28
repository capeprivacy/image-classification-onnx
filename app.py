import numpy as np
import onnxruntime


onnx_sess = onnxruntime.InferenceSession("./onnx_model/resnet50.onnx")


def cape_handler(input_bytes: bytes):
    input = np.frombuffer(input_bytes, dtype=np.float32).reshape(1, 3, 224, 224)
    ort_inputs = {onnx_sess.get_inputs()[0].name: input}
    ort_outs = onnx_sess.run(None, ort_inputs)
    return ort_outs[0].tobytes()
