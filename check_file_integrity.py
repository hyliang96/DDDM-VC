import torch
import torchaudio
from tqdm import tqdm
import os

def main(filelist_path):
    print()
    print(filelist_path)
    with open(filelist_path, 'r') as f:
        filelist = f.readlines()
    pbar = tqdm(filelist)
    for i, file in enumerate(pbar):
        file = file.strip()
        pbar.set_description(os.path.basename(file))
        try:
            if file.split('.')[-1] == 'pt':
                torch.load(file)
            elif file.split('.')[-1] == 'wav':
                torchaudio.load(file)
            else:
                print(f"{file} is neither .pt nor .wav")
        except Exception as e:
            print(f"Error loading {file}: {e}")


if __name__ == '__main__':
    filelist_path_list = [
            'filelist/train_f0.txt',
            'filelist/train_wav.txt',
            'filelist/test_f0.txt',
            'filelist/test_wav.txt' ]
    for filelist_path in filelist_path_list:
        main(filelist_path)

