import os
import cv2
import argparse
import datetime


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
    parser.add_argument("-f", help="filename", required=True)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    try:
        result = {}
        result["filename"] = args.f
        result["debug"] = args.debug
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
        self.video_path = args['filename']
        self.img_path = f'./screen_shots[{self.video_path}]'
        self.debugflag = args["debug"]
        self._error_code = args["error_code"]
        self.log_path = './Log/{datetime.datetime.now()}'

    # ====================================================================== #
    #  関数名: printLog
    # ---------------------------------------------------------------------- #
    #  説明: ログ
    # ====================================================================== #
    def printLog(self, level, message):
        with open(r"self.log_path", 'a') as f:
            f.write(f'[{level}] {message}\n')
        if self.debugflag:
            print(f'[{level}] {message}')

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
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            self.printLog("FATAL", f'[ NG ] File not found.')
            return

        os.makedirs(self.img_path, exist_ok=True)
        message = f'Created「{self.img_path}」directory.'
        self.printLog("INFO", f'[ OK ] {message}')

        base_path = os.path.join(self.img_path, basename)
        digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

        n = 0

        while True:
            ret, frame = cap.read()
            if ret:
                filename = f'{base_path}_{str(n).zfill(digit)}.{ext}'
                cv2.imwrite(filename, frame)
                message = f'Save "{filename}"'
                self.printLog("INFO", f'[ OK ] {message}')
                n += 1
            else:
                return

        # ログ作業後処理
        message = f'save_all_frames completed.'
        self.printLog("INFO", f'[ OK ] {message}')

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

  filename = args['filename']
  targetdir = f'./screen_shots[{filename}]'

  # 保存
  tool.save_all_frames()
  tool.countfiles()

if __name__ == "__main__":
    main()
