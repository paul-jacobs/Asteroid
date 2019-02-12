import tkinter
import os
from PIL import Image
import shutil
from threading import Thread
import time
import math
import random
import pygame
#to turn pictures 


global orientation,bgc,afgc,fgc,abgc,state_engine,accel_value,player_off_img,player_on_img,ship_selected_number,void,accel_value,weapon_speed_value,god_mod 

class Background_process(Thread):
	
	def __init__(self,canvas,player_item,player_on_img,player_off_img,orb_img,a0_img,fire_img,l_ax,l_ay,l_vx_weapon,l_vy_weapon,l_vx_asteroid,l_vy_asteroid,px,py,god_mod,score_label,life,heart_img,invisi_img,best_score):
		Thread.__init__(self)
		self.w, self.h = root.winfo_screenwidth(), root.winfo_screenheight()
		self.runt = True
		self.engine_state=False #True False
		self.rotation_command=""
		self.orientation=0 #0-35
		self.canvas=canvas
		self.player_item=player_item
		self.player_on_img=player_on_img
		self.player_off_img=player_off_img
		self.a0_img=a0_img
		self.fire_img=fire_img
		self.l_ax=l_ax
		self.l_ay=l_ay
		self.orb_img=orb_img
		self.orb=[[0 for i in range(0,3)] for j in range(0,5)]
		self.asteroid=[[0 for i in range(0,10)] for j in range(0,7)]
		self.time=0.028
		
		
		for i in range(0,3):	
			self.orb[0][i]=""
			self.orb[1][i]=-64
			self.orb[2][i]=-64
			self.orb[3][i]=0
			self.orb[4][i]=0
		
		
		for i in range(0,len(self.asteroid[0])):	
			self.asteroid[0][i]=""
			self.asteroid[1][i]=-64
			self.asteroid[2][i]=-64
			self.asteroid[3][i]=0
			self.asteroid[4][i]=0
		
		for i in range(0,5):
			print(self.orb[i])
		print("")
		self.l_vx_weapon=l_vx_weapon
		self.l_vy_weapon=l_vy_weapon
		
		self.l_vx_asteroid=l_vx_asteroid
		self.l_vy_asteroid=l_vy_asteroid
		
			
		self.px=px
		self.py=py
		self.vx=0
		self.vy=0
		self.god_mod=god_mod
		self.score_label=score_label
		self.score=0
		self.life_widget=[]
		self.heart_img=heart_img
		self.life=life
		for i in range(0,life):
			self.life_widget.append(self.canvas.create_image(w-32,i*32,anchor=tkinter.NW,image=self.heart_img))
		self.revive=0
		
		self.invisi_img=invisi_img
	
		self.explosion=pygame.mixer.Sound(os.path.join("musique","explosion.wav"))
		self.tir=pygame.mixer.Sound(os.path.join("musique","tir.wav"))
		
		self.best_score=best_score
		
		
	def run(self) :
	
		self.create_asteroid()
		self.create_asteroid()
		
		
		while self.runt :
			
			if self.rotation_command=="right":
				self.orientation+=1
				if self.orientation==36:
					self.orientation=0
					
			elif self.rotation_command=="left":
				self.orientation+=-1
				if self.orientation==-1:
					self.orientation=35
			
			if self.engine_state==True:
				self.vx,self.vy = self.vx+self.l_ax[self.orientation],self.vy+self.l_ay[self.orientation]
				
				
			elif self.engine_state==False:
				ax,ay = 0,0
			
			self.px=self.px+self.vx
			self.py=self.py+self.vy

				
			if self.revive/5==int(self.revive/5):
		
				if self.engine_state==True:
					self.canvas.itemconfig(self.player_item,image=self.player_on_img[self.orientation])
				elif self.engine_state==False:
					self.canvas.itemconfig(self.player_item,image=self.player_off_img[self.orientation])
			else :
				self.canvas.itemconfig(self.player_item,image=self.invisi_img)
			
			self.canvas.coords(self.player_item, self.px,self.py)
			
			if self.px < -64 :
				self.px = self.w
				
			if self.py < -64 :
				self.py = self.h
				
			if self.px > self.w:
				self.px = -64
				
			if self.py > self.h:
				self.py = -64
				
			
			self.mv_shoot()
			self.moove_asteroid()
			
			#orb_hitbox
			for i in range(0,len(self.orb[0])):
				self.orb_hitbox=self.canvas.find_overlapping(self.orb[1][i],self.orb[2][i],self.orb[1][i]+64,self.orb[2][i]+64)
				if len(self.orb_hitbox)>=2 and self.orb_hitbox[1]!=1:
					self.split(i)

			self.obstacle_state()
			
			if self.revive>0:
				self.revive+=-1
				
			if self.god_mod==False:
				#ship_hitbox
				self.ship_hitbox=self.canvas.find_overlapping(self.px,self.py,self.px+64,self.py+64)
				if len(self.ship_hitbox)==2:
					self.destroy_ship()
					
					
			
				
			time.sleep(self.time)
			

			
	def split(self,orb_nmb):
		for i in range(0,len(self.asteroid[0])):
			for j in range(0, len(self.orb_hitbox)):
				if self.orb_hitbox[j]==self.asteroid[0][i] and self.asteroid[5][i]==0:
				
					if ship_selected_number == 2 or ship_selected_number == 'n':
						self.asteroid[5][i]+=1
						self.point()
						
					
						
					else :
						self.canvas.delete(self.orb[0][orb_nmb])
						self.orb[0][orb_nmb]=""
						self.orb[1][orb_nmb]=-64
						self.orb[2][orb_nmb]=-64
						self.orb[3][orb_nmb]=0
						self.orb[4][orb_nmb]=0
						self.asteroid[5][i]+=1
						self.point()
						
			
	def point(self):
		self.score+=1
		self.explosion.play()
		self.canvas.itemconfig(self.score_label, text='Score : '+str(self.score))
		if self.time > 0.01 :
				self.time=0.02-(float(self.score/5000))
				# print(self.time)
				


	
	def obstacle_state(self):
		for i in range(0,len(self.asteroid[0])):
			if self.asteroid[5][i]>5:
				self.canvas.delete(self.asteroid[0][i])
				self.asteroid[0][i]=""
				self.asteroid[1][i]=-64
				self.asteroid[2][i]=-64
				self.asteroid[3][i]=0
				self.asteroid[4][i]=0
				self.asteroid[5][i]=0
				self.create_asteroid()
		
			if self.asteroid[5][i]>0:
				# print(self.asteroid[5][i]-1)
				self.canvas.itemconfig(self.asteroid[0][i],image=self.fire_img[self.asteroid[5][i]-1])
				self.asteroid[5][i]+=1
				
	def destroy_ship(self):
		for i in range(0,len(self.asteroid[0])):
			if self.ship_hitbox[1]==self.asteroid[0][i] and self.asteroid[5][i]==0:
				# print("destroyed")
				# self.life -=1 :
				if self.life==0 and self.revive==0:
					if self.score>int(self.best_score):
						save=open("save.txt","w")
						save.write(str(self.score))
						print(str(self.score))
					callback("thread")
				elif self.revive==0:
					self.life+=-1
					self.canvas.delete(self.life_widget[self.life])
					self.revive=50
				
	
			
	def create_asteroid(self) :
		for i in range(0,len(self.asteroid[0])):
			# print(self.asteroid[0][i])
			if self.asteroid[0][i]=="":
				side=random.randint(0,3)
				if side==0:
				# top
					self.asteroid[1][i]=random.randint(64,self.w-64)
					self.asteroid[2][i]=-127
					
					dir=random.randint(14,22)
					self.asteroid[3][i]=self.l_vx_asteroid[dir]
					self.asteroid[4][i]=self.l_vy_asteroid[dir]
					self.asteroid[5][i]=0
					
					
				if side==1:
				# bottom
					self.asteroid[1][i]=random.randint(64,self.w-64)
					self.asteroid[2][i]=h-1
					#This because we had to select the angle from 320 to 350 and from 0(=360) to 40
					#in order to have a wide angle from two smaller
					ang=random.randint(0,1)
					if ang==0:
						dir=random.randint(32,35)
						self.asteroid[3][i]=self.l_vx_asteroid[dir]
						self.asteroid[4][i]=self.l_vy_asteroid[dir]
						self.asteroid[5][i]=0
					if ang==1:
						dir=random.randint(0,4)
						self.asteroid[3][i]=self.l_vx_asteroid[dir]
						self.asteroid[4][i]=self.l_vy_asteroid[dir]
						self.asteroid[5][i]=0
						
					
						
				if side==2:
				# left
					self.asteroid[1][i]=-127
					self.asteroid[2][i]=random.randint(64,self.h-64)
					
					dir=random.randint(5,13)
					self.asteroid[3][i]=self.l_vx_asteroid[dir]
					self.asteroid[4][i]=self.l_vy_asteroid[dir]	
					self.asteroid[5][i]=0
					
				if side==3:
				# right
					self.asteroid[1][i]=w-1
					self.asteroid[2][i]=random.randint(64,self.h-64)
					
					dir=random.randint(23,31)
					self.asteroid[3][i]=self.l_vx_asteroid[dir]
					self.asteroid[4][i]=self.l_vy_asteroid[dir]
					self.asteroid[5][i]=0
					
				self.asteroid[0][i]=self.canvas.create_image(self.asteroid[1][0],self.asteroid[2][0],anchor=tkinter.NW,image=self.a0_img)
				# print("created")
			
			
	def moove_asteroid(self):
		for i in range(0,len(self.asteroid[0])):
			self.asteroid[1][i]+=self.asteroid[3][i]
			self.asteroid[2][i]+=self.asteroid[4][i]
			self.canvas.coords(self.asteroid[0][i], self.asteroid[1][i],self.asteroid[2][i])
			
			if self.asteroid[1][i]>self.w:
				self.asteroid[1][i]=-64
				
			if self.asteroid[2][i]>self.h:
				self.asteroid[2][i]=-64
				
			if self.asteroid[1][i]<-64:
				self.asteroid[1][i]=self.w
				
			if self.asteroid[2][i]<-64:
				self.asteroid[2][i]=self.h
			
	def shoot(self,key):
		
		# print("shoot")
		if self.orb[0][0]=="" :
			self.orb[0][0]=self.canvas.create_image(self.px+25,self.py+25,anchor=tkinter.NW,image=self.orb_img)
			self.orb[1][0]=self.px+25
			self.orb[2][0]=self.py+25
			self.orb[3][0]=self.l_vx_weapon[self.orientation]
			self.orb[4][0]=self.l_vy_weapon[self.orientation]
			self.tir.play()
			
		
		elif self.orb[0][1]=="" :
			if ship_selected_number !=2	:

				self.orb[0][1]=self.canvas.create_image(self.px+25,self.py+25,anchor=tkinter.NW,image=self.orb_img)
				self.orb[1][1]=self.px+25
				self.orb[2][1]=self.py+25
				self.orb[3][1]=self.l_vx_weapon[self.orientation]
				self.orb[4][1]=self.l_vy_weapon[self.orientation]
				self.tir.play()
			
		
		elif self.orb[0][2]=="" :
			if ship_selected_number !=2	:

				self.orb[0][2]=self.canvas.create_image(self.px+25,self.py+25,anchor=tkinter.NW,image=self.orb_img)
				self.orb[1][2]=self.px+25
				self.orb[2][2]=self.py+25
				self.orb[3][2]=self.l_vx_weapon[self.orientation]
				self.orb[4][2]=self.l_vy_weapon[self.orientation]
				self.tir.play()
		
	def mv_shoot(self):
		for i in range(0,3):
			self.orb[1][i]+=self.orb[3][i]
			self.orb[2][i]+=self.orb[4][i]
			self.canvas.coords(self.orb[0][i], self.orb[1][i],self.orb[2][i])
			if self.orb[1][i] < -64 or self.orb[2][i] < -64 or self.orb[1][i] >= self.w+64 or self.orb[2][i] >= self.h+64 :
				self.canvas.delete(self.orb[0][i])
				self.orb[0][i]=""
				self.orb[1][i]=-64
				self.orb[2][i]=-64
				self.orb[3][i]=0
				self.orb[4][i]=0
	
	
	
		
		
	def action(self,key):
		if key=="right" or key=="left" or key=="roff":
			self.rotation_command=key
		elif key=="engin_on":
			self.engine_state=True
		elif key=="engin_off":
			self.engine_state=False
		
	
	def stop(self):
		self.runt=False
		pygame.mixer.stop()
	


def init():
	global l_ax,l_ay,player_off_img,player_on_img,orb_img,fire_img,invisi_img,duty_l,loading_value,l_vx_weapon,l_vy_weapon,a0_img,l_vx_asteroid,l_vy_asteroid,accel_value,weapon_speed_value,life,heart_img,best_score
	

	
	calc=0
	calc_label=tkinter.Label(root,text=str(calc))
	# calc_label.pack()
	
	l_ax=[]
	l_ay=[]
	l_vx_weapon=[]
	l_vy_weapon=[]
	l_vx_asteroid=[]
	l_vy_asteroid=[]
	fire_img=[]
	if ship_selected_number != "n":
		accel_value=all_ship[ship_selected_number][1]
		weapon_speed_value=all_ship[ship_selected_number][2]
		life=all_ship[ship_selected_number][3]
	else :
		life=0
		music=pygame.mixer.Sound(os.path.join("musique","nyancat.wav"))
		music.play(loops=-1, maxtime=0, fade_ms=1000)
	asteroid_speed_value=2
	
	#création des dossiers
	if not os.path.exists("temp"):
		os.makedirs("temp")
		os.makedirs(os.path.join("temp","on"))
		os.makedirs(os.path.join("temp","off"))
		print("makedirs")
		loading_value+=1
		add_work(loading_value)
		
	
	#création des images "on"
	image = Image.open(os.path.join("img","player_on_"+str(ship_selected_number)+".png"))
	image.load()
	for i in range(0,36):
		imRotate = image.rotate(-i*10)
		filename = os.path.join("temp","on","player_on" + str(i*10) + ".png")
		imRotate.save(filename)
		print(i)
		loading_value+=1
		add_work(loading_value)
		
		
		
	#creation des orbes personnalisées
	orb_img=tkinter.PhotoImage(file=os.path.join("img","orb_"+str(ship_selected_number)+".png"))
	loading_value+=1
	add_work(loading_value)
		
		
	#création des images "off"
	image2 = Image.open(os.path.join("img","player_off_"+str(ship_selected_number)+".png"))
	image2.load()
	for i in range(0,36):
		imRotate = image2.rotate(-i*10)
		filename = os.path.join("temp","off","player_off" + str(i*10) + ".png")
		imRotate.save(filename)
		print(i)
		loading_value+=1
		add_work(loading_value)
	
	#chargement des images
	player_on_img=[]
	player_off_img=[]

	for i in range (0,36):
		player_on_img.append(tkinter.PhotoImage(file=os.path.join("temp","on","player_on"+str(i*10)+".png")))
		player_off_img.append(tkinter.PhotoImage(file=os.path.join("temp","off","player_off"+str(i*10)+".png")))
		loading_value+=1
		add_work(loading_value)


	
	a0_img=tkinter.PhotoImage(file=os.path.join("img","a0_img.png"))
	loading_value+=1
	add_work(loading_value)
	
	heart_img=tkinter.PhotoImage(file=os.path.join("img","heart.png"))
	loading_value+=1
	add_work(loading_value)
	
	invisi_img=tkinter.PhotoImage(file=os.path.join("img","invisi.png"))
	loading_value+=1
	add_work(loading_value)
	
	
	for i in range(1,6):
		fire_img.append(tkinter.PhotoImage(file=os.path.join("img","bubbling_fire_"+str(i)+".gif")))
		loading_value+=1
		add_work(loading_value)

	

	#calcul des vecteurs accélérations X et Y
	for i in range(0,36):
		l_ax.append(accel_value*math.sin(math.radians(i*10)))
		l_ay.append(-(accel_value*math.cos(math.radians(i*10))))
		print(i)
		loading_value+=1
		add_work(loading_value)
		
	for i in range(0,36):
		l_vx_weapon.append(weapon_speed_value*math.sin(math.radians(i*10)))
		l_vy_weapon.append(-weapon_speed_value*math.cos(math.radians(i*10)))
		loading_value+=1
		add_work(loading_value)
		
	for i in range(0,36):
		l_vx_asteroid.append(asteroid_speed_value*math.sin(math.radians(i*10)))
		l_vy_asteroid.append(-asteroid_speed_value*math.cos(math.radians(i*10)))
		loading_value+=1
		add_work(loading_value)
	
	print("loading_value max = " + str(loading_value))
	
	best_score_txt=open("save.txt","r")
	best_score=best_score_txt.read()
	best_score_txt.close()
	print(best_score)
	
	loading_canvas.destroy()


