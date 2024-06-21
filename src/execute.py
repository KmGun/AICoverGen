import os
import sys

from main import voice_change, find_full_path

if __name__ == "__main__":
    input_song_titles_str = sys.argv[1]  # 첫 번째 인자
    input_song_titles = input_song_titles_str.split(",")
    voice_model = sys.argv[2]  # 두 번째 인자
    isMan = sys.argv[3].lower() == "true"  # 세 번째 인자
    pitch_values_str = sys.argv[4]
    pitch_values = list(map(int, pitch_values_str.split(",")))
    pitch_control = sys.argv[5].lower() == "true"
    print(
        "Received arguments",
        input_song_titles,
        voice_model,
        isMan,
        pitch_values,
        pitch_control,
    )

for song_title in input_song_titles:
    input_paths = find_full_path(song_title, isMan)
    if not os.path.exists(f"/content/drive/MyDrive/infer/{song_title}"):
        os.mkdir(f"/content/drive/MyDrive/infer/{song_title}")
    for index, input_path in enumerate(input_paths):
        if pitch_control:
            pitch_value = pitch_values[index]
        else:
            pitch_value = 0
        file_name = os.path.basename(input_path)
        output_path = f"/content/drive/MyDrive/infer/{song_title}/{file_name}.mp3"
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
