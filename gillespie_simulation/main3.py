from simulation import Simulation

simulation = Simulation()
simulation.set_cycles()
simulation.set_steps()
simulation.add_reactions()
simulation.run()
simulation.average()
simulation.plot()