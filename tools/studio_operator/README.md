# Studio Operator v4

Безопасный оператор разработки Roblox-проекта.

## Что нового в v4

- state-файл процессов
- защита от бесконечных окон
- cleanup только своих процессов
- безопасный build/open/play flow
- git workflow
- GitHub PR workflow

## No Infinite Windows Policy

Оператор не должен бесконечно плодить:

- окна PowerShell
- новые `rojo serve`
- новые `bridge`
- новые окна Roblox Studio для одного и того же `build/game.rbxlx`

Для этого используется state-файл и процессный менеджер.

## Process State File

Состояние хранится тут:

- [logs/studio_operator_state.json](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/logs/studio_operator_state.json)

В нём хранятся:

- PID процессов, запущенных оператором
- последние скриншоты
- последние отчёты
- последний build path
- последний flow status

## Safe Cleanup

Cleanup закрывает только процессы, которые:

- были запущены самим оператором
- записаны в state-файл

Оператор не закрывает:

- браузер
- ChatGPT
- Discord
- проводник
- чужие окна Roblox Studio

## Flow-команды

```powershell
python .\tools\studio_operator\studio_flow.py --flow status
python .\tools\studio_operator\studio_flow.py --flow cleanup
python .\tools\studio_operator\studio_flow.py --flow build
python .\tools\studio_operator\studio_flow.py --flow build-open
python .\tools\studio_operator\studio_flow.py --flow build-open-play --click-mode cautious
python .\tools\studio_operator\studio_flow.py --flow full-safe --click-mode cautious
```

## Git Workflow

Оператор умеет:

- `git init`, если репозиторий ещё не создан
- добавить безопасный `.gitignore`
- создать ветку
- stage safe files
- сделать commit

Он не должен коммитить:

- `.env`
- `build/`
- `logs/screenshots/`
- `logs/*.log`
- `logs/roblox_latest_markers.md`
- `.venv*`

## GitHub PR Workflow

Если установлен `gh`, есть авторизация и настроен `origin`, оператор может:

- push branch
- create PR

Если авторизации нет:

```powershell
gh auth login
```

## Почему не надо вставлять токены в файлы

- это небезопасно
- токены могут попасть в commit, logs или screenshots
- `gh auth login` использует уже нормальный локальный auth flow

## Что делать, если remote origin отсутствует

Оператор не угадывает репозиторий автоматически.

Сделай это вручную:

```powershell
git remote add origin <repo-url>
```

Потом можно повторить PR workflow.
