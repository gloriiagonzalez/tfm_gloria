from cc3d.core.PySteppables import *
import numpy as np

class wetting2dSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        self.file = open(r"C:\CompuCell3D\MYPRO\wetting2d\2d_j14_40mcs.txt", "w")
        self.file.write("MCS Area ContactLength\n")
        self.file.flush()
        
        wall_cell = self.new_cell(self.WALL)
        
        for x in range(self.dim.x):
                for y in range(20):   # range(grosor del sustrato)
                    self.cell_field[x, y, 0] = wall_cell

    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        tot_area = sum(cell.volume for cell in self.cell_list_by_type(self.CELLS))

        contact_length = 0.0
        for cell in self.cell_list_by_type(self.WALL):
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            contact_length = neighbor_list.common_surface_area_with_cell_types(
                cell_type_list=[self.CELLS]
            )

        self.file.write(f"{mcs} {tot_area} {contact_length}\n")
        self.file.flush()

        for cell in self.cell_list:

            print("cell.id=",cell.id)

    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """
