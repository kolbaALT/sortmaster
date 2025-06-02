// Адаптированная версия SortVis для SortMaster
class SortVisualizer {
    constructor(containerId, algorithm) {
        this.container = document.getElementById(containerId);
        this.algorithm = algorithm;
        this.array = [];
        this.isRunning = false;
        this.isPaused = false;
        this.speed = 100;
        this.stats = {
            comparisons: 0,
            swaps: 0,
            steps: 0,
            startTime: null
        };

        this.init();
    }

    init() {
        this.container.innerHTML = '';
        this.container.style.cssText = `
            width: 100%;
            height: 400px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            display: flex;
            align-items: end;
            justify-content: center;
            padding: 20px;
            position: relative;
        `;

        // Добавляем заголовок
        const title = document.createElement('div');
        title.style.cssText = `
            position: absolute;
            top: 10px;
            left: 20px;
            font-weight: bold;
            color: #495057;
            font-size: 16px;
        `;
        title.textContent = `Визуализация: ${this.algorithm}`;
        this.container.appendChild(title);
    }

    generateArray(size) {
        this.array = [];
        for (let i = 0; i < size; i++) {
            this.array.push(Math.floor(Math.random() * 300) + 10);
        }
        this.renderArray();
        this.resetStats();
    }

    renderArray() {
        // Очищаем контейнер, оставляя заголовок
        const title = this.container.querySelector('div');
        this.container.innerHTML = '';
        if (title) this.container.appendChild(title);

        const maxHeight = 300;
        const maxValue = Math.max(...this.array);
        const barWidth = Math.min(40, (this.container.clientWidth - 40) / this.array.length);

        this.array.forEach((value, index) => {
            const bar = document.createElement('div');
            const height = (value / maxValue) * maxHeight;

            bar.style.cssText = `
                width: ${barWidth - 2}px;
                height: ${height}px;
                background: linear-gradient(to top, #007bff, #0056b3);
                margin: 0 1px;
                border-radius: 4px 4px 0 0;
                display: inline-block;
                transition: all 0.3s ease;
                position: relative;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            `;

            // Добавляем значение на столбец
            const label = document.createElement('span');
            label.style.cssText = `
                position: absolute;
                top: -20px;
                left: 50%;
                transform: translateX(-50%);
                font-size: 10px;
                color: #495057;
                font-weight: bold;
            `;
            label.textContent = value;
            bar.appendChild(label);

            bar.dataset.index = index;
            bar.dataset.value = value;
            this.container.appendChild(bar);
        });
    }

    async bubbleSort() {
        const n = this.array.length;

        for (let i = 0; i < n - 1; i++) {
            let swapped = false;

            for (let j = 0; j < n - i - 1; j++) {
                if (this.isPaused) {
                    await this.waitForResume();
                }

                // Подсвечиваем сравниваемые элементы
                this.highlightBars([j, j + 1], '#ffc107');
                this.stats.comparisons++;
                this.updateStats();

                await this.sleep(this.speed);

                if (this.array[j] > this.array[j + 1]) {
                    // Обмен элементов
                    await this.swapElements(j, j + 1);
                    swapped = true;
                    this.stats.swaps++;
                    this.updateStats();
                }

                // Убираем подсветку сравнения
                this.highlightBars([j, j + 1], '#007bff');
                this.stats.steps++;
                this.updateStats();
            }

            // Помечаем последний отсортированный элемент
            this.highlightBars([n - i - 1], '#28a745');

            // Если обменов не было, массив уже отсортирован
            if (!swapped) {
                // Помечаем все оставшиеся элементы как отсортированные
                for (let k = 0; k < n - i - 1; k++) {
                    this.highlightBars([k], '#28a745');
                }
                break;
            }
        }

        // Помечаем первый элемент как отсортированный (если цикл завершился полностью)
        this.highlightBars([0], '#28a745');
    }

