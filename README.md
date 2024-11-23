pip install psycopg2-binary

apt-get update
apt-get install python3-dev libpq-dev build-essential clang

apt install -y ffmpeg
apt-get install tesseract-ocr
apt-get install libtesseract-dev
apt-get install -y tesseract-ocr


#Remove the existing packages:
pip uninstall flask werkzeug


#Reinstall with the correct versions:
pip install -r requirements.txt