import cv2
import numpy as np



class Map:

    def __init__(self):

        map_path = r"C:\Users\jeanbaptiste\Desktop\fourmis\utils\map.txt"

        self.map_liste = [[j for i in line for j in i if j != "\n"] for line in open(map_path, "r")]
        self.map_liste = [i for i in self.map_liste if i != []]

        self.height = len(self.map_liste) * 50
        self.width = len(self.map_liste[0]) * 50

        self.dico_recompense = {}

        self.position_recompense = [(x * 50, y * 50) for y, line in enumerate(self.map_liste) for x, case in enumerate(line) if case == "R"]

        self.dico_recompense_score = {}


    def recompense_to_random_position(self):
        pass


    def create_picture(self):
        return 255 * np.ones((self.height, self.width, 3), np.uint8)

    def draw_case(self, picture):
        [cv2.rectangle(picture, (x, y), (x + 50, y + 50), (0, 0, 0), 1)
        for y in range(0, self.height, 50) for x in range(0, self.width, 50)]

    def draw_wall(self, picture):
        for y, line in enumerate(self.map_liste):
            for x, case in enumerate(line):
                if case == "1":
                    picture[y * 50: y * 50 + 50, x * 50: x * 50 + 50] = (42, 42, 165)
                elif case == "R":
                    picture[y * 50: y * 50 + 50, x * 50: x * 50 + 50] = (0, 255, 0)
                elif case == "F":
                    picture[y * 50: y * 50 + 50, x * 50: x * 50 + 50] = (255, 0, 0)


    def displaying_score(self, picture, copy):
        [cv2.putText(picture, str(round(score, 2)), (x + 25, y + 25), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1, cv2.LINE_AA)
        for (x, y), score in self.dico_case.items()]



