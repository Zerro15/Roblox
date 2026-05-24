local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local EnemyConfig = require(Shared:WaitForChild("configs"):WaitForChild("EnemyConfig"))

local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local EnemyService = {}

local function toVector3(values)
	return Vector3.new(values[1], values[2], values[3])
end

local function toColor3(values)
	return Color3.new(values[1], values[2], values[3])
end

function EnemyService:SpawnEnemy(enemyType, position)
	local config = EnemyConfig[enemyType]
	if not config then
		warn(string.format("[EnemyService] Unknown enemy type: %s", tostring(enemyType)))
		return nil
	end

	local enemiesFolder = RuntimeService:GetContainer("Enemies")
	local enemy = Instance.new("Part")
	enemy.Name = enemyType
	enemy.Size = toVector3(config.size)
	enemy.Color = toColor3(config.color)
	enemy.Anchored = true
	enemy.Shape = Enum.PartType.Block
	enemy.TopSurface = Enum.SurfaceType.Smooth
	enemy.BottomSurface = Enum.SurfaceType.Smooth
	enemy.Material = Enum.Material.Neon
	enemy.Position = position or Vector3.new(0, 3, 0)

	enemy:SetAttribute("EnemyType", enemyType)
	enemy:SetAttribute("DisplayName", config.displayName)
	enemy:SetAttribute("MaxHealth", config.maxHealth)
	enemy:SetAttribute("Health", config.maxHealth)
	enemy:SetAttribute("Speed", config.speed)
	enemy:SetAttribute("Reward", config.reward)
	enemy.Parent = enemiesFolder

	return enemy
end

function EnemyService:Init()
	local count = 0
	for _ in pairs(EnemyConfig) do
		count += 1
	end

	print(string.format("[EnemyService] Loaded %d enemy definitions", count))
end

return EnemyService
