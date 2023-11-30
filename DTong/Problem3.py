import numpy as np
import matplotlib.pyplot as plt

# 시간 범위를 생성
t = np.linspace(-1, 1, 1000)  # -1부터 1까지 1000개의 점

# 𝑇𝑏 값 설정
Tb = 0.2

# 𝑝(𝑡) = sinc(𝑡/𝑇𝑏)를 계산
p_t = np.sinc(t / Tb)

# 𝑦(𝑡) 계산
y_t = p_t + 0.8 * np.roll(p_t, -1) + 1.2 * np.roll(p_t, -2) + 0.3 * np.roll(p_t, -3)

# 그리기
plt.figure(figsize=(10, 6))
plt.plot(t, y_t, label="y(t)")
plt.title("y(t) Graph")
plt.xlabel("Time")
plt.ylabel("Value")
plt.grid(True)
plt.legend()
plt.show()