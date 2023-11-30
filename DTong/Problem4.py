import numpy as np
import matplotlib.pyplot as plt

# 주파수 범위 생성
frequencies = np.linspace(-20, 20, 1000)  # -20 kHz에서 20 kHz까지

Wo = 10  # 중심 주파수 (10 kHz)
roll_off = 1.0  # Roll-off factor

# Raised cosine 필터의 주파수 응답 계산
H_f = np.zeros(len(frequencies), dtype=complex)
for i, f in enumerate(frequencies):
    if abs(f) <= (1 - roll_off) * Wo:
        H_f[i] = 1.0
    elif (1 - roll_off) * Wo < abs(f) <= (1 + roll_off) * Wo:
        H_f[i] = 0.5 * (1 + np.cos(np.pi * ((abs(f) - (1 - roll_off) * Wo) / (roll_off * Wo))))
    else:
        H_f[i] = 0.0

# 주파수 응답 그래프
plt.figure(figsize=(10, 6))
plt.plot(frequencies, np.abs(H_f), label="Raised Cosine Filter Frequency Response")
plt.title("Raised Cosine Filter Frequency Response")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Value")
plt.xlim([-10,10])    # 이것은 r = 0.5 1.0 일 경우 주석을 풀어서 한 주기를 확인
plt.grid(True)
plt.legend()
plt.show()
