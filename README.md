# Roblox Tower Defense Prototype

Проект поддерживает две параллельные схемы работы:

- `MVP bridge` для live-команд в запущенную Roblox Studio
- `Rojo + bridge` для нормальной разработки игры через файлы

Существующий MVP сохранен и не удален. Новый слой `src/` добавлен поверх него.

## Team Workflow & Orchestration

Для удобной работы через Claude и Codex CLI:

- **[CLAUDE.md](CLAUDE.md)** - Инструкции для Claude
- **[AGENTS.md](AGENTS.md)** - Роли агентов для Codex CLI
- **[docs/team/](docs/team/)** - Документация команды
  - `ROLES.md` - Роли команды
  - `ROADMAP.md` - План развития на 6 месяцев
  - `CURRENT_STATE.md` - Текущее состояние игры
  - `NEXT_ACTIONS.md` - Следующие 5 задач
  - `DEVELOPMENT_LOOP.md` - Цикл разработки
  - `TEST_PLAN.md` - План тестирования
  - `MODEL_ROUTING.md` - Выбор моделей AI для задач
- **[prompts/](prompts/)** - Библиотека промтов для AI

### Model Routing

Выбор подходящей модели AI для разных задач:

```powershell
# Получить рекомендацию для задачи
.\scripts\model_recommend.ps1 -Task "add tower placement spending"

# Запустить Claude с нужной моделью
.\scripts\claude_quick.ps1    # haiku - для документации
.\scripts\claude_code.ps1     # sonnet - для кода
.\scripts\claude_deep.ps1     # opusplan - для сложных задач
```

Уровни:
- **Quick (haiku):** Документация, статус, простые скрипты
- **Code (sonnet):** Реализация фич, исправление багов
- **Deep (opus/opusplan):** Архитектура, безопасность, рискованные операции
- **Verify (haiku/sonnet):** Тестирование, анализ логов

### Быстрый старт

```powershell
# Проверить статус
.\scripts\team_status.ps1

# Посмотреть следующие задачи
.\scripts\team_plan_next.ps1

# Запустить полный цикл (статус → план → сборка → демо)
.\scripts\team_cycle.ps1

# Список доступных промтов
.\scripts\prompt_list.ps1

# Показать конкретный промт
.\scripts\prompt_show.ps1 -Name design_feature
```

## Текущая структура

- [bridge/bridge_server.py](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/bridge/bridge_server.py) - локальный Python bridge server
- [bridge/queue/commands.json](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/bridge/queue/commands.json) - очередь live-команд
- [bridge/state/latest_state.json](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/bridge/state/latest_state.json) - последнее состояние из Studio
- [roblox/BridgeClient.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/roblox/BridgeClient.lua) - legacy/manual bridge client для прямой вставки в Studio
- [roblox/ExampleCommands.json](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/roblox/ExampleCommands.json) - примеры live-команд
- [default.project.json](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/default.project.json) - конфиг Rojo
- [src/shared/GameConfig.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/shared/GameConfig.lua) - общая конфигурация игры
- [src/server/BridgeClient.server.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/BridgeClient.server.lua) - bridge client для Rojo-синка
- [src/server/Main.server.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/Main.server.lua) - базовый серверный bootstrap
- [src/client/Main.client.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/client/Main.client.lua) - базовый клиентский bootstrap
- [scripts/start_bridge.ps1](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/scripts/start_bridge.ps1) - запуск Python bridge
- [scripts/start_rojo.ps1](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/scripts/start_rojo.ps1) - запуск `rojo serve`

## Как сейчас работает мост

Схема текущего bridge слоя такая:

1. Python-сервер поднимается на `http://127.0.0.1:8765`.
2. Roblox bridge client раз в несколько секунд читает `/commands`.
3. Сервер отдает накопленные JSON-команды и очищает очередь.
4. Клиент в Studio исполняет команды вроде `ensure_folder`, `create_part`, `set_property`, `create_script`.
5. После исполнения клиент отправляет heartbeat и состояние `Workspace` в `/state`.

Это значит, что bridge удобен для:

