
# 👻 Git-Ghost

[EN] A lightweight, educational Markdown steganography CLI tool built in Python. It invisibly dissolves secret messages inside files (like README.md) using zero-width Unicode characters without breaking the original formatting, allowing instant extraction via direct GitHub links.

[RU] Лёгкая учебная CLI-утилита для скрытия секретных текстовых сообщений внутри файлов Markdown (например, README.md) с помощью методов цифровой стеганографии. Позволяет незаметно «растворять» приватную информацию прямо внутри публичных репозиториев на GitHub без нарушения исходного форматирования, а также мгновенно извлекать данные по прямой ссылке.

> ⚠️ **Educational & Defensive Only** / **Только для обучения и защиты** > This tool is designed for security research, steganography concept demonstration, and secure text sharing experiments. It does not encrypt data by default and should never be used for unauthorized data exfiltration.
> Инструмент создан для исследований в области ИБ, демонстрации концепций стеганографии и экспериментов по безопасной передаче текста. Он не шифрует данные по умолчанию и не должен использоваться для несанкционированной эксфильтрации данных.

---

## ⚡ Features / Возможности

| EN | RU |
| --- | --- |
| 🥷 Absolute invisibility via zero-width characters (ZWSP/ZWNJ) | 🥷 Абсолютная невидимость через символы нулевой ширины (ZWSP/ZWNJ) |
| 🛡️ Header protection using 4-byte Big-Endian size struct | 🛡️ Защита заголовком через 4-байтовую структуру размера Big-Endian |
| 🌐 Direct extraction from GitHub via automatic URL conversion | 🌐 Извлечение напрямую из GitHub через автоконвертацию ссылок |
| 🪶 Zero-Dependency: built using pure Python standard library | 🪶 Zero-Dependency: написан на чистом Python без сторонних пакетов |
| 🌍 Bilingual CLI automatically adapting to OS language | 🌍 Двуязычный CLI с автоадаптацией под язык операционной системы |
| 📝 Zero impact on Markdown tables, lists, and formatting | 📝 Нулевое влияние на Markdown-таблицы, списки и форматирование |

---

## 🛠️ Execution Instructions / Запуск

### 📦 Dependencies / Зависимости (`requirements.txt`)

Create a `requirements.txt` file (Optional, for documentation purposes):

```txt
# Git-Ghost uses only the Python 3 standard library (os, struct, locale, urllib).
# No external packages are required to run this tool.
#
# Git-Ghost использует только стандартную библиотеку Python 3 (os, struct, locale, urllib).
# Для работы утилиты не требуется установка внешних пакетов.

```

### 🚀 Usage Example / Пример работы

```bash
python main.py

```

```
=============================================
 1 - Растворить секрет в README.md
 2 - Извлечь секрет из локального файла
 3 - Извлечь секрет из GitHub по ссылке
 0 - Выход
=============================================
Выберите действие / Select action: 1

Путь к исходному README [README.md]: README.md
Введите секретное сообщение: My private key: SECRET_123_XYZ
Путь для результата [README_hidden.md]: README_hidden.md

[+] Секрет успешно растворен в README_hidden.md (30 байт)

```

---

## 📐 Data Structure / Структура данных

```
+-------------------------+---------------------------------------+
|  Header (4 bytes)       |      Payload (Variable size)          |
|  Data size via '>I'     |      Secret message string in UTF-8   |
+-------------------------+---------------------------------------+
            │                                 │
            ▼                                 ▼
      Split into bits                   Split into bits
            │                                 │
            └────────────────┬────────────────┘
                             ▼
               Encoding into Unicode markers:
               Bit '0' -> \u200b (Zero Width Space)
               Bit '1' -> \u200c (Zero Width Non-Joiner)
                             ▼
               Injection into the tail of README.md

```
