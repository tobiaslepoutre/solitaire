# Marc-Olivier Morin (20187831 ) et Tobias Lepoutre (20177637)

import random
import math

# tableau contenant toute les svg des cartes
cards = ['2C.svg', '2D.svg', '2H.svg', '2S.svg', '3C.svg', '3D.svg', '3H.svg', '3S.svg', '4C.svg', '4D.svg', '4H.svg', '4S.svg', '5C.svg', '5D.svg', '5H.svg', '5S.svg', '6C.svg', '6D.svg', '6H.svg', '6S.svg', '7C.svg', '7D.svg', '7H.svg', '7S.svg', '8C.svg', '8D.svg', '8H.svg', '8S.svg', '9C.svg', '9D.svg', '9H.svg', '9S.svg', '10C.svg', '10D.svg', '10H.svg', '10S.svg','JC.svg', 'JD.svg', 'JH.svg', 'JS.svg', 'QC.svg', 'QD.svg', 'QH.svg', 'QS.svg', 'KC.svg', 'KD.svg', 'KH.svg', 'KS.svg','empty.svg']

# fonction qui prend en paramètre un tableau (vide si il n'y une crée une nouvelle matrice, ou une liste contenant
# les cartes à ne pas brasser lorsque le boutton brasser est appuyé. retourne une matrice contentant 4 tableau de 13
# chiffres aléatoire non répétitif (sauf pour les cases vide qui sont représentés par des -1). Chaque chiffres est la
# position à aller chercher dans le liste cards lors de l'affichage 
def createMatrix(noMatrix):
    nbCards =48                               
    tab=[[],[],[],[]]

    listOrdRef=list(range(nbCards))                 # créé une liste de 48
    print(listOrdRef)
    for _ in range(4):                              # rajoute case vide
        listOrdRef.append(-1)

    nbCards +=4
    rangee=nbCards/4

    for exception in noMatrix:                      # met les positions qui ne doit pas être déplacé
        listOrdRef.remove(exception[0])
        tab[exception[1]].append(exception[0])
        nbCards-=1

    for i in tab:                                  
        while len(i)<rangee:
            x=math.floor(random.random() * nbCards) # mélange les cartes 
            i.append(listOrdRef[x])
            listOrdRef.pop(x)
            nbCards-=1
         
    return tab

# variable à utilisé à travers le programme 
matrix = createMatrix([])
nbBrasser = 3
styleHTML = """\
<style>
    #jeu table { float: none; }
    #jeu table td { border: 0; padding: 1px 2px; height: auto; }
    #jeu table td img { height: auto; }
</style>
"""
buttonShuffle="""
    <br><br>
    <div id="message"> 

    <p style="display:inline-block; text-indent:2ch;">Vous pouvez encore</p>
    <button onclick="brasser()" style="display:inline-block">
    Brasser les cartes</button>
    <p id ="nbShuffle" style="display:inline-block"></p>
    
    </div>
    """
buttonRedo = """
    <br>
    <div style="text-indent:2ch;">
    <button onclick="recommencer()">Nouvelle partie</button>
    </div>
    """


# fonction qui prend deux strings en paramètre et retourne une string contenant la balise <td> pour l'afficahge HTML
def tdHTML(attrs, contenu):
    return '<td'+attrs+'>'+contenu+'</td>'

# fonction qui prend une string en paramètre et retourne une string contenant la balise <img> pour l'afficahge HTML
def imgHTML(src):
    return '<img src=" cards/'+ src +'">'

# fonction qui prend une string en paramètre et retourne une string contenant la balise <tr> pour l'afficahge HTML
def trHTML(contenu):
    return '<tr>' + contenu + '</tr>'

# fonction qui prend une string en paramètre et retourne une string contenant la balise <table> pour l'afficahge HTML
def tableHTML(contenu):
    return '<div id="jeu"> <table>' + contenu + '</table> </div>'