- live-итераций в уже открытой Studio
- генерации сцен и простых объектов на лету
- быстрой диагностики состояния мира

## MVP Bridge

Используй этот режим, если хочешь быстро проверить команды без полного Rojo workflow.

### Что умеет MVP

Команды:

- `ensure_folder`
- `create_part`
- `set_property`
- `create_script`

Состояние:

- список детей `Workspace`
- число объектов в корне `Workspace`
- результаты последнего батча команд
- время последнего heartbeat

### Как запустить Python bridge

Из корня проекта:

```powershell
cd C:\Users\Bogdan\Documents\Codex\2026-05-21\new-chat
.\scripts\start_bridge.ps1
```

Альтернатива без скрипта:

```powershell
python .\bridge\bridge_server.py
```

### Что вставлять в Studio для legacy/manual режима

1. Открой `Game Settings -> Security`
2. Включи `Allow HTTP Requests`
3. Вставь содержимое [roblox/BridgeClient.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/roblox/BridgeClient.lua) в `ServerScriptService`
4. Запусти Play Mode

### Как проверить, что MVP bridge работает

Проверка сервера:

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8765/health
```

Тестовая команда:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8765/enqueue -ContentType 'application/json' -Body (@'
{
  "commands": [
    {
      "type": "ensure_folder",
      "name": "Generated"
    },
    {
      "type": "create_part",
      "name": "SpawnPlatform",
      "parent": "Workspace/Generated",
      "shape": "Block",
      "size": [20, 1, 20],
      "position": [0, 5, 0],
      "anchored": true,
      "color": [0.2, 0.6, 1.0]
    }
  ]
}
'@)
```

Если Studio подключена, в `Workspace/Generated` появится платформа.

