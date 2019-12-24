from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet,configure_uploads,ALL,DATA
import vlc
import pytesseract
from PIL import Image
import pyttsx3 as px
from gtts import gTTS
from googletrans import Translator


app=Flask(__name__)
Bootstrap(app)


files=UploadSet('imgupload',ALL)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/result',methods=['POST','GET'])
def imgupload():
	if request.method=='POST' and 'imgupload' in request.files:
		file=request.files['imgupload']
		x=file.filename
		img=Image.open(file)
		pytesseract.pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"
		result=pytesseract.image_to_string(img)
		p=Translator()
		k=p.translate(result,dest='spanish')
		with open('abc.txt',mode='w') as file:
			file.write(str(k))
		f=open('abc.txt','r')
		text_to_read=f.read()
		f.close()

		myobj=gTTS(text=text_to_read,lang='es',slow=False)
		myobj.save('translated.mp3')
		#os.system(f'start{translated.mp3}')
		player=vlc.MediaPlayer('C:/Users/Bhupesh/Desktop/Image to Speech/translated.mp3')
		player.play()
	return render_template('index.html',text=k)

if __name__ == '__main__':
	app.run(debug=True)