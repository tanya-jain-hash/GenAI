import whisper

model = whisper.load_model("turbo")
result = model.transcribe(r"C:\Users\Anoopkumarjain\Documents\git_reps\GenAI\bark_out.wav")
print(result["text"])