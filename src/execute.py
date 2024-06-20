import os
import sys

from main import voice_change, find_full_path

if __name__ == "__main__":
    input_song_titles_str = sys.argv[1]  # 첫 번째 인자
    input_song_titles = input_song_titles_str.split(",")
    voice_model = sys.argv[2]  # 두 번째 인자
    isMan = sys.argv[3].lower() == "true"  # 세 번째 인자
    print("Received arguments", input_song_titles, voice_model, isMan)

for song_title in input_song_titles:
    input_paths = find_full_path(song_title, isMan)
    if not os.path.exists(f"/content/drive/MyDrive/infer/{song_title}"):
        os.mkdir(f"/content/drive/MyDrive/infer/{song_title}")
    for input_path in input_paths:
        file_name = os.path.basename(input_path)
        output_path = f"/content/drive/MyDrive/infer/{song_title}/{file_name}.mp3"
        voice_change(
            voice_model,
            input_path,
            output_path,
            pitch_change=0,
            f0_method="rmvpe",
            index_rate=0.66,
            filter_radius=3,
            rms_mix_rate=0.25,
            protect=0.33,
            crepe_hop_length=128,
            is_webui=0,
        )
