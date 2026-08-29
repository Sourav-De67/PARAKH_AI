from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Folder where uploaded product images will be stored
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Home page
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )

# Scan product
@app.route("/scan", methods=["POST"])
def scan():

    # Get uploaded image
    image = request.files["product_image"]

    # Make sure an image was selected
    if image.filename == "":
        return "No image selected!"

    # Save image inside uploads folder
    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image.filename
    )

    image.save(image_path)

    # Show result page
    return render_template("result.html", image_filename=image.filename)


# Start Flask server
if __name__ == "__main__":
    app.run(debug=True)