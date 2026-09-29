import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

f = 4
T = 1
t_cont = np.linspace(0, T, 1000)
y_cont = np.sin(2 * np.pi * f * t_cont + np.pi/36) + np.sin(8 * np.pi * f * t_cont)

f_s1 = 32
N1 = int(f_s1 * T)
t1 = np.linspace(0, T, N1, endpoint=False)
y1 = np.sin(2 * np.pi * f * t1 + np.pi/36) + np.sin(8 * np.pi * f * t1)

Y1 = fft(y1)
freqs1 = fftfreq(N1, d=1/f_s1)
memory1 = N1 * 8

f_s2 = f_s1 * 4
N2 = int(f_s2 * T)
t2 = np.linspace(0, T, N2, endpoint=False)
y2 = np.sin(2 * np.pi * f * t2 + np.pi/36) + np.sin(8 * np.pi * f * t2)

Y2 = fft(y2)
freqs2 = fftfreq(N2, d=1/f_s2)
memory2 = N2 * 8

print(f"Ширина спектра (f_s={f_s1} Гц): 0 - {f_s1/2} Гц")
print(f"Объем памяти: {memory1} байт")
print(f"Разность max и min значения массива y1: {np.max(y1) - np.min(y1):.4f}")
print()
print(f"Ширина спектра (f_s={f_s2} Гц): 0 - {f_s2/2} Гц")
print(f"Объем памяти: {memory2} байт")
print(f"Разность max и min значения массива y2: {np.max(y2) - np.min(y2):.4f}")

plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t_cont, y_cont)
plt.title('Оригинальный сигнал')
plt.xlabel('t')
plt.ylabel('y(t)')

plt.subplot(2, 1, 2)
plt.stem(t1, y1, markerfmt=' ')
plt.title(f'Оцифрованный сигнал (f_s={f_s1} Гц)')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t_cont, y_cont)
plt.title('Оригинальный сигнал')
plt.xlabel('t')
plt.ylabel('y(t)')

plt.subplot(2, 1, 2)
plt.plot(t1, y1)
plt.title(f'Восстановление сигнала (f_s={f_s1} Гц)')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t_cont, y_cont)
plt.title('Оригинальный сигнал')
plt.xlabel('t')
plt.ylabel('y(t)')

plt.subplot(2, 1, 2)
plt.stem(t2, y2, markerfmt=' ')
plt.title(f'Оцифрованный сигнал (f_s={f_s2} Гц)')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t_cont, y_cont)
plt.title('Оригинальный сигнал')
plt.xlabel('t')
plt.ylabel('y(t)')

plt.subplot(2, 1, 2)
plt.plot(t2, y2)
plt.title(f'Восстановление сигнала (f_s={f_s2} Гц)')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.tight_layout()
plt.show()

def quantize(y, bits):
    L = 2**bits - 1
    code = np.round((y - np.min(y)) / (np.max(y) - np.min(y)) * L)
    code = np.clip(code, 0, L)
    return code / L * (np.max(y) - np.min(y)) + np.min(y)

half = N2 // 2
S_ref = np.abs(Y2[:half]) / N2 * 2

print()
plt.figure(figsize=(10, 10))
for i, bits in enumerate([3, 4, 5, 6], start=1):
    yq = quantize(y2, bits)
    err = np.mean(np.abs(y2 - yq))
    print(f"Разрядность {bits}: средняя ошибка квантования = {err:.5f}")

    Sq = np.abs(fft(yq)[:half]) / N2 * 2
    plt.subplot(4, 1, i)
    plt.plot(freqs2[:half], S_ref, 'b', label='без квантования')
    plt.plot(freqs2[:half], Sq, 'r', label='с квантованием')
    plt.title(f'Спектр, разрядность {bits}')
    plt.xlabel('Частота, Гц')
    plt.ylabel('Амплитуда')
    plt.xlim(0, f_s2 / 2)
    plt.legend()
plt.tight_layout()
plt.show() 

# show must go on