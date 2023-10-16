#!/usr/bin/bash
src_dir=solutions
target_dir=qmd
files=$src_dir/*

for filename in $files
do
    filename=$(basename -- "$filename")
    extension="${filename##*.}"
    filename="${filename%.*}"
    source_file=$src_dir/$filename.org
    target_file=$target_dir/$filename.qmd
    if [ $extension != org ]
    then
        continue
    fi
    if [ $source_file -nt $target_file ]
    then
        printf '%s\n' "$source_file is newer than $target_file"
        ./publish $source_file
    fi
done

. $HOME/.venvs/aoc/bin/activate
quarto publish gh-pages
