local Lighting = game:GetService("Lighting")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local MapConfig = require(Shared:WaitForChild("configs"):WaitForChild("MapConfig"))

local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local MapService = {
	currentMapId = nil,
}

local MAP_CHILDREN = {
	"Ground",
	"Streets",
	"Buildings",
	"Lamps",
	"Decorations",
	"Zones",
}

local function toVector3(values)
	return Vector3.new(values[1], values[2], values[3])
end

local function toColor3(values)
	return Color3.new(values[1], values[2], values[3])
end

local function ensureFolder(parent, name)
	local existing = parent:FindFirstChild(name)
	if existing and existing:IsA("Folder") then
		return existing
	end

	local folder = Instance.new("Folder")
	folder.Name = name
	folder.Parent = parent
	return folder
end

local function clearChildren(instance)
	for _, child in ipairs(instance:GetChildren()) do
		child:Destroy()
	end
end

local function createPart(parent, name, shape, size, position, color, material)
	local part = Instance.new("Part")
	part.Name = name
	part.Shape = shape or Enum.PartType.Block
	part.Size = size
	part.Position = position
	part.Color = color
	part.Material = material or Enum.Material.SmoothPlastic
	part.Anchored = true
	part.TopSurface = Enum.SurfaceType.Smooth
	part.BottomSurface = Enum.SurfaceType.Smooth
	part.Parent = parent
	return part
end

function MapService:GetMapFolder()
	return RuntimeService:GetContainer("Map")
end

function MapService:GetMapConfig()
	return MapConfig.BacklundFogDistrict
end

function MapService:GetSection(name)
	return ensureFolder(self:GetMapFolder(), name)
end

function MapService:ClearMap()
	for _, sectionName in ipairs(MAP_CHILDREN) do
		clearChildren(self:GetSection(sectionName))
	end
end

function MapService:ApplyAtmosphere(config)
	Lighting.Ambient = toColor3(config.ambientColor)
	Lighting.OutdoorAmbient = toColor3(config.ambientColor)
	Lighting.FogColor = toColor3(config.fogColor)
	Lighting.FogStart = 10
	Lighting.FogEnd = 185
	Lighting.Brightness = 1.4
	Lighting.ClockTime = 21
end

