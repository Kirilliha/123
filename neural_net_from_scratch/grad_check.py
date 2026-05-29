"""
grad_check.py — численная проверка градиентов.

Идея: для каждого скалярного параметра w[i,j] независимо считаем
    numeric = (L(w + eps) - L(w - eps)) / (2 * eps)
и сравниваем с аналитическим dW[i,j], который посчитал backward.

Если |numeric - analytic| / (|numeric| + |analytic| + 1e-12) < 1e-7 — у тебя
правильный backward. На практике для float64 порог 1e-6..1e-7 — норма.

Если упало — лезь в Linear.backward / SoftmaxCrossEntropy.backward.
"""

import numpy as np
from nn import Linear, ReLU, SoftmaxCrossEntropy, NeuralNetwork


def relative_error(a, b):
    """Относительная разница — устойчива к масштабу значений."""
    return np.abs(a - b) / (np.abs(a) + np.abs(b) + 1e-12)


def numerical_gradient(net, loss_fn, x, y, param, eps=1e-5):
    """Считает численный градиент по каждому элементу `param`.
    param — это np.ndarray-ссылка ВНУТРИ слоя (не копия!), иначе оригинал
    не изменится. Возвращает массив той же формы.
    """
    num_grad = np.zeros_like(param)
    it = np.nditer(param, flags=["multi_index"], op_flags=["readwrite"])
    while not it.finished:
        idx = it.multi_index
        orig = param[idx]

        param[idx] = orig + eps
        loss_plus = loss_fn.forward(net.forward(x), y)

        param[idx] = orig - eps
        loss_minus = loss_fn.forward(net.forward(x), y)

        param[idx] = orig  # вернуть значение

        num_grad[idx] = (loss_plus - loss_minus) / (2 * eps)
        it.iternext()
    return num_grad


def run_check():
    np.random.seed(42)

    # Маленькая сеть: 3 -> 5 (ReLU) -> 4 классa.
    # Батч 4. Достаточно маленько, чтобы проверка шла за доли секунды.
    in_features, hidden, n_classes, batch = 3, 5, 4, 4

    layer1 = Linear(in_features, hidden)
    layer2 = Linear(hidden, n_classes)
    net = NeuralNetwork([layer1, ReLU(), layer2])
    loss_fn = SoftmaxCrossEntropy()

    x = np.random.randn(batch, in_features)
    y = np.random.randint(0, n_classes, size=batch)

    # 1) аналитический backward
    logits = net.forward(x)
    loss_fn.forward(logits, y)
    grad = loss_fn.backward()
    net.backward(grad)

    # Снимем КОПИИ аналитических градиентов до того, как numerical начнёт
    # пересчитывать forward — иначе .dW в Linear перезапишется.
    analytic_grads = {
        "layer1.W": layer1.dW.copy(),
        "layer1.b": layer1.db.copy(),
        "layer2.W": layer2.dW.copy(),
        "layer2.b": layer2.db.copy(),
    }

    # 2) численный для каждого параметра
    params = {
        "layer1.W": layer1.W,
        "layer1.b": layer1.b,
        "layer2.W": layer2.W,
        "layer2.b": layer2.b,
    }

    all_ok = True
    for name, p in params.items():
        num = numerical_gradient(net, loss_fn, x, y, p)
        ana = analytic_grads[name]
        err = relative_error(num, ana).max()
        status = "OK" if err < 1e-6 else "FAIL"
        if status == "FAIL":
            all_ok = False
        print(f"  {name:10s}  shape={str(p.shape):12s}  max rel err = {err:.2e}  [{status}]")

    print()
    print("Итог:", "Все градиенты сходятся :)" if all_ok else "Где-то ошибка в backward!")
    return all_ok


if __name__ == "__main__":
    print("Запускаю gradient check (Linear -> ReLU -> Linear -> Softmax+CE)...")
    print()
    run_check()
