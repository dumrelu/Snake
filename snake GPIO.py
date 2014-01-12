#!/usr/bin/python
import time
import os
from random import randint

GPIO.setmode(GPIO.BCM);
BUTON_SUS=17;BUTON_JOS=22;BUTON_STANGA=27;BUTON_DREAPTA=4;
LED0=23;LED1=24;LED2=25;

GPIO.setup(BUTON_SUS,GPIO.IN);
GPIO.setup(BUTON_JOS,GPIO.IN);
GPIO.setup(BUTON_STANGA,GPIO.IN);
GPIO.setup(BUTON_DREAPTA,GPIO.IN);

GPIO.setup(LED0,GPIO.OUT);
GPIO.setup(LED1,GPIO.OUT);
GPIO.setup(LED2,GPIO.OUT);


#Dimensiunea tablei de joc
lungimeTabla = 10;
latimeTabla = 10;

#numarul total de vieti
numarVieti = 7;

#scorul(numar de mancare mancata
scor = 0;

#coordonatele unde se va afla mancarea pe tabla de joc
mancare=[0,0];

#directiile in care sarpele se poate misca
UP = [-1,0];
DOWN = [1,0];
LEFT = [0,-1];
RIGHT = [0,1];

class Sarpe:
    def __init__(self):
        #coordonatele capului sarpelui
        self.coordonate = [lungimeTabla/2,latimeTabla/2];

        #corpul sarpelui e format initial din 2 parti(3 in total cu capul)
        self.corp = [[self.coordonate[0], self.coordonate[1]+1], [self.coordonate[0], self.coordonate[1]+2]];

        #directia initiala a sarpelui
        self.directie = LEFT;

        #indica daca sarpele ar trebui sa-si mareasca dimensiunea data viitoare
        #cand se va misca
        self.shouldGrown = False;

    def grow(self):
        'Indica faptul ca la urmatoarea miscare sarpele trebuie sa se miste'
        self.shouldGrown = True;

    def reset(self):
        'Readuce sarpele la starea initiala'
        self.coordonate = [lungimeTabla/2,latimeTabla/2];
        self.corp = [[self.coordonate[0], self.coordonate[1]+1], [self.coordonate[0], self.coordonate[1]+2]];
        self.directie = LEFT;
        self.grown = False;

    def setDirectie(self, directie):
        'Seteaza directia in care se va misca sarpele'
        #directia nu poate sa fie opusul directiei curente
        if self.directie[0]!=-directie[0] or self.directie[0]!=-directie[0]:
            self.directie=directie;

    def move(self):
        'Misca sarpele in directia curent setata'
        
        #calculeaza coordonate noi
        coordonateNoi = [self.coordonate[0]+self.directie[0],self.coordonate[1]+self.directie[1]];

        #Verifica daca sarpele iese dupa tabla
        if coordonateNoi[0] < 0 or coordonateNoi[0] >= lungimeTabla or coordonateNoi[1] < 0 or coordonateNoi[1] >= latimeTabla:
            return False;

        #Verifica daca sarpele se loveste de propriul corp
        if coordonateNoi in self.corp:
            return False;
        
        #Memoreaza vechea coada sarpelui in caz ca va trebui adaugata o noua parte de corp
        coordonateCoadaVeche = self.corp[len(self.corp)-1];
        
        #Shifteaza corpul sarpelui
        for index in range(len(self.corp)-1, 0, -1):
            self.corp[index] = self.corp[index-1];
        self.corp[0] = self.coordonate;

        #actualizeaza coordonatele capului
        self.coordonate = coordonateNoi;

        #mareste sarpele daca este nevoie
        if self.shouldGrown:
            self.corp.append(coordonateCoadaVeche);
            self.shouldGrown = False;

        return True;

#sarpele
sarpe = Sarpe();




        

def clearScreen():
    'Sterge continutul curent dupa ecran'
    os.system('clear');

def genereazaMancare():
    'Genereaza aleator o mancare pe tabla care nu se suprapune cu sarpele'
    while True:
        mancare[0] =  randint(0,lungimeTabla-1);
        mancare[1] =  randint(0,latimeTabla-1);
        if mancare != sarpe.coordonate and mancare not in sarpe.corp:
            return;

def deseneazaTabla():
    'Afiseaza tabla de joc'

    #Sterge ce e pe ecran
    clearScreen();
    
    #genereaza o matrixe de 0-uri de dimensiunile: lungimeTabla x latimeTabla
    matrice = [[0 for x in xrange(latimeTabla)] for x in xrange(lungimeTabla)];

    'adauga sarpele in matrice'
    #capul sarpelui
    matrice[sarpe.coordonate[0]][sarpe.coordonate[1]] = 'O';
    #corpul sarpelui
    for parteCorp in sarpe.corp:
        matrice[parteCorp[0]][parteCorp[1]] = '*';

    #adauga mancarea in matrice
    matrice[mancare[0]][mancare[1]] = '@';

    #adauga matricei o margine
    matrice.insert(0, ['-' for x in xrange(latimeTabla+2)]);
    matrice.append(['-' for x in xrange(latimeTabla+2)]);
    for index in range(1, len(matrice)-1):
        matrice[index].insert(0, '|');
        matrice[index].append('|');

    #afiseaza matricea
    for rand in matrice:
	for coloana in rand:
            if coloana != 0:
                print coloana,
            else:
                print ' ',
        print

    #afiseaza vieti si scor
    print 'Vieti:',numarVieti,'Scor:',scor

def afiseazaVieti():
    ''''Afiseaza scorul in binar folosind LED-urile
        LED0 fiind cel mai putin semnificativ, LED2 cel mai semnificativ'''
    #reprezentare string a numarului de vieti in binar pe 3 biti
    binar = "{0:03b}".format(numarVieti);
    GPIO.output(LED2,bool(int(binar[0])));
    GPIO.output(LED1,bool(int(binar[1])));
    GPIO.output(LED0,bool(int(binar[2])));

def start():
    'Porneste jocul dupa o numaratoare inversa de la 3'
    #genereaza prima mancare
    genereazaMancare();
    
    deseneazaTabla();

    afiseazaVieti();
    
    #numaratoare inversa pana de la 3
    for i in range(3, 0,-1):
        print "Jocul incepe in:",i;
        time.sleep(1);
        deseneazaTabla();
    else:
        deseneazaTabla();
        print "GO!"
        sarpe.reset();
        time.sleep(0.5);


def puneDirectie():
    'Citeste directia de la butoane si o pune sarpelui'
    if GPIO.input(BUTON_SUS):
        sarpe.setDirectie(UP);
    elif GPIO.input(BUTON_JOS):
        sarpe.setDirectie(DOWN);
    elif GPIO.input(BUTON_STANGA):
        sarpe.setDirectie(LEFT);
    elif GPIO.input(BUTON_DREAPTA):
        sarpe.setDirectie(RIGHT);

    

if __name__=="__main__":
    #porneste jocul
    start();

    while numarVieti!=0:
        puneDirectie();
        
        if sarpe.move()==False:
            numarVieti-=1;
            if numarVieti!=0:
                print "Ai murit!"
                time.sleep(1);
                #reporneste jocul
                start();
                
        #daca sarpele a ajuns cu capul peste mancare, mananc-o
        if mancare == sarpe.coordonate:
            sarpe.grow();
            genereazaMancare();
            scor += 1;

        deseneazaTabla();
        time.sleep(0.15);
        
        

    print "Game over! Scorul tau final:", scor;
