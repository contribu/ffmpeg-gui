import os
import subprocess
from .config import SUPPORTED_EXTENSIONS, OUTPUT_BITRATE

def convert_files(input_dir, output_dir, progress_callback, log_callback):
    files = [
        os.path.join(root, filename)
        for root, _, filenames in os.walk(input_dir)
        for filename in filenames if any(filename.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS)
    ]

    total_files = len(files)
    if total_files == 0:
        log_callback("対象のファイルが見つかりませんでした。")
        return

    for i, file_path in enumerate(files):
        relative_path = os.path.relpath(file_path, input_dir)
        output_file_path = os.path.join(output_dir, os.path.splitext(relative_path)[0] + ".mp3")
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        log_callback(f"{relative_path} の変換を開始します。")

        try:
            command = [
                "ffmpeg", "-i", file_path, "-b:a", OUTPUT_BITRATE, "-y", output_file_path
            ]
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            log_callback(f"{relative_path} の変換が完了しました。")

        except subprocess.CalledProcessError as e:
            log_callback(f"{relative_path} の変換中にエラーが発生しました。")
            raise e  # 例外をGUI側でキャッチさせるために再度raise

        progress_callback((i + 1) / total_files)

    log_callback("全てのファイルの変換が完了しました。")
