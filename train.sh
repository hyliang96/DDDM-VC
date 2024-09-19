config_path="./configs/libritts.json"
model_name="libritts"

export CUDA_VISIBLE_DEVICES=0,1,2,3
export HF_HUB_OFFLINE=1
python train_dddmvc.py -c $config_path -m $model_name