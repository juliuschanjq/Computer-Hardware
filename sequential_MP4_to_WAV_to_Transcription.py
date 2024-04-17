from moviepy.editor import VideoFileClip
import os
import time
import speech_recognition as sr

def convert_mp4_to_wav(input_file, output_file):
    video_clip = VideoFileClip(input_file)     # Load video clip and extract audio
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(output_file, codec='pcm_s16le', fps=44100)

    video_clip.close()

def transcribe_audio_to_text(audio_file):
    recognizer = sr.Recognizer()  

    with sr.AudioFile(audio_file) as source:     # Open the audio file and record the audio
        audio = recognizer.record(source)

    text = recognizer.recognize_google(audio)
    
    return text

def process_mp4_file(mp4_file, input_directory, output_directory):
    # Construct input and output file paths
    input_file = os.path.join(input_directory, mp4_file)
    output_file_wav = os.path.join(output_directory, os.path.splitext(mp4_file)[0] + ".wav")
    output_file_text = os.path.join(output_directory, os.path.splitext(mp4_file)[0] + ".txt")

    # Display information about the processing of the current video file
    print(f"Processing video file: {mp4_file}")

    # Convert MP4 to WAV
    start_time_convert = time.time()
    convert_mp4_to_wav(input_file, output_file_wav)
    end_time_convert = time.time()
    elapsed_time_convert = end_time_convert - start_time_convert

    # Transcribe audio to text
    start_time_transcribe = time.time()
    text = transcribe_audio_to_text(output_file_wav)
    end_time_transcribe = time.time()
    elapsed_time_transcribe = end_time_transcribe - start_time_transcribe

    # Write transcribed text to file
    with open(output_file_text, 'w') as text_file:
        text_file.write(text)

    # Display the time taken for conversion and transcription
    print(f"MP4 to Audio Conversion Time: {elapsed_time_convert} seconds")
    print(f"Transcription Time: {elapsed_time_transcribe} seconds\n")

    return elapsed_time_convert, elapsed_time_transcribe

if __name__ == "__main__":
    input_directory = "C:\\Coventry University\\Computer Hardware\\CW2\\MP4 Video Samples"
    output_directory = "C:\\Coventry University\\Computer Hardware\\CW2\Sequential_Conversion_Results"
    
    mp4_files = [f for f in os.listdir(input_directory) if f.endswith(".mp4")]

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    num_clips = 6
    clip_counter = 0
    total_duration_convert = 0
    total_duration_transcribe = 0

    # Iterate through the MP4 files
    for mp4_file in mp4_files:
        if clip_counter >= num_clips:
            break

        convert_time, transcribe_time = process_mp4_file(mp4_file, input_directory, output_directory)
        total_duration_convert += convert_time
        total_duration_transcribe += transcribe_time
        clip_counter += 1

    # Display the total duration for the processed videos
    print(f"Total Audio Conversion Time for {clip_counter} video(s): {total_duration_convert} seconds")
    print(f"Total Transcription Time for {clip_counter} video(s): {total_duration_transcribe} seconds")