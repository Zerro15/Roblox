local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local services = script:WaitForChild("services")

local RuntimeService = require(services:WaitForChild("RuntimeService"))
local EconomyService = require(services:WaitForChild("EconomyService"))
local EnemyService = require(services:WaitForChild("EnemyService"))
local TowerService = require(services:WaitForChild("TowerService"))
local WaveService = require(services:WaitForChild("WaveService"))

print(string.format("[Server boot] %s v%s", GameConfig.GameName, GameConfig.Version))

RuntimeService:Init()
EconomyService:Init()
EnemyService:Init()
TowerService:Init()
WaveService:Init()

local towerPositionValues = GameConfig.DefaultTowerPosition
local towerPosition = Vector3.new(towerPositionValues[1], towerPositionValues[2], towerPositionValues[3])

local testTower = TowerService:PlaceTower("BasicTower", towerPosition)
if testTower then
	print(string.format("[Main] Placed test tower: %s", testTower.Name))
end

local spawnedEnemies = WaveService:SpawnTestWave()
print(string.format("[Main] Spawned test wave with %d enemies", #spawnedEnemies))
