"""
Задача A: XOR.

Цель — убедиться, что backprop работает. XOR — это не линейно разделимая
задача: один линейный слой её НЕ решит. Нужен скрытый слой с нелинейностью.

Архитектура: 2 -> 4 (ReLU) -> 1 (Sigmoid). Loss: BCE.
"""

import numpy as np
import matplotlib.pyplot as plt

from nn import Linear, ReLU, Sigmoid, BCELoss, NeuralNetwork


# Гиперпараметры — все с пояснением, никаких магических чисел.
EPOCHS = 2000        # XOR — крошечная задача, 1-2к эпох с запасом
LEARNING_RATE = 0.1  # большой батч маленький, можно агрессивно
HIDDEN = 4           # минимум для XOR — 2, но 4 учится надёжнее
SEED = 0             # детерминизм при повторных запусках


def main():
    np.random.seed(SEED)

    # 4 примера: все комбинации двух бит
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]], dtype=np.float64)
    Y = np.array([[0],
                  [1],
                  [1],
                  [0]], dtype=np.float64)

    net = NeuralNetwork([
        Linear(2, HIDDEN),
        ReLU(),
        Linear(HIDDEN, 1),
        Sigmoid(),
    ])
    loss_fn = BCELoss()

    print("До обучения:")
    print("  предсказания:", net.forward(X).flatten().round(3))
    print("  целевые:    ", Y.flatten())

    losses = []
    for epoch in range(EPOCHS):
        loss = net.train_step_bce(X, Y, LEARNING_RATE, loss_fn)
        losses.append(loss)
        if (epoch + 1) % 200 == 0:
            print(f"  epoch {epoch+1:4d}  loss = {loss:.4f}")

    preds = net.forward(X).flatten()
    print()
    print("После обучения:")
    print("  предсказания:    ", preds.round(3))
    print("  бинаризованные:  ", (preds > 0.5).astype(int))
    print("  целевые:         ", Y.flatten().astype(int))

    # График loss — он должен монотонно падать (с короткими плато).
    plt.figure(figsize=(6, 4))
    plt.plot(losses)
    plt.xlabel("epoch")
    plt.ylabel("BCE loss")
    plt.title("XOR: обучение")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("xor_loss.png", dpi=120)
    print("\nГрафик сохранён в xor_loss.png")


if __name__ == "__main__":
    main()
