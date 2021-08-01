import cv2
import numpy as np

from picture import Map
from fourmis import Fourmis
from phéromona import Pheromona

class Main:

    def __init__(self):  

        self.nb_fourmis = 10

        self.constructor_map = Map()
        self.pheromone = Pheromona(self.nb_fourmis)

        self.pause = 0


    def drawing_on_picture(self):
        """Generate pictures & draw on."""

        # Create picture.
        search_recompense_picture = self.constructor_map.create_picture()
        serach_home_picture = self.constructor_map.create_picture()

        # Generate walls.
        self.constructor_map.draw_wall(search_recompense_picture)
        self.constructor_map.draw_wall(serach_home_picture)

        # Generate cases.
        self.constructor_map.draw_case(search_recompense_picture)
        self.constructor_map.draw_case(serach_home_picture)

        return search_recompense_picture, serach_home_picture


    def recuperate_case_score(self):
        """Scoring case"""

        # Case score recompense.
        dico_score = self.pheromone.getter_dico_pheromone()
        # Road ant.
        dico_roads = self.pheromone.getter_roads_fourmise()

        # Case score home.
        dico_score_reverse = self.pheromone.getter_dico_pheromone_reverse()
        dico_roads_reverse = self.pheromone.getter_roads_fourmise_reverse()

        return dico_score, dico_roads, dico_score_reverse, dico_roads_reverse


    def movement_of_ants(self, dico_score, dico_roads, dico_score_reverse, dico_roads_reverse):
        """Ants movements"""

        # Movement random or choiced.
        move_fourmis = [fourmis.move(dico_score, dico_roads[nb], dico_score_reverse, dico_roads_reverse[nb]) 
                        for nb, fourmis in enumerate(self.fourmis)]

        # Update position.
        [fourmis.setter_position(movement) for (movement, fourmis) in zip(move_fourmis, self.fourmis)]

        return move_fourmis


    def descoring(self):
        self.pheromone.remove_trace()
        self.pheromone.remove_trace_reverse()
        self.pheromone.descore_case()


    def displaying_data(self, picture, home):
        [fourmis.blit_fourmis(picture) for fourmis in self.fourmis]
        [fourmis.blit_fourmis(home) for fourmis in self.fourmis]
        self.pheromone.pheromone_road(picture)
        self.pheromone.scoring_case(picture)
        self.pheromone.pheromone_road_reverse(home)
        self.pheromone.scoring_case_reverse(home)


    def display_picture(self, recompense, home):
        """Display picture"""

        # Pictures + labels.
        data = [("recompense", recompense), ("home", home)]

        # Displaying.
        [cv2.imshow(label, picture) for (label, picture) in data]
        if cv2.waitKey(self.pause) & 0xFF == ord('a'):
            # 0 -> click for the next picture, 1 -> automatic frame to frame.
            self.pause = 0 if self.pause == 1 else 1


    def main(self):

        # Create Ants.
        self.fourmis = [Fourmis() for _ in range(self.nb_fourmis)]


        while True:


            # Generate pictures.
            picture, home = self.drawing_on_picture()

            # Environement scores.
            dico_score, dico_roads, dico_score_reverse, dico_roads_reverse = self.recuperate_case_score()

            # Ant has found recompense, go to home.
            recompense = [fourmis.fourmis_has_found_recompense() for fourmis in self.fourmis]

            # Movement of ants.
            move_fourmis = self.movement_of_ants(dico_score, dico_roads, dico_score_reverse, dico_roads_reverse)


            # ---------------------------------------------------------------------
            self.pheromone.scoring_case_dico(move_fourmis, recompense)
            self.pheromone.setter_dico_pheromone(move_fourmis, recompense)


            #
            self.descoring()

            # Draw Ant + scores + roads.
            self.displaying_data(picture, home)

            # Displaying picture.
            self.display_picture(picture, home)






if __name__ == "__main__":

    game = Main()
    game.main()
