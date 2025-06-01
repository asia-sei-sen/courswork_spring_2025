# Банковский транзакционный процессор

## Описание:
Проект предоставляет инструменты для обработки банковских операций, включая:
- Маскировку конфиденциальных данных (номера карт и счетов)
- Форматирование финансовой информации
- Фильтрацию и сортировку транзакций
- Преобразование дат в удобочитаемый формат
- Конвертацию валют через внешний API
- Генераторы для фильтрации и описания транзакций
- ✅ **Поддержку чтения транзакций из CSV- и Excel-файлов**

## Установка:
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-username/ваш-репозиторий.git
   cd ваш-репозиторий
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Тестирование:
Для запуска тестов и проверки покрытия:
```bash
pytest --cov=src
```

## Использование:
Функции чтения файлов находятся в модуле `src/file_parsers`.

- Прочитать CSV-файл:
   ```python
   from src.file_parsers.csv_parser import read_csv

   transactions = read_csv("path/to/transactions.csv")
   ```

- Прочитать Excel-файл:
   ```python
   from src.file_parsers.excel_parser import read_excel

   transactions = read_excel("path/to/transactions_excel.xlsx")
   ```
