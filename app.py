from tkinter import *
from PIL import ImageTk, Image
import functions as f
import os

load=False #czy plik zostal wczytany
global sound
global Window
global img

# ścieżka do pliku
fileDir = os.path.dirname(os.path.realpath('__file__'))
path = os.path.join(fileDir, 'sounds\\')

# klasa areny aplikacji okienkowej
class App(object):
    # konstruktor tworzący arenę
    def __init__(self):
        global Window
        Window=Tk()
        Window.attributes("-fullscreen", True)
        Window.title("Procesor dzwiekowy")
        Window.configure(background='silver')

    # metoda uruchamiająca funkcję wczytaj
    def click_load(self):
        global sound
        global load
        entered_text=name_entry.get()

        if os.path.exists(path+str(entered_text)+".wav"):
            sound=f.Functions(path+str(entered_text)+".wav")
            load=True
            output.delete(0.0,END)
            output.insert(END,"Udało się wczytać plik "+str(entered_text)+
            ".\nMożna przeprowadzić wybraną powyżej funkcję")
            self.visual()
        else:
            output.delete(0.0,END)
            output.insert(END,"Podany plik nie istnieje!\n")

    # metoda uruchamiająca funkcję zapisz
    def click_save(self):
        nfile=save_entry.get()
        if load == False:
            output.delete(0.0,END)
            output.insert(END,"Nie wczytano pliku.\n")
        else:
            sound.save(path+str(nfile)+".wav")
            output.delete(0.0,END)
            output.insert(END,"Udało się zapisał plik.\n")
            self.visual()

    # metoda zamykająca aplikację
    def click_exit(self):
        Window.destroy()
        exit()

    # metoda uruchamiająca funkcję zagrania utworu
    def click_play(self):
        if load == False:
            output.delete(0.0,END)
            output.insert(END,"Nie wczytano pliku.\n")
        else:
            output.delete(0.0,END)
            output.insert(END,"Utwór został odtworzony.\n")
            sound.play()

    # metoda uruchamiająca funkcję nałożenia echa
    def click_echo(self):
        time=float(echo_entry.get())
        if load == False:
            output.delete(0.0,END)
            output.insert(END,"Nie wczytano pliku.\n")
        else:
            if time<len(sound.data)/sound.fs:
                sound.echo(time)
                output.delete(0.0,END)
                output.insert(END,"Efekt nałożony (Echo).\n")
                self.visual()
            else:
                output.delete(0.0,END)
                output.insert(END,"Podany czas musi być mniejszy niż czas trwania utworu.")

    # metoda uruchamiająca funkcję nałożenia odwrócenia
    def click_reverse(self):
        if load == False:
            output.delete(0.0,END)
            output.insert(END,"Nie wczytano pliku.\n")
        else:
            sound.reverse()
            output.delete(0.0,END)
            output.insert(END,"Efekt nałożony (Odwrócenie).\n")
            self.visual()

    # metoda uruchamiająca funkcję zmiany głośności
    def click_volume(self):
        gain=float(volume_entry.get())
        if load == False:
            output.delete(0.0,END)
            output.insert(END,"Nie wczytano pliku.\n")
        else:
            if gain < 0:
                output.delete(0.0,END)
                output.insert(END,"Wprowadza się tylko dodatnie liczby.\n"+
                            "Zakres wprowadzanych liczb: [0;N], gdzie 0 całkowicie wycisza utwór\n")
            else:
                sound.volume(gain)
                output.delete(0.0,END)
                output.insert(END,"Efekt nałożony (Zmiana głośności).\n")
                self.visual()

    # metoda uruchamiająca funkcję zmiany prędkości
    def click_speed(self):
        gain=float(speed_entry.get())
        if load == False:
            output.delete(0.0,END)
            output.insert(END,"Nie wczytano pliku.\n")
        else:
            if gain <= 0:
                output.delete(0.0,END)
                output.insert(END,"Wprowadza się tylko dodatnie liczby.\n"+
                            "Zakres wprowadzanych liczb: (0;N]\n")
            else:
                sound.speed(gain)
                output.delete(0.0,END)
                output.insert(END,"Efekt nałożony (Zmiana prędkości).\n")
                self.visual()

    # metoda uruchamiająca funkcję przycięcia
    def click_cut(self):
        t=cut_entry.get()
        T=t.split(sep=" ")
        t1=float(T[0])
        t2=float(T[1])
        if load == False:
            output.delete(0.0,END)
            output.insert(END,"Nie wczytano pliku.\n")
        else:
            if t1 < 0 or t2 < 0 :
                output.delete(0.0,END)
                output.insert(END,"Wprowadza się tylko dodatnie liczby.\n"+
                            "Zakres wprowadzanych liczb: [0;N)\n")
            else:
                if t2<t1:
                    output.delete(0.0,END)
                    output.insert(END,"Błąd podania kolejności czasów na przycięcie utworu\n")
                else:
                    if t2>len(sound.data)/sound.fs:
                        output.delete(0.0,END)
                        output.insert(END,"Górny zakres przycięcia wykracza poza długość utworu\n")
                    else:
                        sound.cut(t1,t2)
                        output.delete(0.0,END)
                        output.insert(END,"Efekt nałożony (Przycięcie).\n")
                        self.visual()

    # metoda uruchamiająca funkcję liczenia rms
    def click_rms(self):
        if load == False:
            output.delete(0.0,END)
            output.insert(END,"Nie wczytano pliku.\n")
        else:
            l,p,ster=sound.true_rms()
            output.delete(0.0,END)
            output.insert(END,"Wyniki badania:\nKanał lewy: %.3f dB\nKanał prawy: %.3f dB\nStereo: %.3f dB" %(l,p,ster))
            self.visual()

    # metoda uruchamiająca funkcję wizualizacji utworu
    def visual(self):
        global img
        if load == False:
            output.delete(0.0,END)
            output.insert(END,"Nie udało się wygenerować pliku obrazu.\n")
        else:
            sound.visual()
            img=ImageTk.PhotoImage(Image.open("out_sound.jpg"))
            os.remove("out_sound.jpg")
            label=Label(Window,image=img).grid(row=48,column=0)
            label.pack()

