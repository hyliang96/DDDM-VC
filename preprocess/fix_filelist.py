import os

# 读取txt文件，并返回文件路径的列表
def read_file_paths(file_path):
    with open(file_path, 'r') as f:
        paths = f.readlines()
    return [path.strip() for path in paths]

# 根据文件路径中的最后一级文件名排序
def sort_by_filename(file_paths):
    return sorted(file_paths, key=lambda x: os.path.basename(x))

# 将排序后的文件路径写入新的txt文件
def write_sorted_paths(file_paths, output_file):
    with open(output_file, 'w') as f:
        for path in file_paths:
            f.write(path + '\n')

def check_filenames_match(pt_paths, wav_paths):
    mismatched_pairs = []
    for idx, (pt_path, wav_path) in enumerate(zip(pt_paths, wav_paths)):
        pt_basename = os.path.splitext(os.path.basename(pt_path))[0]
        wav_basename = os.path.splitext(os.path.basename(wav_path))[0]
        if pt_basename != wav_basename:
            mismatched_pairs.append((idx, pt_basename, wav_basename))

    if mismatched_pairs:
        print("Mismatched file names found at the following indices:")
        for idx, pt_name, wav_name in mismatched_pairs:
            print(f"Index {idx}: .pt file '{pt_name}' and .wav file '{wav_name}' do not match")
    else:
        print("All file names match!")

# 主函数
def main(pt_file, wav_file, sorted_pt_output, sorted_wav_output):
    # 读取文件
    pt_paths = read_file_paths(pt_file)
    wav_paths = read_file_paths(wav_file)

    # 根据文件名排序
    sorted_pt_paths = sort_by_filename(pt_paths)
    sorted_wav_paths = sort_by_filename(wav_paths)

    # 检查文件名是否匹配
    check_filenames_match(sorted_pt_paths, sorted_wav_paths)

    # 将排序后的结果写入新的文件
    write_sorted_paths(sorted_pt_paths, sorted_pt_output)
    write_sorted_paths(sorted_wav_paths, sorted_wav_output)

if __name__ == '__main__':
    pt_file = '/data/wangweikang22/data/LibriTTS/train_f0.txt'  # 你的 .pt 文件路径列表
    wav_file = '/data/wangweikang22/data/LibriTTS/train_wav.txt'  # 你的 .wav 文件路径列表
    sorted_pt_output = '/data/wangweikang22/project/DDDM-VC/filelist/libritts/train_f0.txt'  # 排序后的 .pt 文件输出路径
    sorted_wav_output = '/data/wangweikang22/project/DDDM-VC/filelist/libritts/train_wav.txt'  # 排序后的 .wav 文件输出路径

    main(pt_file, wav_file, sorted_pt_output, sorted_wav_output)