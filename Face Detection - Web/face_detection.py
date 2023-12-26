# Import library yang dibutuhkan
from flask import Flask, render_template, Response
import cv2

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Inisialisasi objek deteksi wajah OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Fungsi untuk melakukan deteksi wajah pada frame
def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return frame

# Fungsi untuk mengambil frame dari kamera
def generate_frames():
    cap = cv2.VideoCapture(0)  # Ganti angka 0 dengan alamat IP kamera jika menggunakan kamera eksternal

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = detect_faces(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk streaming video dengan deteksi wajah
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Jalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)
