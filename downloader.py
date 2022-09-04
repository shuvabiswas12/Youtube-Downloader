import os
from traceback import print_tb
from typing import Any, Dict, Set
from pytube import YouTube
from pytube.query import StreamQuery
import moviepy.editor as mpe
import uuid
import flag
import datetime


class Downloader:
    def __init__(self, video_link: str) -> None:
        self.__youtube = YouTube(video_link)
        self.__video_info = dict()
        self.__video_file_name = None
        self.__audio_file_name = None
        self.video_streams = None
        self.audio_streams = None
        self.__cwd = os.getcwd()
        self.resolution = ['mp3']
        self.get_video_info()
        self.__set_streams()
        self.__set_video_resolutions(self.video_streams)

    def get_video_info(self) -> None:
        print("Getting video info:...", end="\t")
        self.__video_info["Title"] = self.__youtube.title.strip()
        self.__video_info["Video_id"] = self.__youtube.video_id
        self.__video_info["Thumbnail_url"] = self.__youtube.thumbnail_url
        print("Done!")

    def __set_streams(self) -> None:
        print(
            "Collecting Streams:... [It might take a while to complete!]", end="\t")
        self.video_streams = self.__youtube.streams.filter(
            only_video=True).order_by('resolution').desc()

        self.audio_streams = self.__youtube.streams.filter(
            only_audio=True).order_by('abr').desc()

        print("Done!")

    def __set_video_resolutions(self, video_streams: "StreamQuery") -> Set:
        for stream in video_streams:
            if stream.resolution in {'1080p', '720p', '360p', '480p'}:
                self.resolution.append(stream.resolution)
        self.resolution = list(set(self.resolution))

    def download(self, resolution: str):
        if resolution == "mp3":
            self.download_audio(self.audio_streams, audio_only=True)
            return
        else:
            self.download_audio(self.audio_streams)
            self.download_video(self.video_streams, resolution)
            self.__merge_and_save()
            return

    def download_video(self, videos: "StreamQuery", resolution: str):
        print("Downloading video:...", end="\t")
        self.__video_file_name = self.__video_info["Video_id"] + '.mp4'
        videos.filter(res=resolution).first().download(
            self.__cwd + "\Output", filename=self.__video_file_name)
        print("Done!")

    def download_audio(self, audios: "StreamQuery", audio_only=False):
        print("Downloading audio:...", end="\t")
        if audio_only:
            filename = self.temporary_filename() + '.mp3'
            self.__audio_file_name = filename

        else:
            self.__audio_file_name = self.__video_info["Video_id"] + '.mp3'

        audios.first().download(
            self.__cwd + "\Output", filename=self.__audio_file_name)
        print("Done!")

        if audio_only:
            self.rename(self.__audio_file_name)

    def __merge_and_save(self) -> None:
        print("Merging Started!")

        self.clip = mpe.VideoFileClip("./Output/" + self.__video_file_name)
        self.audio_bg = mpe.AudioFileClip("./Output/" + self.__audio_file_name)
        final_clip = self.clip.set_audio(self.audio_bg)
        temp_filename = self.temporary_filename() + ".mp4"
        final_clip.write_videofile("./Output/" + temp_filename)

        self.rename(temp_filename=temp_filename)
        print("Done!", end="\n\n")

        # deleting the video file which has no sound and delete the audio file as well
        os.remove('./Output/' + self.__video_file_name)
        os.remove('./Output/' + self.__audio_file_name)

    def temporary_filename(self) -> str:
        file_name = self.__video_info['Video_id'] + "_" + str(uuid.uuid4())
        return str(file_name).strip()

    def rename(self, temp_filename: str):
        title = str(self.__video_info['Title'])
        list_of_words = title.replace(',', '').replace(
            '|', '').replace('.', '_').replace('?', '').replace("*", "").replace("<", "").replace(">", "").replace(":", "").replace("/", "").replace("\\", "").replace("@", "").split()
        new_title = "_".join(list_of_words)

        src = "./Output/" + temp_filename

        ext = temp_filename.split(".")[-1]

        dest_filename = flag.dflagize(new_title).replace(
            ":", "") + "_" + str(datetime.datetime.now()).split(" ")[0]

        print(dest_filename)

        dest = "./Output/" + dest_filename + "." + ext

        os.rename(src, dest)
