import os
import sys
import re
import json
import sox

from main import voice_change, find_full_path


# 파일 경로에서 1_,2_ 를 추출하는 함수
def extract_number(file_path):
    # 파일명 추출
    file_name = os.path.basename(file_path)
    # 파일명에서 숫자 추출
    match = re.match(r"(\d+)_", file_name)
    return int(match.group(1)) if match else float("inf")


def change_pitch_sox(input_filepath, output_filepath, semitones):
    tfm = sox.Transformer()
    tfm.pitch(semitones)
    tfm.build(input_filepath, output_filepath)


def process_mp3_files(input_directory, output_directory, semitones):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith("_mr.mp3"):
            input_filepath = os.path.join(input_directory, filename)
            output_filepath = os.path.join(output_directory, filename)
            change_pitch_sox(input_filepath, output_filepath, semitones)
            print(f"{filename}의 피치가 {semitones} 반음만큼 변경되었습니다.")


if __name__ == "__main__":
    song_datas_str = sys.argv[1]  # 첫 번째 인자
    song_datas = json.loads(song_datas_str)
    print(song_datas)

for song_data in song_datas:
    song_title = song_data["song_title"]
    voice_model = song_data["voice_model"]
    pitch_value = song_data["pitch_value"]
    isMan = song_data["isMan"]

    input_paths = find_full_path(song_title, isMan)
    # 파일 경로를 숫자에 따라 정렬
    sorted_input_paths = sorted(input_paths, key=extract_number)
    # 폴더 생성
    ## 보이스 모델 폴더
    if not os.path.exists(f"/content/drive/MyDrive/infer/{voice_model}"):
        os.mkdir(f"/content/drive/MyDrive/infer/{voice_model}")
    ## 추론 폴더
    os.mkdir(f"/content/drive/MyDrive/infer/{voice_model}/[{pitch_value}]{song_title}")

    for input_path in sorted_input_paths:
        file_name = os.path.basename(input_path)
        output_path = f"/content/drive/MyDrive/infer/{voice_model}/[{pitch_value}]{song_title}/{file_name}.mp3"
        voice_change(
            voice_model,
            input_path,
            output_path,
            pitch_value,
            f0_method="rmvpe",
            index_rate=0.66,
            filter_radius=3,
            rms_mix_rate=0.25,
            protect=0.33,
            crepe_hop_length=128,
            is_webui=0,
        )
        # 원키가 아닐경우, mr 처리
        if pitch_value != 0:
            mr_input_path = os.path.dirname(input_path)
            mr_output_path = f"/content/drive/MyDrive/infer/{voice_model}/[{pitch_value}]{song_title}/mr"
            process_mp3_files(mr_input_path, mr_output_path, pitch_value)


# for song_title in input_song_titles:
#     input_paths = find_full_path(song_title, isMan)
#     # 파일 경로를 숫자에 따라 정렬
#     sorted_input_paths = sorted(input_paths, key=extract_number)
#     if not os.path.exists(f"/content/drive/MyDrive/infer/{song_title}"):
#         os.mkdir(f"/content/drive/MyDrive/infer/{song_title}")
#     for index, input_path in enumerate(sorted_input_paths):
#         if pitch_control:
#             pitch_value = pitch_values[index]
#             print(pitch_value)
#         else:
#             pitch_value = 0
#         file_name = os.path.basename(input_path)
#         output_path = f"/content/drive/MyDrive/infer/{song_title}/{file_name}.mp3"
#         voice_change(
#             voice_model,
#             input_path,
#             output_path,
#             pitch_value,
#             f0_method="rmvpe",
#             index_rate=0.66,
#             filter_radius=3,
#             rms_mix_rate=0.25,
#             protect=0.33,
#             crepe_hop_length=128,
#             is_webui=0,
#         )