# fonction qui permet créer une string pour l'affichage HTML à partir de la matrice matrix qui est créé par la
# fonction create matrix
def arrayHTML():
    arrayText = ""
    for i in range(len(matrix)):                                        # passe à travers chaque list de matrix
        arrayTextInner = ""
        for j in range (len(matrix[i])):                                # passe à travers chaque nombres dans les listes

            case = str(j+i*len(matrix[i]))
            temp = imgHTML(cards[matrix[i][j]])                         # assigne le id et le onclick au td
            temp1 = ' id="case' + case +'" onclick="clic(' + case +')"'
            arrayTextInner += tdHTML(temp1,temp)
            
        arrayText += trHTML(arrayTextInner)
    return tableHTML(arrayText)

# fonction permettant de brasser les cartes tout en préservant les cartes déjà placées.
def brasser():
    global matrix; global nbBrasser
    
    noMatrix=[]
    rangee=len(matrix[0])
    for r in range(4):                                 # pour chaque rangée: 
        if matrix[r][0]<=3 and matrix[r][0]>-1:        # si la première carte de la rangée est un deux:
            noMatrix.append([matrix[r][0],r])          # ajouter la carte à noMatrix
            for i in range(1,rangee):                  # pour chaque carte de cette rangé suivant le deux
                if matrix[r][i]==4*i+matrix[r][0]:     # si la carte suivante correspond bien à la suite d'une même couleur:
                    noMatrix.append([matrix[r][i],r])  # ajouter la valeur de la carte suivante à noMatrix
                else:
                    break                              # sinon passer a la rangée suivante

    matrix =createMatrix(noMatrix)
    nbBrasser -=1
    ifOver()
    init()

# fonction qui détermine si elle est encore possible de brasser. Si il n'est pu possible de brasser, elle enlève le 
# bouton qui permet de brasser  
def ifOver():
    global buttonShuffle
    if nbBrasser <= 0: 
        buttonShuffle="""
        <br><br>
        <div id="message"> 
        <p style="display:inline-block; text-indent:2ch;">Vous ne pouvez plus brasser</p>
        </div>
        """

# fonction permettant de recommencer une partie en remttant tout les paramêtres
# à leur état initial.
def recommencer():
    global nbBrasser; global matrix; global buttonShuffle   
    nbBrasser=3                                                               
    matrix=createMatrix([])
    buttonShuffle="""
    <br><br>
    <div id="message"> 
    <p style="display:inline-block; text-indent:2ch;">Vous pouvez encore</p>
    <button onclick="brasser()" style="display:inline-block">
    Brasser les cartes</button>
    <p id ="nbShuffle" style="display:inline-block"></p> 
    </div>
    """
    init()    # fait appelle à init() pour appliquer les valeurs initiales à l'HTML

# fonction utilisée dans greenCards() qui retourne un tableau contenant
# les valeurs des cartes à déplacer en plus des coordonées de la carte blanche à remplacer.
def options():
    movable=[]
    rangee=len(matrix[0])
    for r in range(4):
        for i in range(rangee):
            if matrix[r][i]==-1:                                  # si la carte est vide:
                if i==0:                                          # si il s'agit de la première carte de la rangée:
                    for deux in range(4):                         # ajouter tous les deux à "movable"
                        movable.append([deux,[r,0]])                    
                else:
                    if matrix[r][i-1]>43 or matrix[r][i-1]==-1:   # si la carte précedente est vide ou si c'est un roi:
                        continue                                  # passer à la carte suivante
                    else:
                        x=matrix[r][i-1]+4                       # ajouter la valeur de la carte à "movable"
                    movable.append([x,[r,i]])                     # en plus de [r,i] qui sont les coordonnées de la case vide
    return movable

# fonction permettant de changer la couleur de fond des carte à déplacer.
def greenCards():
    movable = options()
    copy=[]
    for i in range(4):
        copy.extend(matrix[i])                      # crée un tableau simple à partir de la matrix
    for tab in movable:                             # pour chaque tableau de "movable":
        num=copy.index(tab[0])                      # num= valeur de la carte à déplacer
        case='#case'+str(num)
        document.querySelector(case+' > img').setAttribute("style", "background-color: lime")  #changer la couleur de la carte à déplacer