Состояние можно посмотреть так:

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8765/state | ConvertTo-Json -Depth 5
```

## Rojo Workflow

Используй этот режим, если хочешь разрабатывать игру как нормальный файловый проект.

### Структура `src`

- `src/shared` синкается в `ReplicatedStorage/Shared`
- `src/server` синкается в `ServerScriptService`
- `src/client` синкается в `StarterPlayer/StarterPlayerScripts`
- `src/workspace` синкается в `Workspace`

### Что делает Rojo-конфиг

[default.project.json](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/default.project.json) маппит:

- `Workspace` -> `src/workspace`
- `ReplicatedStorage/Shared` -> `src/shared`
- `ServerScriptService` -> `src/server`
- `StarterPlayer/StarterPlayerScripts` -> `src/client`

### Как запускать Rojo

Если `rojo` уже установлен:

```powershell
cd C:\Users\Bogdan\Documents\Codex\2026-05-21\new-chat
.\scripts\start_rojo.ps1
```

Альтернатива без скрипта:

```powershell
rojo serve .\default.project.json
```

### Если Rojo еще не установлен

Я его автоматически не устанавливал. Вот точные варианты установки:

Через `aftman`:

```powershell
aftman add rojo-rbx/rojo
```

Через `cargo`:

```powershell
cargo install rojo
```

Или скачай релиз с GitHub:

- [Rojo Releases](https://github.com/rojo-rbx/rojo/releases)

После установки проверь:

```powershell
rojo --version
```

### Что вставлять в Studio для Rojo режима

1. Открой Roblox Studio
2. Создай или открой place
3. Установи Rojo plugin в Studio, если его еще нет
4. Запусти `rojo serve .\default.project.json`
5. Подключи place к Rojo через плагин
6. Убедись, что в Studio появились:
   - `ReplicatedStorage/Shared/GameConfig`
   - `ServerScriptService/BridgeClient`
   - `ServerScriptService/Main`
   - `StarterPlayer/StarterPlayerScripts/Main`

Для bridge в этом режиме ручная вставка уже не нужна, потому что [src/server/BridgeClient.server.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/BridgeClient.server.lua) синкается через Rojo.

### Как проверить, что Rojo workflow работает

После подключения к Rojo:

1. Запусти Play Mode в Studio
2. В Output должны появиться сообщения:
   - `Server boot`
   - `Client boot`
   - `Bridge client started`
3. В `Workspace` должна появиться папка `GameRuntime`
4. Python bridge должен отвечать на `GET /health`
5. `GET /state` должен вернуть heartbeat после запуска серверной части

## Tower Defense Foundation

Добавлен минимальный, но расширяемый каркас tower defense игры.

### Shared configs

- [src/shared/configs/EnemyConfig.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/shared/configs/EnemyConfig.lua) - типы врагов `Basic`, `Fast`, `Tank`
- [src/shared/configs/WaveConfig.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/shared/configs/WaveConfig.lua) - первые 5 волн
- [src/shared/configs/TowerConfig.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/shared/configs/TowerConfig.lua) - башни `BasicTower`, `SniperTower`, `SplashTower`

### Server services

- [src/server/services/RuntimeService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/RuntimeService.lua)
  создает `Workspace/GameRuntime` и папки `Enemies`, `Towers`, `Projectiles`, `Map`, `Debug`
- [src/server/services/EnemyService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/EnemyService.lua)
  создает тестовых врагов в `GameRuntime/Enemies`
- [src/server/services/WaveService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/WaveService.lua)
  умеет запускать волну и тестово спавнить первую волну с разносом по X
- [src/server/services/TowerService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/TowerService.lua)
  умеет ставить тестовую башню в `GameRuntime/Towers`
- [src/server/services/EconomyService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/EconomyService.lua)
  держит стартовые деньги и базовые методы экономики

### Что делает серверный bootstrap

[src/server/Main.server.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/Main.server.lua):

1. Инициализирует runtime
2. Инициализирует экономику
3. Инициализирует сервисы врагов, башен и волн
4. Создает тестовую башню
5. Спавнит тестовую первую волну
6. Пишет понятные серверные логи

### Как проверить Tower Defense Foundation

1. Запусти bridge:

```powershell
cd C:\Users\Bogdan\Documents\Codex\2026-05-21\new-chat
.\scripts\start_bridge.ps1
```

2. Запусти Rojo:

```powershell
cd C:\Users\Bogdan\Documents\Codex\2026-05-21\new-chat
.\scripts\start_rojo.ps1
```

3. Открой Roblox Studio и подключи place к Rojo
4. Нажми Play
5. Проверь в Explorer:
   - `Workspace/GameRuntime`
   - `Workspace/GameRuntime/Enemies`
   - `Workspace/GameRuntime/Towers`
   - `Workspace/GameRuntime/Projectiles`
   - `Workspace/GameRuntime/Map`
   - `Workspace/GameRuntime/Debug`
6. В `Enemies` должны появиться несколько тестовых врагов из первой волны
7. В `Towers` должна появиться одна тестовая башня
8. В Output должны появиться логи сервисов и boot-сообщения

## Backlund Fog District Map Builder

Добавлен первый атмосферный map builder для tower defense прототипа в стилистике мрачного Баклунда.

### Что создает MapService

- [src/server/services/MapService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/MapService.lua)
  строит `Backlund Fog District` внутри `Workspace/GameRuntime/Map`
- создает папки:
  - `Ground`
  - `Streets`
  - `Buildings`
  - `Lamps`
  - `Decorations`
  - `Zones`
- наполняет карту:
  - большой темной основой
  - дорожными сегментами
  - зданиями по краям
  - газовыми фонарями
  - `SpawnZone`
  - `ExitZone`
  - декоративными объектами вроде ящиков, fog markers, ritual stones и sewer covers

### Что создает PathService

- [src/server/services/PathService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/PathService.lua)
  строит `Workspace/GameRuntime/Map/PathNodes`
- создает минимум 7 точек:
  - `Node_1`
  - `Node_2`
  - `Node_3`
  - `Node_4`
  - `Node_5`
  - `Node_6`
  - `Node_7`
- возвращает упорядоченный массив `Vector3` для следующих этапов движения врагов

### Где это появится в Workspace

После запуска серверной части ты увидишь:

- `Workspace/GameRuntime/Map/Ground`
- `Workspace/GameRuntime/Map/Streets`
- `Workspace/GameRuntime/Map/Buildings`
- `Workspace/GameRuntime/Map/Lamps`
- `Workspace/GameRuntime/Map/Decorations`
- `Workspace/GameRuntime/Map/Zones`
- `Workspace/GameRuntime/Map/PathNodes`

### Как проверить через build_place.ps1

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_place.ps1
```

