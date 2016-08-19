"""
  Crawl through the whole downloaded repo to find all uses of pub/amb/icon
"""

import os
from glob import glob
from FocusBuild import main as magicx
import sys
REPOPATH = r"C:\Users\ptiroff\Desktop\REpos\616DevPgmSource"
OUTFILE = r"C:\users\ptiroff\documents\amb-20684\Output.txt"
SUBROUTINE_CALL = '@NL@CallExternalSub(Mis,MisWebEhrZ.ImagePaths.C,GetImagePath)'


def print_lines_using_filepath():
    os.chdir(REPOPATH)
    subdirs = glob('*/')[17:]
    for a_folder in subdirs:
        files = os.listdir(a_folder)
        for a_file in files:
            if a_file == 'OmOrd.XoFormatEvent.OmOrdSiu.P.focus':
                break
            filepath = os.path.join(a_folder, a_file)
            with open(filepath, 'r') as f:
                with open(OUTFILE, 'a') as w:
                    flag = True
                    count = 0
                    for line in f:
                        if 'pub\\amb\\icon' in line and flag:
                            w.write(a_file)
                            w.write('\n')
                            flag = False
                        if 'pub/amb/icon' in line:
                            w.write(str(count) + ' ')
                            w.write(line)
                        count = count + 1
                    if not flag:
                        w.write('\n')


def print_the_filenames_containing_filepath():
    os.chdir(REPOPATH)
    subdirs = glob('*/')[0:1]
    for a_folder in subdirs:
        files = os.listdir(a_folder)
        for a_file in files:
            filepath = os.path.join(a_folder, a_file)
            with open(filepath, 'r') as f:
                with open(OUTFILE, 'a') as w:
                    for line in f:
                        if 'pub/amb/icon' in line:
                            w.write(a_file)
                            w.write('\n\r')
                            break


def print_files_being_used():
    imagedic = {}
    os.chdir(REPOPATH)
    subdirs = glob('*/')
    for a_folder in subdirs:
        files = os.listdir(a_folder)
        for a_file in files:
            filepath = os.path.join(a_folder, a_file)
            with open(filepath, 'r') as f:
                with open(OUTFILE, 'a') as w:
                    for line in f:
                        find = line.find('pub/amb/icon')
                        if find != -1:
                            end = line.find(r'"', find)
                            image = line[find:end].lower()
                            if image not in imagedic:
                                w.write(image)
                                w.write(os.linesep)
                                imagedic[image] = True


def swap_out_for_subroutine(manual):
    """also prints the line before and after the replace"""
    os.chdir(REPOPATH)
    if manual:
        execute_swap_on(manual)
        return
    subdirs = glob('*/')
    subdirs = subdirs
    for a_folder in subdirs:
        files = os.listdir(a_folder)
        print('checking ' + a_folder)
        for a_file in files:
            if a_file == 'OmOrd.XoFormatEvent.OmOrdSiu.P.focus':
                print('we dont like this one')
                break
            filepath = os.path.join(a_folder, a_file)
            execute_swap_on(filepath)


def swap_out_for_subroutine_focobj():
    """also prints the line before and after the replace"""
    os.chdir(REPOPATH)
    subdirs = glob('*/')
    subdirs = subdirs
    for a_folder in subdirs:
        print('checking ' + a_folder)
        f = os.path.join(a_folder, 'FocObj')
        try:
            files = os.listdir(f)
        except OSError:
            print('FocObj not found in' + f)
            continue
        for a_file in files:
            filepath = os.path.join(f, a_file)
            execute_swap_on(filepath)


def execute_swap_on(filepath):
    with open(filepath, 'r') as c:
        wholecode = c.readlines()
    with open(OUTFILE, 'a') as w:
        with open(filepath, 'w') as f:
            file_not_modified = True
            linenum = 1
            for line in wholecode:
                index = line.lower().find('pub\\amb\\icon')
                if index != -1:
                    if file_not_modified:
                        filename = os.path.split(filepath)[1]
                        w.write(filename)
                        w.write('\n\n')
                        file_not_modified = False
                    w.write(str(linenum))
                    try:
                        newline = do_the_replacing(line, index, w)
                        index = newline.find('pub/amb/icon')
                        while index != -1:
                            newline = do_the_replacing(newline, index, w)
                            index = newline.find('pub/amb/icon')
                        f.write(newline)
                    except AttributeError:
                        print('path was not formatted correctly')
                        f.write(line)
                        pass
                else:
                    f.write(line)
                linenum += 1
        if not file_not_modified:
            if not format_lint_translate(filepath):
                w.write('^^^ERROR TRANSLATING THIS FILE^^^^')
            w.write('\n')


def do_the_replacing(line, index, w):
    w.write('\n')
    w.write('-')
    w.write(line)
    end = line.lower().find('.png', index)
    if line[index-1] != '"' or line[end+4] != '"':
        w.write("DIRECT REPLACEMENT\n")
        begin = line.lower().find('/', index)
        end = line.lower().find('/', begin + 1)
        newline = line[:begin + 1] + 'web' + line[end:]
        return newline
    imagename = line[index + 13:end+4]
    newline = line[:index-1] + '(' + SUBROUTINE_CALL + ',"' + imagename + '")' + line[end+5:]
    w.write("+")
    w.write(newline)
    w.write('\n')
    return newline


def format_lint_translate(filepath):
    full_path = os.path.abspath(filepath)
    return magicx(full_path)


def just_translate():
    focus_files = []
    with open('output1.txt', 'r') as r:
        for line in r:
            if '.focus' in line:
                focus_files.append(line.strip())
    w = open('translate_check1.txt', 'a')
    os.chdir(REPOPATH)
    subdirs = glob('*/')
    subdirs = subdirs
    for a_folder in subdirs:
        files = os.listdir(a_folder)
        print('translating ' + a_folder)
        for a_file in files:
            if a_file not in focus_files:
                continue
            filepath = os.path.join(a_folder, a_file)
            filepath = os.path.join(REPOPATH, filepath)
            oldout = sys.stdout
            sys.stdout = w
            format_lint_translate(filepath)
            sys.stdout = oldout
    w.close()


def did_i_miss_some():
    os.chdir(REPOPATH)
    subdirs = glob('*/')
    for a_folder in subdirs:
        files = os.listdir(a_folder)
        for a_file in files:
            if a_file == 'OmOrd.XoFormatEvent.OmOrdSiu.P.focus':
                print('we dont like this one')
                break
            filepath = os.path.join(a_folder, a_file)
            with open(filepath, 'r') as f:
                with open(OUTFILE, 'a') as w:
                    for line in f:
                        if 'pub/amb/icon' in line.lower():
                            w.write(a_file)
                            w.write('\n\r')
                            break

if __name__ == '__main__':
    try:
        arg = sys.argv[1]
        if arg == 'translate':
            just_translate()
        else:
            swap_out_for_subroutine(arg)
    except IndexError:
        swap_out_for_subroutine(False)
