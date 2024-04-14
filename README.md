# deep_fashion_segmentation_yolov9

This repository uses the following GitHub repositories:

- [yolov9 by WongKinYiu](https://github.com/WongKinYiu/yolov9.git)
- [JSON2YOLO by ultralytics](https://github.com/ultralytics/JSON2YOLO.git)
- [yolov9-onnx-segmentation by spacewalk01](https://github.com/spacewalk01/yolov9-onnx-segmentation.git)

## Installation
### Clone the repository

```bash
git clone https://github.com/Hariharan-MageshAnand/deep_fashion_segmentation_yolov9.git

cd deep_fashion_segmentation_yolov9

docker build -t deep_fashion_segmentation_yolov9 .

```

### Run the docker container

```bash
docker run -it --rm --gpus all deep_fashion_segmentation_yolov9:latest

```
## Run Bash Script

```bash
bash pipeline.sh 0 <example_name> data/deepfashion

```
