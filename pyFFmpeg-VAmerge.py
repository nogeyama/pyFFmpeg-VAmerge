# -*- coding: utf-8 -*-
# 2023.3.21 pyFFmpeg-VAmerge.py
#
#【プログラムの概要】
# このプログラムは、現在のディレクトリ内の指定された条件に一致する動画ファイル（mp4またはwebm拡張子を持ち、「 - DASH_V」という文字列が含まれるファイル）を検索し、
# それらの映像ファイルと音声ファイルを結合して、新しいmp4ファイルを出力するffmpegコマンドを実行します。
# また、このプログラムはログファイルに処理の進捗状況を記録します。


import os
import datetime

# 現在日時を取得し、ログファイル名に使用する
now = datetime.datetime.now()
log_filename = f"{now:%Y%m%d-%H%M%S}-FFmpeg-VAmerge.log"

# ログファイルを開く
with open(log_filename, "a", encoding="utf-8") as log_file:
    search_dir = os.getcwd()  # カレントディレクトリを検索対象にする

    for filename in os.listdir(search_dir):
        # 拡張子がmp4かwebmで、" - DASH_V"が含まれるファイルを検索する
        if (filename.endswith(".mp4") or filename.endswith(".webm")) and " - DASH_V" in filename:
            video_file = filename  # 映像ファイル名
            audio_file = filename.replace(" - DASH_V", " - DASH_A")  # 音声ファイル名
            output_file = filename[:filename.index(" - DASH_V")] + ".mp4"  # 出力ファイル名

            if os.path.exists(output_file):
                print("- SKIP!, output file is exist. ", output_file, )
                continue

            print("- input file_V : ", video_file)
            print("- input file_A : ", audio_file)
            print("- output file  : ", output_file)

            # ffmpegコマンドで映像ファイルと音声ファイルを結合する
            command = f"ffmpeg -i \"{video_file}\" -i \"{audio_file}\" -c copy \"{output_file}\""

            # コマンドをログファイルに出力
            log_file.write(f"{datetime.datetime.now()} - コマンド： {command}\n")

            # コマンドを実行
            os.system(command)

            # 出力ファイルが存在するかどうかを確認して、ログに記録する
            if os.path.exists(output_file):
                log_file.write(f"{datetime.datetime.now()} - 処理成功： {video_file}と{audio_file}を結合して{output_file}に出力しました。\n")
                print(f"{video_file}と{audio_file}を結合して{output_file}に出力しました。")
            else:
                log_file.write(f"{datetime.datetime.now()} - 処理失敗： {video_file}と{audio_file}の結合に失敗しました。\n")
                print(f"エラー：{video_file}と{audio_file}の結合に失敗しました。")

                # "_V"に対する"_A"が存在しない場合には、エラー内容をログファイルに出力する
                if not os.path.exists(audio_file):
                    error_message = f"{datetime.datetime.now()} - エラー：{filename}に対応する音声ファイルが見つかりませんでした。"
                    log_file.write(f"{error_message}\n")
                    print(error_message)

    # ログファイルを閉じる
    log_file.close()
    
quit()
