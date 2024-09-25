# Проект Анализа Финансовых Данных

## Описание
Этот проект представляет собой набор Python-скриптов для обработки и анализа финансовых данных из XLSX файлов. Основные функции включают чтение файлов Excel, обработку данных, расчёт статистики по расходам и доходам, а также работу с API для получения курсов валют и стоимости акций.

## Модули

### 1. `xlsx_reader.py`
Этот модуль отвечает за чтение файлов XLSX с использованием библиотеки `pandas`.

- **Основные функции:**
  - `pandas_reader_xlsx(path: str) -> Union[Dict[str, Any], List[Any]]`: Чтение XLSX файла и преобразование его в словарь данных или список. Если файл не найден, возвращает пустой список.
  
- **Зависимости:**
  - `pandas`

### 2. `views.py`
Этот модуль реализует обработку данных для расчёта расходов и доходов, а также запросы к внешним API для получения валютных курсов и котировок акций.

- **Основные функции:**
  - `calculate_expenses(df: pd.DataFrame, start_date: datetime.date, end_date: datetime.date)`: Функция для расчёта расходов и доходов за указанный период с сортировкой по категориям. Также делает запрос к API для получения актуальных валютных курсов и стоимости акций.
  
- **Зависимости:**
  - `pandas`, `requests`, `dotenv`, `logging`, `src.utils.stock_rates`
  
### 3. `services.py`
Этот модуль предоставляет функции для работы с данными в формате `DataFrame`, включая фильтрацию и обработку транзакций.

- **Основные функции:**
  - `df_to_dict(df: pd.DataFrame) -> Dict`: Преобразует DataFrame в словарь.
  - `transfers_and_cash_grouped(data: Dict) -> str`: Группирует данные по переводам и наличным средствам и возвращает результат в формате JSON.

- **Зависимости:**
  - `json`, `logging`, `re`

### 4. `report.py`
Модуль для создания отчётов и их сохранения в файлы с использованием декораторов.

- **Основные функции:**
  - `spending_by_workday(transactions: pd.DataFrame, date_: Optional[str] = None) -> pd.DataFrame`: Анализирует транзакции за последние три месяца, делит их на рабочие и выходные дни, и считает средние расходы для каждого дня.

- **Зависимости:**
  - `pandas`, `logging`, `json`

### 5. `utils.py`
Содержит вспомогательные функции для работы с датами и получения котировок акций.

- **Основные функции:**
  - `start_of_week(date: datetime.date) -> datetime.date`: Возвращает дату начала недели для переданной даты.
  - `get_date_range(date_str: str, range_type: str) -> Tuple[datetime.date, datetime.date]`: Возвращает диапазон дат (неделя, месяц, год).
  - `stock_rates(users_stocks: List[str]) -> List[Dict[str, Any]]`: Получает котировки акций с помощью API.

- **Зависимости:**
  - `requests`, `dotenv`, `logging`

## Установка

1. Установите зависимости:
2. Создайте файл .env с переменными окружения для доступа к API


## Логирование
Все модули ведут логирование в соответствующие файлы логов, указанные в конфигурационных файлах. Логи сохраняются с использованием формата %(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s.