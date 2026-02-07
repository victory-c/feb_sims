# Formula Electric at Berkeley: Simulations Project | Spring 2026

<h2>General Lap Sim Theory</h2>

A Lap Time Simulation requires:
* Vehicle Modeling
* Track Modeling
* Overall Lap Time Simulation

These three aspects sum up to form the full lap time simulation.


Lap Time Theory:
* Steady-State Simulation:
	* Vehicle states are time independent.
	* The vehicle remains at a similar state at all times so all math equations are simple and straightforward.
	* Calculations are fast and lap times are outputted immediately.
* Transient Simulation:
	* Vehicle states are time dependent.
	* Requires historical vehicle data to solve equations.
	* Complicated and slow.
* The sections below detail how to build a very simple steady-state simulation.


Vehicle Theory:
* A simple vehicle model is called a GG circle.
	* GG circles are formed when the longitudinal and lateral accelerations (measured in G forces) of a racecar is plotted.
	* The resulting graph is approximately a circle centered around (0,0).
		* Which means the vehicle is rarely not accelerating in any direction.
	* The larger the circle, the faster the car.
	* The plotted accelerations of any vehicle would collapse approximately into a circle/ellipse, which dictate the maximum value of acceleration in any one direction.


Track Theory:
* A simple track model is a function of turning radius versus distance.
	* When the track curves, the radius has some real number.
	* When the track goes straight, the radius is infinite.
	* Directionality does not matter.


The Steady-State Algorithm:
* The ultimate goal is to find the velocity of the vehicle.
	* The velocity can be integrated over the full distance to find an approximate lap time for the model.
* Steps to finding the velocity:
	1. Find the apex points and speed values.
		* Apex points are the minimum values of radii, where the vehicle goes into the sharpest curve.
		* The speed values at the curve depend upon the length of the radius.
	2. Simulate acceleration past the apex.
		* After the vehicle reaches its lowest speed at the apex, it should accelerate similarly out of the curve.
	3. Simulate deceleration into the apex.
		* Before the vehicle reaches its lowest speed in the apex, the vehicle should brake similarly into the curve.
	4. Find the braking point of the vehicle.
		* The intersection of the acceleration and deceleration velocities before a curve is the optimal braking point of the vehicle for the curve.
* How the algorithm works:
	* The algorithm simulates the acceleration out of and deceleration into turns continuously for every single point on the track.
	* Then, the algorithm chooses the minimum value of velocity at each point as the optimal velocity of the vehicle.
* Key findings for the steady-state model	
	* The algorithm needs a vehicle and track model.
	* The algorithm must calculate the acceleration and deceleration velocity of each node (location on track) for every single apex (track curve).
	* Closed tracks require looping back to the first/last point.

See basic.py for a basic implementation of the simulation using the above concepts.

___

<h2>Features of the Lap Sim included in this repository</h2>

Track Modeling:
* The current track model is a simple model only considering:
	* Section Length
	* Turn Radius
* The model assumes flat tracks with no banking or elevation.
* A full track is built from distinct curve and straight sections, built with the Segment class.
* The model includes the `split_nodes()` function, splitting velocity-tracking nodes based on a uniform distance `NODE_LEN`.
* Each Segment object accurately the start and end indices of the length of track after splitting, as well as saving an 'apex speed' based on radius for all turns.
* The full track model is stored in TRACK.py.


Vehicle Modeling:
* The full vehicle model tracks:
	* External forces, including the normal, drag, and rolling friction forces.
		* Each force is determined with relevant constants and adjustable values of frontal area, drag coefficient, and rolling coefficient.
		* The drag (aerodynamic) force varies with velocity.
	* A powertrain setup calculating both RPM and engine force.
		* Both RPM and engine force are calculated with relevant constants and adjustable drive (gear) ratio (assuming no gear shifting), powertrain efficiency, maximum engine power, and tire radius values.
		* Engine torque is determined through interpolation based on preexisting motor-torque curves.
	* Lateral and longitudinal forces and accelerations.
		* Forces vary based on engine and external forces detailed above.
		* Lateral and longitudinal forces are subject to limits based on an adjustable friction coefficient.
* The model assumes no lift, no gear shift, and an AWD vehicle.
* Output acceleration values depend upon current velocity and turn radius values.
* The full vehicle model is stored in VEHICLE.py.

Formulae:
* The formula document stores common physics formulas needed for specific calculations across the full simulation.
* These include:
	* `find_apex_speed()`: Determines a turn segment's constant velocity based on the maximum frictional force and turn radius.
	* `travel()`: A function simulating the vehicle moving to the next distance-tracking node based on its current velocity and acceleration value.
	* `power()`: Outputs the power use of the vehicle based on its tractive (engine) force, current velocity, and powertrain efficiency.
	* `energy()`: Sums the full power use of the vehicle over the track and outputs an energy value in kilowatt-hours.
* All above formulas are stored in FORMULAE.py.

Full Lap Simulation:
* The current iteration of the lap simulation functions as follows:
	1. The simulation determines all necessary actions of throttling and braking. This includes:
		* Accelerating from Rest: The vehicle accelerates from rest until it is drag-limited or gear-limited, at which point it is unable to accelerate further.
		* Negotiate Turns: The vehicle decelerates into a turn, maintains a constant speed on the curve, and accelerates out of the curve. 
	2. The simulation collects all such lists and selects the minimum as the true vehicle velocity.
	3. The simulation sums together a time value by dividing inter-node distance by their respective velocities. It outputs the final laptime as the primary end goal of the simulation.
	4. The simulation also generates graphs depicting relevant vehicle and lap statistics. This currently includes: 
		* Velocity (m/s) vs. time (s)
		* Velocity (m/s) vs. distance (m) 
		* All velocity lists (m/s) vs. time (s)
* The functions generating each velocity list can be found at SIMUL.py.
* A general version of the lap sim on a simplified track can be found at test_track.py.
