# S-Curve Time Scaling

Study project on the subject "Information Process Modelling".

---

The implementation of the S-curve velocity profile.
Time scaling consists of seven stages:

1. constant jerk until a desired acceleration in achieved,
2. constant acceleration until the desired velocity is being approached,
3. constant negative jerk until acceleration equals zero,
4. coasting at constant velocity,
5. constant negative jerk,
6. constant deceleration,
7. constant positive jerk until acceleration and velocity reach zero.

At the initial and final points, the velocity and acceleration are equal to zero.

## Usage

Function `s_curve` is generate motion profile for trajectory segment at the time interval [0, time_total]. This function requires the following arguments:

```
jerk: jerk limit
acc: acceleration limit
vel: velocity limit
time_total: time limit
```

The output of the function will be a set that describes the motion profile of the segment:

```
jerk_total: array of jerk values
acc_total: array of acceleration values
vel_total: array of velocity values
pos: array of position values
times: array of timestamps
```

## Example

An example of the work is shown on the plot in a file `'fig.png'` with the following parameters:

```
J = 359.1212   # jerk (rad/s^3)
A = 64.6418    # acceleration (rad/s^2)
V = 34.9065    # velocity (rad/s)
T = 1.8        # total time (s)

step = 0.001   # time step
```
