
from cc3d import CompuCellSetup
        

from wetting2dSteppables import wetting2dSteppable

CompuCellSetup.register_steppable(steppable=wetting2dSteppable(frequency=1))


CompuCellSetup.run()
