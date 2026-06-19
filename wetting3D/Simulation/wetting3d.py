
from cc3d import CompuCellSetup
        

from wetting3dSteppables import wetting3dSteppable

CompuCellSetup.register_steppable(steppable=wetting3dSteppable(frequency=1))


CompuCellSetup.run()
