import os
import tempfile

def videoSummarizer(video_path):
    """
    Extract audio from video, convert to text, and generate summary
    Returns both summary and transcript
    """
    audio_path = None
    try:
        # Test all imports first
        import torch
        from moviepy.editor import VideoFileClip
        import speech_recognition as sr
        from transformers import pipeline
        
        print("✓ All imports successful")
        print(f"Processing video: {video_path}")
        
        # Extract audio from video
        print("Extracting audio from video...")
        video_clip = VideoFileClip(video_path)
        
        # Create temporary audio file
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, "temp_audio.wav")
        
        video_clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
        video_clip.close()
        
        # Convert audio to text
        print("Converting audio to text...")
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(audio_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_data)
        
        print(f"Transcript length: {len(transcript)} characters")
        
        # Generate summary
        print("Generating summary...")
        
        # Use a smaller model for faster processing
        summarizer = pipeline(
            "summarization", 
            model="facebook/bart-large-cnn"
        )
        
        # Handle long transcripts
        if len(transcript) > 1024:
            # Split into chunks
            chunks = [transcript[i:i+1024] for i in range(0, len(transcript), 1024)]
            summaries = []
            for chunk in chunks[:3]:  # Limit to first 3 chunks to avoid timeout
                summary_chunk = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
                summaries.append(summary_chunk[0]['summary_text'])
            summary = " ".join(summaries)
        else:
            summary_result = summarizer(transcript, max_length=150, min_length=30, do_sample=False)
            summary = summary_result[0]['summary_text']
        
        return {
            'summary': summary,
            'transcript': transcript
        }
        
    except Exception as e:
        print(f"Error in video summarization: {e}")
        return {
            'summary': f"Processing error: {str(e)}",
            'transcript': f"Could not process audio: {str(e)}"
        }
    finally:
        # Clean up audio file
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except:
                pass