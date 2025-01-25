from flask import Flask, render_template, request, send_file
import yt_dlp as yt
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        quality = request.form.get("quality")

        if not url:
            return "Please enter a valid YouTube URL.", 400

        try:
            quality = int(quality) if quality else 720
            if quality < 144:
                quality = 720

            ydl_opts = {
                'format': f'best[height<={quality}]',
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'ignoreerrors': True,
            }

            with yt.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                file_path = ydl.prepare_filename(info)
                ydl.download([url])

                if os.path.exists(file_path):
                    return send_file(file_path, as_attachment=True)
                else:
                    return "Failed to download the video. Please try again.", 500

        except Exception as e:
            return f"An error occurred: {str(e)}", 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
