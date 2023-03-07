import json
import os

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


if __name__ == "__main__":
    cape = Cape()
    f = cape.function(function_id_env)
    t = cape.token(token_env)

    input_bytes = process_image("./images_sample/dog.jpeg")

    input_bytes = cape.encrypt(input_bytes)

    top5_classes = cape.run(f, t, input_bytes)

    top5_classes = json.loads(top5_classes)
    for category_name, score in top5_classes.items():
        print(f"{category_name}: {100 * score:.1f}%")