def exit(arg):
	if os.path.exists("temp"):
		shutil.rmtree("temp")
	root.destroy()

def callback(key):
	global thread
	thread.stop()
	aff_menu("callback")

def aff_menu(arg):

	global bgc,afgc,fgc,abgc

	# Remove old widgets
	for widget in root.winfo_children():
		widget.destroy()
		
	# Window configuration
	root.geometry("750x700")
	root.title("ASTEROÏDS")
	root.configure(bg=bgc)
	root.overrideredirect(False)	
	root.bind("<Escape>",exit)
	# root.bind("<Enter>",game(oxo))
	
	
	#title
	menu_title=tkinter.Label(root,text="ASTEROIDS",font=(text_style,50),fg=fgc,bg=bgc)
	menu_title.pack()

	space=tkinter.Label(root,text="",font=(text_style,100),fg=fgc,bg=bgc)
	space.pack()

	
	# Buttons creation
	play_b=tkinter.Button(root,text="PLAY",font=(text_style,text_size1),fg=fgc,bg=bgc,bd=0,activeforeground=afgc,activebackground=abgc,command=game)
	play_b.pack()

	shop_b=tkinter.Button(root,text="SHOP",font=(text_style,text_size1),fg=fgc,bg=bgc,bd=0,activeforeground=afgc,activebackground=abgc,command=aff_shop)
	shop_b.pack()

	option_b=tkinter.Button(root,text="SETTINGS",font=(text_style,text_size1),fg=fgc,bg=bgc,bd=0,activeforeground=afgc,activebackground=abgc,command=settings)
	option_b.pack()
	
