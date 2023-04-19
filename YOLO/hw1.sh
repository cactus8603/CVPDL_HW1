python tools/infer.py --weights best_ckpt.pt --source $1 --save-txt
python yolo2coco.py --save_path $2
rm -rf runs/inference/exp/valid
