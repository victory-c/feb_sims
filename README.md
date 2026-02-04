# Formula Electric at Berkeley: Simulations Project | 2026

A Lap Time Simulation requires:
* Vehicle Modeling
* Track Modeling
* Straight Line Simulations

These three aspects sum up to form the full lap time simulation.


Lap Time Theory:
* Steady-State Simulation:
	* Vehicle states are time independent
	* The vehicle remains at a similar state at all times so all math equations are simple and straightforward
	* Calculations are fast and lap times are outputted immediately
* Transient Simulation:
	* Vehicle states are time dependent
	* Requires historical vehicle data to solve equations
	* Complicated and slow
The steady-state model will be used as a starting point.


Vehicle Theory:
* A simple vehicle model is called a GG circle.
	* GG circles are formed when the longitudinal and lateral accelerations (measured in G forces) of a racecar is plotted.
	* The resulting graph is approximately a circle centered around (0,0)
		* Which means the vehicle is rarely not accelerating in any direction.
	* The larger the circle, the faster the car
	* The plotted accelerations of any vehicle would collapse approximately into a circle/ellipse, which dictate the maximum value of acceleration in any one direction.
* This will be replaced by an actual vehicle model later on.


Track Theory:
* A simple track model is a function of turning radius versus distance.
	* When the track curves, the radius has some real number
	* When the track goes straight, the radius is infinite.
	* Directionality does not matter
* This will also be replaced by an actual track model later on.


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
* Key findings for the steady-state model:
	* The algorithm needs a vehicle and trak model.
	* The algorithm must calculate the acceleration and deceleration velocity of each node (location on track) for every single apex (track curve).
	* Closed tracks require looping back to the first/last point.

See main.py for a simple simulation using the above concepts.
