local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local PlayerSpawnService = {}

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

local function createPart(parent, name, size, position, transparency, material)
	local part = Instance.new("Part")
	part.Name = name
	part.Shape = Enum.PartType.Block
	part.Size = size
	part.Position = position
	part.Anchored = true
	part.CanCollide = true
	part.TopSurface = Enum.SurfaceType.Smooth
	part.BottomSurface = Enum.SurfaceType.Smooth
	part.Transparency = transparency or 0
	part.Material = material or Enum.Material.SmoothPlastic
	part.Parent = parent
	return part
end

function PlayerSpawnService:Init()
	local runtimeFolder = RuntimeService:GetOrCreateRuntimeFolder()
	local playerSpawnFolder = ensureFolder(runtimeFolder, "PlayerSpawn")

	local spawnPlatformPosition = Vector3.new(0, 8, 0)

	local demoSpawnPlatform = playerSpawnFolder:FindFirstChild("DemoSpawnPlatform")
	if not demoSpawnPlatform then
		demoSpawnPlatform = createPart(
			playerSpawnFolder,
			"DemoSpawnPlatform",
			Vector3.new(40, 2, 40),
			spawnPlatformPosition,
			0.35,
			Enum.Material.SmoothPlastic
		)
	end

	local spawnLocationPosition = spawnPlatformPosition + Vector3.new(0, 3, 0)
	local demoSpawnLocation = playerSpawnFolder:FindFirstChild("DemoSpawnLocation")
	if not demoSpawnLocation then
		demoSpawnLocation = Instance.new("SpawnLocation")
		demoSpawnLocation.Name = "DemoSpawnLocation"
		demoSpawnLocation.Shape = Enum.PartType.Block
		demoSpawnLocation.Size = Vector3.new(12, 1, 12)
		demoSpawnLocation.Position = spawnLocationPosition
		demoSpawnLocation.Anchored = true
		demoSpawnLocation.CanCollide = true
		demoSpawnLocation.TopSurface = Enum.SurfaceType.Smooth
		demoSpawnLocation.BottomSurface = Enum.SurfaceType.Smooth
		demoSpawnLocation.Transparency = 0.3
		demoSpawnLocation.Material = Enum.Material.SmoothPlastic
		demoSpawnLocation.Neutral = true
		demoSpawnLocation.AllowTeamChangeOnTouch = false
		demoSpawnLocation.CanCollide = true
		demoSpawnLocation.Parent = playerSpawnFolder
	end

	local safetyFloor = playerSpawnFolder:FindFirstChild("DemoSafetyFloor")
	if not safetyFloor then
		safetyFloor = createPart(
			playerSpawnFolder,
			"DemoSafetyFloor",
			Vector3.new(300, 2, 300),
			Vector3.new(0, -10, 0),
			1,
			Enum.Material.SmoothPlastic
		)
	end

	print("[PlayerSpawnService] Demo spawn ready")
end

return PlayerSpawnService
