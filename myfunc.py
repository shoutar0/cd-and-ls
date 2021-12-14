# -*- coding: utf-8 -*-
"""My Functions

自作関数モジュールとして .xonshrc から呼び出すクラスを定義します。

Note:
    例えば、.xonshrc で以下のように呼び出します。::

    import sys
    sys.path.append('path/to/myfunc.py')

    from myfunc import CdAndLs
    func = CdAndLs()

"""

import os
import unicodedata
from typing import List


class CdAndLs:
    """Change Directory And List All Components.

    cd した後に ls するために必要な属性とメソッドを定義します。

    Attributes:
        new_path (str): 移動先のパスを格納する。
        self.dirs List[str]: ディレクトリ名の一覧を格納する変数。
        self.files List[str]: ファイル名の一覧を格納する変数。
        self.dir_title (str): ディレクトリ一覧のタイトル。
        self.files_title (str): ファイル一覧のタイトル。
        self.dirs_list (str): ディレクトリ一覧を表示するための文字列を格納する変数。
        self.files_list (str): ファイル一覧を表示するための文字列を格納する変数。
        self.str_len (int): 全角を含んだ文字列の文字数を格納する変数。

    """

    def __init__(self):
        self.new_path: str = ''
        self.dirs: List[str] = []
        self.files: List[str] = []
        self.dir_title: str = '\n' + '------- directories -------'.center(52) + '\n'
        self.files_title: str = '\n\n' + '------- files -------'.center(52) + '\n'
        self.dirs_list: str = ''
        self.files_list: str = ''
        self.str_len: int = 0

    def change_dir(self, path: str) -> None:
        """ディレクトリの移動。

        引数で渡されたディレクトリへ移動し、移動先の絶対パスを取得します。

        Args:
            path (str): 移動先を指定するパス。

        """
        os.chdir(path)
        self.new_path = os.getcwd()

    def get_items(self) -> None:
        """ディレクトリ名とファイル名の取得。

        カレントディレクトリのディレクトリ名とファイル名を全て取得し、アルファベット順にソートします。

        """
        all_items: List[str] = os.listdir(self.new_path)  # ディレクトリ名とファイル名の全てを取得する。

        dirs: List[str] = [dir_name for dir_name in all_items
                           if os.path.isdir(os.path.join(self.new_path, dir_name))]  # ディレクトリ名のみを取得する。

        files: List[str] = [file_name for file_name in all_items
                            if os.path.isfile(os.path.join(self.new_path, file_name))]  # ファイル名のみを取得する。

        dirs.sort(key=str.lower)
        files.sort(key=str.lower)

        self.dirs, self.files = dirs, files

    def fullwidth_contains_judge(self, string: str) -> bool:
        """文字列中に全角文字かの判断

        引数に渡した文字列に全角文字が含まれるか判断します。
        全角文字が含まれる場合は、その文字を半角2文字分として文字数をカウントします。

        Args:
            string (str): 全角が含まれるかどうか判断したい文字列。

        Returns:
            contains_fullwidth (bool): 全角文字が含まれる場合は True が返されます。

        """
        contains_fullwidth: bool = False
        count: int = 0  # カウンタ変数。

        for char in string:
            name = unicodedata.name(char)

            if ("CJK UNIFIED" in name) or ("HIRAGANA" in name) or ("KATAKANA" in name):
                count = count + 2  # 全角文字は2文字としてカウントする。
                contains_fullwidth = True

            else:
                count = count + 1

        self.str_len = count
        return contains_fullwidth

    def add_blank(self):
        """ リストの各要素に対して、文字数が38文字になるように空白文字を追加するメソッド """

        # ディレクトリ名について
        for index, dir_name in enumerate(self.dirs):
            dir_name = dir_name + "/"
            if self.fullwidth_contains_judge(dir_name):
                self.dirs[index] = dir_name + " " * (38 - self.str_len)  # 全角文字が含まれる場合
            else:
                self.dirs[index] = dir_name.ljust(38)  # 半角文字のみの場合

        # ファイル名について
        for index, file_name in enumerate(self.files):
            if self.fullwidth_contains_judge(file_name):
                self.files[index] = file_name + " " * (38 - self.str_len)  # 全角文字が含まれる場合
            else:
                self.files[index] = file_name.ljust(38)  # 半角文字のみの場合

    def arrange_list(self):
        """ リスト内の各要素を2個ずつ並べて一覧表示になるように整形する。 """

        dis_len = len(self.dirs)
        files_len = len(self.files)

        dirs_list = ""  # 整形した文字列を格納する。(ディレクトリ名)
        files_list = ""  # 整形した文字列を格納する。(ファイル名)

        # ディレクトリ名について
        for i in range(0, dis_len - 1, 2):  # 2個ずつ並べる。
            dirs_list = dirs_list + self.dirs[i] + self.dirs[i + 1] + "\n"

        if self.dirs and (dis_len % 2):  # 奇数個(0でない)の場合
            dirs_list = dirs_list + self.dirs[-1]

        self.dirs_list = dirs_list

        # ファイル名について
        for i in range(0, files_len - 1, 2):  # 2個ずつ並べる。
            files_list = files_list + self.files[i] + self.files[i + 1] + "\n"

        if self.files and (files_len % 2):  # 奇数個(0でない)の場合
            files_list = files_list + self.files[-1]

        self.files_list = files_list
