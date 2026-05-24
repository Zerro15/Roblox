local TweenService = game:GetService("TweenService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local EnemyConfig = require(Shared:WaitForChild("configs"):WaitForChild("EnemyConfig"))

local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local EnemyService = {
	activeEnemies = {},
}

local function toVector3(values)
	return Vector3.new(values[1], values[2], values[3])
end

local function toColor3(values)
	return Color3.new(values[1], values[2], values[3])
end

local function getEnemyKey(enemy)
	return enemy:GetDebugId()
end

function EnemyService:GetActiveEnemies()
	local aliveEnemies = {}

	for enemyKey, enemy in pairs(self.activeEnemies) do
		if self:IsEnemyAlive(enemy) then
			aliveEnemies[enemyKey] = enemy
		else
			self.activeEnemies[enemyKey] = nil
		end
	end

	return aliveEnemies
end

function EnemyService:IsEnemyAlive(enemy)
	if not enemy then
		return false
	end

	if not enemy.Parent then
		return false
	end

	local health = enemy:GetAttribute("Health") or 0
	return health > 0
end

function EnemyService:CleanupEnemy(enemy)
	if not enemy then
		return
	end

	self.activeEnemies[getEnemyKey(enemy)] = nil

	if enemy.Parent then
		enemy:Destroy()
	end
end

function EnemyService:DamageEnemy(enemy, amount, source)
	if not self:IsEnemyAlive(enemy) then
		return {
			damaged = false,
			defeated = false,
			reward = 0,
			enemyName = enemy and enemy.Name or nil,
			newHealth = 0,
		}
	end

	local currentHealth = enemy:GetAttribute("Health") or 0
	local newHealth = currentHealth - amount
	enemy:SetAttribute("Health", newHealth)

	if newHealth <= 0 then
		local reward = enemy:GetAttribute("Reward") or 0
		local enemyName = enemy.Name
		print("[EnemyService] Enemy defeated: " .. enemyName .. ", reward: " .. tostring(reward))
		self:CleanupEnemy(enemy)
		return {
			damaged = true,
			defeated = true,
			reward = reward,
			enemyName = enemyName,
			newHealth = 0,
		}
	end

	print(string.format("[EnemyService] Damaged enemy %s for %s, health: %s", enemy.Name, tostring(amount), tostring(newHealth)))
	return {
		damaged = true,
		defeated = false,
		reward = 0,
		enemyName = enemy.Name,
		newHealth = newHealth,
	}
end

function EnemyService:MoveEnemyAlongPath(enemy, pathPoints)
	if not self:IsEnemyAlive(enemy) then
		return
	end

	if not pathPoints or #pathPoints == 0 then
		warn(string.format("[EnemyService] No path points available for enemy: %s", enemy.Name))
		return
	end

	local speed = enemy:GetAttribute("Speed") or 8
	enemy:SetAttribute("IsMoving", true)

	for index, point in ipairs(pathPoints) do
		if not self:IsEnemyAlive(enemy) then
			self:CleanupEnemy(enemy)
			return
		end

		local currentPosition = enemy.Position
		local targetPosition = Vector3.new(point.X, currentPosition.Y, point.Z)
		local distance = (targetPosition - currentPosition).Magnitude
		local duration = math.max(distance / speed, 0.1)

		local tween = TweenService:Create(
			enemy,
			TweenInfo.new(duration, Enum.EasingStyle.Linear, Enum.EasingDirection.Out),
			{ Position = targetPosition }
		)
		tween:Play()
		tween.Completed:Wait()

		if self:IsEnemyAlive(enemy) then
			enemy:SetAttribute("PathIndex", index)
		else
			return
		end
	end

	if self:IsEnemyAlive(enemy) then
		print("[EnemyService] Enemy reached exit: " .. enemy.Name)
	end
	self:CleanupEnemy(enemy)
end

function EnemyService:StartEnemyMovement(enemy, pathPoints)
	task.spawn(function()
		self:MoveEnemyAlongPath(enemy, pathPoints)
	end)
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
	enemy:SetAttribute("IsMoving", false)
	enemy:SetAttribute("PathIndex", 1)
	enemy:SetAttribute("Reward", config.reward)
	enemy.Parent = enemiesFolder
	self.activeEnemies[getEnemyKey(enemy)] = enemy

	print(string.format("[EnemyService] Spawned enemy %s at %.1f, %.1f, %.1f", enemy.Name, enemy.Position.X, enemy.Position.Y, enemy.Position.Z))

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
