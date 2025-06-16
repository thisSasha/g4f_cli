# Gpt4Free Cli (g4f_cli)

[**G4F Repository**](https://github.com/techwithanirudh/g4f?tab=readme-ov-file)

## ✨ Обзор

Gpt4Free Cli — это лёгкий CLI-интерфейс на Python к библиотеке [g4f](https://pypi.org/project/g4f/).  
Он упрощает поиск моделей и провайдеров, отправку запросов и получение ответов, а также предоставляет лаконичный логгинг. Отлично подойдёт для изучения библиотеки g4f

## 🚀 Возможности

Gpt4Free CLI поддерживает все актуальные модели и провайдеры из библиотеки `g4f`. Команды `get` и `find` позволяют удобно получать нужные связи и искать по ключевым словам.

Работа с потоками и захват логов в реальном времени позволяют отслеживать задержки запуска браузера, сбои и зависания. В режиме `DEBUG` создаётся лог-файл `.log` (Логи nodriver, urllib3 и др.).

Цветной вывод реализован через `rich.logging`. Также доступно быстрое копирование результатов в буфер обмена по индексу с помощью команды `copy`.

Проект лёгкий, без лишних зависимостей. История команд сохраняется в рамках текущей сессии. Все команды имеют продуманную структуру и легко расширяются.

## ⚙️ Установка

```bash
git clone https://github.com/thisSasha/g4f_cli.git
cd g4f_cli
python3 -m venv .venv
source .venv/bin/activate      # Linux и macOS
.\.venv\Scripts\activate       # Windows PowerShell
pip install -r requirements.txt
````

> [Зависимости](https://github.com/thisSasha/g4f_cli/blob/main/requirements.txt)
> [Точка входа](https://github.com/thisSasha/g4f_cli/blob/main/src/main.py)
> [Src](https://github.com/thisSasha/g4f_cli/tree/main/src)

## ▶️ Использование

Запусти CLI:

```bash
chmod +x ./run.sh
 ./run.sh # Linux и macOS

.\run.exe # Windows

```

В консоли появится приглашение:

```text
g4f > 
```

> **Примеры команд**
>
> ```bash
> g4f > find --provider openai gpt turbo
> g4f > use --model=gpt-3.5 --provider=BaseProvider "Привет, мир"
> g4f > get --all models
> g4f > copy 2
> g4f > version
> ```

---

## 🏗️ Архитектура

``` s
.
├── public/
│   ├── help.txt          # (опциональная справка в HTML)
│   └── logo.txt          # ASCII-логотип
├── requirements.txt
├── VERSION               # Текущая версия CLI
├── src/
│   ├── main.py           # Точка входа и REPL-цикл
│   ├── cli.py            # Логика prompt-toolkit, парсинг флагов
│   └── g4f_execute.py    # Основные действия: find, call, get, update
└── run.{sh|exe}          # Скрипты запуска
```

- `main.py` инициализирует окружение и обрабатывает команды
- `cli.py` реализует парсинг команд, аргументов, историю
- `g4f_execute.py` вызывает g4f.ChatCompletion и анализирует вывод

## Socials

**Автор:** thisDevSasha
**Репозиторий:** [https://github.com/thisSasha/g4f\_cli](https://github.com/thisSasha/g4f_cli)
**Ошибки и фичи:** [https://github.com/thisSasha/g4f\_cli/issues](https://github.com/thisSasha/g4f_cli/issues)
