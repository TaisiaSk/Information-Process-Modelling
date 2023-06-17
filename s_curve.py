import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# S-curve parameters
J = 359.1212
A = 64.6418
V = 34.9065
T = 1.8

step = 0.001


# Сonstant jerk stage
def __const_jerk(jerk, a0, v0, p0, t0, times):
    N = len(times)

    log_j = jerk * np.ones(N)

    diff_a = a0 - jerk * t0
    log_a = jerk * times + diff_a * np.ones(N)

    diff_v = v0 - 0.5 * jerk * (t0 ** 2) - diff_a * t0
    log_v = 0.5 * jerk * np.power(times, 2) + diff_a * times + diff_v * np.ones(N)

    diff_s = p0 - (1 / 6) * jerk * (t0 ** 3) - 0.5 * diff_a * (t0 ** 2) - diff_v * t0
    log_s = (1 / 6) * jerk * np.power(times, 3) + 0.5 * diff_a * np.power(times, 2) + diff_v * times + diff_s * np.ones(N)
    
    return log_j, log_a, log_v, log_s


# Сonstant acceleration stage
def __const_acc(acc, v0, p0, t0, times):
    N = len(times)

    log_j = np.zeros(N)
    log_a = acc * np.ones(N)

    diff_v = v0 - acc * t0
    log_v = acc * times + diff_v * np.ones(N)

    diff_s = p0 - 0.5 * acc * (t0 ** 2) - diff_v * t0
    log_s = 0.5 * acc * np.power(times, 2) + diff_v * times + diff_s * np.ones(N)
    
    return log_j, log_a, log_v, log_s


# Сonstant velocity stage
def __const_vel(vel, p0, t0, times):
    N = len(times)

    log_j = np.zeros(N)
    log_a = np.zeros(N)
    log_v = vel * np.ones(N)

    diff_s = p0 - vel * t0
    log_s = vel * times + diff_s * np.ones(N)
    
    return log_j, log_a, log_v, log_s


# S-curve time scaling
def s_curve(jerk, acc, vel, time_total):
    t0 = 0
    t1 = acc / jerk
    t2 = vel / acc
    t3 = t1 + t2
    t4 = time_total - t3
    t5 = time_total - t2
    t6 = time_total - t1

    times = np.arange(t0, time_total + step, step)

    j1, a1, v1, p1 = __const_jerk(jerk, 0, 0, 0, 0, times[times <= t1])
    j2, a2, v2, p2 = __const_acc(a1[-1], v1[-1], p1[-1], t1, times[(times > t1) & (times <= t2)])
    j3, a3, v3, p3 = __const_jerk((-1) * jerk, a2[-1], v2[-1], p2[-1], t2, times[(times > t2) & (times <= t3)])
    j4, a4, v4, p4 = __const_vel(v3[-1], p3[-1], t3, times[(times > t3) & (times <= t4)])
    j5, a5, v5, p5 = __const_jerk((-1) * jerk, a4[-1], v4[-1], p4[-1], t4, times[(times > t4) & (times <= t5)])
    j6, a6, v6, p6 = __const_acc(a5[-1], v5[-1], p5[-1], t5, times[(times > t5) & (times <= t6)])
    j7, a7, v7, p7 = __const_jerk(jerk, a6[-1], v6[-1], p6[-1], t6, times[times > t6])

    jerk_total = np.concatenate((j1, j2, j3, j4, j5, j6, j7), dtype=float)
    acc_total = np.concatenate((a1, a2, a3, a4, a5, a6, a7), dtype=float)
    vel_total = np.concatenate((v1, v2, v3, v4, v5, v6, v7), dtype=float)
    pos = np.concatenate((p1, p2, p3, p4, p5, p6, p7), dtype=float)

    return jerk_total, acc_total, vel_total, pos, times


# Usage & plots
jerks, accs, vels, pos, times = s_curve(J, A, V, T)

t1 = A / J
t2 = V / A
t3 = t1 + t2
t4 = T - t3
t5 = T - t2
t6 = T - t1
ticks = [0, t1, t2, t3, t4, t5, t6, T]

fig = plt.figure(tight_layout=True, figsize=(10, 5))
fig.suptitle('S-curve', y=0.96, fontsize=16)

gs = gridspec.GridSpec(2, 2)

ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(times, pos, color='#5fbd33')
ax1.vlines(ticks, 0, 1, transform=ax1.get_xaxis_transform(), colors='grey', alpha=0.2, linestyles='dashed')
ax1.set_title('Position')
ax1.set_yticks(np.linspace(0, pos[-1], 5))
ax1.set_xticks(ticks)

ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(times, vels, color='#5fbd33')
ax2.vlines(ticks, 0, 1, transform=ax2.get_xaxis_transform(), colors='grey', alpha=0.2, linestyles='dashed')
ax2.set_title('Velocity')
ax2.set_yticks(np.linspace(0, V, 5))
ax2.set_xticks(ticks)

ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(times, accs, color='#5fbd33')
ax3.vlines(ticks, 0, 1, transform=ax3.get_xaxis_transform(), colors='grey', alpha=0.2, linestyles='dashed')
ax3.set_title('Acceleration')
ax3.set_yticks(np.linspace(-A, A, 5))
ax3.set_xticks(ticks)

ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(times, jerks, color='#5fbd33')
ax4.vlines(ticks, 0, 1, transform=ax4.get_xaxis_transform(), colors='grey', alpha=0.2, linestyles='dashed')
ax4.set_title('Jerk')
ax4.set_yticks(np.linspace(-J, J, 5))
ax4.set_xticks(ticks)

fig.align_labels()
plt.show()
