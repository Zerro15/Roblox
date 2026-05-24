local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local TowerConfig = require(Shared:WaitForChild("configs"):WaitForChild("TowerConfig"))

local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local TowerService = {}

local function toVector3(values)
	return Vector3.new(values[1], values[2], values[3])
end

local function toColor3(values)
	return Color3.new(values[1], values[2], values[3])
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
	tower:SetAttribute("Cost", config.cost)
	tower.Parent = towersFolder

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