Если сборка прошла успешно, появится:

- `build/game.rbxlx`

### Как проверить через auto_play_assisted.ps1

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\auto_play_assisted.ps1
```

Если Windows снова не отдаст foreground окну Studio, `F5` может быть заблокирован, и это допустимо. Главное здесь:

- Rojo build проходит
- карта и path builder попадают в place
- итоговый отчет оператора понятен

### Что должно быть в Explorer после Play

- `Workspace/GameRuntime/Map/Ground/DistrictGround`
- несколько `StreetSegment_*`
- несколько `Building_*`
- несколько `LampPost_*` и `LampGlow_*`
- `Zones/SpawnZone`
- `Zones/ExitZone`
- `PathNodes/Node_1` ... `PathNodes/Node_7`
- `Enemies` с тестовой волной
- `Towers` с тестовой башней рядом с дорогой

## Enemy Movement Along PathNodes

Добавлено простое движение врагов по точкам пути карты.

### Как это работает

- враги появляются рядом с `Node_1`
- `PathService` возвращает точки `Node_1 ... Node_7` в правильном порядке
- `EnemyService` двигает каждого врага по этим точкам через `TweenService`
- после достижения выхода враг удаляется из `Workspace/GameRuntime/Enemies`

### Где смотреть в Studio

- `Workspace/GameRuntime/Enemies`
- `Workspace/GameRuntime/Map/PathNodes`

### Какие логи ожидать в Output

- `[PathService]`
- `[WaveService]`
- `[EnemyService]`

Следующий этап:

- `Tower targeting and damage`

## Tower Targeting and Damage

Добавлен минимальный боевой loop для тестовой башни.

### Как это работает

- башни ищут ближайшего живого врага в радиусе
- выбор цели идет по минимальной дистанции внутри `Range`
- враги получают урон через `Health` attribute
- при `Health <= 0` враг удаляется

### Debug attack beam

- при атаке кратко появляется neon beam
- beam создается в `Workspace/GameRuntime/Projectiles`
- beam автоматически удаляется через `Debris`

### Где смотреть

- `Workspace/GameRuntime/Towers`
- `Workspace/GameRuntime/Enemies`
- `Workspace/GameRuntime/Projectiles`

### Какие логи должны быть в Output

- `[TowerService]`
- `[EnemyService]`

### Следующий этап

- `projectile visuals`
- `reward economy`
- `wave progression`

## Reward Economy

Добавлен минимальный экономический loop за убийства врагов.

### Как это работает

- `reward` хранится в [src/shared/configs/EnemyConfig.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/shared/configs/EnemyConfig.lua)
- при спавне [src/server/services/EnemyService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/EnemyService.lua) копирует `reward` в attribute `Reward`
- `DamageEnemy()` теперь возвращает результат с `damaged`, `defeated`, `reward`, `enemyName`, `newHealth`
- если башня действительно добивает врага, [src/server/services/TowerService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/TowerService.lua) передает reward в [src/server/services/EconomyService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/EconomyService.lua)
- `EconomyService` увеличивает `currentMoney` только за реальные убийства башней

### Где смотреть логи

- `[EnemyService]`
- `[TowerService]`
- `[EconomyService]`

### Следующий этап

- `wave progression`
- `tower placement spending`
- `projectile visuals`
- `UI money display`

## Wave Progression

Добавлен базовый последовательный запуск волн.

### Как это работает

- `WaveService` запускает волны по очереди, а не только одну тестовую
- после спавна всех врагов сервис ждет, пока `EnemyService:GetActiveEnemies()` очистится
- между волнами есть `intermissionSeconds`
- после завершения заданного числа волн loop пишет итоговый лог

### Где смотреть

- `Workspace/GameRuntime/Enemies`
- `Output` logs

### Какие логи должны быть

- `[WaveService] Starting wave`
- `[WaveService] Wave completed`
- `[WaveService] Wave loop completed`

### Следующий этап

- `tower placement spending`
- `UI money display`
- `projectile visuals`
- `base health / lives`

## How to play locally

Build the Roblox place from the project root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\build_place.ps1
```

