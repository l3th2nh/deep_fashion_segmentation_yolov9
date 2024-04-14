#!/bin/bash

$echo "Downloading DeepFashion dataset"
cd data

wget https://s3.us-west-2.amazonaws.com/testing.resources/datasets/deepfashion/deep_fashion.tar

tar -xvf deep_fashion.tar

cd ..