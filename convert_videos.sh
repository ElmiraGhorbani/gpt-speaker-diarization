#!/bin/bash

# Directory containing the videos
video_dir="./resources/videos/"

# Loop through video files in the directory
for video_path in "${video_dir}"*; do
    # Check if the file is a video
    if [[ -f "${video_path}" && $(file -b --mime-type "${video_path}") == video/* ]]; then
        # Get the video file name without the extension
        video_name=$(basename "${video_path}")
        video_name_no_extension="${video_name%.*}"
        
        # Run ffmpeg command to convert the video to audio
        ffmpeg -i "${video_path}" -ar 16000 -ac 1 "./resourcesaudios/${video_name_no_extension}.mp3"
        
        echo "Converted ${video_name} to ${video_name_no_extension}.mp3"
    fi
done

echo "Conversion complete!"