def settings():
	root.bind("<Escape>",aff_menu)
	root.bind("<g>",nyan_cat)
	root.geometry("750x700")

	# Remove menu buttons
	for widget in root.winfo_children():
		widget.destroy()
	
	root.configure(bg=bgc)
	
	
	
	#color mode buttons
	color_choice=tkinter.Label(root,text="COLOR MODE",font=(text_style,text_size1),fg=fgc,bg=bgc)
	color_choice.pack()
	
	color_1=tkinter.Button(root,text=" Standard  ",font=(text_style,text_size1),fg="green yellow",bg="midnight blue",bd=3,activeforeground="green yellow",activebackground="midnight blue",command = lambda : color_mode(1))
	color_1.pack()

	color_2=tkinter.Button(root,text="   Mono    ",font=(text_style,text_size1),fg="white",bg="black",bd=3,activeforeground="white",activebackground="black",command = lambda : color_mode(2))
	color_2.pack()
	
	color_3=tkinter.Button(root,text="  Stellar  ",font=(text_style,text_size1),fg="gold",bg="DarkOrchid4",bd=3,activeforeground="goldenrod",activebackground="DarkOrchid4",command = lambda : color_mode(3))
	color_3.pack()
	
	color_4=tkinter.Button(root,text="Bling Bling",font=(text_style,text_size1),fg="blue2",bg="gold",bd=3,activeforeground="blue2",activebackground="gold",command = lambda : color_mode(4))
	color_4.pack()
		
	#back button
	back_b=tkinter.Button(root,text="APPLY",font=(text_style,text_size1),fg=fgc,bg=bgc,bd=0,activeforeground=afgc,activebackground=abgc,command= lambda : aff_menu(0))
	back_b.pack()

