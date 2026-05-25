local Debris = game:GetService("Debris")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local TowerConfig = require(Shared:WaitForChild("configs"):WaitForChild("TowerConfig"))

local EconomyService = require(script.Parent:WaitForChild("EconomyService"))
local EnemyService = require(script.Parent:WaitForChild("EnemyService"))
local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local TowerService = {
	activeTowers = {},
	nextTowerId = 0,
}

local function toVector3(values)
	return Vector3.new(values[1], values[2], values[3])
end

local function toColor3(values)
	return Color3.new(values[1], values[2], values[3])
end

local function getTowerKey(tower)
	return tower:GetAttribute("RuntimeTowerId") or tower.Name
end

local function createTowerVisuals(parent, tower, config)
	local runtimeId = tower:GetAttribute("RuntimeTowerId") or tower.Name
	local beacon = Instance.new("Part")
	beacon.Name = runtimeId .. "_DemoBeacon"
	beacon.Shape = Enum.PartType.Ball
	beacon.Size = Vector3.new(3.8, 3.8, 3.8)
	beacon.Position = tower.Position + Vector3.new(0, 7, 0)
	beacon.Anchored = true
	beacon.CanCollide = false
	beacon.Material = Enum.Material.Neon
	beacon.Color = Color3.new(0.35, 0.85, 1.0)
	beacon:SetAttribute("RuntimeTowerId", runtimeId)
	beacon:SetAttribute("TowerVisualKind", "Beacon")
	beacon.Parent = parent

	local range = config.range or 0
	if range > 0 then
		local preview = Instance.new("Part")
		preview.Name = runtimeId .. "_RangePreview"
		preview.Size = Vector3.new(range * 2, 0.12, range * 2)
		preview.Position = Vector3.new(tower.Position.X, 0.18, tower.Position.Z)
		preview.Anchored = true
		preview.CanCollide = false
		preview.Material = Enum.Material.Neon
		preview.Color = Color3.new(0.1, 0.42, 1.0)
		preview.Transparency = 0.86
		preview:SetAttribute("RuntimeTowerId", runtimeId)
		preview:SetAttribute("TowerVisualKind", "RangePreview")
		preview.Parent = parent
	end
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

