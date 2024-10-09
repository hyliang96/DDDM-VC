gdiff () {
    cd $(git rev-parse --show-toplevel 2>/dev/null)
    git diff "$@" --ignore-space-at-eol -- ':!filelist' ':!hf' ':!debug.log' ':!preprocess/fix_filelist.py' ':!preprocess/check_file_integrity.py' ':!configs/libritts.json' ':!requirement.txt' ':!train.sh' ':!ckpt/config.json' ':!configs/config.json' ':!.gitignore'
}
