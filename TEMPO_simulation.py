import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ---------- helper ----------
def copies_to_uM(copies, volume_L):
    NA = 6.02214076e23
    return copies / (NA * volume_L) * 1e6  # μM

# ---------- parameters ----------
vol_L = 20e-6
default_D_copies = 1200   # copies → μM
default_D0 = copies_to_uM(default_D_copies, vol_L)

# reaction constants 
k1 = 0.1; k2 = 0.1; k3 = 0.1; k4 = 0.1; k5 = 1
k6 = 0.08; k7 = 0.08; k8 = 0.1; k9 = 0.1; k10 = 0.1; k11 =0.1; k12 = 1
k13 = 5e-4; k14 = 1

# extension (first-order)
k1_ext = k2_ext = k3_ext = k4_ext = k6_ext = k7_ext = 1
k9_ext = k10_ext = 1 

# Michaelis-Menten params
kcat1 = 0.038; Km1 = 3.7
kcat2 = 0.38;  Km2 = 0.37
kcat3 = kcat1/2; Km3 = Km1*2
kcat4 = kcat2/2; Km4 = Km2*2

# ---------- index mapping ----------
IDX = {
    'FP':0, 'BP':1, 'FPP':2,
    'FP_D':3, 'FPP_D':4, 'BP_D':5, 'BP_ST':6, 'FP_AT':7, 'FPP_AT':8,
    'ST':9, 'AT':10, 'ST2':11, 'AT2':12,
    'D':13, 'D2':14, 'C':15, 'CD':16, 'CD2':17,
    'R':18, 'F':19,
    'BP_D2':20, 'FPP_D2':21
}

# ---------- RHS function ----------
def rhs(t, y, k6_local, k7_local, k9_local, k10_local):
    FP, BP, FPP = y[IDX['FP']], y[IDX['BP']], y[IDX['FPP']]
    FP_D, FPP_D, BP_D, BP_ST, FP_AT, FPP_AT = y[3:9]
    ST, AT, ST2, AT2 = y[9:13]
    D, D2, C, CD, CD2, R, F = y[13:20]
    BP_D2, FPP_D2 = y[20], y[21]

    # binding/extension rates
    r1  = k1  * FP * D;  r1e  = k1_ext  * FP_D
    r2  = k2  * BP * D;  r2e  = k2_ext  * BP_D
    r3  = k3  * BP * ST; r3e  = k3_ext  * BP_ST
    r4  = k4  * FP * AT; r4e  = k4_ext  * FP_AT
    r5  = k5  * ST * AT
    r6  = k6_local * FPP * D;  r6e  = k6_ext  * FPP_D
    r7  = k7_local * FPP * AT; r7e  = k7_ext  * FPP_AT
    r8  = k8  * BP * ST2
    r9  = k9_local  * BP * D2; r9e  = k9_ext  * BP_D2  
    r10 = k10_local * FPP * D2; r10e = k10_ext * FPP_D2 
    r11 = k11 * FPP * AT2
    r12 = k12 * ST2 * AT2
    r13 = k13 * C * D
    r14 = k14 * C * D2

    # catalytic rates
    V1 = (kcat1 * CD  * R) / (Km1 + R + 1e-16)
    V2 = (kcat2 * CD2 * R) / (Km2 + R + 1e-16)
    V3 = (kcat3 * CD  * FP) / (Km3 + FP + 1e-16)
    V4 = (kcat3 * CD  * BP) / (Km3 + BP + 1e-16)
    V5 = (kcat3 * CD  * FPP) / (Km3 + FPP + 1e-16)
    V6 = (kcat4 * CD2 * FP) / (Km4 + FP + 1e-16)
    V7 = (kcat4 * CD2 * BP) / (Km4 + BP + 1e-16)
    V8 = (kcat4 * CD2 * FPP) / (Km4 + FPP + 1e-16)

    dydt = np.zeros_like(y)
    dydt[IDX['FP']]  = - r1 - r4 - V3 - V6
    dydt[IDX['BP']]  = - r2 - r3 - r8 - r9 - V4 - V7
    dydt[IDX['FPP']]  = - r6 - r7 - r10 - r11 - V5 - V8
    dydt[IDX['FP_D']] = + r1 - r1e
    dydt[IDX['FPP_D']] = + r6 - r6e
    dydt[IDX['BP_D']] = + r2 - r2e
    dydt[IDX['BP_ST']] = + r3 - r3e
    dydt[IDX['FP_AT']] = + r4 - r4e
    dydt[IDX['FPP_AT']] = + r7 - r7e
    dydt[IDX['BP_D2']] = + r9 - r9e   
    dydt[IDX['FPP_D2']] = + r10 - r10e 

    dydt[IDX['ST']]  = + r1e - r3 - r5
    dydt[IDX['AT']]  = + r2e - r4 - r5
    dydt[IDX['ST2']] = + r6e + r7e + r10e - r8 - r12
    dydt[IDX['AT2']] = + r9e - r11 - r12
    dydt[IDX['D']]   = + r3e + r4e + r5 - r13 - r1 - r6 + r1e + r6e
    dydt[IDX['D2']]  = + r8 + r11 + r12 - r14 - r9 - r10 + r9e + r10e
    dydt[IDX['C']]   = - r13 - r14
    dydt[IDX['CD']]  = + r13
    dydt[IDX['CD2']] = + r14
    dydt[IDX['R']]   = - V1 - V2
    dydt[IDX['F']]   = + V1 + V2
    return dydt

# ---------- scenarios ----------
scenarios = {
    "FP/FPP/BP": {"FP0":200e-3, "BP0":400e-3, "FPP0":200e-3,"D0":default_D0, "D20":0.0,"k6":0.08, "k7":0.08},
    "FPP/BP":  {"FP0":0, "BP0":400e-3, "FPP0":400e-3,"D0":default_D0, "D20":0.0,"k6":0.08, "k7":0.08},
    "FP/BP":  {"FP0":400e-3, "BP0":400e-3, "FPP0":0,"D0":default_D0, "D20":0.0,"k6":0.08, "k7":0.08},
}

# ---------- simulate & plot ----------
t_span = (0, 3600)
t_eval = np.linspace(0, 3600, 1001)

plt.figure(figsize=(9,5))
for label, ini in scenarios.items():
    y0 = np.zeros(len(IDX))
    y0[IDX['FP']] = ini["FP0"]
    y0[IDX['BP']] = ini["BP0"]
    y0[IDX['FPP']] = ini["FPP0"]
    y0[IDX['D']]  = ini["D0"]
    y0[IDX['D2']] = ini["D20"]
    y0[IDX['C']]  = 50e-3
    y0[IDX['R']]  = 500e-3
    y0[IDX['F']]  = 0.0

    sol = solve_ivp(
        lambda t,y: rhs(t,y,ini["k6"],ini["k7"],k9,k10),
        t_span, y0, t_eval=t_eval, method='RK45', rtol=1e-6, atol=1e-12
    )

    plt.plot(sol.t/60, sol.y[IDX['F'],:], label=label)

plt.xlabel("Time (min)")
plt.ylabel("Fluorescence F (μM)")
plt.title("Double-track CRISPR: different primer binding affinity")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

