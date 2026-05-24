local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local services = script:WaitForChild("services")

local RuntimeService = require(services:WaitForChild("RuntimeService"))
local MapService = require(services:WaitForChild("MapService"))
local PathService = require(services:WaitForChild("PathService"))
local EconomyService = require(services:WaitForChild("EconomyService"))
local EnemyService = require(services:WaitForChild("EnemyService"))
local TowerService = require(services:WaitForChild("TowerService"))
local WaveService = require(services:WaitForChild("WaveService"))

print(string.format("[Server boot] %s v%s", GameConfig.GameName, GameConfig.Version))

RuntimeService:Init()
MapService:Init()
PathService:Init()
EconomyService:Init()
EnemyService:Init()
TowerService:Init()
WaveService:Init()

MapService:BuildBacklundFogDistrict()
local pathPoints = PathService:BuildBacklundPath()

local firstPathPoint = pathPoints[1] or Vector3.new(0, 0, 0)
local towerPosition = firstPathPoint + Vector3.new(-14, 2.5, 20)

local testTower = TowerService:PlaceTower("BasicTower", towerPosition)
if testTower then
	print(string.format("[Main] Placed test tower: %s", testTower.Name))
end

TowerService:StartAllTowersCombat()
WaveService:StartWaveLoop(3)
print("[Main] Triggered wave loop")
