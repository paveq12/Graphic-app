# -*- coding: utf-8 -*-

from tkinter.ttk import Frame, Style, Label, Entry, Button, Combobox
from tkinter import BOTH, Tk, W, E, N, S, Canvas, NW, messagebox
from PIL import Image, ImageTk, ImageFilter

max_h=500
max_w=900

class Okno(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent=parent
        self.inicjalizuj()
    def wczytaj_ponownie(self):
        #przezkalowanie do maksymalnych rozmiarów kontrolki canvas
        szer,wys=self.im.size
        factor_w=1 #mnożnik dla w
        factor_h=1 #mnożnik dla h
        if szer>max_w:
            factor_w=max_w/szer
        if wys>max_h:
            factor_h=max_h/wys
        if factor_h>=factor_w:
            factor=factor_w
        else:
            factor=factor_h
        size=int(szer*factor),int(wys*factor)
        ####
        self.image=ImageTk.PhotoImage(self.im.resize(size))
        self.podst.create_image(0,0,image=self.image, anchor=NW)
    def wczytaj_obraz(self):
        sciezka=self.o.get()
        try:
            self.im=Image.open(sciezka)
            self.fbtn.config(state='normal')
            self.zbtn.config(state='normal')
            self.sbtn.config(state='normal')
            self.pbtn.config(state='normal')
            self.obraz_oryg=self.im
            self.wczytaj_ponownie()
        except FileNotFoundError:
            messagebox.showerror('Błąd!','Plik nie istnieje!')
        except OSError:
            messagebox.showerror('Błąd!','Podaj plik graficzny!')


    def skaluj(self):
        w,h=self.im.size
        mnoznik=float(self.scbox.get())
        size=int(w*mnoznik),int(h*mnoznik)
        self.im=self.im.resize(size)
        self.wczytaj_ponownie()

    def przywroc_obraz(self):
        self.im=self.obraz_oryg
        self.wczytaj_ponownie()

    def zapisz(self):
        sciezka=self.z.get()
        if sciezka=='':
            sciezka=self.o.get()

        self.im.save(sciezka)

    def zastosuj_filtr(self):
        filtr=self.fcbox.get()
        if filtr=='BLUR':
            self.im=self.im.filter(ImageFilter.BLUR)
        elif filtr=='CONTOUR':
            self.im=self.im.filter(ImageFilter.CONTOUR)
        else:
            self.im = self.im.filter(ImageFilter.EMBOSS)
        self.wczytaj_ponownie()
    def inicjalizuj(self):
        self.parent.title("Program graficzny")
        self.styl=Style()
        self.styl.theme_use("winnative")
        self.pack(fill=BOTH,expand=1)
        self.columnconfigure(1,weight=1)
        etykieta=Label(self, text="Ścieżka do pliku:")
        etykieta.grid(sticky=W, pady=4, padx=5)

        self.o=Entry(self)
        self.o.grid(row=1, column=0, columnspan=2, rowspan=1, padx=5, pady=4, sticky=E+W+S+N)

        self.z = Entry(self)
        self.z.grid(row=2, column=0, columnspan=2, rowspan=1, padx=5, pady=4, sticky=E+W+S+N)

        otbtn=Button(self, text="Otwórz", command=self.wczytaj_obraz)
        otbtn.grid(row=1, column=3)

        self.zbtn=Button(self, text="Zapisz", command=self.zapisz)
        self.zbtn.grid(row=2, column=3)
        self.zbtn.config(state='disabled')

        self.scbox=Combobox(self, values='0.1 0.2 0.3 0.4')
        self.scbox.current(0)
        self.scbox.grid(row=3, column=0, padx=5, pady=4, sticky=W+N)

        self.fcbox=Combobox(self, values='BLUR CONTOUR EMBOSS')
        self.fcbox.current(0)
        self.fcbox.grid(row=4, column=0, padx=5, pady=4, sticky=W+N)

        self.sbtn=Button(self, text="Skaluj", command=self.skaluj)
        self.sbtn.grid(row=3, column=1, padx=5, pady=4, sticky=W+N)
        self.sbtn.config(state='disabled')

        self.fbtn = Button(self, text="Filtruj", command=self.zastosuj_filtr)
        self.fbtn.grid(row=4, column=1, padx=5, pady=4, sticky=W+N)
        self.fbtn.config(state='disabled')


        self.podst=Canvas(self, width=max_w, height=max_h)
        self.podst.grid(row=5, column=0, padx=5, pady=4, sticky=E+W+S+N, columnspan=3)

        self.pbtn = Button(self, text="Przywróć", command=self.przywroc_obraz)
        self.pbtn.grid(row=5, column=3, padx=5, pady=4, sticky=W + N)
        self.pbtn.config(state='disabled')

def main():
    gui=Tk()
    gui.geometry("1000x700")
    app=Okno(gui)
    gui.mainloop()

if __name__ == '__main__':
    main()