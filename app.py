from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os

from detect import detect_scam
from link_detector import detect_links
from database import create_table, save_report
from ocr import extract_text

from translator import (
    translate_text,
    detect_language,
    translate_analysis
)


app = Flask(__name__)


# ==========================================================
# UPLOAD SETTINGS
# ==========================================================

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================================
# CREATE DATABASE TABLE
# ==========================================================

create_table()


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
@app.route("/home")
@app.route("/home.html")
def home():

    return render_template(
        "home.html"
    )


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
@app.route("/dashboard.html")
def dashboard():

    return render_template(
        "dashboard.html"
    )


# ==========================================================
# CHECK SCAM MESSAGE
# ==========================================================

@app.route(
    "/check",
    methods=["POST"]
)
def check():

    # ======================================================
    # GET MESSAGE
    # ======================================================

    message = request.form.get(
        "message",
        ""
    ).strip()


    # ======================================================
    # GET TARGET LANGUAGE
    # ======================================================

    target_language = request.form.get(
        "target_language",
        ""
    ).strip()


    # ======================================================
    # GET SCREENSHOT
    # ======================================================

    screenshot = request.files.get(
        "screenshot"
    )


    # ======================================================
    # OCR FROM SCREENSHOT
    # ======================================================

    if screenshot and screenshot.filename:

        if not allowed_file(
            screenshot.filename
        ):

            return """
            <h1>Invalid file</h1>

            <p>
                Please upload a PNG, JPG, JPEG or WEBP image.
            </p>

            <br>

            <a href="/">
                Go Back
            </a>
            """


        try:

            filename = secure_filename(
                screenshot.filename
            )


            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )


            screenshot.save(
                image_path
            )


            print("================================")
            print("OCR SCREENSHOT DETECTION")
            print("Image:", filename)
            print("================================")


            # Extract text

            extracted_text = extract_text(
                image_path
            ).strip()


            print("OCR TEXT:")
            print(extracted_text)

            print("================================")


            # Delete image after OCR

            try:

                os.remove(
                    image_path
                )

            except:

                pass


            # No text found

            if not extracted_text:

                return """
                <h1>No text detected</h1>

                <p>
                    We could not read any text from
                    the uploaded screenshot.
                </p>

                <br>

                <a href="/">
                    Go Back
                </a>
                """


            # Use extracted text for AI detection

            message = extracted_text


        except Exception as e:

            print(
                "OCR ERROR:",
                e
            )


            return f"""
            <h1>OCR Error</h1>

            <p>{e}</p>

            <br>

            <a href="/">
                Go Back
            </a>
            """


    # ======================================================
    # EMPTY MESSAGE
    # ======================================================

    if not message:

        return redirect("/")


    # ======================================================
    # SCAM DETECTION
    # ======================================================

    print("================================")
    print("SCAM MESSAGE DETECTION")
    print("Message:", message)
    print("================================")


    try:

        result = detect_scam(
            message
        )


        print(
            "Detection result:",
            result
        )


        # ==================================================
        # TRANSLATE ANALYSIS
        # ==================================================

        translated = translate_analysis(
            result,
            target_language
        )


        print(
            "Translated analysis:",
            translated
        )


        # ==================================================
        # RESULT PAGE
        # ==================================================

        return render_template(

            "result.html",

            message=message,

            probability=result["probability"],
            risk=result["risk"],
            language=result["language"],
            status=result["status"],
            reasons=result["reasons"],
            tips=result["tips"],

            translated_probability=translated["probability"],
            translated_risk=translated["risk"],
            translated_language=translated["language"],
            translated_status=translated["status"],
            translated_reasons=translated["reasons"],
            translated_tips=translated["tips"],

            target_language=target_language
        )


    except Exception as e:

        print(
            "ERROR:",
            e
        )


        return f"""
        <h1>Something went wrong</h1>

        <p>{e}</p>

        <br>

        <a href="/">
            Go Back
        </a>
        """


# ==========================================================
# FAKE LINK DETECTION
# ==========================================================

@app.route(
    "/link-check",
    methods=["GET", "POST"]
)
@app.route(
    "/link_check.html",
    methods=["GET", "POST"]
)
def link_check():

    result = None

    category = ""

    source = ""

    link = ""


    # ======================================================
    # POST REQUEST
    # ======================================================

    if request.method == "POST":

        link = request.form.get(
            "link",
            ""
        ).strip()


        category = request.form.get(
            "category",
            ""
        ).strip()


        source = request.form.get(
            "source",
            ""
        ).strip()


        print("================================")
        print("FAKE LINK DETECTION")
        print("Link:", link)
        print("Category:", category)
        print("Source:", source)
        print("================================")


        if not link:

            return render_template(

                "link_check.html",

                result=None,

                category=category,

                source=source,

                link=link

            )


        try:

            result = detect_links(
                link
            )


            print(
                "Link detection result:",
                result
            )


        except Exception as e:

            print(
                "LINK ERROR:",
                e
            )


            return f"""
            <h1>Something went wrong</h1>

            <p>{e}</p>

            <br>

            <a href="/link-check">
                Go Back
            </a>
            """


    # ======================================================
    # SHOW LINK PAGE
    # ======================================================

    return render_template(

        "link_check.html",

        result=result,

        category=category,

        source=source,

        link=link

    )


