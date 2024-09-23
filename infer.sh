export CUDA_VISIBLE_DEVICES=0

ckpt_model="/home/wangweikang22/project/DDDM-VC/logs/libritts/G_310000.pth"

python3 inference.py \
    --src_path './sample/cn_woman.wav' \
    --trg_path './sample/cn_man.wav' \
    --ckpt_model $ckpt_model \
    --ckpt_voc './ckpt/voc_ckpt.pth' \
    --ckpt_f0_vqvae './ckpt/f0_vqvae.pth' \
    --output_dir './converted' \
    --traj \
    -t 6
