# C:\Users\paul\AppData\Local\Programs\Python\Python35\Scripts\pip3.exe install Pillow-3.1.0-cp35-none-win_amd64.whl
from PIL import Image


image = Image.open("img\player_on.png")
for i in range(0,36):
	imRotate = image.rotate(-i*10)
	filename = "temp\on\player_on" + str(i*10) + ".png"
	imRotate.save(filename)
	print(i)
	
	
image2 = Image.open("img\player_off.png")
for i in range(0,36):
	imRotate = image2.rotate(-i*10)
	filename = "temp\off\player_off" + str(i*10) + ".png"
	imRotate.save(filename)
	print(i)

