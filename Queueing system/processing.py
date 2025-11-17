import subprocess
import json
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_refusal_stats_by_test_simple(tests, test_names=None, start_index=1):
    """
    Упрощенный линейный график (только средние значения с областями)
    """
    if test_names is None:
        test_names = [f'{i+start_index}' for i in range(len(tests))]
    
    means = []
    mins = []
    maxs = []
    
    for test in tests:
        probabilities = [handle['probability_of_refusal'] for handle in test['sources']]
        means.append(np.mean(probabilities))
        mins.append(np.min(probabilities))
        maxs.append(np.max(probabilities))
    
    plt.figure(figsize=(12, 6))
    x_pos = np.arange(len(test_names))
    
    # Основная линия (средние значения)
    plt.plot(x_pos, means, 'o-', color='blue', linewidth=2, label='Средняя вероятность')
    
    # Область отклонений
    plt.fill_between(x_pos, mins, maxs, color='gray', alpha=0.3, label='Диапазон')
    
    plt.xlabel('Число источников')
    plt.ylabel('Вероятность отказа')
    plt.title('Вероятность отказа по тестам')
    plt.xticks(x_pos, test_names)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_usage(tests):
    y = [len(i["handlers"]) for i in tests]
    x = [i["buffer_size"] for i in tests]
    v = []
    for test in tests:
        usage = [handle['utilization_rate'] for handle in test['handlers']]
        v.append(np.mean(usage))

    df = pd.DataFrame({
        'x': x,
        'y': y, 
        'color_param': v})
    df2 = pd.DataFrame({
        'x': x,
        'y': y, 
        'color_param': [i > 0.9 for i in v]})  
    fig = make_subplots(rows=1, cols=2, 
                   subplot_titles=['Удовлетворение условию', 'Непрерывная зависимость'])

    f1 = px.scatter(df, x='x', y='y', color='color_param',
                color_continuous_scale='viridis',
                title='Точки с цветом по параметру (наведите курсор)',
                labels={'color_param': 'Загрузка'},
                hover_data={'x': True, 'y': True, 'color_param': ':.3f'})

    fig.add_trace(f1.data[0], row = 1, col = 2)
    
    f2 = px.scatter(df2, x='x', y='y', color='color_param',
                    color_discrete_sequence=['green', 'red'],
                    title='Точки с цветом по параметру (наведите курсор)',
                    labels={'color_param': 'Удовлетворяют параметрам'})
    for trace in f2.data:
        fig.add_trace(trace, row=1, col=1)

    fig.update_layout(height=800, width=1600, title_text="Загрузка", title_x=0.5)
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Загрузка",
            x=1.02,  # за пределами правого графика
            y=0.5,
            yanchor="middle"))

    # Дискретная легенда - слева  
    fig.update_layout(
        legend=dict(
            title="Условие",
            orientation="h",
            x=0.23,           # центр полотна по горизонтали
            y=-0.14,           # снизу
            yanchor="bottom",
            xanchor="center"  # центр легенды в точке x=0.5
        )
    )
    fig.update_xaxes(title_text="Размер буфера", row=1, col=1)
    fig.update_yaxes(title_text="Число видеокарт", row=1, col=1)

    fig.update_xaxes(title_text="Размер буфера", row=1, col=2)
    fig.update_yaxes(title_text="Число видеокарт", row=1, col=2)
    fig.show()
    fig.write_image('1650_usage.pdf')


def plot_conditions(tests):
    y = [len(i["handlers"]) for i in tests]
    x = [i["buffer_size"] for i in tests]
    v = []
    v1 = []
    v2 = []
    for test in tests:
        usage = [handle['probability_of_refusal'] for handle in test['sources']]
        v1.append(np.mean(usage))
    for test in tests:
        usage = [handle['utilization_rate'] for handle in test['handlers']]
        v2.append(np.mean(usage))

    for a in zip(v1,v2):
        v.append(True if a[0] < 0.1 and a[1] > 0.9 else False)

    df = pd.DataFrame({
        'x': x,
        'y': y, 
        'color_param': v
    })

    # Строим интерактивный график
    fig = px.scatter(df, x='x', y='y', color='color_param',
                    color_discrete_sequence=['red', 'green'],
                    title='Соответствие всем условиям',
                    labels={'color_param': 'Удовлетворяют<br>параметрам'})

    # Настраиваем отображение
    fig.update_layout(
        title_x=0.5,
        xaxis_title='Размер буффера',
        yaxis_title='Число видеокарт',
        width=800,
        height=600
    )


    fig.show()
    fig.write_image('1650_total.pdf')