function TowerService:CreateDebugAttackBeam(tower, targetPosition, targetName)
	if not tower or not tower.Parent or not targetPosition then
		return
	end

	local projectilesFolder = RuntimeService:GetContainer("Projectiles")
	local origin = tower.Position + Vector3.new(0, 5, 0)
	local target = targetPosition
	local delta = target - origin
	local distance = delta.Magnitude
	if distance <= 0 then
		return
	end

	local beam = Instance.new("Part")
	beam.Name = string.format("Beam_%s_to_%s", tower.Name, targetName or "Enemy")
	beam.Anchored = true
	beam.CanCollide = false
	beam.Material = Enum.Material.Neon
	beam.Color = Color3.new(1.0, 0.92, 0.2)
	beam.Size = Vector3.new(0.85, 0.85, distance)
	beam.CFrame = CFrame.lookAt(origin, target) * CFrame.new(0, 0, -distance / 2)
	beam.Parent = projectilesFolder
	Debris:AddItem(beam, 0.28)

	local impact = Instance.new("Part")
	impact.Name = "DemoAttackImpact"
	impact.Shape = Enum.PartType.Ball
	impact.Size = Vector3.new(3.2, 3.2, 3.2)
	impact.Position = target
	impact.Anchored = true
	impact.CanCollide = false
	impact.Material = Enum.Material.Neon
	impact.Color = Color3.new(1.0, 0.42, 0.08)
	impact.Parent = projectilesFolder
	Debris:AddItem(impact, 0.28)

	local muzzle = Instance.new("Part")
	muzzle.Name = "DemoTowerMuzzleFlash"
	muzzle.Shape = Enum.PartType.Ball
	muzzle.Size = Vector3.new(2.6, 2.6, 2.6)
	muzzle.Position = origin
	muzzle.Anchored = true
	muzzle.CanCollide = false
	muzzle.Material = Enum.Material.Neon
	muzzle.Color = Color3.new(1.0, 0.95, 0.35)
	muzzle.Parent = projectilesFolder
	Debris:AddItem(muzzle, 0.22)
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
	warn(string.format("[TowerService] Runtime marker: Tower started combat: %s", tower.Name))

	task.spawn(function()
		while tower and tower.Parent do
			local fireRate = tower:GetAttribute("FireRate") or 1
			local delayTime = math.max(1 / fireRate, 0.1)
			local enemy = self:FindNearestEnemy(tower, EnemyService:GetActiveEnemies())

			if enemy then
				print(string.format("[TowerService] Target acquired: %s -> %s", tower.Name, enemy.Name))
				warn(string.format("[TowerService] Runtime marker: Target acquired: %s -> %s", tower.Name, enemy.Name))
				local damage = tower:GetAttribute("Damage") or 0
				local targetPosition = enemy.Position
				local targetName = enemy.Name
				local result = EnemyService:DamageEnemy(enemy, damage, tower.Name)
				if result and result.damaged then
					print(string.format("[TowerService] Attacked enemy %s with %s", enemy.Name, tower.Name))
					warn(string.format("[TowerService] Runtime marker: Attacked enemy %s with %s", enemy.Name, tower.Name))
					print(string.format("[DemoGameplay] Tower attack fired: %s -> %s", tower.Name, targetName))
					warn(string.format("[DemoGameplay] Tower attack fired: %s -> %s", tower.Name, targetName))
					print(string.format("[Playable] Tower attack fired: %s -> %s", tower.Name, targetName))
					warn(string.format("[Playable] Tower attack fired: %s -> %s", tower.Name, targetName))
					self:CreateDebugAttackBeam(tower, targetPosition, targetName)

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

function TowerService:GetBuildPadsFolder()
	local mapFolder = RuntimeService:GetContainer("Map")
	return mapFolder:FindFirstChild("BuildPads")
end

function TowerService:FindNextOpenBuildPad()
	local buildPadsFolder = self:GetBuildPadsFolder()
	if not buildPadsFolder then
		return nil
	end

	local pads = buildPadsFolder:GetChildren()
	table.sort(pads, function(a, b)
		return a.Name < b.Name
	end)

	for _, pad in ipairs(pads) do
		if pad:IsA("BasePart") and not pad:GetAttribute("Occupied") then
			return pad
		end
	end

	return nil
end

function TowerService:PlaceTowerAtNextPad(towerType, player)
	if not TowerConfig[towerType] then
		warn("[TowerService] Unknown tower type for next pad: " .. tostring(towerType))
		return nil
	end

	local pad = self:FindNextOpenBuildPad()
	if not pad then
		warn("[TowerService] No open build pads available")
		return nil
	end

	local tower = self:PlaceTower(towerType, pad.Position + Vector3.new(0, 5, 0))
	if not tower then
		return nil
	end

	pad:SetAttribute("Occupied", true)
	pad:SetAttribute("TowerName", tower.Name)
	tower:SetAttribute("BuildPad", pad.Name)
	if player then
		tower:SetAttribute("PlacedBy", player.Name)
	end

	self:StartTowerCombat(tower)
	return tower
end

function TowerService:PlaceTower(towerType, position)
	local config = TowerConfig[towerType]
	if not config then
		warn(string.format("[TowerService] Unknown tower type: %s", tostring(towerType)))
		return nil
	end

	local cost = config.cost or 0
	if cost > 0 and not EconomyService:CanAfford(cost) then
		print(string.format(
			"[TowerService] Cannot place %s: costs %d, have %d",
			towerType,
			cost,
			EconomyService:GetMoney()
		))
		return nil
	end

	if cost > 0 then
		local spent = EconomyService:Spend(cost)
		if not spent then
			print(string.format(
				"[TowerService] Failed to spend %d for %s",
				cost,
				towerType
			))
			return nil
		end
	end

	local towersFolder = RuntimeService:GetContainer("Towers")
	local tower = Instance.new("Part")
	self.nextTowerId += 1
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
	tower:SetAttribute("Cost", cost)
	tower:SetAttribute("RuntimeTowerId", string.format("Tower_%03d", self.nextTowerId))
	tower.Parent = towersFolder
	createTowerVisuals(towersFolder, tower, config)
	self.activeTowers[getTowerKey(tower)] = tower

	print(string.format("[TowerService] Tower placed: %s (cost: %d)", tower.Name, cost))
	warn(string.format("[TowerService] Runtime marker: Tower placed: %s", tower.Name))
	print("[DemoGameplay] Tower placed: " .. tower.Name)
	warn("[DemoGameplay] Tower placed: " .. tower.Name)
	print("[Playable] Tower placed: " .. tower.Name)
	warn("[Playable] Tower placed: " .. tower.Name)

	return tower
end

function TowerService:SellTower(towerRuntimeId)
	local tower = nil
	for key, t in pairs(self.activeTowers) do
		if key == towerRuntimeId or t:GetAttribute("RuntimeTowerId") == towerRuntimeId then
			tower = t
			break
		end
	end

	if not tower or not tower.Parent then
		warn("[TowerService] SellTower: tower not found: " .. tostring(towerRuntimeId))
		return false
	end

	local cost = tower:GetAttribute("Cost") or 0
	local refund = math.floor(cost * 0.5)
	local padName = tower:GetAttribute("BuildPad")

	if padName then
		local buildPadsFolder = self:GetBuildPadsFolder()
		if buildPadsFolder then
			local pad = buildPadsFolder:FindFirstChild(padName)
			if pad then
				pad:SetAttribute("Occupied", false)
				pad:SetAttribute("TowerName", "")
			end
		end
	end

	local towerName = tower.Name
	local towerKey = getTowerKey(tower)
	self.activeTowers[towerKey] = nil

	local runtimeId = tower:GetAttribute("RuntimeTowerId")
	local towersFolder = RuntimeService:GetContainer("Towers")
	for _, child in ipairs(towersFolder:GetChildren()) do
		if child ~= tower and child:GetAttribute("RuntimeTowerId") == runtimeId then
			child:Destroy()
		end
	end

	tower:Destroy()

	if refund > 0 then
		EconomyService:Add(refund)
	end

	print(string.format("[TowerService] Tower sold: %s, refund: %d", towerName, refund))
	warn(string.format("[TowerService] Runtime marker: Tower sold: %s", towerName))
	print("[Playable] Tower sold: " .. towerName)
	warn("[Playable] Tower sold: " .. towerName)
	return true
end

function TowerService:PlaceTowerAtPad(towerType, padName, player)
	if not TowerConfig[towerType] then
		warn("[TowerService] Unknown tower type for pad: " .. tostring(towerType))
		return nil
	end

	if type(padName) ~= "string" or padName == "" then
		warn("[TowerService] Missing pad name")
		return nil
	end

	local buildPadsFolder = self:GetBuildPadsFolder()
	if not buildPadsFolder then
		warn("[TowerService] No BuildPads folder")
		return nil
	end

	local pad = buildPadsFolder:FindFirstChild(padName)
	if not pad or not pad:IsA("BasePart") then
		warn("[TowerService] Pad not found: " .. tostring(padName))
		return nil
	end

	if pad:GetAttribute("Occupied") then
		warn("[TowerService] Pad already occupied: " .. padName)
		return nil
	end

	local tower = self:PlaceTower(towerType, pad.Position + Vector3.new(0, 5, 0))
	if not tower then
		return nil
	end

	pad:SetAttribute("Occupied", true)
	pad:SetAttribute("TowerName", tower.Name)
	tower:SetAttribute("BuildPad", pad.Name)
	if player then
		tower:SetAttribute("PlacedBy", player.Name)
	end

	self:StartTowerCombat(tower)
	return tower
end

function TowerService:GetTowerInfo(towerRuntimeId)
	for key, tower in pairs(self.activeTowers) do
		if key == towerRuntimeId or tower:GetAttribute("RuntimeTowerId") == towerRuntimeId then
			return {
				name = tower.Name,
				runtimeId = tower:GetAttribute("RuntimeTowerId"),
				towerType = tower:GetAttribute("TowerType"),
				displayName = tower:GetAttribute("DisplayName"),
				damage = tower:GetAttribute("Damage"),
				range = tower:GetAttribute("Range"),
				fireRate = tower:GetAttribute("FireRate"),
				cost = tower:GetAttribute("Cost"),
				buildPad = tower:GetAttribute("BuildPad"),
			}
		end
	end
	return nil
end

function TowerService:Init()
	local count = 0
	for _ in pairs(TowerConfig) do
		count += 1
	end

	print(string.format("[TowerService] Loaded %d tower definitions", count))
	warn(string.format("[TowerService] Runtime marker: Loaded %d tower definitions", count))
end

return TowerService
