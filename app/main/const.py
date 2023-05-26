AUDIO_BASE_PATH = '/data/audio-core/'
#AUDIO_BASE_PATH = '/Users/conghaoyuan/data/audio-core/'
AUDIO_WAV_PATH = AUDIO_BASE_PATH + 'audio/'
AUDIO_TXT_PATH = AUDIO_BASE_PATH + 'txt/'

WHISPER_PATH = "/home/work/cpp/whisper.cpp/"
#WHISPER_PATH = "/Users/conghaoyuan/cpp/whisper.cpp/"
WHISPER_MODEL_PATH = WHISPER_PATH + "models/"
WHISPER_MODEL_BASE = "ggml-base.bin"
WHISPER_MODEL_SMALL = "ggml-small.bin"
WHISPER_MODEL_MEDIUM = "ggml-medium.bin"
WHISPER_MODEL_LARGE = "ggml-large.bin"
WHISPER_MODEL_MAP = {
    'base': WHISPER_MODEL_BASE,
    'small': WHISPER_MODEL_SMALL,
    'medium': WHISPER_MODEL_MEDIUM,
    'large': WHISPER_MODEL_LARGE,
}

WHISPER_LANG = {
    "en": "English",
    "ar": "Arabic",
    "hy": "Armenian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "zh": "Chinese",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "et": "Estonian",
    "tl": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "iw": "Hebrew",
    "hi": "Hindi",
    "hu": "Hungarian",
    "is": "Icelandic",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "kn": "Kannada",
    "ko": "Korean",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "mk": "Macedonian",
    "ms": "Malay",
    "mt": "Maltese",
    "no": "Norwegian",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sr": "Serbian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "es": "Spanish",
    "sw": "Swahili",
    "sv": "Swedish",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "yi": "Yiddish",
}
