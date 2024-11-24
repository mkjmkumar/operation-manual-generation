import subprocess
import os

def create_frames_directory():
    # Create a frames directory inside Tests if it doesn't exist
    frames_dir = os.path.join("Tests", "frames")
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    return frames_dir

def extract_frames(video_path, output_dir, fps=1):
    """
    Extract frames from video using ffmpeg
    Args:
        video_path: Path to input video file
        output_dir: Directory to save frames
        fps: Frames per second to extract (default: 1 frame per second)
    """
    try:
        # Construct the ffmpeg command
        ffmpeg_command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'fps={fps}',
            '-frame_pts', '1',
            '-f', 'image2',
            os.path.join(output_dir, 'frame_%d.jpg')
        ]
        
        # Execute the command
        subprocess.run(ffmpeg_command, check=True)
        print(f"Frames extracted successfully to {output_dir}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error extracting frames: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Define paths
    video_path = os.path.join("Tests", "EC2.mp4")
    frames_dir = create_frames_directory()
    
    # Check if video file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return
    
    # Extract frames
    extract_frames(video_path, frames_dir)
    
    # Print number of extracted frames
    frames_count = len([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
    print(f"Total frames extracted: {frames_count}")

if __name__ == "__main__":
    main() 