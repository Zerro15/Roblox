local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local EconomyService = {
	startingMoney = 0,
	currentMoney = 0,
}

function EconomyService:CanAfford(amount)
	return self.currentMoney >= amount
end

function EconomyService:Spend(amount)
	if not self:CanAfford(amount) then
		return false
	end

	self.currentMoney -= amount
	return true
end

function EconomyService:Add(amount)
	self.currentMoney += amount
	return self.currentMoney
end

function EconomyService:Init()
	self.startingMoney = GameConfig.StartingMoney or 300
	self.currentMoney = self.startingMoney
	print(string.format("[EconomyService] Starting money: %d", self.currentMoney))
end

return EconomyService
