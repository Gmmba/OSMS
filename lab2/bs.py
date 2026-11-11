import numpy as np
import matplotlib.pyplot as plt

P_BS = 46
P_UE = 24
G_BS = 21
PenM = 15
IM = 1
MIMO = 3
Feeder = 2 + 0.4 + 0.5
f_MHz = 1800
f_GHz = 1.8
BW_UL = 10e6
BW_DL = 20e6
NF_BS = 2.4
NF_UE = 6
SINR_UL = 4
SINR_DL = 2
S_macro = 100
S_micro = 4
k_sect = 1.95

hBS = 30
hms = 1.5
dh = 25
w = 20
b = 40
phi = 45

Thermal_UL = -174 + 10 * np.log10(BW_UL)
RxSens_BS = NF_BS + Thermal_UL + SINR_UL
MAPL_UL = P_UE - Feeder + G_BS + MIMO - IM - PenM - RxSens_BS
print(f'1) UL: RxSens_BS = {RxSens_BS:.2f} дБм, MAPL_UL = {MAPL_UL:.2f} дБ')

Thermal_DL = -174 + 10 * np.log10(BW_DL)
RxSens_UE = NF_UE + Thermal_DL + SINR_DL
MAPL_DL = P_BS - Feeder + G_BS + MIMO - IM - PenM - RxSens_UE
print(f'2) DL: RxSens_UE = {RxSens_UE:.2f} дБм, MAPL_DL = {MAPL_DL:.2f} дБ')

def UMi(d):
    return 26 * np.log10(f_GHz) + 22.7 + 36.7 * np.log10(d * 1000)

A = 46.3
B = 33.9
a_hms = 3.2 * (np.log10(11.75 * hms))**2 - 4.97

def s(d):
    return np.where(d >= 1,
                    44.9 - 6.55 * np.log10(f_MHz),
                    (47.88 + 13.9 * np.log10(f_MHz) - 13.9 * np.log10(hBS)) / np.log10(50))

def Hata(d):
    return A + B * np.log10(f_MHz) - 13.82 * np.log10(hBS) - a_hms + s(d) * np.log10(d)

def L0(d):
    return 32.44 + 20 * np.log10(f_MHz) + 20 * np.log10(d)

if phi < 35:
    angle = -10 + 0.354 * phi
elif phi < 55:
    angle = 2.5 + 0.075 * phi
else:
    angle = 4.0 - 0.114 * phi

L2 = -16.9 - 10 * np.log10(w) + 10 * np.log10(f_MHz) + 20 * np.log10(dh - hms) + angle
L11 = -18 * np.log10(1 + hBS - dh)
ka = 54
kd = 18
kf = -4 + 0.7 * (f_MHz / 925 - 1)

def L1(d):
    return L11 + ka + kd * np.log10(d) + kf * np.log10(f_MHz) - 9 * np.log10(b)

def WI1(d):
    return L0(d) + np.maximum(L1(d) + L2, 0)

def WI2(d):
    return 42.6 + 20*np.log10(f_MHz) + 26*np.log10(d)

d = np.linspace(0.01, 8, 1000)

plt.figure(figsize=(10, 6))
plt.plot(d, UMi(d), 'r', linewidth=1.5, label='UMiNLOS')
plt.plot(d, Hata(d), 'b', linewidth=1.5, label='COST231-Hata')
plt.plot(d, WI1(d), 'g', linewidth=1.5, label='Walfish-Ikegami(L_NLOS)')
plt.plot(d, WI2(d), 'g--', linewidth=1.5, label='Walfish-Ikegami(L_LOS)')
plt.axhline(y=MAPL_UL, color='k', linestyle='--', label=f'MAPL_UL = {MAPL_UL:.1f} дБ')
plt.axhline(y=MAPL_DL, color='k', linestyle=':', label=f'MAPL_DL = {MAPL_DL:.1f} дБ')
plt.legend()
plt.xlabel('Расстояние между приемником и передатчиком, км')
plt.ylabel('Потери сигнала, дБ')
plt.title('Потери сигнала по моделям распространения, f = 1.8 ГГц')
plt.grid(True)
plt.tight_layout()
plt.show()

dd = np.linspace(0.001, 20, 20000)

Hata_dd = Hata(dd)
R_UL_m = np.interp(MAPL_UL, Hata_dd, dd)
R_DL_m = np.interp(MAPL_DL, Hata_dd, dd)
R_m = min(R_UL_m, R_DL_m)
N_m = int(np.ceil(S_macro / (k_sect * R_m**2)))

UMi_dd = UMi(dd)
R_UL_f = np.interp(MAPL_UL, UMi_dd, dd)
R_DL_f = np.interp(MAPL_DL, UMi_dd, dd)
R_f = min(R_UL_f, R_DL_f)
N_f = int(np.ceil(S_micro / (k_sect * R_f**2)))

print(f'\n4) Макросоты (COST231-Hata):')
print(f'R_UL = {R_UL_m:.3f} км, R_DL = {R_DL_m:.3f} км, R = {R_m:.3f} км')
print(f'S одной BS = {k_sect * R_m**2:.3f} км^2, нужно BS на {int(S_macro)} км^2: {N_m}')
print(f'Микро/фемтосоты (UMiNLOS):')
print(f'R_UL = {R_UL_f * 1000:.0f} м, R_DL = {R_DL_f * 1000:.0f} м, R = {R_f * 1000:.0f} м')
print(f'S одной BS = {k_sect * R_f**2:.3f} км^2, нужно BS на {int(S_micro)} км^2: {N_f}')



