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
python .\tools\studio_operator\studio_flow.py --flow build-open-play --click-mode cautious --focus-mode auto
python .\tools\studio_operator\studio_flow.py --flow build-open-play --click-mode cautious --focus-mode assisted
python .\tools\studio_operator\studio_flow.py --flow full-safe --click-mode cautious --focus-mode auto
```

## Human-focus Assisted Mode

Этот режим нужен для сценария, когда Windows не удерживает foreground на Roblox Studio и автоматическая фокусировка перед `F5` оказывается недостаточно надежной.

Что делает пользователь:

- запускает assisted flow
- ждет подсказку в консоли
- один раз кликает по окну `Roblox Studio`

Что делает оператор после клика:

- делает скриншот перед assisted-проверкой
- пишет в консоль, что проверить фокус нужно через 5 секунд
- ждет 5 секунд
- проверяет `active window title`
- нажимает `F5` только если активное окно действительно похоже на `Roblox Studio` или `game.rbxlx`

Почему это безопаснее координатных кликов:

- оператор не кликает по случайным координатам
- оператор не пытается угадывать расположение кнопок
- `F5` отправляется только после явного участия человека и повторной проверки foreground window

Если Windows все равно возвращает фокус в браузер или другое приложение, `F5` блокируется и это считается безопасным результатом, а не ошибкой.

## Demo Test Player / Video Recorder

Этот слой добавляет безопасный demo-runner поверх текущего Studio Operator.

Что он делает:

- собирает проект в `build/game.rbxlx`
- открывает `build/game.rbxlx` в Roblox Studio
- просит пользователя кликнуть окно Studio, если нужен assisted focus
- нажимает `F5` только если фокус Roblox Studio подтвержден
- записывает короткое видео экрана
- сохраняет скриншоты до и после
- собирает Roblox logs и пишет demo report

Как запустить:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_demo_test.ps1
```

Где лежит видео:

- `logs/recordings/`

Где лежит отчёт:

- [logs/demo_test_report.md](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/logs/demo_test_report.md)

Почему нужен assisted focus:

- Windows не всегда разрешает приложению надежно вернуть foreground на Roblox Studio
- demo-runner не делает координатных кликов
- `F5` отправляется только после подтверждения активного окна

Что делать, если статус `DEMO_BLOCKED_FOCUS_NOT_CONFIRMED`:

- вручную кликнуть по окну `game.rbxlx - Roblox Studio`
- снова запустить demo test

Что смотреть в видео:

- карту `Greymoor Veil District`
- врагов на `PathNodes`
- башни
- projectiles / beams
- wave progression
- reward logs

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
