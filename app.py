from moviepy.editor import *
from pathlib import Path
from pymediainfo import MediaInfo


Path("videos").mkdir(parents=True, exist_ok=True)
Path("edited_videos").mkdir(parents=True, exist_ok=True)


def file_():
    """Chcek if video file exist's and check the file type"""
    file_path = Path("videos")
    file_list = []

    try:
        if file_path.is_dir():
            for file in file_path.iterdir():
                if file.is_file():
                    file_list.append(file.name)
                
                    media_info = MediaInfo.parse(file)
                    for track in media_info.tracks:
                        if track.track_type == "Video":
                            print("Format: {t.format}".format(t=track))
                    make_()
                
            if not file_list:
                print(f"Sorry, the directory {file_path} is empty.")
            else:
                print(f"Files in {file_path}:", file_list)
        else:
            print(f"'{file_path}' is not a valid directory.")

    except Exception as e:
        print(f"erro accesing file: {e}")

def make_():
    """getting a clip you want to edit and cut into smaller piece's
    if video duration is 1 hour, cut into 5 pices
    so it will be number of videos you want divided by duration of video
    """
    file_path = Path("videos")
    make_path = Path("edited_videos")

    if file_path.is_dir():
        for file in file_path.iterdir():
            if file.is_file():
                try:
                    clip = VideoFileClip(str(file_path / file.name))

                    if file.suffix.lower() not in ['.mp4', '.mkv', '.avi', '.mov']:
                        print(f"Skipping non-video file: {file}")
                        return
                    
                    parts = 3
                    duration = clip.duration
                    part_duration = duration / parts

                    for i in range(parts):
                        start_time = i * part_duration
                        end_time = (i + 1) * part_duration

                        if end_time > duration:
                            end_time = duration

                        new_clip = clip.subclip(start_time, end_time)
                        output_file = make_path / f"Part-{i + 1}-{file.stem}{file.suffix}"

                        new_clip.write_videofile(str(output_file),
                                                codec="libx264", 
                                                audio_codec="aac",
                                                temp_audiofile=f"{output_file.stem}_temp_audio.m4a",
                                                remove_temp=True
                                                )
                        print(f"Saved: {output_file}")

                except FileNotFoundError as e:
                    print(f"File Not Found: {e}")

                except Exception as e:
                    print(f"An errro occoured while editing the video file: {e}")
                # clip = VideoFileClip(str(file_path / file.name))
                # duration = clip.duration
                # print(f"Duration: {duration:.2f} seconds")

if __name__ == "__main__":
    file_()