function MapService:BuildBacklundFogDistrict()
	local config = self:GetMapConfig()
	self:ClearMap()
	self:ApplyAtmosphere(config)

	local groundFolder = self:GetSection("Ground")
	local streetsFolder = self:GetSection("Streets")
	local buildingsFolder = self:GetSection("Buildings")
	local lampsFolder = self:GetSection("Lamps")
	local decorationsFolder = self:GetSection("Decorations")
	local zonesFolder = self:GetSection("Zones")

	local groundSize = toVector3(config.mapSize)
	createPart(
		groundFolder,
		"DistrictGround",
		Enum.PartType.Block,
		groundSize,
		Vector3.new(0, -2, 0),
		toColor3(config.groundColor),
		Enum.Material.Slate
	)

	local roadSegments = {
		{ name = "StreetSegment_1", size = Vector3.new(26, 1, 34), position = Vector3.new(-48, 0, -66) },
		{ name = "StreetSegment_2", size = Vector3.new(26, 1, 36), position = Vector3.new(-48, 0, -28) },
		{ name = "StreetSegment_3", size = Vector3.new(26, 1, 34), position = Vector3.new(-22, 0, 8) },
		{ name = "StreetSegment_4", size = Vector3.new(26, 1, 34), position = Vector3.new(12, 0, 28) },
		{ name = "StreetSegment_5", size = Vector3.new(26, 1, 34), position = Vector3.new(42, 0, 54) },
		{ name = "StreetSegment_6", size = Vector3.new(26, 1, 30), position = Vector3.new(66, 0, 86) },
	}

	for _, segment in ipairs(roadSegments) do
		createPart(
			streetsFolder,
			segment.name,
			Enum.PartType.Block,
			segment.size,
			segment.position,
			toColor3(config.streetColor),
			Enum.Material.Basalt
		)
	end

	local buildingPositions = {
		{ "Building_NW_1", Vector3.new(-78, 10, -70), Vector3.new(20, 20, 18) },
		{ "Building_NE_1", Vector3.new(-18, 13, -70), Vector3.new(24, 26, 18) },
		{ "Building_NW_2", Vector3.new(-78, 12, -28), Vector3.new(18, 24, 20) },
		{ "Building_NE_2", Vector3.new(-16, 11, -24), Vector3.new(20, 22, 18) },
		{ "Building_W_3", Vector3.new(-52, 14, 18), Vector3.new(18, 28, 18) },
		{ "Building_E_3", Vector3.new(6, 10, 2), Vector3.new(18, 20, 18) },
		{ "Building_W_4", Vector3.new(-14, 13, 42), Vector3.new(18, 26, 16) },
		{ "Building_E_4", Vector3.new(42, 12, 18), Vector3.new(20, 24, 20) },
		{ "Building_W_5", Vector3.new(18, 12, 72), Vector3.new(20, 24, 18) },
		{ "Building_E_5", Vector3.new(74, 11, 44), Vector3.new(18, 22, 18) },
		{ "Building_W_6", Vector3.new(40, 16, 106), Vector3.new(22, 32, 18) },
		{ "Building_E_6", Vector3.new(92, 13, 86), Vector3.new(18, 26, 16) },
	}

	for _, building in ipairs(buildingPositions) do
		local part = createPart(
			buildingsFolder,
			building[1],
			Enum.PartType.Block,
			building[3],
			building[2],
			toColor3(config.buildingColor),
			Enum.Material.Brick
		)
		part.CastShadow = true
	end

	local lampPositions = {
		Vector3.new(-60, 5, -76),
		Vector3.new(-36, 5, -58),
		Vector3.new(-62, 5, -14),
		Vector3.new(-34, 5, -2),
		Vector3.new(-30, 5, 22),
		Vector3.new(-4, 5, 12),
		Vector3.new(2, 5, 48),
		Vector3.new(28, 5, 34),
		Vector3.new(30, 5, 74),
		Vector3.new(54, 5, 60),
		Vector3.new(56, 5, 100),
		Vector3.new(82, 5, 88),
	}

	for index, basePosition in ipairs(lampPositions) do
		local post = createPart(
			lampsFolder,
			string.format("LampPost_%02d", index),
			Enum.PartType.Cylinder,
			Vector3.new(1.2, 10, 1.2),
			basePosition,
			Color3.new(0.18, 0.18, 0.2),
			Enum.Material.Metal
		)
		post.Orientation = Vector3.new(0, 0, 90)

		createPart(
			lampsFolder,
			string.format("LampGlow_%02d", index),
			Enum.PartType.Ball,
			Vector3.new(2.2, 2.2, 2.2),
			basePosition + Vector3.new(0, 5.5, 0),
			toColor3(config.lampColor),
			Enum.Material.Neon
		)
	end

	createPart(
		zonesFolder,
		"SpawnZone",
		Enum.PartType.Block,
		Vector3.new(14, 1, 14),
		Vector3.new(-48, 0.55, -82),
		Color3.new(0.22, 0.58, 0.86),
		Enum.Material.Neon
	).Transparency = 0.35

	createPart(
		zonesFolder,
		"ExitZone",
		Enum.PartType.Block,
		Vector3.new(14, 1, 14),
		Vector3.new(66, 0.55, 102),
		Color3.new(0.82, 0.18, 0.18),
		Enum.Material.Neon
	).Transparency = 0.35

	local decorations = {
		{ "CrateCluster_1", Vector3.new(-68, 2, -42), Vector3.new(4, 4, 4), Color3.new(0.28, 0.2, 0.12), Enum.Material.WoodPlanks },
		{ "CrateCluster_2", Vector3.new(22, 2, 6), Vector3.new(4, 4, 4), Color3.new(0.28, 0.2, 0.12), Enum.Material.WoodPlanks },
		{ "CrateCluster_3", Vector3.new(74, 2, 66), Vector3.new(4, 4, 4), Color3.new(0.28, 0.2, 0.12), Enum.Material.WoodPlanks },
		{ "FogMarker_1", Vector3.new(-44, 2.5, -6), Vector3.new(6, 5, 6), Color3.new(0.75, 0.77, 0.8), Enum.Material.ForceField },
		{ "FogMarker_2", Vector3.new(18, 2.5, 52), Vector3.new(7, 5, 7), Color3.new(0.75, 0.77, 0.8), Enum.Material.ForceField },
		{ "FogMarker_3", Vector3.new(56, 2.5, 92), Vector3.new(6, 5, 6), Color3.new(0.75, 0.77, 0.8), Enum.Material.ForceField },
		{ "RitualStone_1", Vector3.new(-8, 1.5, 32), Vector3.new(5, 3, 5), Color3.new(0.2, 0.18, 0.2), Enum.Material.Slate },
		{ "SewerCover_1", Vector3.new(44, 0.6, 74), Vector3.new(4, 1, 4), Color3.new(0.12, 0.12, 0.12), Enum.Material.Metal },
	}

	for _, decoration in ipairs(decorations) do
		local part = createPart(
			decorationsFolder,
			decoration[1],
			Enum.PartType.Block,
			decoration[3],
			decoration[2],
			decoration[4],
			decoration[5]
		)
		if string.find(decoration[1], "FogMarker") then
			part.Transparency = 0.45
			part.CanCollide = false
		end
	end

	self.currentMapId = config.id
	print(string.format("[MapService] Built map: %s", config.displayName))
end

function MapService:Init()
	for _, sectionName in ipairs(MAP_CHILDREN) do
		self:GetSection(sectionName)
	end

	print("[MapService] Ready map folders inside Workspace/GameRuntime/Map")
end

return MapService
