local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local services = script.Parent:WaitForChild("services")

local RuntimeService = require(services:WaitForChild("RuntimeService"))
local MapService = require(services:WaitForChild("MapService"))
local PathService = require(services:WaitForChild("PathService"))
local HubService = require(services:WaitForChild("HubService"))
local GameStateService = require(services:WaitForChild("GameStateService"))
local EconomyService = require(services:WaitForChild("EconomyService"))
local EnemyService = require(services:WaitForChild("EnemyService"))
local TowerService = require(services:WaitForChild("TowerService"))
local WaveService = require(services:WaitForChild("WaveService"))
local PlayerSpawnService = require(services:WaitForChild("PlayerSpawnService"))
local DemoDiagnosticsService = require(services:WaitForChild("DemoDiagnosticsService"))

print(string.format("[Server boot] %s v%s", GameConfig.GameName, GameConfig.Version))
print("[Main] Playable tower-defense bootstrap starting")
warn(string.format("[Server boot] %s v%s", GameConfig.GameName, GameConfig.Version))
warn("[Main] Playable tower-defense bootstrap starting")

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

runStep("GameStateService:Init", function()
	GameStateService:Init()
end)

runStep("PlayerSpawnService:Init", function()
	PlayerSpawnService:Init()
end)
print("[Main] Demo spectator spawn ready")
DemoDiagnosticsService:Mark("PlayerSpawnBeacon")
warn("[Main] Demo spectator spawn ready")

runStep("HubService:BuildHub", function()
	HubService:BuildHub()
end)

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

EnemyService:SetEnemyReachedBaseCallback(function(enemy)
	local damage = enemy and enemy:GetAttribute("BaseDamage") or 1
	GameStateService:DamageBase(damage, enemy and enemy.Name or "UnknownEnemy")
end)

runStep("TowerService:Init", function()
	TowerService:Init()
end)

runStep("WaveService:Init", function()
	WaveService:Init()
end)

runStep("MapService:BuildGreymoorVeilDistrict", function()
	MapService:BuildGreymoorVeilDistrict()
end)
print("[Main] Demo map build requested")
DemoDiagnosticsService:Mark("MapBuildBeacon")
warn("[Main] Demo map build requested")

runStep("PathService:BuildGreymoorPath", function()
	PathService:BuildGreymoorPath()
end)

local defenseStarted = false

local function startDefense(sourceName)
	if defenseStarted then
		warn("[Main] Defense start ignored; already running")
		return false
	end

	defenseStarted = true
	GameStateService:SetState("Defense")
	HubService:StartDefense(sourceName)
	PlayerSpawnService:EnterDefenseSpectator()

	runStep("TowerService:StartAllTowersCombat", function()
		TowerService:StartAllTowersCombat()
	end)

	runStep("WaveService:StartWaveLoop", function()
		WaveService:StartWaveLoop(GameConfig.TotalWaves or 15)
		print("[Main] Triggered wave loop")
	end)
	print("[Main] Demo wave loop requested")
	DemoDiagnosticsService:Mark("WaveLoopBeacon")
	warn("[Main] Demo wave loop requested")
	return true
end

HubService:SetStartDefenseCallback(function(player)
	startDefense(player and player.Name or "ProximityPrompt")
end)

local placeTowerRequest = RuntimeService:GetRemoteEvent("PlaceTowerRequest")
placeTowerRequest.OnServerEvent:Connect(function(player, towerType, padName)
	if not GameStateService:IsMatchActive() then
		warn(string.format("[Main] Player %s tower request blocked outside Veil Defense", player.Name))
		return
	end

	towerType = towerType or "LanternWarden"
	local tower
	if type(padName) == "string" and padName ~= "" then
		tower = TowerService:PlaceTowerAtPad(towerType, padName, player)
	else
		tower = TowerService:PlaceTowerAtNextPad(towerType, player)
	end
	if tower then
		print(string.format("[Main] Player %s placed tower %s", player.Name, tower.Name))
	else
		warn(string.format("[Main] Player %s could not place tower", player.Name))
	end
end)

local sellTowerRequest = RuntimeService:GetRemoteEvent("SellTowerRequest")
sellTowerRequest.OnServerEvent:Connect(function(player, towerRuntimeId)
	if not GameStateService:IsMatchActive() then
		warn(string.format("[Main] Player %s sell request blocked outside Veil Defense", player.Name))
		return
	end

	if not towerRuntimeId then
		warn(string.format("[Main] Player %s sell request missing tower id", player.Name))
		return
	end
	local sold = TowerService:SellTower(towerRuntimeId)
	if sold then
		print(string.format("[Main] Player %s sold tower %s", player.Name, towerRuntimeId))
	else
		warn(string.format("[Main] Player %s failed to sell tower %s", player.Name, towerRuntimeId))
	end
end)

local towerSelectedNotify = RuntimeService:GetRemoteEvent("TowerSelectedNotify")
towerSelectedNotify.OnServerEvent:Connect(function(player, towerRuntimeId)
	local towerInfo = TowerService:GetTowerInfo(towerRuntimeId)
	if not towerInfo then
		warn(string.format("[Main] Player %s selected invalid tower %s", player.Name, tostring(towerRuntimeId)))
		return
	end
	print(string.format("[Playable] Tower selected: %s by %s", tostring(towerRuntimeId), player.Name))
	warn(string.format("[Playable] Tower selected: %s", tostring(towerRuntimeId)))
end)

local startDefenseRequest = RuntimeService:GetRemoteEvent("StartDefenseRequest")
startDefenseRequest.OnServerEvent:Connect(function(player)
	print(string.format("[Hub] Start defense clicked: %s", player.Name))
	warn("[Hub] Start defense clicked")
	startDefense(player.Name)
end)

if GameConfig.AutomationAutoStartEnabled then
	task.delay(120, function()
		if not defenseStarted then
			warn("[Main] Automation fallback starting Veil Defense")
			startDefense("automation fallback")
		end
	end)
end

