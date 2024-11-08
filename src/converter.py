import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from .config import SUPPORTED_EXTENSIONS, OUTPUT_BITRATE, MAX_WORKERS

def convert_file(file_path, input_dir, output_dir):
    relative_path = os.path.relpath(file_path, input_dir)
    output_path = os.path.join(output_dir, os.path.splitext(relative_path)[0] + ".mp3")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    command = ["ffmpeg", "-i", file_path, "-b:a", OUTPUT_BITRATE, "-y", output_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    return relative_path  # 成功したファイルの相対パスを返す

def convert_files(input_dir, output_dir, progress_callback, log_callback):
    files = [
        os.path.join(root, filename)
        for root, _, filenames in os.walk(input_dir)
        for filename in filenames if any(filename.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS)
    ]

    if not files:
        log_callback("対象のファイルが見つかりませんでした。")
        return

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(convert_file, file, input_dir, output_dir): file for file in files}

        for i, future in enumerate(as_completed(futures)):
            try:
                relative_path = future.result()
                log_callback(f"{relative_path} の変換が完了しました。")
            except subprocess.CalledProcessError:
                log_callback(f"{os.path.relpath(futures[future], input_dir)} の変換中にエラーが発生しました。")

            progress_callback((i + 1) / len(files))

    log_callback("全てのファイルの変換が完了しました。")
