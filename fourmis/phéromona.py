import cv2


class Pheromona:

    def __init__(self, number_fourmis):
 
        MAP_PATH = r"C:\Users\jeanbaptiste\Desktop\fourmis\utils\map.txt"

        self.map_liste = [[j for i in line for j in i if j != "\n"] for line in open(MAP_PATH, "r")]
        self.map_liste = [i for i in self.map_liste if i != []]

        self.dico_pheromone = {(x * 50, y * 50): 0 
        for y, line in enumerate(self.map_liste) for x, case in enumerate(line) if case != "1"}

        self.roads_fourmis = {index: [] for index in range(number_fourmis)}


        self.dico_pheromone_reverse = {(x * 50, y * 50): 0 
        for y, line in enumerate(self.map_liste) for x, case in enumerate(line) if case != "1"}

        self.roads_fourmis_reverse = {index: [] for index in range(number_fourmis)}

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.position_recompense = [(x * 50, y * 50) for y, line in enumerate(self.map_liste) for x, case in enumerate(line) if case == "R"]
        self.position_recompense_reverse = [(x * 50, y * 50) for y, line in enumerate(self.map_liste) for x, case in enumerate(line) if case == "F"]




    def descore_case(self):
        for case, score in self.dico_pheromone.items():
            if score > 0:
                self.dico_pheromone[case] -= 1

        for case, score in self.dico_pheromone_reverse.items():
            if score > 0:
                self.dico_pheromone_reverse[case] -= 1


        for case in self.position_recompense:
            self.dico_pheromone[case] = 1000000

        for case in self.position_recompense_reverse:
            self.dico_pheromone_reverse[case] = 1000000


    def create_road_fourmis(self, number_fourmis_create):
        for n in range(number_fourmis_create):
            if n not in self.roads_fourmis:
                self.roads_fourmis[n] = []
                self.roads_fourmis_reverse[n] = []



    def getter_dico_pheromone(self):
        return self.dico_pheromone

    def getter_roads_fourmise(self):
        return self.roads_fourmis

    def getter_dico_pheromone_reverse(self):
        return self.dico_pheromone_reverse

    def getter_roads_fourmise_reverse(self):
        return self.roads_fourmis_reverse




    def setter_dico_pheromone(self, roads, recompense):
        for nb, (case, rec) in enumerate(zip(roads, recompense)):
            if not rec:
                self.roads_fourmis[nb] += [case]
            else:
                self.roads_fourmis_reverse[nb] += [case]


    def scoring_case_dico(self, cases, recompense):
        for nb, (case, rec) in enumerate(zip(cases, recompense)):

            if not rec:

                if case in self.position_recompense:
                    for i in self.roads_fourmis[nb]:
                        self.dico_pheromone[i] += 500 if self.dico_pheromone[i] < 2000 else 0
                else:
                    if self.dico_pheromone[case] >= 200:
                        for i in self.roads_fourmis[nb]:
                            self.dico_pheromone[i] += 50 if self.dico_pheromone[i] < 2000 else 0
                    else:
                        self.dico_pheromone[case] += 1

                self.roads_fourmis_reverse[nb] = []

            else:
 
                if case in self.position_recompense_reverse:
                    for i in self.roads_fourmis_reverse[nb]:
                        self.dico_pheromone_reverse[i] += 500 if self.dico_pheromone_reverse[i] < 2000 else 0
                else:
                    if self.dico_pheromone_reverse[case] >= 200:
                        for i in self.roads_fourmis_reverse[nb]:
                            self.dico_pheromone_reverse[i] += 50 if self.dico_pheromone_reverse[i] < 2000 else 0
                    else:
                        self.dico_pheromone_reverse[case] += 1

                self.roads_fourmis[nb] = []



    def remove_trace(self):
        for index, roads in self.roads_fourmis.items():
            if len(roads) > 5:
                index_road = int( (30/100) * len(roads) )
                self.roads_fourmis[index] = roads[index_road:]

    def remove_trace_reverse(self):
        for index, roads in self.roads_fourmis_reverse.items():
            if len(roads) > 5:
                index_road = int( (30/100) * len(roads) )
                self.roads_fourmis_reverse[index] = roads[index_road:]

    def pheromone_road(self, picture):

        for road in self.roads_fourmis.values():
            for n in range(len(road) - 1):
                x1, y1 = road[n]
                x2, y2 = road[n + 1]
                cv2.line(picture, (x1 + 25, y1 + 25), (x2 + 25, y2 + 25), (0, 0, 255), 2)

    def scoring_case(self, picture):
        [cv2.putText(picture, str(score), (x+25, y+25), self.font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
        for (x, y), score in self.dico_pheromone.items()]


    def scoring_case_reverse(self, picture):
        [cv2.putText(picture, str(score), (x+25, y+25), self.font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
        for (x, y), score in self.dico_pheromone_reverse.items()]


    def pheromone_road_reverse(self, picture):

        for road in self.roads_fourmis_reverse.values():
            for n in range(len(road) - 1):
                x1, y1 = road[n]
                x2, y2 = road[n + 1]
                cv2.line(picture, (x1 + 25, y1 + 25), (x2 + 25, y2 + 25), (0, 255, 0), 2)
