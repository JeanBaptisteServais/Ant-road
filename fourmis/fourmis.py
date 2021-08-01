
import cv2
import random
import os

class Fourmis:


    def __init__(self):


        MAP_PATH = r"C:\Users\jeanbaptiste\Desktop\fourmis\utils\map.txt"
        IMAGE = cv2.imread(r"C:\Users\jeanbaptiste\Desktop\fourmis\utils\fourmis.jpg")

        self.neightboor = {"d": (50, 0), "g": (-50, 0), "b": (0, 50), "h": (0, -50)}

        self.map_liste = [[j for i in line for j in i if j != "\n"] for line in open(MAP_PATH, "r")]
        self.map_liste = [i for i in self.map_liste if i != []]

        self.height = len(self.map_liste) * 50
        self.width  = len(self.map_liste[0]) * 50

        self.position = (0, 200)

        self.image = cv2.resize(IMAGE, (50, 50))

        self.position_recompense = [(x * 50, y * 50) for y, line in enumerate(self.map_liste) for x, case in enumerate(line) if case == "R"]
        self.position_recompense_reverse = [(x * 50, y * 50) for y, line in enumerate(self.map_liste) for x, case in enumerate(line) if case == "F"]


        self.self_has_found_recompense = False


    def blit_fourmis(self, picture):
        x, y = self.position
        picture[y:y+50, x:x+50] = self.image


    def recuperate_case_neightboors(self):
        x, y = self.position
        return [(x + x_n, y + y_n) for label_move, (x_n, y_n) in self.neightboor.items() 
        if (x + x_n, y + y_n) not in ( (0, 0) )]


    def verify_isnt_wall(self, neightboor_case):
        return [(x, y) for (x, y) in neightboor_case 
        if 0 <= x < self.width and 0 <= y < self.height and
        self.map_liste[y//50][x//50] != "1"] 


    def verify_isnt_out_case(self, neightboor_case):
        return [(x, y) for (x, y) in neightboor_case if 0 <= x < self.width and 0 <= y < self.height]


    def setter_position(self, move):
        self.position = move


    def cases_score(self, dico_score, dico_roads):

        scoring = []

        x, y = self.position
        for k, (x_n, y_n) in self.neightboor.items():
            x_move = x + x_n
            y_move = y + y_n

            pos = (x_move, y_move)

            if pos in dico_score:
                if dico_score[pos] >= 10 and pos not in dico_roads:
                    scoring += [(dico_score[pos], pos)]

        if len(scoring) > 0:
            scoring = max(scoring)

        return scoring


    def move(self, dico_score, dico_roads, dico_score_to_home, dico_roads_to_home):

        case_around = self.recuperate_case_neightboors()
        case = self.verify_isnt_wall(case_around)
        case = self.verify_isnt_out_case(case)

        if not self.self_has_found_recompense:
            scoring = self.cases_score(dico_score, dico_roads)
        else:
            scoring = self.cases_score(dico_score_to_home, dico_roads_to_home)

        return random.choice(case) if len(scoring) == 0 else scoring[1]


    def fourmis_has_found_recompense(self):

        if not self.self_has_found_recompense:

            if self.position in self.position_recompense:
                self.self_has_found_recompense = True

        else:
            if self.position in self.position_recompense_reverse:
                self.self_has_found_recompense = False


        return self.self_has_found_recompense