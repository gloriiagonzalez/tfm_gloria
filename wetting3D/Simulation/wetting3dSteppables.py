from cc3d.core.PySteppables import *
import numpy as np
from scipy import optimize

class wetting3dSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        self.file = open(r"C:\CompuCell3D\MYPRO\wetting3d\j10_dinv2.txt", "w")
        self.file.write("MCS Volumen AContact r h theta\n")
        self.file.flush()   
        
        
        wall_cell = self.new_cell(self.WALL)
        
        for x in range(self.dim.x):
            for y in range(self.dim.y):
                for z in range(20):   # grosor del sustrato
                    self.cell_field[x, y, z] = wall_cell
                    
                    
          
   
        for cell in self.cell_list_by_type(self.CELLS):

            cell.targetVolume = cell.volume #(volumen incial - no crecer)
            #cell.targetVolume = 110.0
            cell.lambdaVolume = 3.0


    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        
        

        for cell in self.cell_list_by_type(self.CELLS):
            dist_to_wall = cell.zCOM - 20.0   # distancia al wall
        #cambio lambda
            if dist_to_wall < 5:
                cell.lambdaVolume = 1.0   
            elif dist_to_wall < 10:
                cell.lambdaVolume = 2.0   
            else:
                cell.lambdaVolume = 3.0   
            

        for cell in self.cell_list:

            print("cell.id=",cell.id)
            
            
            
        #totvol
        
        tot_vol = 0
        for cell in self.cell_list_by_type(self.CELLS):
            tot_vol+=cell.volume
            
        ##altura

        cells = self.cell_list_by_type(self.CELLS)

        if cells:
            z_max = max(cell.zCOM for cell in cells)
            h_max = z_max - 20
        else:
            h_max = 0
        
        #area en contacto
        contact_length = 0.0
        
        for cell in self.cell_list_by_type(self.WALL):
            neighbor_list = self.get_cell_neighbor_data_list(cell)
            common_area = neighbor_list.common_surface_area_with_cell_types( cell_type_list=[self.CELLS] )
            contact_length = common_area

        
        #contact 
        r = np.sqrt(contact_length/np.pi)
        h = optimize.root(lambda x: x**3 +3*r*r*x-6*tot_vol/np.pi, 10)
        h_sol = float(h.x[0])
        cont_angle = 2*np.arctan(h_sol/r) 
        cont = cont_angle*180/np.pi
        
        #guardar archivo 
        self.file.write(f"{mcs} {tot_vol} {contact_length} {r} {h_max} {h_sol} {cont}\n")
        self.file.flush()
            
    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """
        self.file.close()

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """
