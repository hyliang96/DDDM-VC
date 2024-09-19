import os

import torch
from torch.utils.data import DataLoader, Dataset
from extract_f0 import extract, Collate

class ListDataset(Dataset):
    def __init__(self, data_list):
        self.data_list = data_list

    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, idx):
        return self.data_list[idx]

def main(pt_filelist_path, audio_filelist_path):
    with open(pt_filelist_path, 'r') as f:
        pt_filelist = f.readlines()

    with open(audio_filelist_path, 'r') as f:
        audio_filelist = f.readlines()

    error_pts = []
    for file in pt_filelist:
        file = file.strip()
        try:
            torch.load(file)
        except Exception as e:
            print(f"Error loading {file}: {e}")
            error_pts.append(file)
            # delete the file
            if os.path.isfile(file):
                os.remove(file)
    
    if len(error_pts) == 0:
        print("Everything is good!")
        return 0
        
    audio_path_dict = {
        os.path.splitext(os.path.basename(path))[0]: path.strip()
        for path in audio_filelist
    }

    error_audios = [
        audio_path_dict[os.path.splitext(os.path.basename(pt_path))[0]]
        for pt_path in error_pts
    ]
    print(error_audios)

    error_audio_dataset = ListDataset(error_audios)

    d_loader = DataLoader(error_audio_dataset, num_workers=8, shuffle=False,
                          batch_size=1, pin_memory=True,
                          drop_last=False, collate_fn=Collate())
    output_dir = os.path.dirname(error_pts[0])
    audio_type = os.path.splitext(error_audios[0])[1][1:]

    extract(d_loader, output_dir, 0, resample_rate=16000, audio_type=audio_type)


if __name__ == '__main__':
    filelist_path = '/data/wangweikang22/project/DDDM-VC/filelist/libritts/train_f0.txt'
    audiolist_path = '/data/wangweikang22/project/DDDM-VC/filelist/libritts/train_wav.txt'
    main(filelist_path, audiolist_path)
