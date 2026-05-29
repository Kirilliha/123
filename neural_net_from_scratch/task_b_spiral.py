"""
Задача B: классификация 2D-спирали на 3 класса.

Датасет генерируется по формуле из CS231n Stanford: для каждого класса k
радиус r растёт линейно, угол theta = k * 4 + r * 4 + шум.

Архитектуры:
    small:  2 -> 16 (ReLU) -> 3
    big:    2 -> 64 (ReLU) -> 64 (ReLU) -> 3
Сравниваем decision boundary — увидим, что большой модели хватает мощности
выучить спираль, а маленькой нет.
"""

import numpy as np
import matplotlib.pyplot as plt

from nn import Linear, ReLU, SoftmaxCrossEntropy, NeuralNetwork


# ---------- Гиперпараметры ----------
N_PER_CLASS = 100      # 100 точек на класс -> всего 300
N_CLASSES = 3
NOISE = 0.2            # шум угла, побольше -> сложнее задача
TRAIN_FRAC = 0.8
EPOCHS = 3000          # для 2D-спирали 3к обычно хватает
LEARNING_RATE = 1.0    # CE-loss малочувствительна, lr можно крупный
LOG_EVERY = 200
SEED = 1


# ---------- Данные ----------
def make_spiral(n_per_class, n_classes, noise, seed=0):
    """CS231n-style spiral. Возвращает X (N, 2), y (N,) с метками 0..K-1."""
    rng = np.random.RandomState(seed)
    N = n_per_class * n_classes
    X = np.zeros((N, 2))
    y = np.zeros(N, dtype=np.int64)
    for k in range(n_classes):
        ix = range(n_per_class * k, n_per_class * (k + 1))
        r = np.linspace(0.0, 1.0, n_per_class)
        # 4 — "сколько витков", сдвиг по классу 4 — разводит классы по углу
        t = np.linspace(k * 4.0, (k + 1) * 4.0, n_per_class) + rng.randn(n_per_class) * noise
        X[ix] = np.c_[r * np.sin(t), r * np.cos(t)]
        y[ix] = k
    return X, y


def train_val_split(X, y, frac, seed=0):
    """Перемешать и разрезать."""
    rng = np.random.RandomState(seed)
    idx = rng.permutation(len(X))
    cut = int(len(X) * frac)
    tr, va = idx[:cut], idx[cut:]
    return X[tr], y[tr], X[va], y[va]


# ---------- Тренировка ----------
def train(net, loss_fn, X_tr, y_tr, X_va, y_va, epochs, lr, log_every):
    """Полнобатчевый GD: для 300 точек этого достаточно и стабильнее SGD."""
    hist = {"tr_loss": [], "va_loss": [], "tr_acc": [], "va_acc": []}
    for ep in range(epochs):
        loss = net.train_step_softmax(X_tr, y_tr, lr, loss_fn)

        # Валидируемся каждую эпоху — датасет крошечный, это бесплатно.
        va_logits = net.forward(X_va)
        va_loss = loss_fn.forward(va_logits, y_va)
        tr_acc = (loss_fn.predict(net.forward(X_tr)) == y_tr).mean()
        va_acc = (loss_fn.predict(va_logits) == y_va).mean()
        hist["tr_loss"].append(loss)
        hist["va_loss"].append(va_loss)
        hist["tr_acc"].append(tr_acc)
        hist["va_acc"].append(va_acc)

        if (ep + 1) % log_every == 0:
            print(f"  epoch {ep+1:4d}  tr_loss={loss:.4f}  va_loss={va_loss:.4f}  "
                  f"tr_acc={tr_acc:.3f}  va_acc={va_acc:.3f}")
    return hist


# ---------- Визуализация ----------
def plot_curves(hist, title, fname):
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(hist["tr_loss"], label="train")
    ax[0].plot(hist["va_loss"], label="val")
    ax[0].set_title(f"{title}: loss"); ax[0].set_xlabel("epoch")
    ax[0].legend(); ax[0].grid(True, alpha=0.3)

    ax[1].plot(hist["tr_acc"], label="train")
    ax[1].plot(hist["va_acc"], label="val")
    ax[1].set_title(f"{title}: accuracy"); ax[1].set_xlabel("epoch")
    ax[1].legend(); ax[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(fname, dpi=120)
    plt.close()


def plot_decision_boundary(net, loss_fn, X, y, title, fname, grid=200):
    """Прогоняем сетку grid x grid через сеть и красим фон."""
    pad = 0.2
    x_min, x_max = X[:, 0].min() - pad, X[:, 0].max() + pad
    y_min, y_max = X[:, 1].min() - pad, X[:, 1].max() + pad
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, grid),
                          np.linspace(y_min, y_max, grid))
    grid_pts = np.c_[xx.ravel(), yy.ravel()]
    Z = loss_fn.predict(net.forward(grid_pts)).reshape(xx.shape)

    plt.figure(figsize=(6, 5))
    plt.contourf(xx, yy, Z, alpha=0.3, levels=np.arange(N_CLASSES + 1) - 0.5)
    plt.scatter(X[:, 0], X[:, 1], c=y, s=12, edgecolor="k", linewidth=0.3)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(fname, dpi=120)
    plt.close()


# ---------- Main ----------
def build_small():
    # Мало нейронов — модель буквально не может уместить 3 закрученных рукава.
    return NeuralNetwork([Linear(2, 16), ReLU(), Linear(16, N_CLASSES)])


def build_big():
    # 64+64 — с запасом по мощности для трёх-рукавной спирали.
    return NeuralNetwork([
        Linear(2, 64), ReLU(),
        Linear(64, 64), ReLU(),
        Linear(64, N_CLASSES),
    ])


def main():
    np.random.seed(SEED)
    X, y = make_spiral(N_PER_CLASS, N_CLASSES, NOISE, seed=SEED)
    X_tr, y_tr, X_va, y_va = train_val_split(X, y, TRAIN_FRAC, seed=SEED)
    print(f"train={len(X_tr)}, val={len(X_va)}, классов={N_CLASSES}")

    for name, build in [("small (2->16->3)", build_small),
                        ("big (2->64->64->3)", build_big)]:
        print(f"\n=== Архитектура: {name} ===")
        np.random.seed(SEED)  # одинаковая инициализация для честного сравнения
        net = build()
        loss_fn = SoftmaxCrossEntropy()
        hist = train(net, loss_fn, X_tr, y_tr, X_va, y_va,
                     EPOCHS, LEARNING_RATE, LOG_EVERY)
        tag = name.split()[0]
        plot_curves(hist, name, f"spiral_curves_{tag}.png")
        plot_decision_boundary(net, loss_fn, X, y,
                                f"Decision boundary: {name}",
                                f"spiral_boundary_{tag}.png")
        print(f"  final val_acc = {hist['va_acc'][-1]:.3f}")
        print(f"  графики: spiral_curves_{tag}.png, spiral_boundary_{tag}.png")


if __name__ == "__main__":
    main()
