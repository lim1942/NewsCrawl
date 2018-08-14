# -*- coding: utf-8 -*-
# @Author: lim
# @Date:   2018-08-13 13:52:04
# @Last Modified by:   lim
# @Last Modified time: 2018-08-13 16:07:48

import os
import sys
import pinyin


def excel_ensure(path):
    try:
        os.rename(path,path)
        return path
    except:
        print('Please don`t open {} when process is working !!!'.format(path))


def get_pinyin(chinese):
    word = ''
    for i in chinese:
        try:
            w = pinyin.get(i, format='strip')
        except Exception as e:
            print(e)
            w = ''
        word += w
    return word


suffixes = ['pyc', 'pyo']
dirName = ['__pycache__']
def clean_all(root_dirs, suffixes=suffixes): 
    def clean(root_dir, suffixes=suffixes):

        if not os.path.isdir(root_dir):
            print ('Directory {} not exists, skipped.'.format(root_dir))

        suffixes = map(lambda x: '.' + x, suffixes)
        for root, dirs, files in os.walk(root_dir):

            # clear __pycache__ dir
            for _dir in dirs: 
                if any(map(lambda x: _dir==x, dirName)):
                    try:
                        fullDirName = os.path.join(root,_dir)
                        os.system('rd /s /q {}'.format(fullDirName))
                        print(fullDirName+'  done')
                    except Exception as e:
                        print ('Failed to delete {}: {}'.format(fullDirName, str(e)))
                        
            # clear pyc、pyo file
            for file in files:
                if any(map(lambda x: file.endswith(x), suffixes)):
                    try:
                        fileName = os.path.join(root, file)
                        os.remove(fileName)
                        print(fileName+'  done')
                    except Exception as e:
                        print ('Failed to delete {}: {}'.format(file, str(e)))

    for root_dir in root_dirs:
        clean(root_dir, suffixes)




#clear pyc
if __name__ == '__main__':
    if len(sys.argv) == 1:
        root_dirs = [os.path.dirname(os.path.abspath(__file__))]
    else:
        root_dirs = sys.argv[1:]
    clean_all(root_dirs)