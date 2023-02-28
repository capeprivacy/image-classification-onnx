# image-classification-onnx

### Generate ONNX model
```
$ python convert_resnet_to_onnx.py
```

### Deploy with Cape

First, you need to create a deployment folder containing your dependencies and a cape_handler in an `app.py` file.
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
```
$ cape deploy onnx_resnet_deploy
Deploying function to Cape ...
Success! Deployed function to Cape.
Function ID ➜  <FUNCTION_ID>
Function Checksum ➜  <FUNCTION_CHECKSUM>
$ export FUNCTION_ID=<copied from above>
```

### Run Secure Prediction

Generate a personal access token for your account by running:
```
$ cape token create --name resnet
Success! Your token: eyJhtGckO12...(token omitted)
$ export TOKEN=<copied from above>
```

Invoke the image classification model with:
```
$ python run_prediction.py
golden retriever: 39.7%
Labrador retriever: 7.1%
tennis ball: 1.3%
clumber: 0.9%
Brittany spaniel: 0.7%
```