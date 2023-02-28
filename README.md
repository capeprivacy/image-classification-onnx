# image-classification-onnx

### Deploy with Cape
```
# Create a deployment folder
export TARGET="onnx_resnet_deploy"
mkdir $TARGET
# Add function script
cp app.py $TARGET
# Add ONNX resnet model 
cp -r onnx_model $TARGET
# Add onnxrumtime dependency.
docker run -v `pwd`:/build -w /build --rm -it python:3.9-slim-bullseye pip install onnxruntime==1.13.1 --target /build/$TARGET
```