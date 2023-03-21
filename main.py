import pytube
import os
import threading

# paste the URL of the YouTube playlist here
playlist_url = "PASTE_YOUR_PLAYLIST_URL_HERE"

# create a YouTube playlist object
playlist = pytube.Playlist(playlist_url)

# set the download directory
download_dir = "DOWNLOAD_DIRECTORY"

# create the download directory if it doesn't exist
if not os.path.exists(download_dir):
    os.mkdir(download_dir)

# get the preferred video quality from the user
preferred_quality = input("Enter the preferred video quality (e.g. 720p, 1080p, etc.): ")

# define a function to download a single video
def download_video(video, index):
    try:
        # get the stream with the preferred video quality
        stream = video.streams.filter(res=preferred_quality).first()
        if not stream:
            # if the preferred quality is not available, use the highest resolution stream
            stream = video.streams.get_highest_resolution()

        # download the video
        print(f"Downloading [{index}/{len(playlist)}]: {video.title}")
        progress = 0
        while progress < 100:
            progress = stream.download(output_path=download_dir, filename_prefix="temp", progress_callback=print_progress)
        # rename the downloaded file to the correct title
        os.rename(os.path.join(download_dir, "temp.mp4"), os.path.join(download_dir, f"{index}. {video.title}.mp4"))
        print(f"Download completed: {video.title}")
    except Exception as e:
        print(f"Error downloading {video.title}: {e}")

# define a function to show the progress of a video download
def print_progress(chunk, file_handle, bytes_remaining):
    total_bytes = stream.filesize
    bytes_downloaded = total_bytes - bytes_remaining
    progress = round(bytes_downloaded / total_bytes * 100)
    print(f"  [{progress}%] downloaded...", end="\r")

# create a list of threads to download each video
threads = []
for index, video in enumerate(playlist.videos, start=1):
    thread = threading.Thread(target=download_video, args=(video, index))
    threads.append(thread)

# start the threads
for thread in threads:
    thread.start()

# wait for all threads to complete
for thread in threads:
    thread.join()

print("All videos downloaded!")
