import argparse
import os
import shutil
import re

# 给md文件各级变体加上锚点
def rename_titles(mdfile: str):
    f = open(mdfile, encoding="utf-8", mode="r")
    lines = f.readlines()
    h1, h2, h3 = -1, -1, -1
    # 是否已进入代码块
    shell_flag = False
    for i, line in enumerate(lines):
        # 代码块中也有#符号，所以在代码块中的行直接跳过
        if shell_flag:
            if line == "```\n":
                shell_flag = False
                continue
            continue

        if line == "```shell\n":
            shell_flag = True
            continue

        if line[0] == "#" and line[:2] != "##":
            h1 += 1
            h2 = -1
            h3 = -1
            lines[i] = line[0:len(line) - 1] + "<a id=\"" + str(h1) + "\"></a>\n"
        if line[:2] == "##" and line[:3] != "###":
            h2 += 1
            h3 = -1
            lines[i] = line[0:len(line) - 1] + "<a id=\"" + str(h1) + '.' + str(h2) + "\"></a>\n"
        if line[:3] == "###":
            h3 += 1
            lines[i] = line[0:len(line) - 1] + "<a id=\"" + str(h1) + '.' + str(h2) + '.' + str(h3) + "\"></a>\n"

    f.close()

    f = open(mdfile, encoding="utf-8", mode="w+")
    f.writelines(lines)
    f.close()


# 依据锚点名称，添加目录
def add_catalog(mdfile: str):
    f = open(mdfile, encoding="utf-8", mode="r")
    lines = f.readlines()
    h_list = []
    # 是否已进入代码块
    shell_flag = False
    for i, line in enumerate(lines):
        # 代码块中也有#符号，所以在代码块中的行直接跳过
        if shell_flag:
            if line == "```\n":
                shell_flag = False
                continue
            continue

        if line == "```shell\n":
            shell_flag = True
            continue
        # 获取所有标题锚点的id值
        if line.startswith("#"):
            searchObj = re.search(r'#+ (.*)<a id="(.*)"', line)
            headline = searchObj.group(1)
            id = searchObj.group(2)
            h_str = ' '*4*id.count('.')+'- ['+headline+']'+'('+ '#' + id + ')\n'
            h_list.append(h_str)
    f.close()
    finished = h_list + lines
    f = open(mdfile, encoding="utf-8", mode='w+')
    f.writelines(finished)
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add a catalogue into your markdown file.')
    parser.add_argument('input', help='an input markdown file path')
    parser.add_argument('-o', metavar='OUTPUT', help='specify an output file path, "./default.md" by default',
                        default='default.md')
    args = parser.parse_args()
    inputFile = args.input
    outputFile = args.o
    # 判断用户输入是否为markdown文件，如果不是，则抛出异常
    if not re.match(r'(.*).md$', inputFile):
        raise argparse.ArgumentTypeError("Only markdown file is accepted.")
    shutil.copyfile(inputFile, outputFile)
    rename_titles(outputFile)
    add_catalog(outputFile)

