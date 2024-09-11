python3 inference.py \
    --src_path './sample/cn_woman.wav' \
    --trg_path './sample/cn_man.wav' \
    --ckpt_model './ckpt/model_base.pth' \
    --ckpt_voc './ckpt/voc_ckpt.pth' \
    --ckpt_f0_vqvae './ckpt/f0_vqvae.pth' \
    --output_dir './converted' \
    -t 6
