# Confidential Image Classification
The purpose of this repository is to demonstrate how you can deploy a confidential image classification model with [Cape](https://capeprivacy.com/).

### Generate ONNX model
To deploy a [pre-trained Resnet50](https://pytorch.org/vision/main/models/generated/torchvision.models.resnet50.html#resnet50) image classification model, we will use the [ONNX runtime](https://onnxruntime.ai/) to reduce the size of the dependencies and improve performance. The folder contains the Pytorch model converted to ONNX (`./onnx_model/resnet50.onnx`). You can execute the following script if you want to re-generate the ONNX file.
```console
$ python convert_resnet_to_onnx.py
```

### Sign up with Cape:
Before deploying and invoking your model, you must sign up from [Cape's website](https://capeprivacy.com/). You can also sign up using [Cape's CLI](https://docs.capeprivacy.com/getting-started/#install-the-cape-cli):
```console
cape signup
```

### Deploy with Cape

First, create a deployment folder containing your dependencies and a cape_handler in an `app.py` file. To learn in general how to write a Cape function and deploy it with Cape, you can consult the [documentation](https://docs.capeprivacy.com/tutorials/writing).
```
# Create a deployment folder
$ export TARGET="onnx_resnet_deploy"
$ mkdir $TARGET
# Add function script
$ cp app.py $TARGET
# Add ONNX resnet model
$ cp -r onnx_model $TARGET
# Add imagenet classes file
$ cp imagenet_classes.txt $TARGET
# Add onnxrumtime dependency.
$ docker run -v `pwd`:/build -w /build --rm -it python:3.9-slim-bullseye pip install onnxruntime==1.13.1 --target /build/$TARGET
```

Then you can deploy your function using the Cape cli:
```console
$ cape deploy onnx_resnet_deploy
Deploying function to Cape ...
Success! Deployed function to Cape.
Function ID ➜  <FUNCTION_ID>
Function Checksum ➜  <FUNCTION_CHECKSUM>
$ export FUNCTION_ID=<copied from above>
```

### Run Secure Prediction

Then to authenticate with Cape from the SDKs, you need to generate a [personal access token](https://docs.capeprivacy.com/reference/user-tokens/#creating-a-personal-access-token). You can create it from the UI or with the Cape CLI:
```console
$ cape token create --name resnet
Success! Your token: eyJhtGckO12...(token omitted)
$ export TOKEN=<copied from above>
```

You are ready to invoke your confidential image classification service by running the python script `python run_prediction.py`. To execute this script, you must install the dependencies listed in the `requirements.txt` file (`pip install -r requirements.txt`).
```console
$ python run_prediction.py
golden retriever: 39.7%
Labrador retriever: 7.1%
tennis ball: 1.3%
clumber: 0.9%
Brittany spaniel: 0.7%
```

### Run Secure Prediction with Encryption

You can encrypt data before sending it to Cape to be processed in your function. You can encrypt
to yourself or you can encrypt for another person. If you encrypt for yourself only you can decrypt the
data and if you encrypt for another person only they can decrypt it.

There are three examples for testing this out:

Returns the encrypted string for you.

```
$ python encrypt.py
Encrypted: cape:KTTGfoNTQu....
```

Returns the encrypted string for the capedocs user. (Note: the capedocs user is a user we use to deploy example functions).

```
$ python encrypt_for_user.py capedocs
Encrypted: cape:MQrGNmp6V1im7cu.....
```

`run_encrypt.py` is just like `run_prediction.py` except it encrypts the data before sending it. The
output is the same as the input is decrypted securely inside the enclave before processing.

```
$ python run_encrypt.py
golden retriever: 39.7%
Labrador retriever: 7.1%
tennis ball: 1.3%
clumber: 0.9%
Brittany spaniel: 0.7%
```

See [here](https://docs.capeprivacy.com/concepts/encrypt) for more details.