Open `build/game.rbxlx` in Roblox Studio and press Play.

Управление:

- **Нажми на синюю площадку**, чтобы выбрать место, затем нажми `Построить базовую башню ($100)` в панели.
- **Нажми на существующую башню**, чтобы увидеть характеристики; нажми `Продать башню (50% возврат)`, чтобы продать её.
- Нажми `B` или кнопку `Быстрая постройка (B)`, чтобы купить базовую башню на следующей свободной площадке.
- Каждая башня стоит `$100`; стартовые деньги — `$300`.
- Одна базовая башня уже стоит рядом с первым участком пути, чтобы бой начинался сразу.

Цель:

- Враги появляются в синей зоне и идут по яркому пути к красным воротам базы.
- Башни автоматически атакуют врагов в радиусе.
- За убитых врагов начисляются деньги.
- Интерфейс показывает деньги, номер волны, здоровье базы и состояние игры.
- Победи, зачистив все волны до того, как здоровье базы станет `0`; проигрыш наступает, если слишком много врагов дойдёт до базы.

Текущие ограничения:

- Это минимальный playable-срез; визуал и баланс пока на уровне прототипа.
- Камера зафиксирована в тактическом ракурсе; панорамирования и зума пока нет.
- Игрок пока может строить только базовую башню; конфиги `SniperTower` и `SplashTower` существуют, но ещё не добавлены в меню постройки.
- Улучшение башен запланировано, но пока не реализовано: кнопка показывает `Улучшение скоро`.
- Режим героя/командира запланирован для будущего PR.

## Следующий этап развития

1. `enemy movement along PathNodes`
2. `tower targeting`
3. `damage system`
4. `wave progression`
5. `gacha units`
6. `UI`
7. `save system`

## Практичный режим работы

Самый удобный пайплайн теперь такой:

1. Ты запускаешь Python bridge
2. Ты запускаешь `rojo serve`
3. Studio подключается к Rojo
4. Я правлю `.lua` файлы в `src/`
5. При необходимости мы используем bridge как live-командный слой для генерации или тестовых операций в открытой Studio

Так у нас есть и нормальная кодовая база, и быстрый live-канал управления игрой.

## Demo Player Spawn

Добавлен безопасный спавн для игрока при демо-записях и тестировании.

### Как это работает

- [src/server/services/PlayerSpawnService.lua](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/src/server/services/PlayerSpawnService.lua)
  создает `Workspace/GameRuntime/PlayerSpawn` с:
  - `DemoSpawnPlatform` — видимая платформа (40x2x40) на Y=8
  - `DemoSpawnLocation` — Roblox SpawnLocation (12x1x12) на Y=11
  - `DemoSafetyFloor` — невидимый пол (300x2x300) на Y=-10 для защиты от падения в пустоту
- игрок спавнится на `DemoSpawnLocation` вместо падения в void
- при Play Mode в Studio персонаж остается на платформе и видна карта, враги, башни

### Где смотреть в Studio

- `Workspace/GameRuntime/PlayerSpawn/DemoSpawnPlatform`
- `Workspace/GameRuntime/PlayerSpawn/DemoSpawnLocation`
- `Workspace/GameRuntime/PlayerSpawn/DemoSafetyFloor`

### Какие логи ожидать в Output

- `[PlayerSpawnService] Demo spawn ready`
- `[Client] Demo camera activated`

## Demo Recording with Auto-Play

Добавлена безопасная автоматизация нажатия F5 для запуска Play Mode во время демо-записей.

### Как это работает

- [tools/studio_operator/demo_test_player.py](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/tools/studio_operator/demo_test_player.py)
  получает параметры `--auto-play` и `--auto-play-mode`
