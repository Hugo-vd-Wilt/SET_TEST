#Engelse kleuren
N2C = {1:"red", 2:"green", 3:"purple"}
#Engelse vormen
N2S = {1:"oval", 2:"squiggle", 3:"diamond"}
#Engelse vullingen
N2F = {1:"empty", 2:"shaded", 3:"filled"}


#Deze returnt welke eigenschap (1,2,3) gewenst is
# VB: 1,1 -> 1 ; 1,2 -> 3
def overeenkomst(a, b, eigenschap:str):
    if not type(a) == Set and type(b) == Set:
        raise TypeError("Dit moet voor set kaarten")
        
    a , b = vars(a)[eigenschap] , vars(b)[eigenschap]
    # a en b zijn dus int's in [1,2,3]
    if a == b:
        return a
    else:
        x=[1,2,3]
        x.remove(a)
        x.remove(b)
        return x[0]
  
    
#Deze returnt de naam van de foto zoals gegeven in de opdracht
def image_name(card):
    if not type(card)==Set:
        raise TypeError("Dit moet voor set kaarten")
    else:
        TEXT = str(card)
        return TEXT.replace(" ","")+".gif"

#Deze vind, in een lijst van set kaarten, alle sets
def find_all_sets(lijst):
    setjes = []
    for kaart1 in lijst:
        for kaart2 in lijst:
            if kaart1 != kaart2 and kaart1+kaart2 in lijst:
                setjes.append((kaart1, kaart2, kaart1+kaart2))
    return setjes

#functie returnt een set
def find_a_set(lijst):
    import random
    setjes = find_all_sets(lijst)
    N = len(setjes)
    return setjes[random.randint(0,N-1)]

def is_set(kaart1, kaart2, kaart3):
    return (kaart1 + kaart2) == kaart3


class Set:
    def __init__ (self, kleur = 3, vorm = 1, vulling = 1, aantal = 3 ):
        self.kleur = kleur
        self.vulling = vulling
        self.aantal = aantal
        self.vorm = vorm
    
    def __str__(self):
        self=vars(self)
        C = self['kleur']
        F = self['vulling']
        a = self['aantal']
        S = self['vorm']
        return N2C[C] + " " + N2S[S] + " " + N2F[F] + " " + str(a) 
    
    def __print__(self):
        return str(self)
    
    def __repr__(self):
        return str(self)
    
    def __add__(self,other):
        r = Set()
        r.kleur = overeenkomst(self, other, "kleur")
        r.vorm = overeenkomst(self, other, "vorm")
        r.vulling = overeenkomst(self, other, "vulling")
        r.aantal = overeenkomst(self, other, "aantal")
        return r

    def __eq__ (self, other):
        return vars(self) == vars(other)
    
    def __neq__(self,other):
        return not self == other


    