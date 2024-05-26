import tkinter as tk
from tkinter import simpledialog
import numpy as np
import librosa
from tkinter import filedialog
from tkinter import *
import pygame
from pydub import AudioSegment
import matplotlib.pyplot as plt
import soundfile as sf
from PIL import Image, ImageTk, ImageDraw


current_audio = None
musicBox = None
filePath = None
lineLeangth1 = 400
coun=1
global last_x1, last_y1, last_x2, last_y2, last_x3, last_y3, la_ev_x1, la_ev_x2, la_ev_x3, call_count, duration_in_seconds, flag, gamm, flagg, continue_moving 

def on_press1(event):
    global last_x1, last_y1, ball1, la_ev_x1
    x1, y1, x2, y2 = canvas.coords(ball1)
    last_x1 = (x1 + x2) / 2
    last_y1 = (y1 + y2) / 2
    la_ev_x1 = event.x


def on_press2(event):
    global last_x2, last_y2, ball2, la_ev_x2
    x1, y1, x2, y2 = canvas.coords(ball2)
    last_x2 = (x1 + x2) / 2
    last_y2 = (y1 + y2) / 2
    la_ev_x2 = event.x

def on_press3(event):
    global last_x3, last_y3, ball3, la_ev_x3
    x1, y1, x2, y2 = canvas.coords(ball3)
    last_x3 = (x1 + x2) / 2
    last_y3 = (y1 + y2) / 2
    la_ev_x3 = event.x
##############################################################################
def on_drag1(event):
    global last_x1, last_y1, last_x2, la_ev_x1
    x0, y0, x1, y1 = canvas.coords(ball1)
    ball_center_x = (x0 + x1) / 2
    ball_center_y = (y0 + y1) / 2
    delta_x = event.x - la_ev_x1
    if 50 <= ball_center_x + delta_x <= last_x2:
        canvas.move(ball1, delta_x, 0)
        canvas.move(ball0, delta_x, 0)
        last_x1 = (x0 + x1) / 2
        last_y1 = (y0 + y1) / 2
        la_ev_x1 = event.x

def on_drag2(event):
    global last_x2, last_y2, last_x1, la_ev_x2
    x0, y0, x1, y1 = canvas.coords(ball2)
    ball_center_x = (x0 + x1) / 2
    ball_center_y = (y0 + y1) / 2
    delta_x = event.x - la_ev_x2
    if last_x1 <= ball_center_x + delta_x <= 450:
        canvas.move(ball2, delta_x, 0)
        last_x2 = (x0 + x1) / 2
        last_y2 = (y0 + y1) / 2
        la_ev_x2 = event.x

def on_drag3(event):
    global last_x3, last_y3, la_ev_x3
    x0, y0, x1, y1 = canvas.coords(ball3)
    ball_center_x = (x0 + x1) / 2
    ball_center_y = (y0 + y1) / 2
    delta_x = event.x - la_ev_x3
    if 150 <= ball_center_x + delta_x <= 350:
        canvas.move(ball3, delta_x, 0)
        last_x3 = (x0 + x1) / 2
        last_y3 = (y0 + y1) / 2
        la_ev_x3 = event.x
    set_vol()
#############################################################################
def set_vol():
    global la_ev_x3
    vol = (la_ev_x3-150)/200
    if vol > 1: 
        vol = 1
    if vol < 0:
        vol = 0
    pygame.mixer.music.set_volume(vol)
