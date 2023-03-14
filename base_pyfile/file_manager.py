import datetime
import os
import site
from logging import NullHandler, getLogger
from typing import List, Optional, Tuple, Union

module_path = r"C:\tool\base_pyfile"
site.addsitedir(module_path)
from function_timer import logger_timer
from log_setting import get_log_handler, make_logger
from path_manager import get_files, unique_path

logger = getLogger("log").getChild(__name__)
logger.addHandler(NullHandler())


existing_files = {}


@logger_timer()
def read_text_file(
    file_path: str, delimiter: Optional[str] = None, return_encoding: bool = False
) -> Union[str, Tuple[List[str], str]]:
    """
    テキストファイルを読み込み、指定された区切り文字で分割して返します。

    Args:
        file_path (str): ファイルパス
        delimiter (Optional[str], optional): 区切り文字。デフォルトはNone
        return_encoding (bool, optional): エンコーディングを返すかどうかを指定するフラグ。デフォルトはFalse

    Returns:
        Union[str, Tuple[List[str], str]]: テキストファイルの内容を文字列で返す場合と、
        指定された区切り文字で分割したテキストを含むリストとエンコーディングを含むタプルのどちらかを返します
    """

    encodings = ["utf-8", "Shift_JIS", "euc_jp", "iso2022_jp"]
    # 一般的なエンコーディングのリストでファイルを開きます
    for file_encoding in encodings:
        try:
            with open(file_path, "r", encoding=file_encoding) as f:
                text = f.read()
                break
        except:
            text = ""
    else:
        logger.warning(f"{file_path}を開くのに失敗しました")
        logger.warning("空の文字列を返します")

    if delimiter:
        if delimiter == "\n":
            logger.debug("\\nでリスト化しました")
        else:
            logger.info(rf"{delimiter}でリスト化しました")
        text = text.split(delimiter)

    if return_encoding:
        logger.info(f"エンコードは{file_encoding}")
        return text, file_encoding
    else:
        return text


@logger_timer()
def write_file(
    file_path: str,
    write_text: str = "",
    extension="txt",
    file_encoding: str = "utf-8",
    write_mode: str = "w",
    back_up_mode: bool = True,
) -> None:
    """
    ファイルにテキストを書き込む。

    Parameters
    ----------
    file_path : str
        書き込み先ファイルのパス
    write_text : str, optional
        書き込むテキスト。デフォルトは空文字列
    file_encoding : str, optional
        ファイルのエンコーディング。デフォルトは"utf-8"
    write_mode : str, optional
        書き込みモード。デフォルトは"w"
    back_up_mode : bool, optional
        Trueの場合、書き込み先にファイルが存在している場合は、バックアップを作成して上書き保存する。デフォルトはTrue

    Returns
    -------
    None
    """
    write_text = str(write_text)
    if not "." in extension:
        extension = "." + extension
    # 拡張子が引数と一致していなければ変更する
    if not (file_path.endswith(f"{extension}")):
        logger.info(f"拡張子が{extension}ではありません\n{extension}に変更します")
        file_path = os.path.splitext(file_path)[0] + f"{extension}"

    # バックアップを作成し、上書き保存をする
    if back_up_mode and os.path.exists(file_path):
        logger.info("既に書き込み先にはファイルが存在しています。バックアップを作成して上書き保存をします")
        backup_file(file_path)

    # ファイルを開いて書き込む
    with open(file_path, write_mode, encoding=file_encoding) as f:
        f.write(write_text)

    logger.debug(f"{file_path}にテキストファイルを保存しました")


def backup_file(file_path: str) -> None:
    """
    ファイルのバックアップを作成します。

    Args:
        file_path (str): バックアップを作成するファイルのパス。

    Returns:
        None
    """
    # 既存のファイルから読み込む
    file_content = read_text_file(file_path)
    # 現在日時を取得
    jst_timezone = datetime.timezone(datetime.timedelta(hours=9), "JST")
    current_datetime = datetime.datetime.now(jst_timezone)
    date_string = current_datetime.strftime("%y年%m月%d日")

    # バックアップフォルダを作成し、そこに日付を入れたファイル名で保存
    backup_file_path = os.path.join(
        os.path.dirname(file_path),
        "backup",
        f"{os.path.splitext(os.path.basename(file_path))[0]}_{date_string}_backup{{}}.txt",
    )
    # バックアップファイルを保存
    write_file(
        unique_path(backup_file_path, existing_text=file_content),
        file_content,
        back_up_mode=False,
    )


if __name__ == "__main__":
    logger = make_logger(handler=get_log_handler(10))

    print(get_files(r""))
    print(read_text_file(r"file_manager.py"))