# -*-coding:utf-8-*-

import os
from xml.etree.ElementTree import dump
import json
import pprint

import argparse

from preprocessing import *

from Format import VOC, COCO, UDACITY, KITTI, YOLO

parser = argparse.ArgumentParser(description='label Converting example.')
parser.add_argument('--datasets', type=str, help='type of datasets')
parser.add_argument('--img_path', type=str, help='directory of image folder')
parser.add_argument('--label', type=str,
                    help='directory of label folder or label file path')
parser.add_argument('--convert_output_path', type=str,
                    help='directory of label folder')
parser.add_argument('--img_type', type=str, help='type of image')
parser.add_argument('--manifest_path', type=str,
                    help='directory of manipast file', default="./")
parser.add_argument('--cls_list_file', type=str,
                    help='directory of *.names file', default="./")

parser.add_argument('--original_path', type=str, default='test_dataset', help='test dataset path')

args = parser.parse_args()


def main(config):

    if config["datasets"] == "VOC":
        voc = VOC()
        yolo = YOLO(os.path.abspath(config["cls_list"]))

        flag, data = voc.parse(config["label"])

        if flag == True:

            flag, data = yolo.generate(data)
            if flag == True:
                flag, data = yolo.save(data, config["output_path"], config["img_path"],
                                       config["img_type"], config["manifest_path"])

                if flag == False:
                    print("Saving Result : {}, msg : {}".format(flag, data))

            else:
                print("YOLO Generating Result : {}, msg : {}".format(flag, data))

        else:
            print("VOC Parsing Result : {}, msg : {}".format(flag, data))

    elif config["datasets"] == "COCO":
        coco = COCO()
     
        flag, data, cls_hierarchy = coco.parse(
            config["label"], config["img_path"])
        yolo = YOLO(os.path.abspath(
            config["cls_list"]), cls_hierarchy=cls_hierarchy)

        if flag == True:
            flag, data = yolo.generate(data)

            if flag == True:
                flag, data = yolo.save(data, config["output_path"], config["img_path"],
                                       config["img_type"], config["manifest_path"])

                if flag == False:
                    print("Saving Result : {}, msg : {}".format(flag, data))

            else:
                print("YOLO Generating Result : {}, msg : {}".format(flag, data))

        else:
            print("COCO Parsing Result : {}, msg : {}".format(flag, data))



        
    elif config["datasets"] == "UDACITY":
        udacity = UDACITY()
        yolo = YOLO(os.path.abspath(config["cls_list"]))

        flag, data = udacity.parse(config["label"])

        if flag == True:
            flag, data = yolo.generate(data)

            if flag == True:
                flag, data = yolo.save(data, config["output_path"], config["img_path"],
                                       config["img_type"], config["manifest_path"])

                if flag == False:
                    print("Saving Result : {}, msg : {}".format(flag, data))

            else:
                print("UDACITY Generating Result : {}, msg : {}".format(flag, data))

        else:
            print("COCO Parsing Result : {}, msg : {}".format(flag, data))

    elif config["datasets"] == "KITTI":
        kitti = KITTI()
        yolo = YOLO(os.path.abspath(config["cls_list"]))

        flag, data = kitti.parse(
            config["label"], config["img_path"], img_type=config["img_type"])

        if flag == True:
            flag, data = yolo.generate(data)

            if flag == True:
                flag, data = yolo.save(data, config["output_path"], config["img_path"],
                                       config["img_type"], config["manifest_path"])

                if flag == False:
                    print("Saving Result : {}, msg : {}".format(flag, data))

            else:
                print("YOLO Generating Result : {}, msg : {}".format(flag, data))

        else:
            print("KITTI Parsing Result : {}, msg : {}".format(flag, data))

    else:
        print("Unkwon Datasets")


if __name__ == '__main__':

    config = {
        "datasets": args.datasets,
        "img_path": args.img_path,
        "label": args.label,
        "img_type": args.img_type,
        "manifest_path": args.manifest_path,
        "output_path": args.convert_output_path,
        "cls_list": args.cls_list_file,
    }
    
    
    
    original_root = args.original_path
    save_root = 'preprocessed_dataset'

    classes = ['PET', 'PS', 'PP', 'PE']

    copy_images(original_root, save_root, classes)
    merge_json(save_root)
    os.makedirs(os.path.join(save_root, 'annotation','yolov4'), exist_ok=True)


    json_files = [i for i in os.listdir(os.path.join(save_root, 'annotation')) if i.endswith('json')]
    for jf in tqdm(json_files):
        os.remove(f"{save_root}/annotation/{jf}")

    main(config)
    
    make_txt(save_root)
    