def plot_rejection_rate(tests):
    y = [len(i["handlers"]) for i in tests]
    x = [i["buffer_size"] for i in tests]
    v = []
    for test in tests:
        usage = [handle['probability_of_refusal'] for handle in test['sources']]
        v.append(np.mean(usage))

    df = pd.DataFrame({
        'x': x,
        'y': y, 
        'color_param': v
    })

    df2 = pd.DataFrame({
        'x': x,
        'y': y, 
        'color_param': [x < 0.1 for x in v]
    })

    fig = make_subplots(rows=1, cols=2, 
                   subplot_titles=['Удовлетворение условию', 'Непрерывная зависимость'])

    f1 = px.scatter(df, x='x', y='y', color='color_param',
                    color_continuous_scale='viridis',
                    title='Точки с цветом по параметру (наведите курсор)',
                    labels={'color_param': 'Вероятность отказа'},
                    hover_data={'x': True, 'y': True, 'color_param': ':.3f'})
    
    f2 = px.scatter(df2, x='x', y='y', color='color_param',
                    color_discrete_sequence=['red','green'],
                    title='Точки с цветом по параметру (наведите курсор)',
                    labels={'color_param': 'Удовлетворяют параметрам'})

    fig.add_trace(f1.data[0], row = 1, col = 2)
    for trace in f2.data:
        fig.add_trace(trace, row=1, col=1)

    fig.update_layout(height=800, width=1600, title_text="Вероятность отказа", title_x=0.5)
    fig.update_layout(
    coloraxis_colorbar=dict(
        title="Вероятность<br>отказа",
        x=1.02,  # за пределами правого графика
        y=0.5,
        yanchor="middle"))

    # Дискретная легенда - слева  
    fig.update_layout(
        legend=dict(
            title="Условие",
            orientation="h",
            x=0.23,           # центр полотна по горизонтали
            y=-0.14,           # снизу
            yanchor="bottom",
            xanchor="center"  # центр легенды в точке x=0.5
        )
    )
    fig.update_xaxes(title_text="Размер буфера", row=1, col=1)
    fig.update_yaxes(title_text="Число видеокарт", row=1, col=1)

    fig.update_xaxes(title_text="Размер буфера", row=1, col=2)
    fig.update_yaxes(title_text="Число видеокарт", row=1, col=2)
    fig.show()
    fig.write_image('1650_rejection_rate.pdf')

def run_executable_and_process_json(params):
    """ Запускает исполняемый файл и обрабатывает созданный JSON """
    try:
        # Запускаем исполняемый файл
        args = [params["path_exe"], "-a", "-o", params["path_output"]]
        p = params["default_params"]
        default_params = [p["sources"],
                          p["sources_lambda"],
                          p["hadlers"],
                          p["handling_min"],
                          p["handling_max"],
                          p["buffer_size"],
                          p["modelling_time"]]
        args += ["-p"] + [str(i) for i in default_params]
        
        v = params["vars"]
        for params_set in v:
                var_params = [params_set["var_param"],
                              params_set["var_min"],
                              params_set["var_max"]]
                args += ["-v"] +  [str(i) for i in var_params]

        print(f"Запуск {" ".join(args)}")
        subprocess.run(args, capture_output=True, text=True, check=True)
        
        # Проверяем, что файл создался
        if not os.path.exists(params["path_output"]):
            raise FileNotFoundError(f"JSON файл не создан: {params["path_output"]}")
        
        # Читаем и парсим JSON
        with open(params["path_output"], 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Успешно запущено и обработано!")
        return data
        
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске исполняемого файла: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

# Использование
if __name__ == "__main__":    
    with open("config.json") as f:
        params = json.load(f)    
    data = run_executable_and_process_json(params)
    
    if data:
        # Обработка данных
        print("Обработка данных...")
        print(f"Количество источников: {len(data[0]['sources'])}")
        print(f"Количество обработчиков: {len(data[0]['handlers'])}")
        
        # Пример анализа данных
        for source in data[0]['sources']:
            print(f"Источник {source['id']}: отказы {source['probability_of_refusal']:.2%}")

    #plot_refusal_stats_by_test_simple(data)
    plot_usage(data)
    plot_rejection_rate(data)
    plot_conditions(data)