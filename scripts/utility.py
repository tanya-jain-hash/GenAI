import whisper
from crewai import LLM
import scipy
from transformers import AutoProcessor, BarkModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from templates import schema

processor = AutoProcessor.from_pretrained("suno/bark-small")
tts_model = BarkModel.from_pretrained("suno/bark-small")
stt_model = whisper.load_model("turbo")

model_path = 'gaussalgo/T5-LM-Large-text2sql-spider'
sql_model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

def convert_speech_to_text(file_path):
    result = stt_model.transcribe(file_path)
    return result["text"]

def load_model():
    llm = LLM(
    model="ollama/BahaSlama/llama3.1-finetuned:latest",
    base_url="http://localhost:11434"
)
    return llm


def convert_text_to_speech(text, file_name):
    voice_preset = "v2/en_speaker_6"
    inputs = processor(text, voice_preset=voice_preset)
    audio_array = tts_model.generate(**inputs)
    audio_array = audio_array.cpu().numpy().squeeze()
    sample_rate = tts_model.generation_config.sample_rate
    scipy.io.wavfile.write(f"{file_name}.wav", rate=sample_rate, data=audio_array)

def insert_to_db(question):
    input_text = " ".join(["Question: ",question, "Schema:", schema])

    model_inputs = tokenizer(input_text, return_tensors="pt")
    outputs = sql_model.generate(**model_inputs, max_length=512)
    output_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print(output_text)
