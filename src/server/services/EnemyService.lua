local Debris = game:GetService("Debris")
local TweenService = game:GetService("TweenService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local EnemyConfig = require(Shared:WaitForChild("configs"):WaitForChild("EnemyConfig"))

local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local EnemyService = {
	activeEnemies = {},
	nextEnemyId = 0,
	enemyReachedBaseCallback = nil,
}

local function toVector3(values)
	return Vector3.new(values[1], values[2], values[3])
end

local function toColor3(values)
	return Color3.new(values[1], values[2], values[3])
end

local function getEnemyKey(enemy)
	return enemy:GetAttribute("RuntimeEnemyId") or enemy.Name
end

local function updateEnemyHealthLabel(enemy)
	local billboard = enemy:FindFirstChild("DemoHealthBillboard")
	local label = billboard and billboard:FindFirstChild("HealthText")
	if not label or not label:IsA("TextLabel") then
		return
	end

	local health = math.max(enemy:GetAttribute("Health") or 0, 0)
	local maxHealth = enemy:GetAttribute("MaxHealth") or health
	label.Text = string.format("%s  %d/%d", enemy.Name, health, maxHealth)
end

local function createEnemyHealthBillboard(enemy)
	local billboard = Instance.new("BillboardGui")
	billboard.Name = "DemoHealthBillboard"
	billboard.Size = UDim2.new(0, 150, 0, 34)
	billboard.StudsOffset = Vector3.new(0, 4.5, 0)
	billboard.AlwaysOnTop = true
	billboard.Parent = enemy

	local label = Instance.new("TextLabel")
	label.Name = "HealthText"
	label.Size = UDim2.new(1, 0, 1, 0)
	label.BackgroundColor3 = Color3.new(0.05, 0.05, 0.05)
	label.BackgroundTransparency = 0.25
	label.BorderSizePixel = 0
	label.TextColor3 = Color3.new(1.0, 0.95, 0.55)
	label.TextScaled = true
	label.Font = Enum.Font.GothamBold
	label.Parent = billboard

	updateEnemyHealthLabel(enemy)
end

local function createDamageFlash(enemy)
	local flash = Instance.new("Part")
	flash.Name = "DemoDamageFlash"
	flash.Shape = Enum.PartType.Ball
	flash.Size = Vector3.new(5.5, 5.5, 5.5)
	flash.Position = enemy.Position
	flash.Anchored = true
	flash.CanCollide = false
	flash.Material = Enum.Material.Neon
	flash.Color = Color3.new(1.0, 0.18, 0.08)
	flash.Transparency = 0.25
	flash.Parent = enemy.Parent
	Debris:AddItem(flash, 0.22)
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

function EnemyService:SetEnemyReachedBaseCallback(callback)
	self.enemyReachedBaseCallback = callback
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
	updateEnemyHealthLabel(enemy)
	createDamageFlash(enemy)
	print(string.format("[DemoGameplay] Enemy damaged: %s for %s", enemy.Name, tostring(amount)))
	warn(string.format("[DemoGameplay] Enemy damaged: %s", enemy.Name))
	print(string.format("[Playable] Enemy damaged: %s for %s", enemy.Name, tostring(amount)))
	warn(string.format("[Playable] Enemy damaged: %s", enemy.Name))

	if newHealth <= 0 then
		local reward = enemy:GetAttribute("Reward") or 0
		local enemyName = enemy.Name
		print("[EnemyService] Enemy defeated: " .. enemyName .. ", reward: " .. tostring(reward))
		warn("[EnemyService] Runtime marker: Enemy defeated: " .. enemyName)
		print("[Playable] Enemy killed: " .. enemyName)
		warn("[Playable] Enemy killed: " .. enemyName)
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
	warn(string.format("[EnemyService] Runtime marker: Damaged enemy %s", enemy.Name))
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
	print("[DemoGameplay] Enemy pathing started: " .. enemy.Name)
	warn("[DemoGameplay] Enemy pathing started: " .. enemy.Name)
	print("[Playable] Enemy pathing started: " .. enemy.Name)
	warn("[Playable] Enemy pathing started: " .. enemy.Name)

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
		warn("[EnemyService] Runtime marker: Enemy reached exit: " .. enemy.Name)
		if self.enemyReachedBaseCallback then
			self.enemyReachedBaseCallback(enemy)
		else
			print("[Playable] Enemy reached base: " .. enemy.Name)
			warn("[Playable] Enemy reached base: " .. enemy.Name)
		end
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
	self.nextEnemyId += 1
	enemy.Name = config.displayName
	enemy.Size = toVector3(config.size)
	enemy.Color = toColor3(config.color)
	enemy.Anchored = true
	enemy.Shape = Enum.PartType.Block
	enemy.TopSurface = Enum.SurfaceType.Smooth
	enemy.BottomSurface = Enum.SurfaceType.Smooth
	enemy.Material = config.isBoss and Enum.Material.ForceField or Enum.Material.Neon
	enemy.Position = position or Vector3.new(0, 3, 0)

	enemy:SetAttribute("EnemyType", enemyType)
	enemy:SetAttribute("DisplayName", config.displayName)
	enemy:SetAttribute("MaxHealth", config.maxHealth)
	enemy:SetAttribute("Health", config.maxHealth)
	enemy:SetAttribute("Speed", config.speed)
	enemy:SetAttribute("IsMoving", false)
	enemy:SetAttribute("PathIndex", 1)
	enemy:SetAttribute("Reward", config.reward)
	enemy:SetAttribute("BaseDamage", config.baseDamage or 1)
	enemy:SetAttribute("IsBoss", config.isBoss == true)
	enemy:SetAttribute("RuntimeEnemyId", string.format("Enemy_%03d", self.nextEnemyId))
	enemy.Parent = enemiesFolder
	createEnemyHealthBillboard(enemy)
	self.activeEnemies[getEnemyKey(enemy)] = enemy

	print(string.format("[EnemyService] Spawned enemy %s at %.1f, %.1f, %.1f", enemy.Name, enemy.Position.X, enemy.Position.Y, enemy.Position.Z))
	warn(string.format("[EnemyService] Runtime marker: Spawned enemy %s", enemy.Name))
	print("[DemoGameplay] Enemy spawned: " .. enemy.Name)
	warn("[DemoGameplay] Enemy spawned: " .. enemy.Name)
	print("[Playable] Enemy spawned: " .. enemy.Name)
	warn("[Playable] Enemy spawned: " .. enemy.Name)

	return enemy
end

function EnemyService:Init()
	local count = 0
	for _ in pairs(EnemyConfig) do
		count += 1
	end

	print(string.format("[EnemyService] Loaded %d enemy definitions", count))
	warn(string.format("[EnemyService] Runtime marker: Loaded %d enemy definitions", count))
end

return EnemyService
