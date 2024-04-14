#!/bin/bash

IS_YOLO_DATASET=$1
DATASET_NAME=$2
INPUT_DIR=$3

#bash download_data.sh 
OUTPUT_DIR=data/$DATASET_NAME
TMP_DIR=data/tmp
if [ $IS_YOLO_DATASET -eq 1 ]; then
    $echo "Training YOLOv5 on $DATASET_NAME"
    python3 yolo/segment/train.py --workers 8 --device 0 --batch 4 --data $OUTPUT_DIR/data.yaml --project $OUTPUT_DIR --weights pre-trained_ckpt/yolov9-c-converted.pt --cfg yolo/models/segment/gelan-c-seg.yaml --epochs 150 --hyp yolo/data/hyps/hyp.scratch-high.yaml --evolve

    $echo "Evaluating YOLOv5 on $DATASET_NAME"
    python3 yolo/segment/predit.py --weights $OUTPUT_DIR/exp/weights/best.pt --source $OUTPUT_DIR/test/images --project $OUTPUT_DIR --device 0 --hide-labels

    $echo "Converting YOLOv5 to onnx"
    python3 yolo/export.py --weights $OUTPUT_DIR/exp/weights/best.pt --include onnx 

    $echo "Evaluating YOLOv5 onnx on $DATASET_NAME"
    python3 yolo-onnx-run/onnxruntime/main.py --model $OUTPUT_DIR/exp/weights/best.onnx --input $OUTPUT_DIR/test/images --data_dir $OUTPUT_DIR/test/labels --output $OUTPUT_DIR
else
    python3 coco_extract.py --input_dir $INPUT_DIR --json_path $INPUT_DIR/annotations/instances_train2024.json --output_dir $TMP_DIR --image_dir $INPUT_DIR/images/train --type train --total_image 500
    python3 coco_extract.py --input_dir $INPUT_DIR --json_path $INPUT_DIR/annotations/instances_val2024.json --output_dir $TMP_DIR  --image_dir $INPUT_DIR/images/val --type val --total_image 150
    
    python3 coco_to_yolo.py --input_dir $TMP_DIR --output_dir $OUTPUT_DIR

    $echo "Training YOLOv5 on $DATASET_NAME"
    python3 yolo/segment/train.py --workers 8 --device 0 --batch 4 --data $OUTPUT_DIR/data.yaml --project $OUTPUT_DIR --weights pre-trained_ckpt/yolov9-c-converted.pt --cfg yolo/models/segment/gelan-c-seg.yaml --epochs 150 --hyp yolo/data/hyps/hyp.scratch-high.yaml --evolve

    $echo "Evaluating YOLOv5 on $DATASET_NAME"
    python3 yolo/segment/predict.py --weights $OUTPUT_DIR/exp/weights/best.pt --source $OUTPUT_DIR/test/images --project $OUTPUT_DIR --device 0 --hide-labels

    $echo "Converting YOLOv5 to onnx"
    python3 yolo/export.py --weights $OUTPUT_DIR/exp/weights/best.pt --include onnx 

    $echo "Evaluating YOLOv5 onnx on $DATASET_NAME"
    python3 yolo-onnx-run/onnxruntime/main.py --model $OUTPUT_DIR/exp/weights/best.onnx --input $OUTPUT_DIR/test/images --data_dir $OUTPUT_DIR

    $echo "rename exp folder"
    mv $OUTPUT_DIR/exp2 $OUTPUT_DIR/output_pytorch

    $echo "zipping $OUTPUT_DIR"
    tar  -cvf $OUTPUT_DIR.tar $OUTPUT_DIR
fi

