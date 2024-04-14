from pycocotools.coco import COCO
import os
import shutil
import json
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='data')
    parser.add_argument('--json_path', type=str, default='data')
    parser.add_argument('--image_dir', type=str, default='data')
    parser.add_argument('--output_dir', type=str, default='data')
    parser.add_argument("--type", type=str, default="train")
    parser.add_argument("--total_image", type=int, default=500)

    args = parser.parse_args()
    input_dir = args.input_dir
    json_path = args.json_path
    image_dir = args.image_dir
    output_dir = args.output_dir
    total_image = args.total_image
    coco_type = args.type

    os.makedirs(os.path.join(output_dir, 'annotations'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', coco_type), exist_ok=True)

    if not (os.path.exists(os.path.join(output_dir, 'images', 'test'))) and coco_type == 'val':
        os.makedirs(os.path.join(output_dir, 'images', 'test'), exist_ok=True)
        list_test_images = os.listdir(os.path.join(input_dir, 'images', 'test'))
        list_test_images_sort = list_test_images[:50]
        #print(list_test_images_sort)
        for image in list_test_images_sort:
            shutil.copy(os.path.join(input_dir, 'images', 'test', image), os.path.join(output_dir, 'images', 'test'))
    
        
    output_annotation_file = os.path.join(output_dir, 'annotations', f'instances_{coco_type}.json')
    json_data = json.load(open(json_path, 'r'))
    coco = COCO(json_path)
    all_image_ids = coco.getImgIds()
    num_images_to_extract = total_image
    num_images_extracted = 0

    sorted_categories = sorted(json_data["categories"], key=lambda x: x["id"])
    coco_annotations = {
        "info": json_data['info'],
        "categories": sorted_categories,
        "images": [],
        "annotations": [],
    }

    for image_id in all_image_ids:
        if num_images_extracted >= num_images_to_extract:
            break

        image_info = coco.loadImgs([image_id])[0]
        image_filename = image_info['file_name']
        image_path = os.path.join(image_dir, image_filename)

        shutil.copy(image_path, os.path.join(output_dir, 'images', coco_type))

        coco_annotations["images"].append(image_info)

        ann_ids = coco.getAnnIds(imgIds=[image_id])
        annotations = coco.loadAnns(ann_ids)

        coco_annotations["annotations"].extend(annotations)

        num_images_extracted += 1
    
    with open(output_annotation_file, 'w') as f:
        json.dump(coco_annotations, f, indent=4)
    
    print(f"Extracted {num_images_extracted} images and saved annotations to {output_annotation_file}")
