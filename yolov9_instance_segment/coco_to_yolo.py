from json2yolo.general_json2yolo import convert_coco_json
import os
import argparse
import shutil
import yaml
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='data')
    parser.add_argument('--output_dir', type=str, default='data')
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir

    annotation_folder = os.path.join(input_dir, 'annotations')

    # #convert coco json to yolo format
    convert_coco_json(annotation_folder, use_segments=True,dir=output_dir)
    #copy test images from input_dir to output_dir
    if not (os.path.exists(os.path.join(output_dir, 'test','images'))):
        os.makedirs(os.path.join(output_dir, 'test','images'), exist_ok=True)
        list_test_images = os.listdir(os.path.join(input_dir, 'images', 'test'))
        list_test_images_sort = list_test_images[:50]
        #print(list_test_images_sort)
        for image in list_test_images_sort:
            shutil.copy(os.path.join(input_dir, 'images', 'test', image), os.path.join(output_dir, 'test','images'))

    #copy images to train and valid folders
    shutil.copytree(os.path.join(input_dir, 'images', 'train'), os.path.join(output_dir, 'train','images'))
    shutil.copytree(os.path.join(input_dir, 'images', 'val'), os.path.join(output_dir, 'valid','images'))
    #copy labels to train and valid folders
    shutil.copytree(os.path.join(output_dir, 'labels', 'train'), os.path.join(output_dir, 'train','labels'))
    shutil.copytree(os.path.join(output_dir, 'labels', 'val'), os.path.join(output_dir, 'valid','labels'))

    #generate yaml file
    #reading json file for catorgies

    with open(os.path.join(input_dir, 'annotations', 'instances_train.json')) as f:
        data = json.load(f)
    
    categories = data['categories']
    category_names = []
    for category in categories:
        category_names.append(category['name'])
    category_names = list(category_names)
    
    data = dict(
        train = "../"+str(os.path.join(output_dir, 'train', 'images')),
        val = "../"+str(os.path.join(output_dir, 'valid', 'images')),
        test = "../"+str(os.path.join(output_dir, 'test', 'images')),
        nc = len(category_names),
        names = category_names
    )
    with open(os.path.join(output_dir, 'data.yaml'), 'w') as outfile:
        yaml.dump(data, outfile)
    
    #remove unused folders
    shutil.rmtree(os.path.join(output_dir, 'labels'))
    shutil.rmtree(os.path.join(output_dir, 'images'))
    shutil.rmtree(os.path.join(input_dir))
