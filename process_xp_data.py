# main_script.py

# Exemple d'appel : python process_xp_data.py 1

import numpy as np
import os
import matplotlib.pyplot as plt
from time import time
from tqdm import tqdm
import csv

n_obs    = 5             #Nombre de points d'oservations voulu dans la simu, par niveau de PIV (25, 50, 75)
hauteurs = [25, 50, 75]  # Hauteur, en % du diffuseur, des plans PIV
tronque  = 89            # 89 car données sup à r=0.3 après (dans la zone de mesure brouillée)
nb_plans = len(hauteurs) # Nombre de plans PIV
pression = 1             # Nombre de point d'observation à la pression (0 : code initial, 1 ou 2 : code modifié)
                         # En cours d'implémentation

# Fonction pour lire les fichiers et les convertir en tableau numpy
def reader_function(file, nb_columns=10125):
    A = np.fromstring(file.read(), sep=' ', dtype='float64')
    if A.size % nb_columns != 0:
        raise ValueError(f"Data cannot be reshaped into ({nb_columns}, -1).")
    return A.reshape(nb_columns, -1)

def writer_function(file, data):
        """Écrit les données dans un fichier texte."""
        try:
            with open(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/{file}.txt", "x") as fichier:
                np.savetxt(fichier, data, fmt='%.6f')
                print(f"Le fichier {fichier} a été créé avec succès.")
        except FileExistsError:
            print(f"Le fichier '{file}.txt' existe déjà. Veuillez le supprimer ou choisir un autre nom.")

# Les données sont organisées en colonnes :
# 0: x   1: y   2: Ux   3: Uy   4: r   5: theta   6: Vr   7: Vtheta   8: Vz   9: ??
    # Vr = Vx*np.cos(theta) + Vy*np.sin(theta)
    # Vtheta = -Vx*np.sin(theta) + Vy*np.cos(theta)
    # In our case, theta = pi/2 so Vr = Vy and Vtheta = -Vx


################## Partie 1 ##################
# To plot l'endroit où x est aligné avec theta
# Une autre métode est de voir où sont les deux premières lignes où les rayons sont identiques

def partie_1():
    print("Exécution de la partie 1...")
    with open("/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/Qn_D130R1_25%/H09D130R1_1341.txt", "r") as file:
        A = reader_function(file)
        X = A[:80, 0]
        theta1 = A[:80, 5]
        theta2 = A[50*81:50*81+80, 5]
        theta3 = A[100*81:100*81+80, 5]
        plt.plot(X, theta1, label="1", color="blue")
        plt.plot(X, theta2, label="2", color="red")
        plt.plot(X, theta3, label="3", color="green")
        plt.title("To find the alignment")
        plt.legend()
        plt.show()

        X= A[:, 0]
        Y= A[:, 1]

        X_reduit = [X[10*i+810*j] for i in range(9) for j in range(13)]#X[::10]
        Y_reduit = [Y[10*i+810*j] for i in range(9) for j in range(13)]#Y[::10]

        print(len(X_reduit))

        plt.scatter(X_reduit, Y_reduit, label="point", color="blue")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.axis("equal")
        plt.title("PIV points (1 over 10)")
        plt.legend()
        plt.grid(True)
        plt.show()

        points = np.column_stack((X_reduit, Y_reduit))
        #try:
        np.savetxt("points_piv_tikz.txt", points, fmt="%.6f", header="x y", comments='')
        print("Fichier 'points_piv_tikz.txt' généré ou mis à jour.")
        #except FileExistsError:
            #print("Le fichier 'points_piv_tikz.txt' existe déjà. Veuillez le supprimer ou choisir un autre nom.")


################## Partie 2 ##################
# Moyenne temporelle des données
def partie_2():
    print("Exécution de la partie 2...")
    debut = time()
    for PIV in tqdm(["Qn_D130R1_25%", "Qn_D130R1_50%", "Qn_D130R1_75%", 
                     "Qn_D130R2_25%", "Qn_D130R2_50%", "Qn_D130R2_75%"]):
        print(f"case : {PIV}")
        SUM = np.zeros((10125, 10))
        compteur = 0
        for i, file in tqdm(enumerate(sorted(os.listdir(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/{PIV}")))):
            with open(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/{PIV}/{file}", "r") as file:
                A=reader_function(file)
                SUM = SUM + A
                compteur +=1
        SUM = np.divide(SUM, int(compteur))
        print(f"Instants : {compteur}")
        try:
            with open(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/{PIV}_moy_temp.txt", "x") as summed:
                np.savetxt(summed, SUM, fmt='%.6f')
                print(f"Les valeurs de {PIV} ont été sauvegardées dans {summed}")
        except FileExistsError:
            print(f"Le fichier '{PIV}_moy_temp.txt' existe déjà. Veuillez le supprimer ou choisir un autre nom.")
            break
    print("Durée = ", time() - debut, "sec") #209


################## Partie 3 ##################
# Echantillonage selon x et moyenne selon ((R1 et R2) ET (theta, fait automatiquement car la pompe tourne))
def partie_3():
    print("Exécution de la partie 3...")
    # 89 car données sup à r=0.3 après
    # Input : 6 fichiers de 10125 lignes et 10 colonnes
    # Output : 3 fichiers de 89 lignes et 10 colonnes
    for prct, decalage in zip(hauteurs, [55, 55, 65]): # décalage : PIV pas alignés
        OUT = np.zeros((tronque, 10))  # 89/125 car données sup à r=0.3 après
        ########## R1 #################
        with open(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/Qn_D130R1_{prct}%_moy_temp.txt", "r") as file:
            A = reader_function(file)

            for i in range(tronque):
                OUT[i] = (A[i*81 + decalage] + A[i*81 + decalage+1])/2

# Explication : 81 est le nombre de r (et 125theta). On veut prendre la moy des éléments x=55 et x=56, là où x ne varie pas selon theta/y/r, pour aligner les repères.
# Cependant, le repère est différent pour 75% car le champ de la caméra placé au dessus est plus petit > x entre 65 et 66

        ########## R2+R1 #################
        with open(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/Qn_D130R2_{prct}%_moy_temp.txt", "r") as file:
            A = reader_function(file)
            for i in range(tronque):
                OUT[i] = (OUT[i] + (A[i*81 + decalage] + A[i*81 + decalage+1])/2)  /2 # Moyenne avec les données de R1 et R2
        
        try:
            with open(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/data_{prct}%_Y_125_sampled.txt", "x") as sampled:
                np.savetxt(sampled, OUT, fmt='%.6f')
                print(f"Les valeurs à {prct}% ont été sauvegardées dans {sampled}")
        except FileExistsError:
            print(f"Le fichier 'data_{prct}%_Y_125_sampled.txt' existe déjà. Veuillez le supprimer ou choisir un autre nom.")
            break


################## Partie 4 ##################
# Mise en forme pour CONES

def partie_4():
    print("Exécution de la partie 4...")
    # colonne 4, 5, 6, 7, 8 à garder
    # Entrée : 3 fichiers de 89 lignes et 10 colonnes
    # Sortie : 2 fichier :
    #         - field : len(hauteurs)3*n_obs lignes et 1 colonne
    #         - coords : len(hauteurs)*n_obs lignes et 3 colonnes

    pas = tronque//n_obs # pas entre les données X
    fieldCylindrical_RefPIV = np.zeros((3*3*n_obs,1))
    fieldCylindrical_RefCFD = np.zeros((3*3*n_obs,1))
    fieldCarthesian_RefPIV  = np.zeros((3*3*n_obs,1))
    fieldCarthesian_RefCFD  = np.zeros((3*3*n_obs,1))
    coords = np.zeros((0,3))

    for k, pct in enumerate(hauteurs):

        with open(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/data_{pct}%_Y_125_sampled.txt", "r") as file:
            A = reader_function(file, nb_columns=tronque)
            
            for j, ligne in enumerate(np.linspace(0, n_obs*pas, n_obs).astype(int)):


                ################## field ##################
#Codable avec v_stack aussi

# Rappel : 0: x   1: y   2: Ux   3: Uy   4: r   5: theta   6: Vr   7: Vtheta   8: Vz   9: ??  #

# L'axe z de la PIV est inversé par rapport à l'axe z de la simulation numérique
# Dans le filtre de Kalman, nous utiliserons les données Cylindriques dans le fomalisme du repère de la simulation numérique

                '''
                fieldCarthesian_RefPIV[  k                 *n_obs + j, 0] =   A[ligne][2] # Ux
                fieldCarthesian_RefPIV[ (k+  len(hauteurs))*n_obs + j, 0] =   A[ligne][3] # Uy
                fieldCarthesian_RefPIV[ (k+2*len(hauteurs))*n_obs + j, 0] =   A[ligne][8] # Uz

                fieldCarthesian_RefCFD[  k                 *n_obs + j, 0] =  -A[ligne][2] # Ux
                fieldCarthesian_RefCFD[ (k+  len(hauteurs))*n_obs + j, 0] =   A[ligne][3] # Uy
                fieldCarthesian_RefCFD[ (k+2*len(hauteurs))*n_obs + j, 0] =  -A[ligne][8] # Uz

                fieldCylindrical_RefPIV[ k                 *n_obs + j, 0] =   A[ligne][6] # Vr
                fieldCylindrical_RefPIV[(k+  len(hauteurs))*n_obs + j, 0] =   A[ligne][7] # Vtheta
                fieldCylindrical_RefPIV[(k+2*len(hauteurs))*n_obs + j, 0] =   A[ligne][8] # Uz
                '''

                fieldCylindrical_RefCFD[ k                 *n_obs + j, 0] =   A[ligne][6] # Vr
                fieldCylindrical_RefCFD[(k+  len(hauteurs))*n_obs + j, 0] =  -A[ligne][7] # Vtheta
                fieldCylindrical_RefCFD[(k+2*len(hauteurs))*n_obs + j, 0] =  -A[ligne][8] # Uz


                ################## coords ##################
                X      = 0        
                Y      = A[ligne,4]          
                if pct == 25:
                    Z      = 0.01   # or *np.ones((0,n_obs))
                if pct == 50:
                    Z      = 0      # or np.zeros((0,n_obs))
                if pct == 75:
                    Z      = - 0.01 # or *np.ones((0,n_obs))
                coord = np.hstack([X, Y, Z])
                coords = np.vstack([coords, coord])

    if pression != 0:
        fieldCylindrical_RefCFD = np.vstack([fieldCylindrical_RefCFD, -410])
        coords = np.vstack([coords, np.hstack([0, 0, -0.35])])
        print("ATTENTION : Pression non nulle !")

    writer_function('field', fieldCylindrical_RefCFD)
    writer_function('obs_coordinates', coords)


################## Partie 5 ##################
# Suite de la mise en forme pour CONES : création des points d'observation pour la fonction d'interpolation de la simulation numérique

def partie_5():
    print("Exécution de la partie 5...")
    #echantillonage = 0.015  # environ 1,4mm
    nb_echantillonage_pts = 150
    theta_max = np.pi/7  # OU pi # 2*pi/7
    PIVwedgeAngle = np.pi/2
    coords_seventh = np.zeros((nb_echantillonage_pts*n_obs*len(hauteurs), 3))
    # pas = epsilon/r (avec r=y dans notre cas). Et ... = 2pi/7e
    obs_coords = np.loadtxt("/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/obs_coordinates.txt")
    for source_pt_i, (x_s, y_s, z_s) in enumerate(obs_coords):
        r_s = y_s
        #length = 0
        #for theta_s in np.arange(-np.pi/7, np.pi/7, r_s*echantillonage):
        for target_pt, theta_s in enumerate(np.linspace(-theta_max, theta_max, nb_echantillonage_pts)):
            coords_seventh[source_pt_i*nb_echantillonage_pts + target_pt, 0] = np.cos(theta_s+PIVwedgeAngle)*r_s
            coords_seventh[source_pt_i*nb_echantillonage_pts + target_pt, 1] = np.sin(theta_s+PIVwedgeAngle)*r_s
            coords_seventh[source_pt_i*nb_echantillonage_pts + target_pt, 2] = z_s
            #length+=1
        #lengths.append(length)

    writer_function('coords_seventh', coords_seventh)
  

################## Partie 6 ##################
# Affichage des courbes de vitesse (de la PARTIE 2 : expérimentale) en fonction de x
# Les coubres Vy et Vr sont censées se superposer, de même pour Vx et -Vtheta

def partie_6():
    print("Exécution de la partie 6...")
    plt.figure(figsize=(12,4))
    for k, pct in enumerate(hauteurs):
        with open(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/data_{pct}%_Y_125_sampled.txt", "r") as file:
            A = reader_function(file, nb_columns=tronque)

            r  = A[:,4]
            Vx = A[:,2]
            Vy = A[:,3]
            Vr = A[:,6]
            Vt = -A[:,7]
            Vz = A[:,8]

            plt.subplot(1, len(hauteurs), k + 1)  # 1 ligne, autant de colonnes que de hauteurs
            plt.plot(r, Vx, label="Vx")
            plt.plot(r, Vy, label="Vy")
            plt.plot(r, Vr, label="Vr")
            plt.plot(r, Vt, label="Vt")
            plt.plot(r, Vz, label="Vz")
            plt.xlabel("r")
            plt.ylabel("Vitesses")
            plt.title(f"Hauteur {pct}%")
            plt.legend()
            plt.grid(True)

    plt.tight_layout()  # Ajuste la disposition des graphes pour éviter le chevauchement
    plt.show()



####################
def partie_7():
    print("Exécution de la partie 7 : Conversion des données numériques en Cylindrical et rectification du repère (sens de rotation et Vz) de l'experimental...")
    hauteurs = [25, 50, 75]
    nb_plans = len(hauteurs)
    radius = np.array([0.387763, 0.366763, 0.345763, 0.324763, 0.302763])
    n_obs = len(radius)

    data = np.loadtxt(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/numFieldMoyCarthesian.txt")
    Vx         =   data[0               :nb_plans*n_obs  ]
    Vy         =   data[nb_plans*n_obs  :2*nb_plans*n_obs]
    Vz         =   data[2*nb_plans*n_obs:3*nb_plans*n_obs]
    Vr = Vy
    Vtheta = -Vx
    Cylindrical = np.hstack([Vr, Vtheta, Vz])
    try:
        with open("/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/numFieldMoyCylindical.txt", "x") as fichier:
            np.savetxt(fichier, Cylindrical, fmt='%.6f', delimiter=',')
    except FileExistsError:
        print("Le fichier 'numFieldMoyCylindical.txt' existe déjà. Veuillez le supprimer ou choisir un autre nom.")

    '''
    data2 = np.loadtxt(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/fieldCylindrical.txt")
    Vr         =   data2[0               :nb_plans*n_obs  ] # Inchangé
    Vtheta         =   data2[nb_plans*n_obs  :2*nb_plans*n_obs] 
    Vz         =   data2[2*nb_plans*n_obs:3*nb_plans*n_obs] 
    Vtheta = -Vtheta
    Vz = -Vz
    new = np.hstack([Vr, Vtheta, Vz])
    try:
        with open("/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/expefieldCylindrical.txt", "x") as fichier:
            np.savetxt(fichier, new, fmt='%.6f', delimiter=',')
    except FileExistsError:
        print("Le fichier 'expefieldCylindrical.txt' existe déjà. Veuillez le supprimer ou choisir un autre nom.")
    '''
#################""




################## Affichage des courbes numériques et expériementales ##################
def partie_8():
    print("Exécution de la partie 8 : affichage des courbes numériques et expérimentales...")
    hauteurs = [25, 50, 75]
    nb_plans = len(hauteurs)
    radius = np.array([0.387763, 0.366763, 0.345763, 0.324763, 0.302763])
    n_obs = len(radius)
    fichiers = ["numFieldMoyCylindical", "field"]
    noms = {"numFieldMoyCylindical": "Numérique", "field": "Expérimentale"}
    # field <=> experimental field Cylindrical RefCFD (expefieldCylindrical)


    styles_ligne = {"numFieldMoyCylindical": "-", "field": "--"}
    couleurs = {"Vr": "tab:blue", "Vtheta": "tab:orange", "Vz": "tab:green"}
    marqueurs = {"Vr": "o", "Vtheta": "o", "Vz": "o"}

    fig, axes = plt.subplots(1, nb_plans, figsize=(18, 6), sharey=True)

    handles_dict = {comp: {} for comp in ["Vr", "Vtheta", "Vz"]}

    for h, hauteur in enumerate(hauteurs):
        ax = axes[h]

        for fichier in fichiers:
            data = np.loadtxt(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/{fichier}.txt")

            Vr         =   data[h*n_obs                     :(h+1)*n_obs                 ]
            Vtheta     =   data[h*n_obs+  n_obs*nb_plans    :(h+1)*n_obs+  n_obs*nb_plans] 
            Vz         =   data[h*n_obs+2*n_obs*nb_plans    :(h+1)*n_obs+2*n_obs*nb_plans]

            for comp, values in zip(["Vr", "Vtheta", "Vz"], [Vr, Vtheta, Vz]):
                label = f"{comp} {noms[fichier]}"
                handle, = ax.plot(
                    radius,
                    values,
                    label=label,
                    linestyle=styles_ligne[fichier],
                    color=couleurs[comp],
                    marker=marqueurs[comp],
                    linewidth=1.5
                )
                # Stocker handle pour la légende dans l'ordre voulu
                if fichier not in handles_dict[comp]:
                    handles_dict[comp][fichier] = handle

        ax.set_xlabel(r"$r \, [m]$", fontsize=16)
        if h == 0:
            ax.set_ylabel(r"$V \, [m/s]$", fontsize=16)
        ax.set_title(fr"$b/b_3 = {hauteur} \%$", fontsize=18)
        ax.tick_params(axis='both', labelsize=12)
        ax.grid(True)


    # Construction de la légende dans l’ordre Vr -> Vtheta -> Vz
    handles_global = []
    labels_global = []
    for comp, comp_label in zip(["Vr", "Vtheta", "Vz"], [r"$V_r$", r"$V_{\theta}$", r"$V_z$"]):
        for fichier in fichiers:
            handles_global.append(handles_dict[comp][fichier])
            # Ajouter le signe moins uniquement pour Vtheta numérique
            if comp == 'Vtheta' and fichier == 'num_field_moy':
                prefix = r'$-V_{\theta}$'
            else:
                prefix = comp_label

            label = f"{prefix} {noms[fichier]}"

            labels_global.append(label)

    fig.legend(
        handles_global,
        labels_global,
        loc='lower center',
        ncol=3,
        fontsize=13,
        frameon=True
    )
    plt.tight_layout(rect=[0, 0.1, 1, 1])
    plt.show()

    #generer_rapport_pdf()


def generer_rapport_pdf():
    print("Génération automatique d'un rapport PDF...")

    #Exemple
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    ax.set_title("Rapport automatique - Partie N")

    fig.savefig("rapport_partie8.pdf")
    print("Rapport sauvegardé sous 'rapport_partieN.pdf'.")

# Mapping des parties
mapping = {
    1: partie_1,
    2: partie_2,
    3: partie_3,
    4: partie_4,
    5: partie_5,
    6: partie_6,
    7: partie_7,
    8: partie_8,
}

def main(PARTIE):
    if PARTIE in mapping:
        mapping[PARTIE]()
    else:
        print(f"Partie {PARTIE} non reconnue.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        print("Usage : python main_script.py <PARTIE>")













#def extract_probe_values(data):
    """
    Extrait les valeurs des probes à partir d'une chaîne contenant des lignes avec des valeurs entre parenthèses.
    :param data: Chaîne contenant les valeurs des probes sous forme "(x y z)".
    :return: Liste des valeurs y extraites de chaque ligne de probe.
    """
    #pattern = re.findall(r"# Probe \d+ \(([^,]+),\s*([^\)]+),", data)
    #return [float(y) for _, y in pattern]


'''
#pour la partie instationnaire
if PARTIE == 4:
    theta_moy=1.52
    ma_fenetre = 0.14
    #PIV_MOY_RAD = np.zeros((120, 4))
    for PIV in os.listdir("/home/clementt/Documents/ibm_test/PIV_pour_Miguel/PIV_moy_temp_et_R"):
        for ligne in range(10125):
            for i, rayons in enumerate(np.linspace(0.3, 0.39, 120)):
                if theta_moy-ma_fenetre/2 < theta < theta_moy+ma_fenetre/2:

            PIV_MOY_RAD[ligne][...]
'''

# plus de theta
        
###### Plot pour voir si schéma répété sur cycle 7 le coder avant
###### Ensuite moyenner par 7 puis 7 pour arriver à 1 (eft le faire)
###### Ensuite, récupérer les données pour r allant de 0.3 à max avec un pas permettant 100 données ensuite raccourcis à 10


        #with open(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/data/{PIV}/??{i:04d}.txt", "r") as file:
    #for files in os.listdir(f"/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/data/{PIV}"):
        #print(PIV, files)
        #with open(f"/home/clementt/Documents/ibm_test

"""
with open("/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/data/Qn_D130R1_25%/H09D130R1_0001.txt", "r") as R1_0001_25:
    print(R1_0001_25)
    A = R1_0001_25.read()
    print(len(A))
    print(np.shape(A))
    A = A.split()
    print(len(A))
    #print(A[:2])
    #print(A[:131])
    A = np.reshape(A, (10, 10125))
    print(np.shape(A))
    print(A[0][2])

#with open("/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/Qn_D130R1_25%/data.txt", "x") as data:
    #data.write("\nBonjour monde")


#import mmap

# Ouvre le fichier en mode lecture et récupère sa taille
with open('/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/Qn_D130R1_25%/H09D130R1_0001.txt', 'r') as f:
    print
    #print(f.read())

#with open('/home/clementt/Documents/ibm_testcases/pump/PIV_pour_Miguel/Qn_D130R1_25%/H09D130R1_0001.txt', 'r') as f:
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    contents = mm.read()

    size = f.seek(0, 2)
    f.seek(0)
    
    # Crée un objet mmap à partir du fichier
    mm = mmap.mmap(f.fileno(), size)
    
    # Lit le contenu du fichier à l'aide de l'objet mmap
    contents = mm.read()

# Affiche le contenu du fichier
#print(contents)"
"""