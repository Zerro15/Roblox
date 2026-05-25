local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local PlayerSpawnService = {}
PlayerSpawnService.spawnCFrame = nil

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

function PlayerSpawnService:MoveCharacterToSpawn(character)
	if not character or not self.spawnCFrame then
		return
	end

	local humanoidRootPart = character:FindFirstChild("HumanoidRootPart") or character:FindFirstChildOfClass("BasePart")
	local humanoid = character:FindFirstChildOfClass("Humanoid")

	if humanoidRootPart then
		character:PivotTo(self.spawnCFrame)
		humanoidRootPart.AssemblyLinearVelocity = Vector3.zero
		humanoidRootPart.AssemblyAngularVelocity = Vector3.zero
	end

	if humanoid then
		humanoid.Health = humanoid.MaxHealth
	end

	print("[PlayerSpawnService] Character moved to demo spawn")
end

function PlayerSpawnService:SetupPlayer(player)
	player.CharacterAdded:Connect(function(character)
		task.wait(0.2)
		self:MoveCharacterToSpawn(character)

		task.spawn(function()
			while character.Parent do
				local hrp = character:FindFirstChild("HumanoidRootPart")
				if hrp and hrp.Position.Y < -20 then
					self:MoveCharacterToSpawn(character)
					warn("[PlayerSpawnService] Character fell below safety floor; moved back to spawn")
				end
				task.wait(1)
			end
		end)
	end)

	if player.Character then
		task.defer(function()
			self:MoveCharacterToSpawn(player.Character)
		end)
	else
		task.defer(function()
			player:LoadCharacter()
		end)
	end

	print(string.format("[PlayerSpawnService] Player setup: %s", player.Name))
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

	self.spawnCFrame = CFrame.new(spawnLocationPosition + Vector3.new(0, 5, 0))

	for _, player in ipairs(Players:GetPlayers()) do
		self:SetupPlayer(player)
	end

	Players.PlayerAdded:Connect(function(player)
		self:SetupPlayer(player)
	end)

	print("[PlayerSpawnService] Demo spawn ready")
end

return PlayerSpawnService

