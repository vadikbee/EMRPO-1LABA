import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.optimize import fsolve
from scipy.special import factorial # Импорт остается для таблицы 24242424333
from io import StringIO

# --- Конфигурация страницы ---
st.set_page_config(
    page_title="Лабораторная работа №1 | Jupyter & Python",
    page_icon="📚",
    layout="wide"
)

# --- Стилизация (ТЁМНАЯ ТЕМА) ---
st.markdown("""
<style>
    /* Основной фон и текст */
    .stApp {
        background-color: #0E1117; /* Темный фон Streamlit по умолчанию */
        color: #FAFAFA; /* Светлый текст */
    }
    /* Заголовки */
    h1, h2, h3 {
        color: #33A4FF; /* Яркий синий для акцента */
    }
    /* Боковая панель */
    .css-1d391kg {
        background-color: #1F222B; /* Чуть светлее основного фона */
        border-right: 2px solid #33A4FF;
    }
    /* Информационные блоки */
    .stAlert {
        border-radius: 10px;
        border: 1px solid #33A4FF;
        background-color: #1F222B;
    }
    /* Таблицы Pandas */
    .dataframe-container {
        background-color: #0E1117;
    }
</style>
""", unsafe_allow_html=True)

# --- Настройка стиля для графиков Matplotlib (ТЁМНАЯ ТЕМА) ---
plt.style.use('dark_background')
plt.rc('figure', facecolor='#0E1117', edgecolor='#33A4FF')
plt.rc('axes', facecolor='#1F222B', edgecolor='gray', labelcolor='white', titlecolor='#33A4FF')
plt.rc('xtick', color='white')
plt.rc('ytick', color='white')
plt.rc('legend', facecolor='#1F222B', edgecolor='gray')


# --- Функции для Задания 2 ---
@st.cache_data
def get_time_in_microseconds():
    """Возвращает словарь с временными интервалами в микросекундах."""
    return {
        "Секунда": 1e6,
        "Минута": 60 * 1e6,
        "Час": 3600 * 1e6,
        "День": 24 * 3600 * 1e6,
        "Месяц": 30 * 24 * 3600 * 1e6,
        "Год": 365 * 24 * 3600 * 1e6,
        "Век": 100 * 365 * 24 * 3600 * 1e6
    }

def solve_for_n(func_name, t):
    """Вычисляет максимальное n для заданной функции f(n) и времени t (в микросекундах)."""
    try:
        if func_name == "lg n":
            # Ограничение для избежания переполнения
            return 2**t if t < 1023 else float('inf')
        elif func_name == "√n":
            return t**2
        elif func_name == "n":
            return t
        elif func_name == "n lg n":
            if t == 0: return 0
            func = lambda x: x * np.log2(x) - t if x > 0 else -t
            solution = fsolve(func, x0=t if t > 1 else 1)
            return solution[0]
        elif func_name == "n²":
            return np.sqrt(t)
        elif func_name == "n³":
            return np.cbrt(t)
        elif func_name == "2ⁿ":
            return np.log2(t) if t > 0 else 0
        elif func_name == "n!":
            if t < 1: return 0
            n = 1
            factorial_val = 1
            while factorial_val <= t:
                n += 1
                try:
                    factorial_val *= n
                except OverflowError:
                    return n - 1 # Возвращаем предыдущее значение при переполнении
            return n - 1
        else:
            return "N/A"
    except (ValueError, OverflowError):
        return float('inf') # Если результат слишком большой


# --- ОСНОВНАЯ ЧАСТЬ ПРИЛОЖЕНИЯ ---

st.sidebar.title("Навигация по работе")
app_mode = st.sidebar.selectbox(
    "Выберите раздел:",
    [
        "Введение и постановка задачи",
        "Упражнения: Основы работы",
        "Задание 2: Анализ сложности алгоритмов",
        "Задание 4: Особенности и преимущества Jupyter"
    ]
)

if app_mode == "Введение и постановка задачи":
    st.title("📚 Лабораторная работа №1: Знакомство с Jupyter Notebook")
    st.info("Этот Streamlit-отчет представляет собой интерактивное выполнение заданий из методического указания.")

    st.header("Цели работы:")
    st.markdown("""
    - **Освоить запуск и сохранение** блокнотов Jupyter.
    - **Познакомиться со структурой и интерфейсом** блокнотов.
    - **Получить практическое понимание** самостоятельного использования Jupyter Notebook для анализа данных и программирования на Python.
    """)

    st.header("Задачи к лабораторной работе:")
    st.markdown("""
    1.  **Выполнить все упражнения** из данного документа.
    2.  **Заполнить таблицу** максимальных значений `n` для различных функций сложности `f(n)` и **построить графики** этих функций с помощью Matplotlib.
    3.  Представить отчёт в виде файла `.ipynb` с результатами вашей работы. *(В данном случае отчет представлен в виде Streamlit-приложения)*.
    4.  **Рассказать** основные особенности и преимущества Jupyter Notebook.
    """)