# fonction permettant de remplacer les carte directement dans l'HTML et de changer la couleur
# des cartes en fonction de ces changements.
def change(case,movable,space):
    caseId1='#case'+str(case)
    original=document.querySelector(caseId1).innerHTML
    caseId2='#case'+str(space)
    empty=document.querySelector(caseId2).innerHTML
    
    document.querySelector(caseId1).innerHTML=empty                       # échanger la position de carte en vide avec la carte à déplacer
    document.querySelector(caseId2).innerHTML=original

    copy=[]
    for i in range(4):
        copy.extend(matrix[i])                                            # crée un tableau simple à partir de la matrix
    for tab in movable:                                                   # pour chaque tableau de "movable":
        num=copy.index(tab[0])
        case='#case'+str(num)                                             # num= valeur de la carte déplacée
        document.querySelector(case+' > img').removeAttribute("style")    # enlever le style de tout les cartes qui pouvaient être déplacer

# fonction permettant d'envoyer un message adapté à la situation du jeux
# (victoire, échec, obligation de brasser)
def verification():
    for i in range(4):                                                    # si la dernière carte de la rangé est vide & 
        if matrix[i][-1]==-1 and matrix[i][-2]==matrix[i][0]+11*4:        # avant dernière carte==au roi de la carte en première position:
            gagner=True
        else:
            gagner=False
            break    
    if nbBrasser > 0 and gagner==False:                                   # si on peut encore brasser et qu'on n'a pas gagné: obligation de brasser
        document.querySelector("#message").innerHTML="""
        <p style="display:inline-block; text-indent:2ch;">Vous devez</p>
        <button onclick="brasser()" style="display:inline-block">
        Brasser les cartes</button>
        """
    if nbBrasser <= 0 and gagner==False:                                  # si on peut plus brasser et qu'on n'a pas gagné: echec
        document.querySelector("#message").innerHTML="""
        <p style="display:inline-block; text-indent:2ch;">
        Vous n'avez pas réussi à placer toutes les cartes... Essayez à nouveau!</p>
        """
    if gagner==True:                                                      # si on a gagné: alerter le joueur
        document.querySelector("#message").innerHTML="""
        <p style="display:inline-block; text-indent:2ch;">Vous avez réussi! Bravo!</p>
        """

# fonction qui applique les fonctions options(), change(), greenCards() et verification() en fonction de la position
# du clic du joueur.
def clic(case):
    global matrix
    movable=options()
    index=case%13                                          # index dans la rangée
    r=math.floor(case/13)                                  # position en terme de rangée
    valeur=matrix[r][index]                                # valeur de la carte dans la case donnée
    for tab in movable:                             
        if tab[0]==valeur:                                 
            matrix[tab[1][0]].pop(tab[1][1])               # retirer dans la rangée (tab[1][0]) la valeur située à l'index (tab[1][1]) corréspondant à la case vide
            matrix[tab[1][0]].insert(tab[1][1],valeur)     # ajouter à cette même position la valeur de la carte à déplacer
            space=tab[1][0]*13+tab[1][1]                   # retirer la valeur de l'index (tab[1][1]) de la rangée tab[1][0]) correspondant à la carte à déplacer
            matrix[r].pop(index)                           # ajouter à cette même position la valeur d'une carte vide (soi -1)
            matrix[r].insert(index,-1)                     # calculer l'id de la case vide à partir de la rangée(tab[1][0]) et l'index (tab[1][1]) contenu dans le tableau de "movable"
            change(case,movable,space)                     # changer la position dans l'HTML grâce à la nouvelle matrix
            break
    greenCards()
    if "lime" not in document.querySelector("#jeu").innerHTML:    
        verification()


# fonction que permet de modifier l'intérieur de la balise ayant l'id main. Ensuite elle met en place le nombre de 
# shuffle qui reste et initialise la fonction qui permet de mettre en lime les cartes que l'on peut déplacer
def init():
    document.querySelector("#main").innerHTML = styleHTML + arrayHTML() + buttonShuffle + buttonRedo
    document.querySelector("#nbShuffle").innerHTML = str(nbBrasser) + " fois"
    greenCards()