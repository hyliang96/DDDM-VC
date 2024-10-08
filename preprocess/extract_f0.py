import os
import glob
import random
import argparse
import numpy as np
from tqdm import tqdm

import torch
import torchaudio
from torch.utils.data import DataLoader
import torch.multiprocessing as mp
import torch.distributed as dist

import torchaudio.functional as F
import torchaudio.transforms as T
import librosa
import amfm_decompy.basic_tools as basic
import amfm_decompy.pYAAPT as pYAAPT

def get_yaapt_f0(audio, sr=16000, interp=False):
    # sr: sample rate
    to_pad = int(20.0 / 1000 * sr) // 2
    f0s = []
    for y in audio.astype(np.float64):
        y_pad = np.pad(y.squeeze(), (to_pad, to_pad), "constant", constant_values=0)
        pitch = pYAAPT.yaapt(basic.SignalObj(y_pad, sr),
                             **{'frame_length': 20.0, 'frame_space': 5.0, 'nccf_thresh1': 0.25, 'tda_frame_length': 25.0})
        f0s.append(pitch.samp_interp[None, None, :] if interp else pitch.samp_values[None, None, :])

    return np.vstack(f0s)


def main(args):
    n_gpus = torch.cuda.device_count()
    port = 50000 + random.randint(0, 100)
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = str(port)
    os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

    mp.spawn(run, nprocs=n_gpus, args=(n_gpus, args))


def run(rank, n_gpus, args):
    dist.init_process_group(backend='nccl', init_method='env://', world_size=n_gpus, rank=rank)
    torch.manual_seed(1234)
    torch.cuda.set_device(rank)

    dset = DLoader(args.input_dir)
    d_sampler = torch.utils.data.distributed.DistributedSampler(
        dset,
        num_replicas=n_gpus,
        rank=rank,
        shuffle=False)

    collate_fn = Collate()
    d_loader = DataLoader(dset, num_workers=8, shuffle=False,
                          batch_size=1, pin_memory=True,
                          drop_last=False, collate_fn=collate_fn, sampler=d_sampler)

    for epoch in range(1):
        extract(d_loader, args.output_dir, rank)


class DLoader():
    def __init__(self, input_dir):
        self.wavs = []
        self.wavs += sorted(glob.glob(os.path.join(input_dir, '**/*.wav'), recursive=True))
        print('wav num: ', len(self.wavs))

    def __getitem__(self, index):
        return self.wavs[index]

    def __len__(self):
        return len(self.wavs)

class Collate():
    def __init__(self):
        pass

    def __call__(self, batch):
        return batch[0]

def extract(d_loader, output_dir, rank, resample_rate=16000):
    with torch.no_grad():
        pbar = tqdm(d_loader)
        for _, audio_path in enumerate(pbar):
            # if os.path.basename(audio_path) != '6120_56179_000054_000000.wav':
               # os.path.basename(audio_path) != '1116_132851_000036_000000.wav':
                # continue
            pbar.set_description(os.path.basename(audio_path))
            f0_filename = os.path.join(output_dir, os.path.basename(audio_path).replace(".wav", ".pt"))

            if not os.path.isfile(f0_filename):
                os.makedirs(os.path.dirname(f0_filename), exist_ok=True)

                audio, sample_rate = torchaudio.load(audio_path)
                resampler = T.Resample(sample_rate, resample_rate, dtype=audio.dtype)
                audio = resampler(audio)

                # torchaudio.save('/data/haoyu/data/LibriTTS/LibriTTS_16k/'+os.path.basename(audio_path), audio, resample_rate)

                p = (audio.shape[-1] // 1280 + 1) * 1280 - audio.shape[-1]
                audio = torch.nn.functional.pad(audio, (0, p), mode='constant').data

                try:
                    f0 = get_yaapt_f0(audio.numpy(), sr=resample_rate)
                except:
                    f0 = np.zeros((1, 1, audio.shape[-1] // 80))

                f0 = torch.FloatTensor(f0.astype(np.float32).squeeze(0))
                torch.save(f0, f0_filename)


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', default='/data/haoyu/data/LibriTTS/extract/train/LibriTTS-train-clean-360')
    parser.add_argument('-o', '--output_dir', default='/data/haoyu/data/LibriTTS/16k_f0/train/LibriTTS_train-clean-360_16k_f0)
    a = parser.parse_args()
    main(a)