################################################################################
flagg=False
def play_music(event):
    global last_x1, last_x2, lineLeangth1, coun, call_count, duration_in_seconds, flagg, ball0, gamm, flag, continue_moving
    if flagg:
        unpause_song()
        flagg=False
        x0, y0, x1, y1 = canvas.coords(ball0)
        moveball00(x0)
    else:
        global continue_moving
        # continue_moving = False
        gamm=0
        flag=False
        call_count = 0
        pygame.init()
        song = musicBox.get(ACTIVE)
        song = f"D:/downloads/testlib-master/audio_editor/music/{song}.mp3"
        audio = AudioSegment.from_file(song)
        duration_in_seconds = audio.duration_seconds
        if last_x1 == 50 and last_x2 == 450:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)
            moveball0()
        else:   
            start = ((last_x1-50) /lineLeangth1) * duration_in_seconds*1000
            end = ((last_x2-50) /lineLeangth1) * duration_in_seconds*1000
            trimmed_audio = audio[start:end]
            # print(filePath)
            trimmed_file_path = "D:/downloads/testlib-master/audio_editor/music/song"
            trimmed_file_path+=str(coun)
            trimmed_file_path+=".mp3" 
            trimmed_audio.export(trimmed_file_path, format="mp3")

            audio = AudioSegment.from_file(trimmed_file_path)
            duration_in_seconds = audio.duration_seconds
            coun+=1
            musicBox.insert(END, "song"+str(coun-1))

            canvas.coords(ball2,445, 20, 455, 30)
            canvas.coords(ball1, 45, 20, 55, 30)
            canvas.coords(ball0, 45, 20, 55, 30)
            last_x1 = 50
            last_x2 = 450

            pygame.mixer.music.load(trimmed_file_path)
            pygame.mixer.music.play(loops=0)
            flag = False
            continue_moving = True
            moveball0()
##############################################################################
def reverse_music(event):
    global last_x1, last_x2, lineLeangth1, coun, call_count, duration_in_seconds
    call_count = 0
    pygame.init()
    song = musicBox.get(ACTIVE)
    song = f"D:/downloads/testlib-master/audio_editor/music/{song}.mp3"
    audio = AudioSegment.from_file(song)
    duration_in_seconds = audio.duration_seconds
    start = ((last_x1-50) /lineLeangth1) * duration_in_seconds*1000
    end = ((last_x2-50) /lineLeangth1) * duration_in_seconds*1000
    trimmed_audio = audio[start:end]
    trimmed_file_path = "D:/downloads/testlib-master/audio_editor/music/test"
    trimmed_file_path+=".mp3" 
    trimmed_audio.export(trimmed_file_path, format="mp3")
    audio = AudioSegment.from_file(trimmed_file_path)
    duration_in_seconds = audio.duration_seconds
    reversed_audio = audio.reverse()
    # return reversed_audio
    reversed_audio_path = "D:/downloads/testlib-master/audio_editor/music/reversed_song"
    reversed_audio_path+=str(coun)
    reversed_audio_path+=".mp3" 
    coun+=1
    musicBox.insert(END, "reversed_song"+str(coun-1))
    reversed_audio.export(reversed_audio_path, format="mp3")
    pygame.mixer.init()

    canvas.coords(ball2,445, 20, 455, 30)
    canvas.coords(ball1, 45, 20, 55, 30)
    canvas.coords(ball0, 45, 20, 55, 30)
    last_x1 = 50
    last_x2 = 450

    pygame.mixer.music.load(reversed_audio_path)
    pygame.mixer.music.play(loops=0)
    moveball0()
##############################################################################
ratef = 2
def fast_music(event):
    global ratef, coun, duration_in_seconds, last_x1, last_x2
    if ratef>5:
        ratef=5
    if ratef<1:
        ratef=1
    song= musicBox.get(ACTIVE)
    song = musicBox.get(ACTIVE)
    song = f"D:/downloads/testlib-master/audio_editor/music/{song}.mp3"
    audio = AudioSegment.from_file(song)
    duration_in_seconds = audio.duration_seconds
    start = ((last_x1-50) /lineLeangth1) * duration_in_seconds*1000
    end = ((last_x2-50) /lineLeangth1) * duration_in_seconds*1000
    trimmed_audio = audio[start:end]
    trimmed_file_path = "D:/downloads/testlib-master/audio_editor/music/test"
    trimmed_file_path+=".mp3" 
    trimmed_audio.export(trimmed_file_path, format="mp3")
    audio = AudioSegment.from_file(trimmed_file_path)
    faster_audio = audio.speedup(playback_speed=ratef)
    faster_audio_path = "D:/downloads/testlib-master/audio_editor/music/faster_song"
    faster_audio_path+=str(coun)
    faster_audio_path+=".mp3"
    coun+=1
    musicBox.insert(END, "faster_song"+str(coun-1))
    faster_audio.export(faster_audio_path, format="mp3")
    audio = AudioSegment.from_file(faster_audio_path)
    duration_in_seconds = audio.duration_seconds
    canvas.coords(ball2,445, 20, 455, 30)
    canvas.coords(ball1, 45, 20, 55, 30)
    canvas.coords(ball0, 45, 20, 55, 30)
    last_x1 = 50
    last_x2 = 450
    pygame.mixer.init()
    pygame.mixer.music.load(faster_audio_path)
    pygame.mixer.music.play(loops=0)
    moveball0()
