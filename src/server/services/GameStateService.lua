local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local GameStateService = {
	baseHealth = 0,
	currentWave = 0,
	state = "Booting",
}

function GameStateService:GetRuntimeFolder()
	return RuntimeService:GetOrCreateRuntimeFolder()
end

function GameStateService:SetAttribute(name, value)
	self:GetRuntimeFolder():SetAttribute(name, value)
end

function GameStateService:SetMoney(value)
	self:SetAttribute("Money", value)
end

function GameStateService:SetWave(value)
	self.currentWave = value
	self:SetAttribute("Wave", value)
end

function GameStateService:SetEnemiesAlive(value)
	self:SetAttribute("EnemiesAlive", value)
end

function GameStateService:SetState(value)
	self.state = value
	self:SetAttribute("GameState", value)
end

function GameStateService:GetState()
	return self.state
end

function GameStateService:IsMatchActive()
	return self.state == "Defense"
		or self.state == "Running"
		or self.state == "WaveRunning"
		or self.state == "Intermission"
end

function GameStateService:GetBaseHealth()
	return self.baseHealth
end

function GameStateService:DamageBase(amount, source)
	if self.baseHealth <= 0 or not self:IsMatchActive() then
		return self.baseHealth
	end

	self.baseHealth = math.max(self.baseHealth - math.max(amount or 0, 0), 0)
	self:SetAttribute("BaseHealth", self.baseHealth)
	print(string.format("[Playable] Enemy reached base: %s, base health: %d", source or "UnknownEnemy", self.baseHealth))
	warn(string.format("[Playable] Enemy reached base: %s", source or "UnknownEnemy"))
	print(string.format("[Playable] Base damaged: %d remaining", self.baseHealth))
	warn(string.format("[Playable] Base damaged: %d remaining", self.baseHealth))

	if self.baseHealth <= 0 then
		self:SetState("GameOver")
		print("[Playable] Game over")
		warn("[Playable] Game over")
	end

	return self.baseHealth
end

function GameStateService:Init()
	self.baseHealth = GameConfig.BaseHealth or 20
	self.currentWave = 0
	self:SetMoney(GameConfig.StartingMoney or 300)
	self:SetWave(0)
	self:SetEnemiesAlive(0)
	self:SetAttribute("BaseHealth", self.baseHealth)
	self:SetAttribute("MaxBaseHealth", self.baseHealth)
	self:SetState("Lobby")
	print("[Playable] Game started")
	warn("[Playable] Game started")
end

return GameStateService
