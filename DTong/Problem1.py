import numpy as np
import matplotlib.pyplot as plt

# 시간 범위를 생성합니다.
t = np.linspace(0, 20, 1000)  # 0부터 20까지 1000개의 점

# 𝜏 값을 설정합니다.
tau = 3

# 𝑠(𝑡) = ∏(t/𝜏)을 사용하여 사각파형을 생성합니다.
signal = np.array([1 if (0 <= (t_i % (2 * tau)) <= tau) else -1 for t_i in t])

# 파형을 그립니다.
plt.figure(figsize=(10, 6))
plt.plot(t, signal, label=f'τ = {tau}')
plt.title("Rectangular Pulse")
plt.xlabel("Time")
plt.ylabel("Value")
plt.grid(True)
plt.ylim([-3,3])
plt.xlim([0,20])
plt.legend()
plt.show()
