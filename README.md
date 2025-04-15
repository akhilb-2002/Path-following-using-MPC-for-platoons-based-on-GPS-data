**UGRC**

![](https://github.com/akhilb-2002/Path-following-using-MPC-for-platoons-based-on-GPS-data/blob/main/NMPC.png)

A truck platoon is a truck formation that moves
at high speeds along a specific route with relatively small intervehicular distances. A fundamental problem in such formations is
that the platoon must follow the prescribed route while avoiding
collisions and keeping the platoon stable. We must also ensure
that the energy consumed in the process is minimal. To solve
this problem, a non-linear model predictive controller has been
proposed while also considering the two-dimensional dynamics of
the truck operation. To solve the problem of route following, we
implement a technique that reads from the previously obtained
Geo-spatial data and generates waypoints as markers for the
platoon to follow. The tracking of these waypoints are formulated
as a Non-Linear optimization problem while integrating velocity
minimization among the vehicles. This problem is then solved
using the CasADi optimal control framework. The controller’s
capability to establish a stable, working platoon for different
routes has been studied.
