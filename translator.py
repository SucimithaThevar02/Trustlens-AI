from deep_translator import GoogleTranslator
from langdetect import detect


# ==========================================
# DETECT LANGUAGE
# ==========================================

def detect_language(text):

    try:

        language = detect(text)

        # Convert langdetect codes
        # into our project languages

        if language == "en":
            return "English"

        elif language == "hi":
            return "Hindi"

        elif language == "mr":
            return "Marathi"

        else:
            return "Other"

    except:

        return "Unknown"


# ==========================================
# TRANSLATE TEXT
# ==========================================

def translate_text(text, target_language):

    # Target language codes
    # used by GoogleTranslator

    language_codes = {

        "English": "en",

        "Hindi": "hi",

        "Marathi": "mr"

    }

    target_code = language_codes.get(
        target_language
    )

    if not target_code:

        return text

    # Nothing to translate

    if not text:

        return text

    try:

        translated = GoogleTranslator(
            source="auto",
            target=target_code
        ).translate(text)

        return translated

    except Exception as e:

        print(
            "TRANSLATION ERROR:",
            e
        )

        # If translation fails,
        # keep original text

        return text


# ==========================================
# TRANSLATE LIST
# ==========================================

def translate_list(items, target_language):

    translated_items = []

    for item in items:

        translated_items.append(
            translate_text(
                item,
                target_language
            )
        )

    return translated_items


# ==========================================
# TRANSLATE ANALYSIS RESULT
# ==========================================

def translate_analysis(
    result,
    target_language
):

    translated_result = result.copy()

    # Translate risk

    translated_result["risk"] = translate_text(
        result["risk"],
        target_language
    )

    # Translate status

    translated_result["status"] = translate_text(
        result["status"],
        target_language
    )

    # Translate detected language

    translated_result["language"] = translate_text(
        result["language"],
        target_language
    )

    # Translate reasons

    translated_result["reasons"] = translate_list(
        result["reasons"],
        target_language
    )

    # Translate safety tips

    translated_result["tips"] = translate_list(
        result["tips"],
        target_language
    )

    return translated_result