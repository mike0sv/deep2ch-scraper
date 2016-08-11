from __future__ import print_function

import json
import os
from codecs import open as c_open
import requests

threads_url = 'http://2ch.hk/b/%s.json'
thread_url = 'http://2ch.hk/b/res/%s.json'
stat_file = './stat.json'
data_dir = './data/'
statistics = None


def grab_thread(thread_num):
    posts = json.loads(requests.get(thread_url % thread_num).content)['threads'][0]['posts']
    texts = []
    for post in posts:
        texts.append(post['comment'])
    with c_open(data_dir + thread_num + '.txt', 'w', encoding='utf8') as post_dump:
        #post_dump.write('\n'.join(texts))
        json.dump(texts, post_dump, ensure_ascii=False)


def init():
    global statistics
    if os.path.isfile(stat_file):
        statistics = json.load(open(stat_file, 'r'))
        print('Loaded history', len(statistics))
    else:
        statistics = dict()

    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)


def end():
    json.dump(statistics, open(stat_file, 'w'))


def main():
    init()
    try:
        for page in ['index'] + map(str, range(1, 100)):
            print('Page', page)
            response = requests.get(threads_url % page)
            if response.status_code != 200:
                break
            threads = json.loads(response.content)['threads']
            for thread in threads:
                num, count = thread['thread_num'], thread['posts_count']
                if num not in statistics or count != statistics[num]:
                    print('\t Thread', num, 'count', count)
                    grab_thread(num)
                    statistics[num] = count
    except Exception as e:
        print('Oooops,', e)
    print('That\'s all, folks!', len(statistics), 'threads!')
    end()


if __name__ == '__main__':
    main()