def nyan_cat(key):

	global ship_selected_number,accel_value,weapon_speed_value,god_mod
	aff_menu("fonction")

	ship_selected_number="n"
	accel_value=0.5
	weapon_speed_value=50
	god_mod=True
	
	

def color_mode(mode):
	

	global bgc,afgc,fgc,abgc
	
	#set the color
	if mode==1:
		
		bgc="midnight blue"
		afgc="white"
		fgc="green yellow"
		abgc="midnight blue"
		
	elif mode==2:
		bgc="black"
		afgc="gray40"
		fgc="white"
		abgc="black"
		
	elif mode==3:
		bgc="DarkOrchid4"
		afgc="goldenrod"
		fgc="gold"
		abgc="DarkOrchid4"
	
	
	elif mode==4:
		bgc="gold"
		afgc="blue"
		fgc="blue4"
		abgc="gold"
		
		
	#dislpay the color choice
	settings()

#Start game 	
# def game(oxo):
def game():
	global thread,accel_value,l_ax,l_ay,player_off_img,player_on_img,orb_img,a0_img,fire_img,invisi_img,duty_l,loading_value,w, h, loading_canvas,l_vx_weapon,l_vy_weapon,l_vx_asteroid,l_vy_asteroid,god_mod,ship_selected_number,bg_img,fgc,bgc,life,heart_img,best_score

	root.bind("<Escape>",callback)

	# Remove menu buttons
	for widget in root.winfo_children():
		widget.destroy()
	
	# Set the fullscreen mode	
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.overrideredirect(True)
	root.geometry(str(w) + "x" + str(h) + "+0+0")
	
	# creation of the canvas
	canvas=tkinter.Canvas(root,width=w,height=h)
	# canvas.pack()
	canvas.configure(bg=space_bg)
	
	#barre de chargement
	loading_value=0
	loading_canvas=tkinter.Canvas(root,width=w,height=h,bg=space_bg)
	loading_canvas.pack()
	loading_text=loading_canvas.create_text(w/2,h/5, text="loading",fill="white",font=(text_style,100))
	init()
	
	if ship_selected_number=="n":
		print("bg_img")
		bg_img=tkinter.PhotoImage(file=os.path.join("img","bg_nyan_cat.png"))
		a0_img=tkinter.PhotoImage(file=os.path.join("img","carrot.png"))
		canvas.create_image(0,0,anchor=tkinter.NW,image=bg_img)
		
	score_label = canvas.create_text(w/2,40, text='Score : 0',fill=fgc,font=(text_style,50))
	best_score_label = canvas.create_text(w/2,120, text='Best : '+str(best_score),fill=fgc,font=(text_style,30))

	px,py = w/2-32,h/2-32
	
	#spaceship creation
	player=canvas.create_image(px,py,anchor=tkinter.NW,image=player_off_img[0])
	canvas.pack()
	
	

	#start the thread
	thread = Background_process(canvas,player,player_on_img,player_off_img,orb_img,a0_img,fire_img,l_ax,l_ay,l_vx_weapon,l_vy_weapon,l_vx_asteroid,l_vy_asteroid,px,py,god_mod,score_label,life,heart_img,invisi_img,best_score)
	thread.start()
	
	
	#spaceship control
	
	#spaceship forward control
	root.bind("<KeyRelease-Up>",lambda key : thrust(key,0,player,canvas))
	root.bind("<Up>",lambda key : thrust(key,1,player,canvas))
	
	
	root.bind("<Right>",lambda key : rotation(key,"right",player,canvas))
	root.bind("<Left>",lambda key : rotation(key,"left",player,canvas))
	
	root.bind("<KeyRelease-Right>",lambda key : rotation(key,"roff",player,canvas))
	root.bind("<KeyRelease-Left>",lambda key : rotation(key,"roff",player,canvas))
	
	#Weapon control
	root.bind("<space>",thread.shoot)

	

	
