"""
nn.py — мини-фреймворк нейронной сети на чистом NumPy.

Состав:
    Layer            — абстрактный интерфейс слоя
    Linear           — полносвязный слой Z = X·W + b
    ReLU             — активация max(0, z)
    Sigmoid          — активация 1/(1+e^-z)  (для бинарной классификации)
    SoftmaxCrossEntropy — Softmax-выход + Cross-Entropy loss одним блоком
    BCELoss          — Binary Cross-Entropy (поверх Sigmoid)
    NeuralNetwork    — контейнер: forward / backward / update / train_step

Соглашение о размерностях:
    X имеет форму (m, in_features), где m = batch_size.
    W имеет форму (in_features, out_features).
    b имеет форму (1, out_features) и броадкастится по строкам.
    Выход слоя Z = X·W + b имеет форму (m, out_features).
"""

import numpy as np


# ---------------------------------------------------------------------------
# Базовый интерфейс слоя
# ---------------------------------------------------------------------------
class Layer:
    """Абстрактный слой. Любой конкретный слой реализует forward/backward."""

    def forward(self, x):
        """x -> y. Сохраняем то, что понадобится в backward."""
        raise NotImplementedError

    def backward(self, grad_output):
        """grad относительно выхода -> grad относительно входа.
        Если у слоя есть параметры, тут же считаем dW, db и сохраняем их."""
        raise NotImplementedError

    def get_params(self):
        """Список ссылок на параметры (W, b)."""
        return []

    def get_grads(self):
        """Список ссылок на градиенты параметров (dW, db)."""
        return []

    def update_params(self, lr):
        """Простой SGD: W -= lr * dW."""
        for p, g in zip(self.get_params(), self.get_grads()):
            # in-place, чтобы не пересоздавать массив и не ломать ссылку
            p -= lr * g


# ---------------------------------------------------------------------------
# Полносвязный слой
# ---------------------------------------------------------------------------
class Linear(Layer):
    """Полносвязный слой: Z = X·W + b.

    He initialization: W ~ N(0, 2/in_features). Подходит для ReLU, потому что
    дисперсия активаций сохраняется примерно постоянной от слоя к слою —
    нет ни взрыва, ни затухания сигнала.
    """

    def __init__(self, in_features, out_features):
        self.in_features = in_features
        self.out_features = out_features

        # He init: масштаб sqrt(2 / fan_in). Нули давали бы одинаковые градиенты
        # для всех нейронов слоя — сеть так и осталась бы "одним нейроном".
        self.W = np.random.randn(in_features, out_features) * np.sqrt(2.0 / in_features)
        self.b = np.zeros((1, out_features))

        # Градиенты заполнятся в backward
        self.dW = np.zeros_like(self.W)
        self.db = np.zeros_like(self.b)

        # Кэш для backward
        self.x_cache = None

    def forward(self, x):
        # x: (m, in_features) -> z: (m, out_features)
        if x.ndim != 2 or x.shape[1] != self.in_features:
            raise ValueError(
                f"Linear.forward: ожидался x формы (m, {self.in_features}), "
                f"получено {x.shape}"
            )
        self.x_cache = x  # понадобится для dW = X^T·dZ
        return x @ self.W + self.b  # broadcasting b по batch измерению

    def backward(self, grad_output):
        # grad_output: dL/dZ формы (m, out_features).
        # ВАЖНОЕ соглашение: loss-функция (Softmax+CE, BCE) уже усреднила по
        # батчу — то есть grad_output уже содержит множитель 1/m. Поэтому
        # здесь мы НИЧЕГО на m не делим, чтобы не учесть его дважды.
        # Цепное правило:
        #   dL/dW = X^T · dZ      — (in, m)·(m, out) = (in, out)
        #   dL/db = sum(dZ, axis=0)
        #   dL/dX = dZ · W^T      — (m, out)·(out, in) = (m, in)
        if grad_output.shape[1] != self.out_features:
            raise ValueError(
                f"Linear.backward: ожидался grad формы (m, {self.out_features}), "
                f"получено {grad_output.shape}"
            )
        self.dW = self.x_cache.T @ grad_output
        self.db = np.sum(grad_output, axis=0, keepdims=True)
        grad_input = grad_output @ self.W.T
        return grad_input

    def get_params(self):
        return [self.W, self.b]

    def get_grads(self):
        return [self.dW, self.db]


# ---------------------------------------------------------------------------
# ReLU
# ---------------------------------------------------------------------------
class ReLU(Layer):
    """ReLU(z) = max(0, z). Производная: 1 при z>0, 0 при z<=0.

    Почему не Sigmoid в скрытых слоях:
      производная sigmoid'(z) = s(z)*(1 - s(z)) <= 0.25.
      В глубокой сети градиент умножается на маленькие числа на каждом слое,
      и быстро затухает (vanishing gradient). У ReLU производная = 1 в активной
      зоне — градиент проходит без затухания.
    """

    def __init__(self):
        self.mask = None  # 1.0 где z > 0, иначе 0.0

    def forward(self, x):
        self.mask = (x > 0).astype(x.dtype)
        return x * self.mask

    def backward(self, grad_output):
        # dL/dx = dL/dy * 1[x>0]
        return grad_output * self.mask


