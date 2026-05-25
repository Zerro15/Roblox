local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local services = script.Parent:WaitForChild("services")

local RuntimeService = require(services:WaitForChild("RuntimeService"))
local MapService = require(services:WaitForChild("MapService"))
local PathService = require(services:WaitForChild("PathService"))
local EconomyService = require(services:WaitForChild("EconomyService"))
local EnemyService = require(services:WaitForChild("EnemyService"))
local TowerService = require(services:WaitForChild("TowerService"))
local WaveService = require(services:WaitForChild("WaveService"))
local PlayerSpawnService = require(services:WaitForChild("PlayerSpawnService"))
local DemoDiagnosticsService = require(services:WaitForChild("DemoDiagnosticsService"))

print(string.format("[Server boot] %s v%s", GameConfig.GameName, GameConfig.Version))
print("[Main] Demo spectator bootstrap starting")
warn(string.format("[Server boot] %s v%s", GameConfig.GameName, GameConfig.Version))
warn("[Main] Demo spectator bootstrap starting")

local function runStep(name, callback)
	print("[Main] Starting " .. name)
	local ok, err = pcall(callback)
	if ok then
		print("[Main] Completed " .. name)
	else
		warn("[Main] Failed " .. name .. ": " .. tostring(err))
	end
end

runStep("RuntimeService:Init", function()
	RuntimeService:Init()
end)

runStep("DemoDiagnosticsService:Init", function()
	DemoDiagnosticsService:Init()
end)

DemoDiagnosticsService:Mark("ServerBootBeacon")
warn("[Main] Demo runtime server boot confirmed")

runStep("PlayerSpawnService:Init", function()
	PlayerSpawnService:Init()
end)
print("[Main] Demo spectator spawn ready")
DemoDiagnosticsService:Mark("PlayerSpawnBeacon")
warn("[Main] Demo spectator spawn ready")

runStep("MapService:Init", function()
	MapService:Init()
end)

runStep("PathService:Init", function()
	PathService:Init()
end)

runStep("EconomyService:Init", function()
	EconomyService:Init()
end)

runStep("EnemyService:Init", function()
	EnemyService:Init()
end)

runStep("TowerService:Init", function()
	TowerService:Init()
end)

runStep("WaveService:Init", function()
	WaveService:Init()
end)

runStep("MapService:BuildBacklundFogDistrict", function()
	MapService:BuildBacklundFogDistrict()
end)
print("[Main] Demo map build requested")
DemoDiagnosticsService:Mark("MapBuildBeacon")
warn("[Main] Demo map build requested")

local pathPoints
runStep("PathService:BuildBacklundPath", function()
	pathPoints = PathService:BuildBacklundPath()
end)

local firstPathPoint = pathPoints and pathPoints[1] or Vector3.new(0, 0, 0)
local towerPosition = firstPathPoint + Vector3.new(-14, 2.5, 20)

runStep("TowerService:PlaceTower", function()
	local testTower = TowerService:PlaceTower("BasicTower", towerPosition)
	if testTower then
		print(string.format("[Main] Placed test tower: %s", testTower.Name))
	else
		warn("[Main] Failed to place test tower")
	end
end)

runStep("TowerService:StartAllTowersCombat", function()
	TowerService:StartAllTowersCombat()
end)

runStep("WaveService:StartWaveLoop", function()
	WaveService:StartWaveLoop(3)
	print("[Main] Triggered wave loop")
end)
print("[Main] Demo wave loop requested")
DemoDiagnosticsService:Mark("WaveLoopBeacon")
warn("[Main] Demo wave loop requested")