def aff_shop():
	global ship_selected_number,vaisseau_1,vaisseau_2,vaisseau_3,void,bgc,afgc,fgc,abgc,god_mod
	
	
	root.bind("<Escape>",aff_menu)
	root.bind("<Return>",aff_menu)
	root.geometry("750x700")
	god_mod=False
	if ship_selected_number =="n":
		ship_selected_number=0


	# Remove menu buttons
	for widget in root.winfo_children():
		widget.destroy()
		
	frame_1=tkinter.Frame(root, bg=bgc, width=375, height=700)
	frame_1.bind("<Button-1>", previous_ship)
	frame_1.grid(row=1,column=1)
	
	frame_2=tkinter.Frame(root, bg=bgc, width=375, height=700)
	frame_2.bind("<Button-1>", next_ship)
	frame_2.grid(row=1,column=2)
	
	frame_vaisseau_1=tkinter.Frame(root, width=64, height=64)
	frame_vaisseau_1.grid(row=1,column=1, sticky=tkinter.W)
	
	frame_vaisseau_2=tkinter.Frame(root, width=64, height=64)
	frame_vaisseau_2.grid(row=1,column=1, columnspan=2)
	
	frame_vaisseau_3=tkinter.Frame(root, width=64, height=64)
	frame_vaisseau_3.grid(row=1,column=2, sticky=tkinter.E)

	if ship_selected_number>0:
		vaisseau_1=tkinter.Label(frame_vaisseau_1,image=all_ship[ship_selected_number-1][0], bg=bgc)
	else:
		vaisseau_1=tkinter.Label(frame_vaisseau_1,image=invi_img, bg=bgc)
	vaisseau_1.pack()
	
	vaisseau_2=tkinter.Label(frame_vaisseau_2,image=all_ship[ship_selected_number][0], bg=bgc)
	vaisseau_2.pack()
	
	if ship_selected_number<len(all_ship)-1:
		vaisseau_3=tkinter.Label(frame_vaisseau_3,image=all_ship[ship_selected_number+1][0], bg=bgc)
	else:
		vaisseau_3=tkinter.Label(frame_vaisseau_3,image=invi_img, bg=bgc)
	vaisseau_3.pack()
	
	title=tkinter.Label(root,text="SHIP :",font=(text_style,50),fg=fgc,bg=bgc,bd=0,activeforeground=afgc,activebackground=abgc)
	title.grid(row=1,column=1,columnspan=2, sticky=tkinter.N, pady=50)
	select_button=tkinter.Button(root,text="SELECT",command=lambda:aff_menu("select_b"),font=(text_style,text_size1),fg=fgc,bg=bgc,bd=0,activeforeground=afgc,activebackground=abgc)
	select_button.grid(row=1,column=1,columnspan=2, sticky=tkinter.S,pady=100)
	