- два режима auto-play:
  - **safe** (по умолчанию): скрипт сам фокусирует Studio окно и нажимает F5
  - **assisted**: пользователь кликает Studio, скрипт проверяет фокус и нажимает F5
- в обоих режимах:
  1. проверяется, что активное окно действительно Roblox Studio
  2. если фокус подтвержден — нажимается F5 и ждется 4 секунды перед записью
  3. если фокус не подтвержден — пропускается F5 и продолжается запись (без ошибок)
- в report добавляются поля:
  - `auto_play_enabled`: true/false
  - `auto_play_mode`: safe/assisted
  - `auto_play_status`: AUTO_PLAY_F5_PRESSED / AUTO_PLAY_ASSISTED_F5_PRESSED / AUTO_PLAY_FOCUS_NOT_CONFIRMED / AUTO_PLAY_ASSISTED_FOCUS_NOT_CONFIRMED / AUTO_PLAY_DISABLED
  - `active_window_before_auto_play`
  - `active_window_after_auto_play`

### Быстрый старт с auto-play

**Assisted режим (рекомендуется для Windows):**
```powershell
# 30 секунд с assisted auto-play
.\scripts\run_demo_assisted_auto_play_30s.ps1

# Или с параметром
.\scripts\run_demo_record_30s.ps1 -AutoPlay -Assisted
```

**Safe режим (автоматический фокус):**
```powershell
# 30 секунд с safe auto-play
.\scripts\run_demo_auto_play_30s.ps1

# Или с параметром
.\scripts\run_demo_record_30s.ps1 -AutoPlay

# 90 секунд с safe auto-play
.\scripts\run_demo_test.ps1 -AutoPlay
```

### Старый режим (ручной)

```powershell
# 30 секунд без auto-play (нужно нажимать F5 вручную)
.\scripts\run_demo_record_30s.ps1

# 90 секунд без auto-play
.\scripts\run_demo_test.ps1
```

### Когда использовать какой режим

**Assisted (рекомендуется):**
- ✅ Самый надежный на Windows
- ✅ Пользователь контролирует момент нажатия F5
- ✅ Не требует автоматического фокусирования
- ✅ Лучше всего для CI/CD и автоматизации

**Safe:**
- ✅ Полностью автоматический
- ✅ Не требует участия пользователя
- ⚠️ Может не сработать, если Studio не видна или фокус не подтверждается
- ❌ Менее надежен на Windows из-за особенностей фокусирования

**Manual:**
- ✅ Полный контроль пользователя
- ✅ Для подготовки сцены перед Play
- ❌ Требует ручного нажатия F5

## Demo Autofix Loop

Добавлен ограниченный автономный диагностический цикл для demo recorder. Он собирает проект, запускает assisted demo, читает `logs/demo_test_report.md`, агрегирует Roblox logs, проверяет MP4 metadata и пишет понятный отчёт без бесконечных попыток.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo_autofix_loop.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\demo_autofix_loop.ps1 -DiagnoseOnly
```

Отчёты:

- `logs/demo_autofix_report.md`
- `logs/demo_test_report.md`
- `logs/roblox_latest_markers.md`

Demo runtime также создаёт видимые diagnostic beacons в `Workspace/DemoDiagnostics`: blue server, green spawn, yellow map, red wave. На клиенте появляется UI-текст `DEMO SPECTATOR CAMERA ACTIVE`, чтобы видео можно было оценить даже если Roblox log-файл не поймал обычные `print()` строки.

Для нестабильного Windows foreground добавлен Studio Play Controller:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\studio_force_play.ps1
```

Он выбирает именно `build\game.rbxlx - Roblox Studio`, пробует поднять окно через WinAPI и нажать F5. Если foreground заблокирован, в отчёте будет явный статус вместо тихого провала.

Политика безопасности описана в [DEMO_AUTOFIX_POLICY.md](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/docs/team/DEMO_AUTOFIX_POLICY.md). Loop не мержит PR, не удаляет файлы, не делает force push и не коммитит build/logs/videos.


