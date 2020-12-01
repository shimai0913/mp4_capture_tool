import os
import re
import argparse
import time
import datetime
import cv2
import youtube_dl
# import json

# ========================================================================== #
#  関数名: check_args
# -------------------------------------------------------------------------- #
#  説明: コマンドライン引数の受け取り
#  返り値: dict
# ========================================================================== #
def check_args():
    # ---------------------
    # コマンドライン引数の受け取り
    # ---------------------
    parser = argparse.ArgumentParser(add_help=False)

    # 引数の追加
    parser.add_argument("-url", help="url", required=True)
    # parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    try:
        result = {}
        result["url"] = args.url
        # result["debug"] = args.debug
        result["error_code"] = 1

        return result
    except Exception as e:
        if args.debug:
            print(f"引数指定に誤りがありそうです{e}")
        return 1

# -------------------------------------------------------------------------- #
#  クラス名    MyTool
#  説明        スクショ作成クラス
#  引数1       dict(コマンドライン引数)
# -------------------------------------------------------------------------- #
class MyTool:
    # [Dont Touch] インスタンス変数
    def __init__(self, args):
        self.def_name = "init"
        # self.video_path = args['filename']

        # self.debugflag = args["debug"]
        self._error_code = args["error_code"]

    # ====================================================================== #
    #  関数名: printLog
    # ---------------------------------------------------------------------- #
    #  説明: ログ
    # ====================================================================== #
    def printLog(self, level, message):
        # with open(r"self.log_path", 'a') as f:
        #     f.write(f'[{level}] {message}\n')
        # if self.debugflag:
        print(f'[{level}] {message}')

    # ========================================================================== #
    #  関数名: dl_youtube
    # -------------------------------------------------------------------------- #
    #  説明: YouTube から動画をmp4形式でダウンロード
    # ========================================================================== #
    def dl_youtube(self, url):
        self.def_name = "dl_youtube"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        options = {
            'outtmpl': '%(title)s.%(ext)s',
            'format':'bestvideo'
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            result = ydl.extract_info(url, download=True)
            # 文字列置換は正規表現で拾えるようにここに記載していく
            filename = re.sub(r"[|/]", "_", result["title"])
            self.video_name = f'{filename}.mp4'
            self.img_path = f'./screen_shots[{self.video_name}]'
            # with open('result.json', 'w') as f:
            #     json.dump(result, f, indent=4)
            print('='*60)
            self.printLog("INFO", f'title:        {filename}')
            self.printLog("INFO", f"id:           {result['id']}")
            self.printLog("INFO", f'dl_format:    {result["format"]}')
            self.printLog("INFO", f'uploader:     {result["uploader"]}')
            self.printLog("INFO", f'uploader_url: {result["uploader_url"]}')
            self.printLog("INFO", f'channel_id:   {result["channel_id"]}')
            self.printLog("INFO", f'channel_url:  {result["channel_url"]}')
            self.printLog("INFO", f'upload_date:  {result["upload_date"]}')
            print('='*60)

        # ログ作業後処理
        message = f'dl_youtube completed.'
        self.printLog("INFO", f'[ OK ] {message}')

    # ========================================================================== #
    #  関数名: save_all_frames
    # -------------------------------------------------------------------------- #
    #  説明: フレームごとにimg作成
    # ========================================================================== #
    def save_all_frames(self, basename='img', ext='jpg'):
        self.def_name = "save_all_frames"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        cap = cv2.VideoCapture(self.video_name)
        if not cap.isOpened():
            self.printLog("FATAL", f'[ NG ] File not found.')
            return

        os.makedirs(self.img_path, exist_ok=True)
        message = f'Created「{self.img_path}」directory.'
        self.printLog("INFO", f'[ OK ] {message}')

        base_path = os.path.join(self.img_path, basename)
        digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
        # ファイル名用
        n = 0
        # 動く文字用
        num = 1
        # クロック
        clock = 0.1
        while True:
            ret, frame = cap.read()
            if ret:
                filename = f'{base_path}_{str(n).zfill(digit)}.{ext}'
                cv2.imwrite(filename, frame)
                message = f'Save "{filename}"'
                # self.printLog("INFO", f'[ OK ] {message}')
                n += 1

                # ====================================================
                # ここから文字が動くコード
                # while num != 0:
                moji = 'Please wait a moment. Capturing now.'
                space = ' ' * num
                count = num - len(moji)

                if num < len(moji):
                    # time.sleep(clock)
                    # 文字の描写の部分。numの値が増加するほど横に移動する
                    print(f'\r{space} {moji}', end='')
                    num += 1
                else:
                    # 右に全角スペース20個分移動したら、右にoutして、左からinする部分
                    if count <= len(moji):
                        # time.sleep(clock)
                        a = moji[len(moji) - count:]
                        b = ' ' * (num - count)
                        c = moji[:(len(moji) - count)]
                        print(f'\r{a} {b} {c}', end='')
                        num += 1
                    else:
                        num = 1
                # ====================================================
            else:
                # ログ作業後処理
                message = f'save_all_frames completed.'
                print('\n')
                self.printLog("INFO", f'[ OK ] {message}')
                return



    # ========================================================================== #
    #  関数名: countfiles
    # -------------------------------------------------------------------------- #
    #  説明: 作成したimgファイルをカウント
    # ========================================================================== #
    def countfiles(self):
        self.def_name = "countfiles"
        description = f'Processing of "{self.def_name}" function is started.'
        self.printLog("INFO", f'[ OK ] {description}')

        # メインコード
        # フォルダ内の全ファイル名をリスト化
        files = os.listdir(self.img_path)
        # リストの長さ（ファイル数）を取得
        count = len(files)
        # ファイル数を確認
        self.printLog("INFO", f'Created "{count}" files.')

        # ログ作業後処理
        message = f'countfiles completed.'
        self.printLog("INFO", f'[ OK ] {message}')


# ========================================================================== #
#  メインパート
# ========================================================================== #
def main():
    # コマンドライン引数の受け取り
    args = check_args()
    assert args != 1, "Abnormality in argument."

    tool = MyTool(args)

    # mp4ダウンロード
    tool.dl_youtube(args['url'])

    # 保存
    tool.save_all_frames()
    tool.countfiles()

if __name__ == "__main__":
    main()