def next_ship(key):
	global ship_selected_number
	
	print("next")
	if ship_selected_number<len(all_ship)-1:
		ship_selected_number+=1
		print_shop_ship()


def previous_ship(key):
	global ship_selected_number
	
	print("previous")
	if ship_selected_number>0:
		ship_selected_number+=-1
		print_shop_ship()
	
	
def print_shop_ship():
	global ship_selected_number,vaisseau_1,vaisseau_2,vaisseau_3
	
	# print(len(all_ship))
	
	if ship_selected_number>0:
		vaisseau_1.configure(image=all_ship[ship_selected_number-1][0])
	else :
		vaisseau_1.configure(image=invi_img)
	
	vaisseau_2.configure(image=all_ship[ship_selected_number][0])
	
	if ship_selected_number<len(all_ship)-1:
		vaisseau_3.configure(image=all_ship[ship_selected_number+1][0])
	else :
		vaisseau_3.configure(image=invi_img)	


def thrust(arg,state,player,canvas):

	global state_engine
	if state==1:
		thread.action("engin_on")
	#if engine on
		#skin change for engine on
		# canvas.itemconfig(player,image=player_on_img)
		state_engine=1
	else:
		thread.action("engin_off")
	#if engine off
		#skin change for engine off
		# canvas.itemconfig(player,image=player_off_img)
		state_engine=0
		
		