elif app_mode == "Упражнения: Основы работы":
    st.header("Выполнение упражнений из документа")

    st.subheader("Упражнение 1: Hello World")
    st.markdown("Первая ячейка в блокноте - кодовая. Вводим `print('Hello World!')` и нажимаем `Ctrl+Enter`.")
    st.code('In [1]: print("Hello World!")\n\nHello World!', language='python')
    st.markdown("Метка `In [1]` слева показывает, что ячейка с кодом была выполнена первой.")

    st.subheader("Упражнение 2: Работа с задержкой")
    st.markdown("Создаем новую ячейку и выполняем код, который ждет 5 секунд.")
    st.code('In [*]: import time\n        time.sleep(5)', language='python')
    st.markdown("Метка `In [*]` означает, что ячейка в данный момент выполняется ядром (kernel). После завершения она получит свой порядковый номер, например, `In [2]`.")

    st.subheader("Упражнение 3: Возврат значения из функции")
    st.markdown("Ячейка может возвращать значение последней строки. Создадим и вызовем функцию:")
    st.code("""In [2]: def say_hello(recipient):
                 return 'Hello, {}!'.format(recipient)
             say_hello('Tim!')

Out[2]: 'Hello, Tim!'""", language='python')
    st.markdown("Текст `Out[2]` показывает вывод, который вернула ячейка с номером `2`.")

    st.subheader("Упражнение 4: Ячейки Markdown")
    st.markdown("Jupyter позволяет создавать текстовые ячейки с форматированием с помощью языка разметки Markdown. Ниже пример кода разметки и результат его отображения.")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Код в ячейке Markdown:**")
        st.code("""# Это заголовок 1 уровня
## Это заголовок 2 уровня

Это обычный текст параграфа.
Можно выделить текст **жирным** или *курсивом*.

- Можно делать списки
- С несколькими элементами

1. И нумерованные списки
2. Тоже можно

[Это гиперссылка на сайт Python](https://www.python.org)
""", language='markdown')
    with col2:
        st.write("**Результат:**")
        st.markdown("""
        # Это заголовок 1 уровня
        ## Это заголовок 2 уровня
        Это обычный текст параграфа.
        Можно выделить текст **жирным** или *курсивом*.
        - Можно делать списки
        - С несколькими элементами
        1. И нумерованные списки
        2. Тоже можно
        [Это гиперссылка на сайт Python](https://www.python.org)
        """)

    st.subheader("Упражнение 5: Графики с Matplotlib")
    st.markdown("Jupyter Notebook отлично подходит для визуализации данных. С помощью библиотеки `matplotlib` можно строить графики прямо в блокноте.")
    st.code("""import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y1 = x
y2 = x**2

plt.figure()
plt.plot(x, y1, label='y = x')
plt.plot(x, y2, label='y = x^2', linestyle='--')
plt.title("Простой график в Jupyter")
plt.xlabel("Ось X")
plt.ylabel("Ось Y")
plt.legend()
plt.grid(True)
plt.show()
""")
    st.write("**Результат выполнения кода:**")
    x = np.linspace(0, 10, 50)
    y1 = x
    y2 = x**2
    fig, ax = plt.subplots()
    ax.plot(x, y1, label='y = x', color='cyan')
    ax.plot(x, y2, label='y = x^2', linestyle='--', color='magenta')
    ax.set_title("Простой график в Jupyter")
    ax.set_xlabel("Ось X")
    ax.set_ylabel("Ось Y")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)


