import os
import sys
from moviepy.editor import VideoFileClip

def split_video_equally(video_path):
    """
    Splits a video file into two equal parts and saves them in a new directory.

    Args:
        video_path (str): The full path to the input video file.
    """
    # 1. Path and Naming Setup
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at '{video_path}'")
        return

    base_name = os.path.basename(video_path)
    file_name_no_ext, file_ext = os.path.splitext(base_name)
    
    # Create the output directory next to the input video
    # Directory name will be based on the video name + '_split'
    output_dir = os.path.join(os.path.dirname(video_path), f"{file_name_no_ext}_split")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Define output file paths
    output_path_1 = os.path.join(output_dir, f"{file_name_no_ext}_part1{file_ext}")
    output_path_2 = os.path.join(output_dir, f"{file_name_no_ext}_part2{file_ext}")

    print(f"Processing video: {base_name}")
    print("-" * 30)

    try:
        # 2. Load the video clip
        clip = VideoFileClip(video_path)
        duration = clip.duration
        midpoint = duration / 2

        print(f"Total Duration: {duration:.2f} seconds")
        print(f"Split Point: {midpoint:.2f} seconds (Midpoint)")

        # 3. Extract Part 1 (Start to Midpoint)
        clip_part_1 = clip.subclip(0, midpoint)
        
        # 4. Extract Part 2 (Midpoint to End)
        clip_part_2 = clip.subclip(midpoint, duration)

        # 5. Save the clips
        print(f"1/2: Writing Part 1 to {os.path.basename(output_path_1)}...")
        
        # Use a common high-quality codec like 'libx264' and 'aac' for maximum compatibility and quality.
        # MoviePy's defaults often preserve quality well.
        clip_part_1.write_videofile(
            output_path_1,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None # Suppresses detailed ffmpeg output
        )
        print("Part 1 saved successfully.")

        print(f"2/2: Writing Part 2 to {os.path.basename(output_path_2)}...")
        clip_part_2.write_videofile(
            output_path_2,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        print("Part 2 saved successfully.")
        
        # 6. Cleanup
        clip.close()
        print("-" * 30)
        print(f"Video splitting complete! Files saved in: {output_dir}")

    except Exception as e:
        print(f"\nAn unexpected error occurred during processing: {e}")
        print("Ensure the video file is not corrupt and moviepy/ffmpeg are installed correctly.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python video_splitter.py <video_file_path>")
        print("Example: python video_splitter.py /path/to/my_movie.mp4")
    else:
        input_video_path = sys.argv[1]
        split_video_equally(input_video_path)