## Pipeline Smoke Test

Быстрая проверка инфраструктуры demo/runtime pipeline без запуска Roblox Studio.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\pipeline_smoke_test.ps1
```

Что проверяет:

- все обязательные файлы (Lua services, scripts, tools)
- `rojo` доступен и сборка проходит
- venv и зависимости на месте
- существуют demo report, marker report, recordings
- серверные маркеры (`[Server boot]`, `[DemoDiagnostics]`, `[WaveService]`) присутствуют в Roblox logs

Результат: `logs/pipeline_smoke_report.md` с pass/fail статусом, commit info, и инструкциями по ручным шагам.

Если серверные маркеры отсутствуют, это значит что Roblox Studio ещё не выполнила Play mode. Для полной проверки:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo_autofix_loop.ps1
```

## Demo Evidence Report

Добавлен короткий отчёт для ревьюера, который агрегирует уже созданные pipeline/demo артефакты в один Markdown без повторного запуска Roblox Studio.

Рекомендуемый порядок:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '.\scripts\pipeline_smoke_test.ps1'"
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '.\scripts\demo_autofix_loop.ps1'"
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '.\scripts\demo_evidence_report.ps1'"
```

Отчёт создаётся здесь:

- `logs/demo_evidence_report.md`
- `logs/demo_evidence_report.json`

Что показывает evidence report:

- branch, commit и рабочий статус git
- результат smoke test и количество проверок
- demo diagnosis и Play confirmation evidence
- выбранное окно Studio, HWND/PID/root HWND
- F5 method и попытки запуска Play
- количество runtime markers и ключевые markers
- путь к последнему MP4 и размер видео
- пути к исходным reports
- какие артефакты сгенерированы, но намеренно не коммитятся

Успешный ожидаемый результат:

- `smoke test: PASS`
- `smoke checks: 22/22`
- `demo diagnosis: OK`
- runtime markers найдены
- MP4 существует в `logs/recordings/`

Важно: `logs/`, `logs/recordings/`, screenshots, build output и диагностические CSV остаются generated artifacts и не должны попадать в commit.

## Static CI Checks

Добавлена лёгкая статическая CI-проверка для GitHub Actions.

Что делает CI:

- не запускает Roblox Studio
- не имитирует demo/runtime успех
- проверяет Python syntax для `tools/studio_operator/*.py`
- проверяет наличие обязательных pipeline/demo файлов
- проверяет, что generated artifacts не попали в tracked git files

Для локальной полной demo-проверки по-прежнему используются только ручные сценарии:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '.\scripts\demo_autofix_loop.ps1'"
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '.\scripts\demo_evidence_report.ps1'"
```

## Safe PR Merge Manager

Добавлен безопасный менеджер merge для Pull Request.

### Как посмотреть PR

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\pr_status.ps1
```

### Как безопасно смержить конкретный PR

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\pr_safe_merge.ps1 -PrNumber 7
```

### Как смержить единственный открытый PR

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\pr_safe_merge_latest.ps1
```

### Какие проверки выполняются

- `working tree` должен быть чистым
- `gh auth status` должен проходить
- PR должен быть не `draft`
- PR должен целиться в `main`
- PR не должен быть `cross-repository`
- PR не должен быть в состоянии `CONFLICTING`
- локальный `rojo build` через [scripts/build_place.ps1](C:/Users/Bogdan/Documents/Codex/2026-05-21/new-chat/scripts/build_place.ps1) должен проходить
- `build/game.rbxlx` должен реально появиться
- если у PR есть GitHub checks, они не должны падать

### Почему нельзя мержить вслепую

- можно протащить конфликтный PR
- можно смержить ветку с поломанным build
- можно случайно смержить чужой или cross-repo PR
- можно сломать локальную рабочую копию, если merge запускать из dirty tree

### Что делать, если merge не проходит

- если `checks failed`, починить PR и повторить проверку
- если есть `conflicts`, сначала обновить ветку PR
- если `dirty tree`, очистить локальные изменения или зафиксировать их в отдельной ветке
