import Set_class
Set = Set_class.Set 
image_name = Set_class.image_name
find_a_set = Set_class.find_a_set
find_all_sets = Set_class.find_all_sets
is_set = Set_class.is_set

import pygame
import random
import time
import os
pygame.init()

PLAYER_SCORED = pygame.USEREVENT + 1
COMPUTER_SCORED = pygame.USEREVENT + 2

WIDTH , HEIGHT = 1000 , 800
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Speel SET tegen de computer!")

CARD_WIDTH , CARD_HEIGHT = 100 , 200

def card_image(card):
    return pygame.image.load(os.path.join('kaarten', image_name(card)))

KAARTEN_IN_POT = [(Set(a,b,c,d) , card_image(Set(a,b,c,d))) 
                  for a in range(1,4) for b in range(1,4) for c in range(1,4) for d in range(1,4)]
KAARTEN_OP_SCHERM = []
KAARTEN_AL_GESPEELD = []

RICK_ROLL = pygame.mixer.Sound(os.path.join('Audio', 'Never Gonna Give You Up Original.mp3'))
CHILDREN_CHEERING = []
for i in range(4):
    CHILDREN_CHEERING.append( pygame.mixer.Sound(os.path.join('Audio','beloning', 'KID_'+str(i+1)+'.mp3')) )

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
PURPLE = (210, 26, 210) 

TITLE_FONT = pygame.font.SysFont('comicsans', 50)
SMALL_FONT = pygame.font.SysFont('comicsans', 25)

TITLE_KLEUR = BLACK
SMALL_KLEUR = BLACK

FPS = 60

