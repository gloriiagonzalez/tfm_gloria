from cc3d.core.PySteppables import *
import numpy as np

class wall_gradSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        # crear gradiente
        N = 10 #numero de zonas 
        strip_width = self.dim.x // N  #anchura equitativa 

        wall_types = [self.WALL1, self.WALL2, self.WALL3, self.WALL4, self.WALL5,
            self.WALL6, self.WALL7, self.WALL8, self.WALL9, self.WALL10]
        #wall_types = [self.WALL1, self.WALL2] (caso N = 2)

 
        wall_cells = [self.new_cell(wt) for wt in wall_types]

        for x in range(self.dim.x):
            idx = min(x // strip_width, N - 1)  
            for y in range(self.dim.y):
                for z in range(20):
                    self.cell_field[x, y, z] = wall_cells[idx]
                    
                    
                    
                    
                    
       # cell track
        self.track_field = self.create_scalar_field_py("cell_track")
        
       #volumen (tamaño inicial)
        for cell in self.cell_list_by_type(self.CELLS):

            cell.targetVolume = cell.volume
            #cell.targetVolume = 110.0 
            cell.lambdaVolume = 3.0 
            
            
            
            
            
    # write   
        self.file = open(r"C:\CompuCell3D\MYPRO\wall_grad\wall_grad.txt", "w")
        self.file.write("# mcs  x_com  y_com  z_com  tot_vol  contact_area\n")
        self.file.flush()
        
        # lista de tipos de wall para reutilizar en step()
        self.wall_type_ids = [self.WALL1, self.WALL2, self.WALL3, self.WALL4, self.WALL5,
                              self.WALL6, self.WALL7, self.WALL8, self.WALL9, self.WALL10]
        
    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        for cell in self.cell_list_by_type(self.CELLS):
            dist_to_wall = cell.zCOM - 20.0   # distancia al wall
        
            if dist_to_wall < 2:
                cell.lambdaVolume = 1.0   
            elif dist_to_wall < 5:
                cell.lambdaVolume = 2.0   
            else:
                cell.lambdaVolume = 3.0  
               
              
             
             
        for cell in self.cell_list_by_type(self.CELLS):
            x = int(cell.xCOM)
            y = int(cell.yCOM)
            z = int(cell.zCOM)
            
            self.track_field[x, y, z] = mcs
            
            
            
    #guardar posicion COM cada 100-200 mcs        
        if mcs % 100 == 0:
            
            # COM
            sx = sy = sz = vol = 0.0
            for cell in self.cell_list_by_type(self.CELLS):
                sx += cell.xCOM * cell.volume 
                sy += cell.yCOM * cell.volume
                sz += cell.zCOM * cell.volume
                vol += cell.volume

            # contact area
            contact_area = 0.0
            for wall_type in self.wall_type_ids:
                for cell in self.cell_list_by_type(wall_type):
                    neighbor_list = self.get_cell_neighbor_data_list(cell)
                    contact_area += neighbor_list.common_surface_area_with_cell_types(
                        cell_type_list=[self.CELLS])

            self.file.write("%d %.3f %.3f %.3f %.3f %.3f\n" % (
                mcs, sx/vol, sy/vol, sz/vol, vol, contact_area))
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
