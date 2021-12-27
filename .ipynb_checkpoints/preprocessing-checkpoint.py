import random
import os
from tqdm import tqdm
import shutil
import json
import argparse




def copy_images(original_root, save_root, classes):

    for c in tqdm(classes, desc=f'TOTAL'):  ## generated는 train에만 들어가게 바꿔.
        random.seed(42)

        file_names = [i.split('.')[0] for i in os.listdir(os.path.join(original_root, d, c, 'image')) if
                      i.endswith('.jpg')]

        for file_name in tqdm(file_names, desc=f'{c}_{d}'):
            shutil.copy(os.path.join(original_root, c, 'image', file_name + '.jpg'),
                        os.path.join(save_root, 'image'))
            shutil.copy(os.path.join(original_root, c, 'annotation', file_name + '.json'),
                        os.path.join(save_root, 'annotation'))

def merge_json(root):

    save_root = os.path.join(root, 'annotation', 'mask_rcnn')
    os.makedirs(save_root, exist_ok=True)

    json_list = [i for i in os.listdir(os.path.join(root, 'annotation')) if i.endswith('json')]
    result = {'images': [], 'categories': [], 'annotations': []}
    cnt = 1
    for idx, json_id in enumerate(tqdm(json_list)):

        input_json = os.path.join(root, 'annotation', json_id)

        with open(input_json) as json_reader:
            dataset = json.load(json_reader)

        if idx == 0:
            result['categories'] = dataset['categories']

        images = dataset['images'][0]
        images['id'] = idx + 1
        result['images'].append(images)

        annotations = dataset['annotations']

        for anno in annotations:
            anno['id'] = cnt
            anno['image_id'] = images['id']
            result['annotations'].append(anno)
            cnt += 1

    with open(save_root + f'/test.json', 'w') as f:
        json.dump(result, f)

    print(f'merge complete!')


def make_txt(save_root):
    
    
    img_ids = [i.split('.j')[0]+".txt" for i in os.listdir(os.path.join(save_root, 'image'))]

    label_ids = os.listdir(os.path.join(save_root, 'annotation/yolov4'))

    SetList1 = set(img_ids)
    SetList2 = set(label_ids)

    empty = SetList1.difference(SetList2)        
    for em in empty:
        img_id = em.split('.')[0]

        with open(f'{save_root}/annotation/yolov4/{img_id}.txt', 'w'):
            pass
            
                
                
                





# python preprocessing.py --file_path {test 데이터셋 폴더이름}
# python convert2Yolo/example.py --datasets COCO --img_path preprocessed_dataset/image --label preprocessed_dataset/annotation/mask_rcnn/test.json --convert_output_path preprocessed_dataset/annotation/yolov4 --img_type ".jpg" --cls_list_file convert2Yolo/names.txt
