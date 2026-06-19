
from cc3d import CompuCellSetup
        

from wall_gradSteppables import wall_gradSteppable

CompuCellSetup.register_steppable(steppable=wall_gradSteppable(frequency=1))


CompuCellSetup.run()