###############################################################################
rates = 0.9
def slow_music(event):
    global rate, coun, duration_in_seconds, last_x1, last_x2, rates
    song= musicBox.get(ACTIVE)
    if rates<0.5:
        rate=0.5
    if rates>1:
        rate=1
    song = musicBox.get(ACTIVE)
    song = f"D:/downloads/testlib-master/audio_editor/music/{song}.mp3"
    audio = AudioSegment.from_file(song)
    duration_in_seconds = audio.duration_seconds
    start = ((last_x1-50) /lineLeangth1) * duration_in_seconds*1000
    end = ((last_x2-50) /lineLeangth1) * duration_in_seconds*1000
    trimmed_audio = audio[start:end]
    trimmed_file_path = "D:/downloads/testlib-master/audio_editor/music/test"
    trimmed_file_path+=".mp3" 
    trimmed_audio.export(trimmed_file_path, format="mp3")
    audio = AudioSegment.from_file(trimmed_file_path)
    audio_array = np.array(audio.get_array_of_samples(), dtype=np.float32)
    ratee=(2*rates)
    slow_audio = librosa.effects.time_stretch(audio_array, rate=ratee)
    no_noise_audio = librosa.effects.remix(slow_audio, intervals=librosa.effects.split(slow_audio))
    slow_audio_path = "D:/downloads/testlib-master/audio_editor/music/slower_song"
    slow_audio_path+=str(coun)
    slow_audio_path+=".mp3"
    coun+=1
    musicBox.insert(END, "slower_song"+str(coun-1))
    sf.write(slow_audio_path, no_noise_audio, audio.frame_rate)
    audio = AudioSegment.from_file(slow_audio_path)
    duration_in_seconds = audio.duration_seconds
    canvas.coords(ball2,445, 20, 455, 30)
    canvas.coords(ball1, 45, 20, 55, 30)
    canvas.coords(ball0, 45, 20, 55, 30)
    last_x1 = 50
    last_x2 = 450
    pygame.mixer.init()
    pygame.mixer.music.load(slow_audio_path)
    pygame.mixer.music.play(loops=0)
    moveball0()
###############################################################################
def change_ratef():
        global ratef
        new_value = simpledialog.askfloat(title="Change Rate", prompt="please ,enter the new rate", initialvalue=ratef, minvalue=1, maxvalue=5)
        if new_value:
            ratef = new_value

def change_rates():
        global rates
        new_value = simpledialog.askfloat(title="Change Rate", prompt="please ,enter the new rate", initialvalue=rates, minvalue=0.5, maxvalue=1)
        if new_value:
            rates = new_value
###############################################################################
def close_music(event):
    global musicBox, last_x1, last_x2, ball1, ball2, canvas, ball0, x, flag, root, flagg
    pygame.mixer.music.stop()
    musicBox.selection_clear(ACTIVE)
    canvas.coords(ball2,445, 20, 455, 30)
    canvas.coords(ball1, 45, 20, 55, 30)
    canvas.coords(ball0, 45, 20, 55, 30)
    flag = False
    last_x1 = 50
    last_x2 = 450
    canvas.coords(ball0, 45, 20, 55, 30)
    flagg = False

