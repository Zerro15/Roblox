local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local GameStateService = require(script.Parent:WaitForChild("GameStateService"))

local EconomyService = {
	startingMoney = 0,
	currentMoney = 0,
}

function EconomyService:CanAfford(amount)
	return self.currentMoney >= amount
end

function EconomyService:Spend(amount)
	if amount <= 0 then
		return true
	end

	if not self:CanAfford(amount) then
		return false
	end

	self.currentMoney -= amount
	GameStateService:SetMoney(self.currentMoney)
	return true
end

function EconomyService:Add(amount)
	if amount <= 0 then
		return self.currentMoney
	end

	self.currentMoney += amount
	GameStateService:SetMoney(self.currentMoney)
	return self.currentMoney
end

function EconomyService:GetMoney()
	return self.currentMoney
end

function EconomyService:AwardForEnemy(enemyName, reward, source)
	if reward <= 0 then
		return self.currentMoney
	end

	local currentMoney = self:Add(reward)
	print(string.format(
		"[EconomyService] Awarded %d for %s by %s. Money: %d",
		reward,
		enemyName or "UnknownEnemy",
		source or "UnknownSource",
		currentMoney
	))
	print(string.format("[Playable] Reward granted: %d for %s", reward, enemyName or "UnknownEnemy"))
	warn(string.format("[Playable] Reward granted: %d", reward))
	return currentMoney
end

function EconomyService:Init()
	self.startingMoney = GameConfig.StartingMoney or 300
	self.currentMoney = self.startingMoney
	GameStateService:SetMoney(self.currentMoney)
	print(string.format("[EconomyService] Starting money: %d", self.currentMoney))
end

return EconomyService