    async selectionSort() {
        const n = this.array.length;

        for (let i = 0; i < n - 1; i++) {
            if (this.isPaused) {
                await this.waitForResume();
            }

            let minIdx = i;
            this.highlightBars([i], '#dc3545'); // Текущая позиция

            for (let j = i + 1; j < n; j++) {
                if (this.isPaused) {
                    await this.waitForResume();
                }

                this.highlightBars([j], '#ffc107'); // Проверяемый элемент
                this.stats.comparisons++;
                this.updateStats();

                await this.sleep(this.speed);

                if (this.array[j] < this.array[minIdx]) {
                    if (minIdx !== i) this.highlightBars([minIdx], '#007bff');
                    minIdx = j;
                    this.highlightBars([minIdx], '#dc3545'); // Новый минимум
                } else {
                    this.highlightBars([j], '#007bff');
                }

                this.stats.steps++;
                this.updateStats();
            }

            if (minIdx !== i) {
                await this.swapElements(i, minIdx);
                this.stats.swaps++;
            }

            this.highlightBars([i], '#28a745'); // Отсортированный
        }

        this.highlightBars([n - 1], '#28a745');
    }

    async insertionSort() {
        const n = this.array.length;
        this.highlightBars([0], '#28a745'); // Первый элемент уже "отсортирован"

        for (let i = 1; i < n; i++) {
            if (this.isPaused) {
                await this.waitForResume();
            }

            let key = this.array[i];
            let j = i - 1;

            // Подсвечиваем вставляемый элемент
            this.highlightBars([i], '#ffc107');
            await this.sleep(this.speed);

            // Сдвигаем элементы, которые больше key
            while (j >= 0) {
                if (this.isPaused) {
                    await this.waitForResume();
                }

                this.stats.comparisons++;
                this.updateStats();

                // Подсвечиваем сравниваемый элемент
                this.highlightBars([j], '#dc3545');
                await this.sleep(this.speed);

                if (this.array[j] <= key) {
                    // Нашли правильное место
                    this.highlightBars([j], '#28a745');
                    break;
                }

                // Сдвигаем элемент вправо (НЕ обмен!)
                this.array[j + 1] = this.array[j];
                await this.shiftElement(j, j + 1);

                this.highlightBars([j], '#28a745'); // Элемент остается отсортированным
                j--;

                this.stats.steps++;
                this.updateStats();
            }

            // Вставляем key в правильную позицию
            this.array[j + 1] = key;
            await this.insertElement(j + 1, key);

            // Помечаем вставленный элемент как отсортированный
            this.highlightBars([j + 1], '#28a745');

            this.stats.steps++;
            this.updateStats();
        }
    }

    async swapElements(i, j) {
        const bars = this.container.querySelectorAll('div[data-index]');
        const bar1 = bars[i];
        const bar2 = bars[j];

        if (!bar1 || !bar2) return;

        // Подсвечиваем обмениваемые элементы
        this.highlightBars([i, j], '#dc3545');

        // Анимация подъема
        bar1.style.transform = 'translateY(-30px)';
        bar2.style.transform = 'translateY(-30px)';

        await this.sleep(this.speed / 2);

        // Обмен значений в массиве
        [this.array[i], this.array[j]] = [this.array[j], this.array[i]];

        // Обмен высот столбцов
        const tempHeight = bar1.style.height;
        bar1.style.height = bar2.style.height;
        bar2.style.height = tempHeight;

        // Обмен значений в подписях
        const label1 = bar1.querySelector('span');
        const label2 = bar2.querySelector('span');
        if (label1 && label2) {
            const tempText = label1.textContent;
            label1.textContent = label2.textContent;
            label2.textContent = tempText;
        }

        await this.sleep(this.speed / 2);

        // Возвращаем элементы на место
        bar1.style.transform = '';
        bar2.style.transform = '';
    }

    async moveElement(from, to) {
        const bars = this.container.querySelectorAll('div[data-index]');
        const bar = bars[from];

        bar.style.transform = 'translateY(-20px)';
        await this.sleep(this.speed / 2);
        bar.style.transform = '';
    }

    async shiftElement(from, to) {
        const bars = this.container.querySelectorAll('div[data-index]');
        const fromBar = bars[from];
        const toBar = bars[to];

        if (!fromBar || !toBar) return;

        // Анимация сдвига
        fromBar.style.transform = 'translateX(10px)';
        await this.sleep(this.speed / 3);

        // Копируем высоту и значение
        toBar.style.height = fromBar.style.height;
        const fromLabel = fromBar.querySelector('span');
        const toLabel = toBar.querySelector('span');
        if (fromLabel && toLabel) {
            toLabel.textContent = fromLabel.textContent;
        }

        fromBar.style.transform = '';
    }