elif app_mode == "Задание 2: Анализ сложности алгоритмов":
    st.header("Задание 2: Анализ времени выполнения алгоритмов")
    st.info("""
    **Условие:** Заполнить таблицу максимальных значений `n`, для которых задача может быть решена за время `t`.
    Время работы алгоритма равно `f(n)` микросекунд.
    """)

    times = get_time_in_microseconds()
    functions = ["lg n", "√n", "n", "n lg n", "n²", "n³", "2ⁿ", "n!"]

    # Создаем DataFrame для результатов
    df = pd.DataFrame(index=functions, columns=times.keys())

    # Заполняем DataFrame
    for func_name in functions:
        for time_name, time_value in times.items():
            result_n = solve_for_n(func_name, time_value)
            # Форматируем для красивого вывода
            if result_n < 1e5:
                df.loc[func_name, time_name] = f"{result_n:,.0f}"
            else:
                df.loc[func_name, time_name] = f"{result_n:.2e}"


    st.subheader("Таблица максимальных размеров задачи (n)")
    st.dataframe(df.style.set_properties(**{'background-color': '#1F222B', 'color': 'white'}), use_container_width=True)
    st.markdown("""
    *Значения `inf` означают, что `n` настолько велико, что вычисления приводят к переполнению.
    Значения в экспоненциальной нотации (например, `1.23e+4`) используются для очень больших чисел.*
    """)

    st.subheader("Графики функций временной сложности")
    
    # --- НАЧАЛО ИЗМЕНЕНИЙ ---

    # Диапазон n от 1 до 50
    n_values = np.linspace(1, 50, num=200)

    fig, ax = plt.subplots(figsize=(12, 8))

    # Вычисляем значения функций (без факториала)
    with np.errstate(divide='ignore', invalid='ignore'):
        fn_values = {
            "lg n": np.log2(n_values),
            "√n": np.sqrt(n_values),
            "n": n_values,
            "n lg n": n_values * np.log2(n_values),
            "n²": n_values**2,
            "n³": n_values**3,
            "2ⁿ": 2**n_values,
        }

    # Цвета для графиков
    colors = plt.cm.viridis(np.linspace(0, 1, len(fn_values)))

    # Отображаем графики функций
    for (label, y_values), color in zip(fn_values.items(), colors):
        y_plot = np.where(y_values > 0, y_values, np.nan)
        ax.plot(n_values, y_plot, label=label, color=color)
    
    # Настройка графика: линейная шкала по X, логарифмическая по Y
    ax.set_yscale('log')
    ax.set_title('Сравнение функций роста (n от 1 до 50)', fontsize=16)
    ax.set_xlabel('Размер задачи (n)', fontsize=12)
    ax.set_ylabel('Количество операций f(n) (логарифмическая шкала)', fontsize=12)
    ax.legend()
    ax.grid(True, which="both", ls="--", alpha=0.3)
    ax.set_xlim(0, 50)
    ax.set_ylim(bottom=1e-1)

    # --- КОНЕЦ ИЗМЕНЕНИЙ ---

    st.pyplot(fig)
    st.markdown("""
    На графике использована **линейная шкала по оси X** для наглядного отображения диапазона n от 1 до 50 и **логарифмическая шкала по оси Y** для сравнения функций, растущих с очень разной скоростью.
    Благодаря логарифмической шкале, на одном графике удалось разместить как медленно растущие функции (например, `lg n`), так и чрезвычайно быстро растущую (`2^n`).
    """)


elif app_mode == "Задание 4: Особенности и преимущества Jupyter":
    st.header("Задание 4: Основные особенности и преимущества Jupyter Notebook")

    st.markdown("""
    Jupyter Notebook — это интерактивная веб-среда для вычислений, которая позволяет создавать и обмениваться документами, содержащими "живой" код, уравнения, визуализации и сопроводительный текст.
    """)

    st.subheader("1. Интерактивная среда выполнения (REPL)")
    st.markdown("""
    - **Пошаговое исполнение:** Код можно писать и выполнять в небольших, независимых блоках (ячейках). Это идеально подходит для исследования данных, отладки и быстрого прототипирования, так как не нужно перезапускать всю программу для проверки одного изменения.
    - **Сохранение состояния:** Ядро (kernel) хранит состояние вычислений. Переменные, функции и импортированные библиотеки, определенные в одной ячейке, доступны во всех последующих. Это позволяет строить сложные рабочие процессы шаг за шагом.
    """)

    st.subheader("2. Объединение кода и документации")
    st.markdown("""
    - **Формат "грамотного программирования":** Jupyter позволяет смешивать исполняемый код (Python, R, Julia и др.) с форматированным текстом (используя Markdown), математическими формулами (LaTeX), изображениями и графиками.
    - **Воспроизводимые отчеты:** Результатом работы является единый документ (`.ipynb`), который можно легко передать коллегам. Он содержит не только код, но и результаты его выполнения и пояснения, что делает исследование полностью воспроизводимым и понятным.
    """)

    st.subheader("3. Встроенная визуализация данных")
    st.markdown("""
    - **Графики "inline":** Jupyter отлично интегрируется с библиотеками для визуализации, такими как Matplotlib, Seaborn, Plotly. Графики и диаграммы отображаются непосредственно под ячейкой с кодом, который их сгенерировал. Это упрощает анализ и интерпретацию данных "на лету".
    """)

    st.subheader("4. Широкая поддержка языков и экосистема")
    st.markdown("""
    - **Мультиязычность:** Хотя Python является самым популярным языком для Jupyter, среда поддерживает десятки других языков через систему "ядер" (kernels), включая R, Julia, Scala, SQL и многие другие.
    - **Расширяемость:** Существует огромная экосистема расширений (nbextensions), которые добавляют новую функциональность, например, автоформатирование кода, проверку орфографии, создание оглавлений и многое другое.
    """)

    st.subheader("5. Легкость установки и обмена")
    st.markdown("""
    - **Веб-интерфейс:** Jupyter работает в брауере, что делает его кросс-платформенным.
    - **Облачные сервисы:** Платформы, такие как Google Colab, Kaggle Kernels и Binder, позволяют запускать Jupyter Notebooks в облаке без необходимости локальной установки, что упрощает совместную работу и доступ к мощным вычислительным ресурсам.
    """)