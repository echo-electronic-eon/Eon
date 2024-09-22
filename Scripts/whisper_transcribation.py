import whisper
import torch
import os

device = "cuda" if torch.cuda.is_available() else "cpu"

# Загрузка модели whisper-large-v3
whisper_model = whisper.load_model("large-v3").to(device)

def transcribe(video_file, language, beam_size, patience, initial_prompt):
    result = whisper_model.transcribe(
        video_file,
        language=language,
        beam_size=beam_size,
        patience=patience,
        initial_prompt=initial_prompt
    )
    return result["segments"]

def create_txt(segments, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for segment in segments:
            f.write(f"{segment['text']}\n")

def process_video_file(video_file_path, language, beam_size, patience, initial_prompt):
    try:
        print(f"Processing video file: {video_file_path}")

        transcribed_segments = transcribe(video_file_path, language=language, beam_size=beam_size,
                                          patience=patience, initial_prompt=initial_prompt)

        # Сохраняем транскрибацию в TXT файл
        transcription_txt = os.path.splitext(video_file_path)[0] + '_transcription.txt'
        create_txt(transcribed_segments, transcription_txt)

        print(f"TXT file created successfully: {transcription_txt}")

    except Exception as e:
        print(f"Error processing {video_file_path}: {str(e)}")

if __name__ == "__main__":
    video_file = "path/to/video.mp4"  # Укажите путь к вашему видеофайлу

    # Задаем параметры здесь
    language = "en"  # Укажите язык транскрипции, например, 'en' для английского
    beam_size = 5
    patience = 5
    initial_prompt = "Transcription of the video in English."

    process_video_file(video_file, language=language, beam_size=beam_size, patience=patience, initial_prompt=initial_prompt)
