local Debris = game:GetService("Debris")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local TowerConfig = require(Shared:WaitForChild("configs"):WaitForChild("TowerConfig"))

local EconomyService = require(script.Parent:WaitForChild("EconomyService"))
local EnemyService = require(script.Parent:WaitForChild("EnemyService"))
local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local TowerService = {
	activeTowers = {},
}

local function toVector3(values)
	return Vector3.new(values[1], values[2], values[3])
end

local function toColor3(values)
	return Color3.new(values[1], values[2], values[3])
end

local function getTowerKey(tower)
	return tower:GetDebugId()
end

function TowerService:GetActiveTowers()
	return self.activeTowers
end

function TowerService:FindNearestEnemy(tower, enemies)
	if not tower or not tower.Parent then
		return nil
	end

	local range = tower:GetAttribute("Range") or 0
	local towerPosition = tower.Position
	local nearestEnemy = nil
	local nearestDistance = math.huge

	for _, enemy in pairs(enemies) do
		if EnemyService:IsEnemyAlive(enemy) then
			local distance = (enemy.Position - towerPosition).Magnitude
			if distance <= range and distance < nearestDistance then
				nearestEnemy = enemy
				nearestDistance = distance
			end
		end
	end

	return nearestEnemy
end

function TowerService:CreateDebugAttackBeam(tower, enemy)
	if not tower or not tower.Parent or not enemy or not enemy.Parent then
		return
	end

	local projectilesFolder = RuntimeService:GetContainer("Projectiles")
	local origin = tower.Position
	local target = enemy.Position
	local delta = target - origin
	local distance = delta.Magnitude
	if distance <= 0 then
		return
	end

	local beam = Instance.new("Part")
	beam.Name = string.format("Beam_%s_to_%s", tower.Name, enemy.Name)
	beam.Anchored = true
	beam.CanCollide = false
	beam.Material = Enum.Material.Neon
	beam.Color = tower.Color
	beam.Size = Vector3.new(0.25, 0.25, distance)
	beam.CFrame = CFrame.lookAt(origin, target) * CFrame.new(0, 0, -distance / 2)
	beam.Parent = projectilesFolder
	Debris:AddItem(beam, 0.12)
end

function TowerService:StartTowerCombat(tower)
	if not tower or not tower.Parent then
		return
	end

	if tower:GetAttribute("IsAttacking") then
		return
	end

	tower:SetAttribute("IsAttacking", true)
	print(string.format("[TowerService] Tower started combat: %s", tower.Name))

	task.spawn(function()
		while tower and tower.Parent do
			local fireRate = tower:GetAttribute("FireRate") or 1
			local delayTime = math.max(1 / fireRate, 0.1)
			local enemy = self:FindNearestEnemy(tower, EnemyService:GetActiveEnemies())

			if enemy then
				print(string.format("[TowerService] Target acquired: %s -> %s", tower.Name, enemy.Name))
				local damage = tower:GetAttribute("Damage") or 0
				local result = EnemyService:DamageEnemy(enemy, damage, tower.Name)
				if result and result.damaged then
					print(string.format("[TowerService] Attacked enemy %s with %s", enemy.Name, tower.Name))
					self:CreateDebugAttackBeam(tower, enemy)

					if result.defeated == true then
						EconomyService:AwardForEnemy(result.enemyName, result.reward, tower.Name)
					end
				end
			end

			task.wait(delayTime)
		end
	end)
end

function TowerService:StartAllTowersCombat()
	for _, tower in pairs(self.activeTowers) do
		self:StartTowerCombat(tower)
	end
end

function TowerService:PlaceTower(towerType, position)
	local config = TowerConfig[towerType]
	if not config then
		warn(string.format("[TowerService] Unknown tower type: %s", tostring(towerType)))
		return nil
	end

	local towersFolder = RuntimeService:GetContainer("Towers")
	local tower = Instance.new("Part")
	tower.Name = towerType
	tower.Size = toVector3(config.size)
	tower.Color = toColor3(config.color)
	tower.Anchored = true
	tower.Shape = Enum.PartType.Cylinder
	tower.TopSurface = Enum.SurfaceType.Smooth
	tower.BottomSurface = Enum.SurfaceType.Smooth
	tower.Material = Enum.Material.Metal
	tower.Position = position or Vector3.new(0, 4, -18)

	tower:SetAttribute("TowerType", towerType)
	tower:SetAttribute("DisplayName", config.displayName)
	tower:SetAttribute("Damage", config.damage)
	tower:SetAttribute("Range", config.range)
	tower:SetAttribute("FireRate", config.fireRate)
	tower:SetAttribute("IsAttacking", false)
	tower:SetAttribute("Cost", config.cost)
	tower.Parent = towersFolder
	self.activeTowers[getTowerKey(tower)] = tower

	print(string.format("[TowerService] Tower placed: %s", tower.Name))

	return tower
end

function TowerService:Init()
	local count = 0
	for _ in pairs(TowerConfig) do
		count += 1
	end

	print(string.format("[TowerService] Loaded %d tower definitions", count))
end

return TowerService