    async insertElement(index, value) {
        const bars = this.container.querySelectorAll('div[data-index]');
        const bar = bars[index];

        if (!bar) return;

        // Анимация вставки
        bar.style.transform = 'scale(1.1)';

        // Обновляем высоту и значение
        const maxValue = Math.max(...this.array);
        const height = (value / maxValue) * 300;
        bar.style.height = `${height}px`;

        const label = bar.querySelector('span');
        if (label) {
            label.textContent = value;
        }

        await this.sleep(this.speed / 2);
        bar.style.transform = '';
    }

    highlightBars(indices, color) {
        const bars = this.container.querySelectorAll('div[data-index]');
        indices.forEach(index => {
            if (bars[index]) {
                bars[index].style.background = `linear-gradient(to top, ${color}, ${this.darkenColor(color, 20)})`;
            }
        });
    }

    darkenColor(color, percent) {
        // Простая функция затемнения цвета
        const colorMap = {
            '#007bff': '#0056b3',
            '#ffc107': '#e0a800',
            '#28a745': '#1e7e34',
            '#dc3545': '#bd2130'
        };
        return colorMap[color] || color;
    }

    resetStats() {
        this.stats = {
            comparisons: 0,
            swaps: 0,
            steps: 0,
            startTime: null
        };
        this.updateStats();
    }

    updateStats() {
        document.getElementById('comparisons').textContent = this.stats.comparisons;
        document.getElementById('swaps').textContent = this.stats.swaps;
        document.getElementById('steps').textContent = this.stats.steps;

        if (this.stats.startTime) {
            const elapsed = Date.now() - this.stats.startTime;
            document.getElementById('time').textContent = elapsed;
        }
    }

    async start() {
        if (this.isRunning) return;

        this.isRunning = true;
        this.isPaused = false;
        this.stats.startTime = Date.now();

        try {
            switch (this.algorithm.toLowerCase()) {
                case 'bubble sort':
                    await this.bubbleSort();
                    break;
                case 'selection sort':
                    await this.selectionSort();
                    break;
                case 'insertion sort':
                    await this.insertionSort();
                    break;
                case 'merge sort':
                    await this.mergeSort();
                    break;
                case 'quick sort':
                    await this.quickSort();
                    break;
                case 'heap sort':
                    await this.heapSort();
                    break;
                case 'counting sort':
                    await this.countingSort();
                    break;
                default:
                    console.log(`Алгоритм "${this.algorithm}" пока не реализован`);
                    alert(`Алгоритм "${this.algorithm}" будет добавлен в следующих обновлениях!`);
            }
        } catch (error) {
            console.error('Ошибка при выполнении сортировки:', error);
        }

        this.isRunning = false;

        // Сохраняем статистику в Django
        await this.saveStatistics();
    }

    pause() {
        this.isPaused = !this.isPaused;
    }

    reset() {
        this.isRunning = false;
        this.isPaused = false;
        this.generateArray(parseInt(document.getElementById('arraySize').value));
    }

    setSpeed(speed) {
        const speedMap = {
            'slow': 300,
            'normal': 100,
            'fast': 30
        };
        this.speed = speedMap[speed] || 100;
    }

    async saveStatistics() {
        const data = {
            algorithm_id: window.algorithmId,
            array_size: this.array.length,
            initial_array: JSON.stringify(this.array),
            steps_count: this.stats.steps,
            comparisons_count: this.stats.comparisons,
            swaps_count: this.stats.swaps,
            execution_time: Date.now() - this.stats.startTime,
            completed: true
        };

        try {
            const response = await fetch('/algorithms/api/save-simulation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                console.log('Статистика сохранена');
            }
        } catch (error) {
            console.error('Ошибка сохранения статистики:', error);
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    waitForResume() {
        return new Promise(resolve => {
            const checkPause = () => {
                if (!this.isPaused) {
                    resolve();
                } else {
                    setTimeout(checkPause, 100);
                }
            };
            checkPause();
        });
    }
}

// Глобальная переменная для визуализатора
let visualizer = null;
