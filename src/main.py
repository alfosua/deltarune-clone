from engine import *
from deltarune.scenes import Coconut, Wip, Adventure

# setup = GameSetup("Coconut", [Wip(), Coconut(), Adventure()])
setup = GameSetup("Coconut", [Adventure()])

Game(setup).run()
