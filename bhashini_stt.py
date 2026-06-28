"""
AwaazBank — Bhashini STT + TTS Integration
Uses India's sovereign NLP platform for speech-to-text and text-to-speech
in 10+ Indian languages.
"""

import requests
import base64
import os
from langdetect import detect

BHASHINI_API_KEY = os.getenv("BHASHINI_API_KEY", "")
BHASHINI_BASE_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

LANGUAGE_CODES = {
    "hi": "Hindi",
    "mr": "Marathi",
    "bn": "Bengali",
    "or": "Odia",
    "pa": "Punjabi",
    "gu": "Gujarati",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "bh": "Bhojpuri",
}


def audio_to_text(audio_base64: str, source_language: str = "hi") -> dict:
    """
    Convert WhatsApp voice note (base64 audio) to text using Bhashini STT.
    Returns: { "text": str, "language": str, "confidence": float }
    """
    payload = {
        "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {"sourceLanguage": source_language},
                    "serviceId": "ai4bharat/conformer-hi-gpu--t4",
                    "audioFormat": "ogg",
                    "samplingRate": 16000,
                }
            }
        ],
        "inputData": {
            "audio": [{"audioContent": audio_base64}]
        }
    }

    headers = {
        "Authorization": BHASHINI_API_KEY,
        "Content-Type": "application/json",
    }

    # TODO: Uncomment when API key is available
    # response = requests.post(BHASHINI_BASE_URL, json=payload, headers=headers)
    # result = response.json()
    # transcribed_text = result["pipelineResponse"][0]["output"][0]["source"]

    # Stub for demo
    transcribed_text = "Mujhe SBI mein khata kholna hai"

    return {
        "text": transcribed_text,
        "language": source_language,
        "confidence": 0.94,
    }


def text_to_audio(text: str, target_language: str = "hi") -> str:
    """
    Convert text to speech using Bhashini TTS.
    Returns: base64-encoded audio string (ogg format for WhatsApp).
    """
    payload = {
        "pipelineTasks": [
            {
                "taskType": "tts",
                "config": {
                    "language": {"sourceLanguage": target_language},
                    "serviceId": "ai4bharat/indic-tts-coqui-hi-gpu--t4",
                    "gender": "female",
                }
            }
        ],
        "inputData": {
            "input": [{"source": text}]
        }
    }

    headers = {
        "Authorization": BHASHINI_API_KEY,
        "Content-Type": "application/json",
    }

    # TODO: Uncomment when API key is available
    # response = requests.post(BHASHINI_BASE_URL, json=payload, headers=headers)
    # audio_base64 = response.json()["pipelineResponse"][0]["audio"][0]["audioContent"]
    # return audio_base64

    # Stub for demo
    return base64.b64encode(b"[audio stub]").decode()


def detect_language(text: str) -> str:
    """
    Detect language of transcribed text.
    Returns ISO 639-1 language code.
    """
    try:
        detected = detect(text)
        return detected if detected in LANGUAGE_CODES else "hi"
    except Exception:
        return "hi"  # Default to Hindi


if __name__ == "__main__":
    # Quick test
    sample_audio = base64.b64encode(b"[fake audio bytes]").decode()
    result = audio_to_text(sample_audio, source_language="hi")
    print("Transcribed:", result["text"])
    print("Language:", result["language"])

    audio_out = text_to_audio("Namaste! Aapka account kholne mein main aapki madad karunga.", "hi")
    print("TTS output (base64 length):", len(audio_out))