def closee():
    global musicBox, last_x1, last_x2, ball1, ball2, canvas, ball0, x, flag, root, flagg
    canvas.coords(ball2,445, 20, 455, 30)
    canvas.coords(ball1, 45, 20, 55, 30)
    canvas.coords(ball0, 45, 20, 55, 30)
    flag = False
    last_x1 = 50
    last_x2 = 450
    canvas.coords(ball0, 45, 20, 55, 30)
    flagg = False
################################################################################
def moveball0():
    global x, last_x1, flag, root, duration_in_seconds, flagg, gam, gamm, continue_moving
    flag = True
    print(duration_in_seconds)
    diff=(last_x2-last_x1)
    x = last_x1
    gam=diff / duration_in_seconds
    def move_ball():
        print(0)
        # closee()
        global x, flag, root, gamm, flagg
        if (x + (diff / duration_in_seconds)) > last_x2 - 5:
            x = last_x2 - 5
        else:
            x += (diff / duration_in_seconds)
        if flag:
            canvas.coords(ball0, x, 20, x+10, 30)
        # print(flag)
        # print(continue_moving)
        if flag and x <= last_x2-5 :  
            root.after(1040, move_ball) 
        else:
            if flagg==False:
                canvas.coords(ball0, 45, 20, 55, 30)


    move_ball() 


def moveball00(xx):
    global x, last_x1, flag, root, duration_in_seconds, gam, gamm
    flag = True
    diff=(last_x2-last_x1)
    if (xx-gam)>=(last_x1-5):
        xx-=gam
    x = xx

    def move_balll():
        print(00)
        global x, flag, root, gamm, flagg
        if (x + (diff / duration_in_seconds)) > last_x2 - 5:
            x = last_x2 - 5
        else:
            x += (diff / duration_in_seconds)
        if flag:
            canvas.coords(ball0, x, 20, x+10, 30)
        if flag and x <= last_x2-5 : 
            root.after(1040, move_balll)  
        elif flag==False:
            canvas.coords(ball0, x-gam, 20, x+10-gam, 30)
            if flagg==False:
                canvas.coords(ball0, 45, 20, 55, 30)

    move_balll()  
#################################################################################
def plot_waveform():
    song= musicBox.get(ACTIVE)
    song = f"D:/downloads/testlib-master/audio_editor/music/{song}.mp3"
    data, sample_rate = sf.read(song)
    time = [i / sample_rate for i in range(len(data))]
    plt.plot(time, data)
    plt.title('Waveform of Audio File')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()
#################################################################################
def pause_song(event):
    global flagg, flag, gam, last_x1
    flagg=True
    flag = False
    print("psu")
    pygame.mixer.music.pause()

def unpause_song():
    pygame.mixer.music.unpause()
################################################################################
def add_song():
        global musicBox
        song = filedialog.askopenfilename(initialdir='D:\\downloads\\testlib-master\\audio_editor\\music' ,title="Choose a song",filetypes=[("Audio files", "*.mp3;*.wav")])
        song = song.replace("D:/downloads/testlib-master/audio_editor/music/", "")
        song = song.replace(".mp3", "")
        song = song.replace(".wav", "")
        musicBox.insert(END, song)
        if musicBox.size() == 1:
            musicBox.activate(0)
            musicBox.selection_clear(0, 'end') 
            musicBox.selection_set(0)

def delete_song():
        musicBox.delete(ACTIVE)
        if musicBox.size() == 1:
            musicBox.activate(0)
            musicBox.selection_clear(0, 'end')  
            musicBox.selection_set(0)
################################################################################
def next_song(event):
    global musicBox
    current_selection = musicBox.curselection()
    if current_selection:  
        next_index = current_selection[0] + 1  
        if next_index == musicBox.size():  
            next_index = 0 
        musicBox.selection_clear(current_selection)
        musicBox.selection_set(next_index)  
        musicBox.activate(next_index)  

