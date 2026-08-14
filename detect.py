# ==========================================
# TrustLens AI
# AI-Based Multilingual Scam Detection
# English + Hindi + Marathi
# ==========================================

import joblib
from langdetect import detect


# ==========================================
# LOAD MULTILINGUAL MODELS
# ==========================================

models = joblib.load(
    "model/multilingual_models.pkl"
)


# ==========================================
# SCAM DETECTION FUNCTION
# ==========================================

def detect_scam(message):

    # --------------------------------------
    # CLEAN MESSAGE
    # --------------------------------------

    message = str(message).strip()


    # --------------------------------------
    # LANGUAGE DETECTION
    # --------------------------------------

    try:

        if len(message) < 10:

            language_code = "unknown"

        else:

            language_code = detect(message)

    except:

        language_code = "unknown"


    # --------------------------------------
    # CONVERT LANGUAGE CODE
    # --------------------------------------

    if language_code == "en":

        language = "English"

        model_language = "en"


    elif language_code == "hi":

        language = "Hindi"

        model_language = "hi"


    elif language_code == "mr":

        language = "Marathi"

        model_language = "mr"


    else:

        # For unsupported languages,
        # use English model as fallback.

        language = language_code

        model_language = "en"


    # --------------------------------------
    # SELECT CORRECT AI MODEL
    # --------------------------------------

    model = models[model_language]


    # --------------------------------------
    # AI PREDICTION
    # --------------------------------------

    prediction = model.predict(
        [message]
    )[0]

    prediction = str(
        prediction
    ).lower()


    # --------------------------------------
    # GET SCAM PROBABILITY
    # --------------------------------------

    probability_values = model.predict_proba(
        [message]
    )[0]

    classes = model.classes_


    spam_probability = 0


    for i in range(len(classes)):

        if str(
            classes[i]
        ).lower() == "spam":

            spam_probability = (
                probability_values[i] * 100
            )


    probability = round(
        spam_probability,
        2
    )


    # --------------------------------------
    # STATUS
    # --------------------------------------

    if prediction == "spam":

        status = "Scam"

    else:

        status = "Safe"


    # --------------------------------------
    # RISK LEVEL
    # --------------------------------------

    if probability >= 80:

        risk = "High"

    elif probability >= 50:

        risk = "Medium"

    else:

        risk = "Low"


    # ======================================
    # DETECTION REASONS
    # ======================================

    reasons = []


    # English suspicious words

    suspicious_words_en = [

        "click",
        "prize",
        "winner",
        "otp",
        "password",
        "bank",
        "urgent",
        "money",
        "offer",
        "free",
        "link",
        "reward",
        "verify",
        "verification",
        "kyc",
        "upi",
        "refund",
        "blocked",
        "suspended",
        "account"

    ]


    # Hindi suspicious words

    suspicious_words_hi = [

        "बैंक",
        "खाता",
        "ओटीपी",
        "otp",
        "पासवर्ड",
        "इनाम",
        "पुरस्कार",
        "लिंक",
        "सत्यापित",
        "सत्यापन",
        "केवाईसी",
        "kyc",
        "यूपीआई",
        "upi",
        "रिफंड",
        "ब्लॉक",
        "बंद",
        "तुरंत",
        "कैशबैक"

    ]


    # Marathi suspicious words

    suspicious_words_mr = [

        "बँक",
        "खाते",
        "ओटीपी",
        "otp",
        "पासवर्ड",
        "बक्षीस",
        "इनाम",
        "लिंक",
        "सत्यापित",
        "सत्यापन",
        "केवायसी",
        "kyc",
        "यूपीआय",
        "upi",
        "परतावा",
        "ब्लॉक",
        "बंद",
        "त्वरित",
        "कॅशबॅक"

    ]


    # --------------------------------------
    # SELECT SUSPICIOUS WORDS
    # --------------------------------------

    if model_language == "hi":

        suspicious_words = (
            suspicious_words_hi
        )

    elif model_language == "mr":

        suspicious_words = (
            suspicious_words_mr
        )

    else:

        suspicious_words = (
            suspicious_words_en
        )


    # --------------------------------------
    # CHECK SUSPICIOUS WORDS
    # --------------------------------------

    for word in suspicious_words:

        if word.lower() in message.lower():

            reasons.append(

                "Suspicious word detected: "
                + word

            )


    # --------------------------------------
    # AI REASON
    # --------------------------------------

    if prediction == "spam":

        reasons.append(

            "AI model identified patterns "
            "similar to spam/scam messages."

        )


    # --------------------------------------
    # NO REASON FOUND
    # --------------------------------------

    if len(reasons) == 0:

        reasons.append(

            "No suspicious pattern detected."

        )


    # ======================================
    # SAFETY TIPS
    # ======================================

    tips = []


    if status == "Scam":

        tips.append(

            "Never share OTPs, passwords "
            "or banking details."

        )

        tips.append(

            "Do not click unknown or "
            "suspicious links."

        )

        tips.append(

            "Verify the sender before "
            "taking any action."

        )

        tips.append(

            "Report suspicious messages "
            "to the appropriate authority."

        )

    else:

        tips.append(

            "Message appears relatively safe "
            "based on the AI analysis."

        )

        tips.append(

            "Stay alert when dealing with "
            "unknown contacts."

        )

        tips.append(

            "Never share sensitive information "
            "through messages."

        )


    # ======================================
    # RETURN RESULT
    # ======================================

    return {

        "language": language,

        "probability": probability,

        "risk": risk,

        "status": status,

        "reasons": reasons,

        "tips": tips

    }


# ==========================================
# TESTING SECTION
# ==========================================

if __name__ == "__main__":

    message = input(
        "Enter message: "
    )


    result = detect_scam(
        message
    )


    print(
        "\n----- TrustLens AI Result -----"
    )


    print(
        "Language:",
        result["language"]
    )


    print(
        "Scam Probability:",
        result["probability"],
        "%"
    )


    print(
        "Risk Level:",
        result["risk"]
    )


    print(
        "Status:",
        result["status"]
    )


    print("\nReasons:")


    for reason in result["reasons"]:

        print(
            "-",
            reason
        )


    print("\nSafety Tips:")


    for tip in result["tips"]:

        print(
            "-",
            tip
        )