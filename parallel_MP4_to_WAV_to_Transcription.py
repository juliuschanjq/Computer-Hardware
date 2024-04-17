import multiprocessing
from moviepy.editor import VideoFileClip
import os
import time
import speech_recognition as sr

def convert_mp4_to_wav(input_file, output_file):
    video_clip = VideoFileClip(input_file)  # Load video clip and extract audio
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(output_file, codec='pcm_s16le', fps=44100, logger=None)

    video_clip.close()

def transcribe_audio_to_text(audio_file):
    recognizer = sr.Recognizer()  # Initialize speech recognizer

    with sr.AudioFile(audio_file) as source:  # Open the audio file and record the audio
        audio = recognizer.record(source)

    text = recognizer.recognize_google(audio)
    
    return text

def process_mp4_file(mp4_file, input_directory, output_directory):
    # Construct input and output file paths
    input_file = os.path.join(input_directory, mp4_file)
    output_file_wav = os.path.join(output_directory, os.path.splitext(mp4_file)[0] + ".wav")
    output_file_text = os.path.join(output_directory, os.path.splitext(mp4_file)[0] + ".txt")

    print(f"Processing video file: {mp4_file}")

    # Record the start time for conversion
    start_time_convert = time.time()

    convert_mp4_to_wav(input_file, output_file_wav)

    # Record the end time for conversion
    end_time_convert = time.time()
    elapsed_time_convert = end_time_convert - start_time_convert

    # Record the start time for transcription
    start_time_transcribe = time.time()

    # Transcribe audio to text
    text = transcribe_audio_to_text(output_file_wav)

    # Record the end time for transcription
    end_time_transcribe = time.time()
    elapsed_time_transcribe = end_time_transcribe - start_time_transcribe

    # Save the transcribed text to a file
    with open(output_file_text, 'w') as text_file:
        text_file.write(text)

    # Display the time taken for conversion and transcription
    print(f"MP4 to Audio Conversion Time: {elapsed_time_convert} seconds")
    print(f"Audio Transcription Time: {elapsed_time_transcribe} seconds\n")

    return elapsed_time_convert, elapsed_time_transcribe

def process_mp4_files_parallel(mp4_files, input_directory, output_directory):
    # Record the start time for the entire process
    start_time_process = time.time()

    with multiprocessing.Pool() as pool:
        results = pool.starmap(process_mp4_file, [(mp4_file, input_directory, output_directory) for mp4_file in mp4_files])

    # Record the end time for the entire process
    end_time_process = time.time()
    elapsed_time_process = end_time_process - start_time_process

    total_duration_convert = sum(result[0] for result in results)
    total_duration_transcribe = sum(result[1] for result in results)

    return total_duration_convert, total_duration_transcribe, elapsed_time_process

if __name__ == "__main__":
    input_directory = "C:\\Coventry University\\Computer Hardware\\CW2\\MP4 Video Samples"
    output_directory = "C:\\Coventry University\\Computer Hardware\\CW2\\Parallel_Conversion_Results"

    mp4_files = [f for f in os.listdir(input_directory) if f.endswith(".mp4")]

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process the video files in parallel using multiprocessing
    total_duration_convert, total_duration_transcribe, total_duration_process = process_mp4_files_parallel(mp4_files, input_directory, output_directory)

    # Display the total duration for the entire process
    print(f"Total Conversion Time for {len(mp4_files)} video(s): {total_duration_convert} seconds")
    print(f"Total Transcription Time for {len(mp4_files)} video(s): {total_duration_transcribe} seconds")
    print(f"Total Processing Time for {len(mp4_files)} video(s): {total_duration_process} seconds")