# ---------------------------------------------------------------------------
# Sigmoid — для бинарной классификации
# ---------------------------------------------------------------------------
class Sigmoid(Layer):
    """sigmoid(z) = 1 / (1 + exp(-z)). Производная: s*(1-s)."""

    def __init__(self):
        self.out = None

    def forward(self, x):
        # Численно стабильная реализация: разделяем положительные/отрицательные z
        out = np.empty_like(x)
        pos = x >= 0
        neg = ~pos
        out[pos] = 1.0 / (1.0 + np.exp(-x[pos]))
        ex = np.exp(x[neg])
        out[neg] = ex / (1.0 + ex)
        self.out = out
        return out

    def backward(self, grad_output):
        return grad_output * self.out * (1.0 - self.out)


# ---------------------------------------------------------------------------
# Softmax + Cross-Entropy одним блоком
# ---------------------------------------------------------------------------
class SoftmaxCrossEntropy:
    """Объединённый слой Softmax + Cross-Entropy.

    Почему вместе? Производная очень простая и численно стабильная:
        dL/dZ = (P - Y) / m,
    где P = softmax(Z), Y — one-hot, m — batch_size.
    А если считать Softmax и CE по отдельности — у CE появляется деление на
    p_k, что взрывается при p_k -> 0.

    Численно стабильный softmax: вычитаем max по строке перед exp, чтобы
    не словить overflow в exp(big_number).
    """

    def __init__(self):
        self.probs = None
        self.y_onehot = None

    @staticmethod
    def _softmax(z):
        # z: (m, C)
        z_shift = z - np.max(z, axis=1, keepdims=True)  # стабилизация
        exp = np.exp(z_shift)
        return exp / np.sum(exp, axis=1, keepdims=True)

    def forward(self, z, y):
        """
        z: (m, C) — сырые логиты с последнего Linear-слоя
        y: (m,)   — индексы классов 0..C-1
        Возвращает скалярный средний loss по батчу.
        """
        if z.ndim != 2:
            raise ValueError(f"SoftmaxCE.forward: z должен быть 2D, получено {z.shape}")
        if y.ndim != 1 or y.shape[0] != z.shape[0]:
            raise ValueError(
                f"SoftmaxCE.forward: y должен быть 1D длины {z.shape[0]}, "
                f"получено {y.shape}"
            )
        m, C = z.shape
        self.probs = self._softmax(z)  # (m, C)

        # one-hot для backward
        self.y_onehot = np.zeros_like(self.probs)
        self.y_onehot[np.arange(m), y] = 1.0

        # Cross-entropy: -log(p_yi). Берём вероятность правильного класса.
        # Клип защищает от log(0) при численном нуле.
        eps = 1e-12
        correct_probs = self.probs[np.arange(m), y]
        loss = -np.mean(np.log(correct_probs + eps))
        return loss

    def backward(self):
        """dL/dZ = (P - Y) / m — выводится аналитически из softmax+CE."""
        m = self.probs.shape[0]
        return (self.probs - self.y_onehot) / m

    def predict(self, z):
        """Удобная утилита: индексы предсказанных классов."""
        return np.argmax(z, axis=1)


# ---------------------------------------------------------------------------
# BCE — для бинарной классификации (XOR)
# ---------------------------------------------------------------------------
class BCELoss:
    """Binary Cross-Entropy поверх Sigmoid.

    Принимает уже посчитанные вероятности p (выход Sigmoid).
    L = -mean(y*log(p) + (1-y)*log(1-p)).
    dL/dp = (p - y) / (p*(1-p) * m). Если её соединить с производной Sigmoid
    (s*(1-s)), то на ВХОДЕ В Sigmoid получим dL/dz = (p - y) / m — простой и
    численно стабильный градиент. Но здесь мы держим Sigmoid отдельным слоем,
    поэтому возвращаем dL/dp и пускаем его обратно через Sigmoid.backward.
    """

    def __init__(self):
        self.p = None
        self.y = None

    def forward(self, p, y):
        # p: (m, 1) — вероятности; y: (m, 1) — 0/1
        if p.shape != y.shape:
            raise ValueError(f"BCE: shape mismatch p={p.shape}, y={y.shape}")
        eps = 1e-12
        self.p = np.clip(p, eps, 1 - eps)
        self.y = y
        return -np.mean(self.y * np.log(self.p) + (1 - self.y) * np.log(1 - self.p))

    def backward(self):
        m = self.p.shape[0]
        return (self.p - self.y) / (self.p * (1 - self.p) * m)


# ---------------------------------------------------------------------------
# Контейнер сети
# ---------------------------------------------------------------------------
class NeuralNetwork:
    """Список слоёв + удобные методы train_step/predict."""

    def __init__(self, layers):
        self.layers = layers

    def forward(self, x):
        out = x
        for layer in self.layers:
            out = layer.forward(out)
        return out

    def backward(self, grad_output):
        """Идём по слоям в обратном порядке, прокидывая grad."""
        grad = grad_output
        for layer in reversed(self.layers):
            grad = layer.backward(grad)
        return grad

    def update(self, lr):
        for layer in self.layers:
            layer.update_params(lr)

    def train_step_softmax(self, x, y, lr, loss_fn):
        """Шаг обучения для многоклассовой классификации (Softmax+CE)."""
        logits = self.forward(x)
        loss = loss_fn.forward(logits, y)
        grad = loss_fn.backward()
        self.backward(grad)
        self.update(lr)
        return loss

    def train_step_bce(self, x, y, lr, loss_fn):
        """Шаг обучения для бинарной классификации (Sigmoid+BCE)."""
        p = self.forward(x)
        loss = loss_fn.forward(p, y)
        grad = loss_fn.backward()
        self.backward(grad)
        self.update(lr)
        return loss