# ==========================================================
# ABOUT
# ==========================================================

@app.route("/about")
@app.route("/about.html")
def about():

    return render_template(
        "about.html"
    )


# ==========================================================
# SCAM AWARENESS
# ==========================================================

@app.route("/awareness")
@app.route("/awareness.html")
def awareness():

    return render_template(
        "awareness.html"
    )


# ==========================================================
# CONTACT
# ==========================================================

@app.route("/contact")
@app.route("/contact.html")
def contact():

    return render_template(
        "contact.html"
    )


# ==========================================================
# PRIVACY
# ==========================================================

@app.route("/privacy")
@app.route("/privacy.html")
def privacy():

    return render_template(
        "privacy.html"
    )


# ==========================================================
# REPORT SCAM
# ==========================================================

@app.route(
    "/report",
    methods=["GET", "POST"]
)
@app.route(
    "/report.html",
    methods=["GET", "POST"]
)
def report():

    # ======================================================
    # SUBMIT REPORT
    # ======================================================

    if request.method == "POST":

        message = request.form.get(
            "message",
            ""
        ).strip()


        category = request.form.get(
            "category",
            ""
        ).strip()


        source = request.form.get(
            "source",
            ""
        ).strip()


        print("================================")
        print("SCAM REPORT")
        print("Message:", message)
        print("Category:", category)
        print("Source:", source)
        print("================================")


        # ==================================================
        # CHECK MESSAGE
        # ==================================================

        if not message:

            return redirect(
                "/report"
            )


        # ==================================================
        # SAVE REPORT
        # ==================================================

        try:

            save_report(
                message,
                category
            )


            print(
                "Report saved successfully!"
            )


            # ==================================================
            # SUCCESS PAGE
            # ==================================================

            return redirect(
                "/thankyou"
            )


        except Exception as e:

            print(
                "DATABASE ERROR:",
                e
            )


            return f"""
            <h1>Could not submit report</h1>

            <p>{e}</p>

            <br>

            <a href="/report">
                Go Back
            </a>
            """


    # ======================================================
    # REPORT PAGE
    # ======================================================

    return render_template(
        "report.html"
    )


# ==========================================================
# THANK YOU / SUCCESS PAGE
# ==========================================================

@app.route("/thankyou")
@app.route("/success.html")
def thankyou():

    return render_template(
        "success.html"
    )


@app.route("/translator", methods=["GET", "POST"])
@app.route("/translator.html", methods=["GET", "POST"])
def translator_page():

    text = ""
    detected_language = ""
    target_language = ""
    translated_text = ""
    analysis = None

    analysis_labels = {
        "scam_probability": "Scam Probability",
        "risk_level": "Risk Level",
        "status": "Status",
        "reasons": "Reasons",
        "safety_tips": "Safety Tips"
    }

    if request.method == "POST":

        text = request.form.get(
            "text",
            ""
        ).strip()

        target_language = request.form.get(
            "target_language",
            ""
        ).strip()

        if not text:
            return render_template(
                "translator.html",
                text="",
                detected_language="",
                target_language=target_language,
                translated_text="",
                analysis=None,
                analysis_labels=analysis_labels
            )

        # ==============================
        # DETECT LANGUAGE
        # ==============================

        detected_language = detect_language(
            text
        )

        print("================================")
        print("TRANSLATOR")
        print("Original Text:", text)
        print("Detected Language:", detected_language)
        print("Target Language:", target_language)
        print("================================")

        # ==============================
        # TRANSLATE MESSAGE
        # ==============================

        translated_text = translate_text(
            text,
            target_language
        )

        # ==============================
        # SCAM ANALYSIS
        # ==============================

        try:

            result = detect_scam(
                text
            )

            print(
                "Scam Analysis:",
                result
            )

            # ==============================
            # TRANSLATE ANALYSIS
            # ==============================

            analysis = translate_analysis(
                result,
                target_language
            )

            # Keep probability numeric
            analysis["probability"] = result["probability"]

            # ==============================
            # TRANSLATE LABELS
            # ==============================

            if target_language == "Hindi":

                analysis_labels = {
                    "scam_probability": "स्कैम संभावना",
                    "risk_level": "जोखिम स्तर",
                    "status": "स्थिति",
                    "reasons": "कारण",
                    "safety_tips": "सुरक्षा सुझाव"
                }

            elif target_language == "Marathi":

                analysis_labels = {
                    "scam_probability": "स्कॅम संभाव्यता",
                    "risk_level": "जोखीम पातळी",
                    "status": "स्थिती",
                    "reasons": "कारणे",
                    "safety_tips": "सुरक्षा टिप्स"
                }

            print("================================")
            print("Translation completed")
            print(
                "Translated Text:",
                translated_text
            )
            print(
                "Translated Analysis:",
                analysis
            )
            print("================================")

        except Exception as e:

            print(
                "TRANSLATOR ERROR:",
                e
            )

            analysis = None

    return render_template(

        "translator.html",

        text=text,

        detected_language=detected_language,

        target_language=target_language,

        translated_text=translated_text,

        analysis=analysis,

        analysis_labels=analysis_labels

    )
# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )