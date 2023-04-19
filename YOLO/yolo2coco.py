import json
import os
from tqdm import tqdm
from glob import glob
import argparse

def get_args_parser(add_help=True):
    parser = argparse.ArgumentParser(description='YOLOv6 PyTorch Training', add_help=add_help)
    parser.add_argument('--save_path', default='./pred.json', type=str)
    return parser


if __name__ == '__main__':
    args = get_args_parser().parse_args()

    # img_folder = glob(os.path.join("labels/", "*.jpg"))
    lable_folder = glob(os.path.join("./runs/inference/exp/valid/", "*.txt"))
    # print(lable_folder)
    label_dict = {}

    pbar = tqdm(total=len(lable_folder))

    for img_path in lable_folder:
        # print(img_path)
        # jpg file name and its label
        basename = os.path.basename(img_path)
        filename = os.path.splitext(basename)[0]

        # label_path = 'labels/' + filename + '.txt'

        ### labels, cx, cy, w, h, scores ###
        label = []
        with open(img_path, 'r') as f:
            # print("read")
            for rows in f.readlines():
                label.append(rows.split())

        label = sorted(label, key=lambda x: x[5], reverse=True)
        # print(label)
        # break

        ### format ###
        # {
        #   FILE_NAME:{
        #       boxes:[],
        #       labels:[],
        #       scores:[]
        #   },
        #   FILE_NAME2:{
        #   ...
        #   }
        # }
        ### format ###

        boxes = []
        labels = []
        scores = []

        for ele in label:
            cx, cy, w, h, H, W = float(ele[1]), float(ele[2]), float(ele[3]), float(ele[4]), float(ele[6]), float(ele[7])
            # print(H, W)
        
            x1 = (cx - w/2) * W 
            y1 = (cy - h/2) * H
            x2 = (cx + w/2) * W
            y2 = (cy + h/2) * H

            # if x1 < 0: x1 = 0
            # if y1 < 0: y1 = 0
            # if x2 < 0: x2 = 0
            # if y2 < 0: y2 = 0

            if ([x1, y1, x2, y2] not in boxes):
                boxes.append([x1, y1, x2, y2])
                labels.append(int(ele[0]))
                scores.append(float(ele[5]))
        
        predict = {
            'boxes': boxes,
            'labels': labels,
            'scores': scores
        }

        label_dict['{}'.format(str(filename) + '.jpg')] = predict
        pbar.update(1)
    save_path = args.save_path
    

    with open(save_path, 'w') as file:
        json.dump(label_dict, file, indent=4)
        