def prev_song(event):
    global musicBox
    current_selection = musicBox.curselection()
    if current_selection:  
        prev_index = current_selection[0] - 1 
        if prev_index == -1:  
            prev_index = musicBox.size()-1 
        musicBox.selection_clear(current_selection)
        musicBox.selection_set(prev_index) 
        musicBox.activate(prev_index)  
##############################################################################
def make_circle_image(img):
    size = (50, 50)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    result = Image.new("RGBA", size)
    result.paste(img, (0, 0), mask=mask)
    return result



def main():
    global musicBox
    global root, ball0, ball1, ball2, ball3, last_x1, last_y1, last_x2, last_y2, last_x3, last_y3, canvas, lineLeangth1
    root = tk.Tk()
    root.title("Audio Player")
    root.iconbitmap("D:\\downloads\\testlib-master\\audio_editor\\images\\project.ico")
    root.geometry("500x500")

    controlsFrame = tk.Frame(root)
    controlsFrame.pack()
    controlsFrame2 = tk.Frame(root)
    controlsFrame2.pack()

    musicBox = Listbox(controlsFrame, bg="black", fg="white", width=60, selectbackground="gray", selectforeground="black")
    musicBox.grid(row=0, column=0, pady=20)

    canvas = tk.Canvas(controlsFrame, width=500, height=75, bg="white")
    canvas.grid(row=1, column=0, pady=20)

    canvas.create_line(50, 25, 450, 25, fill="black")
    canvas.create_line(150, 50, 350, 50, fill="black")
    lineLeangth1 = 400
    lineLeangth2 = 200

    ball0 = canvas.create_oval(45, 20, 55, 30, fill="yellow")
    ball1 = canvas.create_oval(45, 20, 55, 30, fill="red")
    ball2 = canvas.create_oval(445, 20, 455, 30, fill="blue")
    ball3 = canvas.create_oval(345, 45, 355, 55, fill="black")

    last_x1 = 50
    last_y1 = 0
    last_x2 = 450
    last_y2 = 0
    last_x3 = 350
    last_y3 = 0

    canvas.tag_bind(ball1, "<Button-1>", on_press1)
    canvas.tag_bind(ball1, "<B1-Motion>", on_drag1)
    canvas.tag_bind(ball2, "<Button-1>", on_press2)
    canvas.tag_bind(ball2, "<B1-Motion>", on_drag2)
    canvas.tag_bind(ball3, "<B1-Motion>", on_drag3)
    canvas.tag_bind(ball3, "<Button-1>", on_press3)

    nextImgPath = "D:\\downloads\\testlib-master\\audio_editor\\images\\next.png" 
    prevImgPath = "D:\\downloads\\testlib-master\\audio_editor\\images\\prev.png" 
    playImgPath = "D:\\downloads\\testlib-master\\audio_editor\\images\\stop.png" 
    stopImgPath = "D:\\downloads\\testlib-master\\audio_editor\\images\\containue.png" 
    closeImgPath = "D:\\downloads\\testlib-master\\audio_editor\\images\\close.png" 
    fastImgPath = "D:\\downloads\\testlib-master\\audio_editor\\images\\fast.png" 
    slowImgPath = "D:\\downloads\\testlib-master\\audio_editor\\images\\slow.png" 
    reverseImgPath = "D:\\downloads\\testlib-master\\audio_editor\\images\\reverse.png" 


    nextImage = Image.open(nextImgPath)
    prevImage = Image.open(prevImgPath)
    playImage = Image.open(playImgPath)
    stopImage = Image.open(stopImgPath)
    closeImage = Image.open(closeImgPath)
    fastImage = Image.open(fastImgPath)
    slowImage = Image.open(slowImgPath)
    reverseImage = Image.open(reverseImgPath)

    nextImage = nextImage.resize((50, 50), Image.Resampling.LANCZOS)
    prevImage = prevImage.resize((50, 50), Image.Resampling.LANCZOS)
    playImage = playImage.resize((50, 50), Image.Resampling.LANCZOS)
    stopImage = stopImage.resize((50, 50), Image.Resampling.LANCZOS)
    closeImage = closeImage.resize((50, 50), Image.Resampling.LANCZOS)
    fastImage = fastImage.resize((50, 50), Image.Resampling.LANCZOS)
    slowImage = slowImage.resize((50, 50), Image.Resampling.LANCZOS)
    reverseImage = reverseImage.resize((50, 50), Image.Resampling.LANCZOS)

    circlenextImage = make_circle_image(nextImage)
    circleprevImage = make_circle_image(prevImage)
    circleplayImage = make_circle_image(playImage)
    circlestopImage = make_circle_image(stopImage)
    circlecloseImage = make_circle_image(closeImage)
    circlefastImage = make_circle_image(fastImage)
    circleslowImage = make_circle_image(slowImage)
    circlereverseImage = make_circle_image(reverseImage)

    nextImage = ImageTk.PhotoImage(circlenextImage)
    prevImage = ImageTk.PhotoImage(circleprevImage)
    playImage = ImageTk.PhotoImage(circleplayImage)
    stopImage = ImageTk.PhotoImage(circlestopImage)
    closeImage = ImageTk.PhotoImage(circlecloseImage)
    fastImage = ImageTk.PhotoImage(circlefastImage)
    slowImage = ImageTk.PhotoImage(circleslowImage)
    reverseImage = ImageTk.PhotoImage(circlereverseImage)


    nextLabel = tk.Label(controlsFrame2, image=nextImage, width=50, height=50, bd=0)
    prevLabel = tk.Label(controlsFrame2, image=prevImage, width=50, height=50, bd=0)
    playLabel = tk.Label(controlsFrame2, image=playImage, width=50, height=50, bd=0)
    stopLabel = tk.Label(controlsFrame2, image=stopImage, width=50, height=50, bd=0)
    closeLabel = tk.Label(controlsFrame2, image=closeImage, width=50, height=50, bd=0)
    fastLabel = tk.Label(controlsFrame2, image=fastImage, width=50, height=50, bd=0)
    slowLabel = tk.Label(controlsFrame2, image=slowImage, width=50, height=50, bd=0)
    reverseLabel = tk.Label(controlsFrame2, image=reverseImage, width=50, height=50, bd=0)

    playLabel.grid(row=2, column=0, padx=15, pady=5)
    stopLabel.grid(row=2, column=1, padx=15, pady=5)
    closeLabel.grid(row=2, column=2, padx=15, pady=5)
    reverseLabel.grid(row=2, column=3, padx=15, pady=5)
    prevLabel.grid(row=3, column=0, padx=15, pady=5)
    slowLabel.grid(row=3, column=1, padx=15, pady=5)
    fastLabel.grid(row=3, column=2, padx=15, pady=5)
    nextLabel.grid(row=3, column=3, padx=15, pady=5)

    nextLabel.bind("<Button-1>", next_song) #next_song
    prevLabel.bind("<Button-1>", prev_song) #prev_song
    playLabel.bind("<Button-1>", play_music) #play_music
    stopLabel.bind("<Button-1>", pause_song) #pause_song
    closeLabel.bind("<Button-1>", close_music) #close_music
    fastLabel.bind("<Button-1>", fast_music) #fast_music
    slowLabel.bind("<Button-1>", slow_music) #slow_music
    reverseLabel.bind("<Button-1>", reverse_music) #reverse_music


    myMenu = Menu(root)
    root.config(menu=myMenu)

    Menuu = Menu(myMenu)
    myMenu.add_cascade(label="Menu", menu=Menuu)
    Menuu.add_command(label="Add Audio", command=add_song)
    Menuu.add_separator()
    Menuu.add_command(label="Remove Audio", command=delete_song)
    Menuu.add_separator()
    Menuu.add_command(label="Draw the wave", command=plot_waveform)
    Menuu.add_separator()
    Menuu.add_command(label="Change fast rate", command=change_ratef)
    Menuu.add_command(label="Change slow rate", command=change_rates)

    root.mainloop()

if __name__ == "__main__":
    main()