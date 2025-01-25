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
        quality = int(request.form.get("quality", 720))

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

        return send_file(file_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)