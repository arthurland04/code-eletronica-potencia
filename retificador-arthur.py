import numpy as np #biblioteca numérica
import matplotlib.pyplot as plt #gráficos
from scipy.integrate import solve_ivp #solução de edos

#1)parâmetros do circuito rlc
V0 = 900 #[V] tensão inicial do capacitor
L  = 11e-6 #[H] indutância
R  = 85e-3 #[Ω] resistência
C  = 180e-6 #[F] capacitância

#2)modelo edos
def circuito(t, x):
    """
    x[0] = i  -> corrente no indutor
    x[1] = vC -> tensão no capacitor
    """
    i, vC = x

    #comutação pelo diodo
    #se vC>0: diodo desligado -> C e L em série
    if vC > 0:
        di_dt = vC / L #equação da indutância (V=Ldi/dt)
        dv_dt = -i / C #capacitor descarregando

    #se vC<=0: diodo conduz -> C, L e R em paralelo
    else:
        di_dt = (vC - R * i) / L #queda em R + L
        dv_dt = -(i + vC / R) / C #corrente somada no capacitor

    return [di_dt, dv_dt]

#3)condições iniciais no tempo
i0 = 0.0 #corrente inicial no indutor
v0 = V0 #tensão inicial no capacitor

x0 = [i0, v0] #vetor de estados
t0 = 0.0 #início do tempo
tf = 400e-6 #fim da simulação (400 µs)
t_eval = np.linspace(t0, tf, 4000) #malha de tempo com pontos igualmente espaçados pra função t_eval calcular nesses pontos específicos

#4)solução numérica
#solve_ivp resolve o sistema de edos
sol = solve_ivp(circuito, [t0, tf], x0, t_eval=t_eval)

tempo    = sol.t #eixo do tempo
corrente = sol.y[0] #i(t)
tensao   = sol.y[1] #vC(t)

#5)gráficos da resposta
plt.figure(figsize=(9, 6))

#corrente no indutor
plt.subplot(2, 1, 1) #primeiro gráfico
plt.plot(tempo * 1e6, corrente)
plt.title("Resposta Temporal do Circuito RLC com Diodo")
plt.ylabel("Corrente no Indutor [A]")
plt.grid(True)

#tensão no capacitor
plt.subplot(2, 1, 2) #segundo gráfico
plt.plot(tempo * 1e6, tensao)
plt.xlabel("Tempo [µs]")
plt.ylabel("Tensão no Capacitor [V]")
plt.grid(True)

plt.tight_layout()
plt.show()

#6)resutados numéricos
#valores de pico
print("===== Resultados da Simulação =====")
print(f"Corrente máxima no indutor: {np.max(corrente):.2f} A")
print(f"Tensão mínima no capacitor: {np.min(tensao):.2f} V")
print("===================================")