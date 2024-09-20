config_path="./configs/config.json"
model_name="try0.1"

export CUDA_VISIBLE_DEVICES=4,5,6,7
# export HF_HUB_OFFLINE=1
python train_dddmvc.py  -c $config_path -m $model_name