def rotation(arg,command,player,canvas):
	global orientation
	
	thread.action(command)
	
	
def add_work(loading_value):
	global w, h, loading_canvas
	
	loading_max_value=219
	work2=int(loading_value/loading_max_value*100)
	x1=w/100*work2
	x2=w/100*(work2-1)
	y1=h/2+50
	y2=h/2-30
	loading_canvas.create_rectangle(x1,y1,x2,y2, fill="white",width=0)
	loading_canvas.update()
	
	
def music():
	freq = 44100     # audio CD quality
	bitsize = 16    # unsigned 16 bit
	channels = 2     # 1 is mono, 2 is stereo
	buffer = 2048    # number of samples (experiment to get best sound)
	pygame.mixer.init(freq, bitsize, channels, buffer)

	






	
# Size and color choice
text_size1=25
text_style="system"
bgc="midnight blue"
abgc="midnight blue"
fgc="green yellow"
afgc="white"

space_bg="black"

orientation=0
state_engine=0

# Window creation
root=tkinter.Tk()



ship_selected_number=0

all_ship=[[0 for i in range(0,4)] for j in range(0,3)]

all_ship[0][0]=tkinter.PhotoImage(file=os.path.join("img","player_off_"+str(0)+".png"))
all_ship[0][1]=0.25 #accel_value
all_ship[0][2]=30 #weapon_speed_value
all_ship[0][3]=2 #Number Heal points

all_ship[1][0]=tkinter.PhotoImage(file=os.path.join("img","player_off_"+str(1)+".png"))
all_ship[1][1]=0.1 #accel_value
all_ship[1][2]=40 #weapon_speed_value
all_ship[1][3]=2 
all_ship[1][3]=2 #Number Heal points

all_ship[2][0]=tkinter.PhotoImage(file=os.path.join("img","player_off_"+str(2)+".png"))
all_ship[2][1]=0.05 #accel_value
all_ship[2][2]=50 #weapon_speed_value
all_ship[2][3]=5 #Number Heal points

# all_ship[3][0]=tkinter.PhotoImage(file=os.path.join("img","player_off_"+str(3)+".png"))
# all_ship[3][1]=0.05 #accel_value
# all_ship[3][2]=50 #weapon_speed_value
# all_ship[2][3]=5 
void=tkinter.PhotoImage(file=os.path.join("img","void.png"))
invi_img=tkinter.PhotoImage(file=os.path.join("img","invisi.png"))


god_mod=False

print(all_ship)

#Skins
# player_off_img=tkinter.PhotoImage(file=os.path.join("img","Player_off.png"))
# player_on_img=tkinter.PhotoImage(file=os.path.join("img","Player_on.png"))



# frame_list=init_image()

# Show menu
aff_menu(0)

music()

root.mainloop()