# Tworzenie areny
A=App()

#========================== Pola Tekstowe ======================================
Label(Window,text="Podaj nazwę pliku do wczytania (format wav):",bg='silver',fg='navy',font='none 12 bold').grid(row=0,column=0,sticky=W)
Label(Window,text="Zapis pliku z pamięci podręcznej",bg='silver',fg='navy',font='none 12 bold').grid(row=1,column=0,sticky=W)
Label(Window,text="Zagraj utwór z pamięci podręcznej",bg='silver',fg='navy',font='none 12 bold').grid(row=2,column=0,sticky=W)
Label(Window,text="\n",bg='silver',fg='navy',font='none 12 bold').grid(row=3,column=0,sticky=W)
Label(Window,text="-Echo- Nakłada echo po podanym czasie. Podaj czas [s] opoznienia: ",bg='silver',fg='navy',font='none 12 bold').grid(row=4,column=0,sticky=W)
Label(Window,text="-Odwrócenie- Puszcza otwór od końca",bg='silver',fg='navy',font='none 12 bold').grid(row=5,column=0,sticky=W)
Label(Window,text="-Zmiana głośności- Zmienia głośność. Podaj wzmocnienie/tłumienie:",bg='silver',fg='navy',font='none 12 bold').grid(row=6,column=0,sticky=W)
Label(Window,text="-Zmiana prędkości- Podaj skalowanie prędkości:",bg='silver',fg='navy',font='none 12 bold').grid(row=7,column=0,sticky=W)
Label(Window,text="-Pomiar RMS- ",bg='silver',fg='navy',font='none 12 bold').grid(row=8,column=0,sticky=W)
Label(Window,text="-Przycięcie utworu. Podaj czasy startu i zakończenia oddzielone spacją [t1 t2]:",bg='silver',fg='navy',font='none 12 bold').grid(row=10,column=0,sticky=W)
Label(Window,text="Zamknięcie programu:",bg='silver',fg='navy',font='none 12 bold').grid(row=50,column=2,sticky=W)

#======================== Pola interakcyjne ====================================
#pole do wczytania pliku
name_entry=Entry(Window,width=10,bg="white")
name_entry.grid(row=0,column=1,sticky=W)

#pole do zapisu pliku
save_entry=Entry(Window,width=10,bg="white")
save_entry.grid(row=1,column=1,sticky=W)

#pole do echo
echo_entry=Entry(Window,width=10,bg="white")
echo_entry.grid(row=4,column=1,sticky=W)

#pole do glosnosci
volume_entry=Entry(Window,width=10,bg="white")
volume_entry.grid(row=6,column=1,sticky=W)

#pole do predkosci
speed_entry=Entry(Window,width=10,bg="white")
speed_entry.grid(row=7,column=1,sticky=W)

#pole do odciecia
cut_entry=Entry(Window,width=10,bg="white")
cut_entry.grid(row=10,column=1,sticky=W)

#=============================== Przyciski =====================================
Button(Window,text="Wczytaj",width=10,command=A.click_load).grid(row=0,column=3,sticky=W) #wczytanie nazwy pliku
Button(Window,text="Zapisz",width=10,command=A.click_save).grid(row=1,column=3,sticky=W) #zapisanie pliku
Button(Window,text="Graj",width=10,command=A.click_play).grid(row=2,column=3,sticky=W) #zagraj utwor
Button(Window,text="Przetworz",width=10,command=A.click_echo).grid(row=4,column=3,sticky=W) #echo
Button(Window,text="Przetworz",width=10,command=A.click_reverse).grid(row=5,column=3,sticky=W) #odwrocenie
Button(Window,text="Przetworz",width=10,command=A.click_volume).grid(row=6,column=3,sticky=W) #glośnosc
Button(Window,text="Przetworz",width=10,command=A.click_speed).grid(row=7,column=3,sticky=W) #predkosc
Button(Window,text="Oblicz",width=10,command=A.click_rms).grid(row=8,column=3,sticky=W) #rms
Button(Window,text="Przetworz",width=10,command=A.click_cut).grid(row=10,column=3,sticky=W) #przyciecie

Button(Window,text="Zakoncz",width=10,command=A.click_exit).grid(row=50,column=3,sticky=W) #zakonczenie pracy programu

#============================= Pole komunikatow ================================
output=Text(Window,width=80,height=4,wrap=WORD,background='white')
output.grid(row=40,column=0,sticky=W)

# nieskończona pętla utworu
Window.mainloop()