LIJST_VAN_RECTS = []
for n in range(12):
    CARD_DISTANCE = 25
    CARD_POS = (50 + (CARD_WIDTH + CARD_DISTANCE) * (n // 3) , 100 + (CARD_HEIGHT + CARD_DISTANCE) * (n % 3))
    x = pygame.Rect(CARD_POS[0] - CARD_DISTANCE // 3 , CARD_POS[1] - CARD_DISTANCE // 3 ,
                    CARD_WIDTH + CARD_DISTANCE * 2 // 3 ,  CARD_HEIGHT + CARD_DISTANCE * 2 // 3 )
    LIJST_VAN_RECTS.append(x)
 

RECT_WIDTH = 350
RECT_HEIGHT = 50
DROP_SIZE = 6
X_CORD = 600
Y_CORD = 500
DROP = pygame.Rect(X_CORD - DROP_SIZE ,Y_CORD - DROP_SIZE ,
                   RECT_WIDTH + 2 * DROP_SIZE, RECT_HEIGHT + 2 * DROP_SIZE)
BOVEN = pygame.Rect(X_CORD  ,Y_CORD  , RECT_WIDTH , RECT_HEIGHT )
    
#Tekent het scherm
def draw_window(KAARTEN_OP_SCHERM ,KAARTEN_IN_POT, punten_speler, punten_comp, 
                tijd_0 ,Time_left , LIJST_VAN_RECTS, LIJST_VAN_GESELECTEERDE_KAARTEN, DROP, BOVEN):
    WIN.fill(CYAN)
    draw_title = TITLE_FONT.render('SET spelen', 1, TITLE_KLEUR)
    WIN.blit(draw_title, (WIDTH // 2 - draw_title.get_width() // 2, 0 ))
    
    Trios = find_all_sets([kaart[0] for kaart in KAARTEN_OP_SCHERM])
    if Trios !=[]:
        if len(Trios) // 6 == 1:
            Mogelijkheid_text = "Er is 1 set op het scherm"
        else:
            Mogelijkheid_text = "Er zijn " + str(len(Trios) // 6)+" sets op het scherm"
    else:
        Mogelijkheid_text = "Er zijn geen sets op het scherm"
    
    draw_mogelijkheid = SMALL_FONT.render(Mogelijkheid_text, 1, SMALL_KLEUR)
    WIN.blit(draw_mogelijkheid, (600 , 450  )) 
    
    Nieuwe_kaarten = SMALL_FONT.render('Nieuwe kaarten', 1, SMALL_KLEUR )
    
    pygame.draw.rect(WIN, BLACK, DROP)
    pygame.draw.rect(WIN, PURPLE, BOVEN)
    WIN.blit(Nieuwe_kaarten, (DROP.x + DROP.width // 2 - Nieuwe_kaarten.get_width() // 2, 
                              DROP.y + DROP.height // 2 -  Nieuwe_kaarten.get_height() // 2))
    
    draw_jouw_punten = SMALL_FONT.render('Jouw punten: ' + str(punten_speler), 1, SMALL_KLEUR)
    WIN.blit(draw_jouw_punten, (600 , 200))
    
    draw_comp_punten = SMALL_FONT.render('Punten computer: ' + str(punten_comp), 1, SMALL_KLEUR)
    WIN.blit(draw_comp_punten, (600 , 225))

    draw_pot= SMALL_FONT.render("Kaarten in de pot: " + str(len(KAARTEN_IN_POT)), 1, SMALL_KLEUR)
    WIN.blit(draw_pot, (10 , 0))
    
    txt = "{MIN:02} : {SEC:02}"
    
    Ronde_tijd = Time_left
    draw_Sessie_time = SMALL_FONT.render('Tijd over: ' + txt.format(MIN = Ronde_tijd//60 , SEC = Ronde_tijd%60) , 1, SMALL_KLEUR)
    WIN.blit(draw_Sessie_time, (600 , 150))
    
    Sessie_tijd = int(time.perf_counter()-tijd_0)
    draw_Sessie_time = SMALL_FONT.render(txt.format(MIN = Sessie_tijd//60 , 
                                                    SEC = Sessie_tijd%60) 
                              , 1, SMALL_KLEUR)
    WIN.blit(draw_Sessie_time, (WIDTH - 100 , 0))
    
    for n in LIJST_VAN_GESELECTEERDE_KAARTEN:
        pygame.draw.rect(WIN, BLACK, LIJST_VAN_RECTS[n])
    
    CARD_DISTANCE = 25
    n=0
    for kaart in KAARTEN_OP_SCHERM:
        CARD_POS = (50 + (CARD_WIDTH + CARD_DISTANCE) * (n // 3) , 100 + (CARD_HEIGHT + CARD_DISTANCE) * (n % 3))
        
        WIN.blit(kaart[1], CARD_POS)
        n+=1
        
    pygame.display.update()
      
#Voegt een willekeurige kaart toe aan de lijst van kaarten op scherm, haalt hem uit pot
def add_card(KAARTEN_IN_POT , KAARTEN_OP_SCHERM):
    RANDOM_NUMBER = random.randint(0,len(KAARTEN_IN_POT)-1)
    card = KAARTEN_IN_POT[RANDOM_NUMBER]
    
    KAARTEN_OP_SCHERM.append(card)
    KAARTEN_IN_POT.remove(card)
 
#Verwijderd een kaart van de lijst van kaarten op scherm, 
# voegt hem toe aan lijst van kaarten die al gespeeld zijn
def remove_card(card , KAARTEN_OP_SCHERM , KAARTEN_AL_GESPEELD):
    KAARTEN_OP_SCHERM.remove(card)
    KAARTEN_AL_GESPEELD.append(card)
  
def replace_cards(lijst ,KAARTEN_IN_POT, KAARTEN_OP_SCHERM , KAARTEN_AL_GESPEELD ):
    for card in lijst:
        i=KAARTEN_OP_SCHERM.index(card)
        RANDOM_NUMBER = random.randint(0,len(KAARTEN_IN_POT)-1)
        
        Ncard = KAARTEN_IN_POT[RANDOM_NUMBER]
        KAARTEN_IN_POT.remove(Ncard)
        KAARTEN_OP_SCHERM[i] =  Ncard
        KAARTEN_AL_GESPEELD.append(card) 

def check_set(LIJST_VAN_GESELECTEERDE_KAARTEN, KAARTEN_OP_SCHERM,  
              KAARTEN_AL_GESPEELD, punten_speler, punten_comp, tijd_r ):
    Lijst_van_tupels = [ KAARTEN_OP_SCHERM[i] for i in  LIJST_VAN_GESELECTEERDE_KAARTEN]
    lijst = [kaart[0] for kaart in Lijst_van_tupels]
    if is_set(lijst[0], lijst[1], lijst[2]):
        pygame.event.post(pygame.event.Event(PLAYER_SCORED))       
    else:
        pygame.event.post(pygame.event.Event(COMPUTER_SCORED)) 
    
    while LIJST_VAN_GESELECTEERDE_KAARTEN != []:
        i= LIJST_VAN_GESELECTEERDE_KAARTEN[0]
        replace_cards([ KAARTEN_OP_SCHERM[i] ] ,KAARTEN_IN_POT, KAARTEN_OP_SCHERM , KAARTEN_AL_GESPEELD)
        LIJST_VAN_GESELECTEERDE_KAARTEN.remove(i)
    
# De main
def main():
    TIJD_MAX = 30

    tijd_0 = time.perf_counter()
    tijd_r = time.perf_counter()
    punten_speler = 0
    punten_comp = 0
    
    # kaart1 = pygame.Rect(50, 75, CARD_WIDTH, CARD_HEIGHT)
    for i in range(12):
        add_card(KAARTEN_IN_POT , KAARTEN_OP_SCHERM)
    
    LIJST_VAN_GESELECTEERDE_KAARTEN = []    
    
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        
        Time_left = int(TIJD_MAX-(time.perf_counter()-tijd_r) + 1)
        
        if Time_left <= 0:
            LIJST_VAN_GESELECTEERDE_KAARTEN = []
            lijst_met_kaarten = [ kaart[0] for kaart in KAARTEN_OP_SCHERM ]
            een_set = find_a_set(lijst_met_kaarten)
            weg_te_halen = []
            for kaart in KAARTEN_OP_SCHERM:
                if kaart[0] in een_set:
                    weg_te_halen.append(kaart)
            
            for kaart in weg_te_halen:
                LIJST_VAN_GESELECTEERDE_KAARTEN.append(KAARTEN_OP_SCHERM.index(kaart))  
            
            for t in range(2):
                draw_window(KAARTEN_OP_SCHERM ,KAARTEN_IN_POT, punten_speler, punten_comp, 
                        tijd_0,  Time_left , LIJST_VAN_RECTS, LIJST_VAN_GESELECTEERDE_KAARTEN, DROP, BOVEN)        
                pygame.time.delay(1000) 
            
            pygame.event.post(pygame.event.Event(COMPUTER_SCORED))
            replace_cards(weg_te_halen ,KAARTEN_IN_POT, KAARTEN_OP_SCHERM , KAARTEN_AL_GESPEELD)
            
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type  == pygame.KEYDOWN:
    
                # if event.key == pygame.K_p:
                #     i = random.randint(0, len(CHILDREN_CHEERING)-1)
                #     CHILDREN_CHEERING[i].play()
                #     punten_speler +=1
                    
                # if event.key == pygame.K_c:
                #     punten_comp += 1
                    
                if event.key == pygame.K_r:
                    RICK_ROLL.play()
                    pygame.time.delay(5 * 1000)
                    RICK_ROLL.stop()
                   
            #Selecteren van een kaart
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                MUIS = pygame.Rect(pos[0], pos[1], 1, 1)
                for RECT in LIJST_VAN_RECTS:
                    if RECT.colliderect(MUIS):
                        i = LIJST_VAN_RECTS.index(RECT)
                        
                        if i in LIJST_VAN_GESELECTEERDE_KAARTEN:
                            LIJST_VAN_GESELECTEERDE_KAARTEN.remove(i)
                        else:
                            LIJST_VAN_GESELECTEERDE_KAARTEN.append(i)
                    
                if DROP.colliderect(MUIS):
                    replace_cards(KAARTEN_OP_SCHERM, KAARTEN_IN_POT, KAARTEN_OP_SCHERM, KAARTEN_IN_POT)
                    LIJST_VAN_GESELECTEERDE_KAARTEN = []
                    tijd_r = time.perf_counter()
            
            
            if event.type == PLAYER_SCORED:
                i = random.randint(0, len(CHILDREN_CHEERING)-1)
                CHILDREN_CHEERING[i].play(fade_ms = 2000)
                punten_speler +=1
                tijd_r = time.perf_counter()
                
            if event.type == COMPUTER_SCORED:
                punten_comp +=1
                tijd_r = time.perf_counter()
           
        if  find_all_sets([kaart[0] for kaart in KAARTEN_OP_SCHERM]) == []:
            draw_window(KAARTEN_OP_SCHERM ,KAARTEN_IN_POT, punten_speler, punten_comp, 
                    tijd_0,  Time_left , LIJST_VAN_RECTS, LIJST_VAN_GESELECTEERDE_KAARTEN, DROP, BOVEN)
            pygame.time.delay(1000) 
            
            draw_window(KAARTEN_OP_SCHERM ,KAARTEN_IN_POT, punten_speler, punten_comp, 
                    tijd_0,  Time_left , LIJST_VAN_RECTS, LIJST_VAN_GESELECTEERDE_KAARTEN, DROP, BOVEN)
            
            replace_cards(KAARTEN_OP_SCHERM, KAARTEN_IN_POT, KAARTEN_OP_SCHERM, KAARTEN_IN_POT)
            LIJST_VAN_GESELECTEERDE_KAARTEN = []
           
        
        if len(LIJST_VAN_GESELECTEERDE_KAARTEN) == 3:
            check_set(LIJST_VAN_GESELECTEERDE_KAARTEN, KAARTEN_OP_SCHERM,  
                      KAARTEN_AL_GESPEELD, punten_speler, punten_comp, tijd_r )
                
        
        draw_window(KAARTEN_OP_SCHERM ,KAARTEN_IN_POT, punten_speler, punten_comp, 
                tijd_0,  Time_left , LIJST_VAN_RECTS, LIJST_VAN_GESELECTEERDE_KAARTEN, DROP, BOVEN)

if __name__ == "__main__":
    main()

