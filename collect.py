from __future__ import print_function
import os
import re
import json
from codecs import open as copen
from grab import data_dir

collect_fname = 'collect.txt'


def main():
    collect = copen(collect_fname, 'w', encoding='utf8  ')
    for thread_file in os.listdir(data_dir):
        with copen(data_dir + thread_file, 'r', encoding='utf8') as thread:
            posts = json.load(thread, encoding='utf8')
            print(thread_file, len(posts), 'posts')
            for post in posts:
                post = re.sub('<.*>', ' ', post)
                post = post.replace('\n', ' ')
                if len(post.strip()) > 0:
                    collect.write(post.strip() + '\n')


if __name__ == '__main__':
    main()
