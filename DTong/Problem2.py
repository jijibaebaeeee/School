import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# 시간 범위를 생성합니다.
t = np.linspace(0, 10, 1000)  # 0부터 10까지 1000개의 점

# 𝜏 값을 설정합니다.
tau = 3

# 𝑠(𝑡) = ∏(t/𝜏)을 사용하여 사각파형을 생성합니다.
signal = np.array([1 if (0 <= (t_i % (2 * tau)) <= tau) else -1 for t_i in t])

# Fourier 변환을 수행합니다.
signal_fft = fft(signal)

# 주파수 영역에서의 주파수 값 생성
N = len(signal)
freq = np.fft.fftfreq(N)

# 파형을 그립니다.
plt.figure(figsize=(10, 6))

# plt.subplot(2, 1, 1)
# plt.plot(t, signal)
# plt.title("시간 영역에서의 사각파형")
# plt.xlabel("시간")
# plt.ylabel("신호 값")
# plt.grid(True)

# plt.subplot(2, 1, 2)
plt.plot(freq, np.abs(signal_fft))
plt.title("Sinc Function")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.xlim([-0.1, 0.1])
plt.tight_layout()
plt.show()