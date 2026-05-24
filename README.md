# Codex Roblox Bridge

Проект теперь поддерживает две параллельные схемы работы:

- `MVP bridge` для live-команд в запущенную Roblox Studio
- `Rojo + bridge` для нормальной разработки игры через файлы

Существующий MVP сохранен и не удален. Новый слой `src/` добавлен поверх него.

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
