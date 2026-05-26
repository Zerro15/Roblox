local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local PlayerSpawnService = {}
PlayerSpawnService.spawnCFrame = nil
PlayerSpawnService.demoSpectatorMode = false

local function createPart(parent, name, size, position, color, transparency, material, canCollide)
	local part = Instance.new("Part")
	part.Name = name
	part.Shape = Enum.PartType.Block
	part.Size = size
	part.Position = position
	part.Color = color
	part.Anchored = true
	part.CanCollide = canCollide ~= false
	part.TopSurface = Enum.SurfaceType.Smooth
	part.BottomSurface = Enum.SurfaceType.Smooth
	part.Transparency = transparency or 0
	part.Material = material or Enum.Material.SmoothPlastic
	part.Parent = parent
	return part
end

local function makeSpawnHelperNonObstructive(part, size, position, canCollide)
	if not part then
		return
	end

	part.Size = size
	part.Position = position
	part.Transparency = 1
	part.CanCollide = canCollide == true
	part.CanQuery = false
	part.CanTouch = false
	part.CastShadow = false
end

local function findDescendantByName(root, name)
	if not root then
		return nil
	end

	if root.Name == name then
		return root
	end

	for _, descendant in ipairs(root:GetDescendants()) do
		if descendant.Name == name then
			return descendant
		end
	end

	return nil
end

local function getHubSpawnCFrame()
	local hub = Workspace:FindFirstChild("Hub")
	local hubSpawn = findDescendantByName(hub, "HubSpawn")
	if hubSpawn and hubSpawn:IsA("BasePart") then
		return CFrame.new(hubSpawn.Position + Vector3.new(0, 4, 0))
	end

	return CFrame.new(Vector3.new(155, 5, -29))
end

function PlayerSpawnService:MoveCharacterToSpawn(character)
	if not character or not self.spawnCFrame then
		return
	end

	local humanoidRootPart = character:FindFirstChild("HumanoidRootPart")
	if not humanoidRootPart then
		humanoidRootPart = character:WaitForChild("HumanoidRootPart", 10)
	end

	if not humanoidRootPart then
		warn("[PlayerSpawnService] HumanoidRootPart not found")
		return
	end

	local humanoid = character:FindFirstChildOfClass("Humanoid")

	if humanoid then
		humanoid.Health = humanoid.MaxHealth
		humanoid.PlatformStand = false
		humanoid.Sit = false
		humanoid.WalkSpeed = 16
		humanoid.JumpPower = 50
	end

	for i = 1, 5 do
		character:PivotTo(self.spawnCFrame)
		humanoidRootPart.AssemblyLinearVelocity = Vector3.zero
		humanoidRootPart.AssemblyAngularVelocity = Vector3.zero
		task.wait(0.15)
	end

	local forceField = character:FindFirstChildOfClass("ForceField")
	if not forceField then
		forceField = Instance.new("ForceField")
		forceField.Visible = false
		forceField.Parent = character
	end

	print("[PlayerSpawnService] Character moved to hub spawn")
end

function PlayerSpawnService:HideCharacter(character)
	if not character then
		return
	end

	local humanoidRootPart = character:FindFirstChild("HumanoidRootPart")
	local humanoid = character:FindFirstChildOfClass("Humanoid")

	if humanoidRootPart then
		character:PivotTo(CFrame.new(0, -500, 0))
		humanoidRootPart.Anchored = true
		humanoidRootPart.AssemblyLinearVelocity = Vector3.zero
		humanoidRootPart.AssemblyAngularVelocity = Vector3.zero
	end

	if humanoid then
		humanoid.WalkSpeed = 0
		humanoid.JumpPower = 0
		humanoid.Health = humanoid.MaxHealth
		humanoid.PlatformStand = true
		humanoid.Sit = false
	end

	for _, descendant in ipairs(character:GetDescendants()) do
		if descendant:IsA("BasePart") then
			descendant.Transparency = 1
			descendant.CanCollide = false
			descendant.AssemblyLinearVelocity = Vector3.zero
			descendant.AssemblyAngularVelocity = Vector3.zero
		elseif descendant:IsA("Decal") then
			descendant.Transparency = 1
		end
	end

	print("[PlayerSpawnService] Character hidden for demo spectator mode")
end

function PlayerSpawnService:SetupPlayer(player)
	player.CharacterAdded:Connect(function(character)
		task.wait(0.5)
		if self.demoSpectatorMode then
			self:HideCharacter(character)
			print(string.format("[PlayerSpawnService] Player configured as demo spectator: %s", player.Name))
			return
		end

		self:MoveCharacterToSpawn(character)

		task.spawn(function()
			while character.Parent do
				local hrp = character:FindFirstChild("HumanoidRootPart")
				local humanoid = character:FindFirstChildOfClass("Humanoid")

				if hrp then
					local y = hrp.Position.Y
					if y < -80 or y > 260 then
						self:MoveCharacterToSpawn(character)
						warn("[PlayerSpawnService] Character unsafe position; reset to hub spawn")
					end
				end

				if humanoid and humanoid.Health <= 0 then
					warn("[PlayerSpawnService] Character died; reloading")
					player:LoadCharacter()
				end

				task.wait(0.25)
			end
		end)
	end)

	if self.demoSpectatorMode then
		if player.Character then
			task.defer(function()
				self:HideCharacter(player.Character)
			end)
		end

		print(string.format("[PlayerSpawnService] Player configured as demo spectator: %s", player.Name))
		return
	end

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
	print("[PlayerSpawnService] Playable player spawn initializing")
	Players.CharacterAutoLoads = true

	local demoRoot = Workspace:FindFirstChild("DemoPlayerSpawnRoot")
	if not demoRoot then
		demoRoot = Instance.new("Folder")
		demoRoot.Name = "DemoPlayerSpawnRoot"
		demoRoot.Parent = Workspace
	end

	local demoSpawnPlatform = demoRoot:FindFirstChild("DemoSpawnPlatform")
	if not demoSpawnPlatform then
		demoSpawnPlatform = createPart(
			demoRoot,
			"DemoSpawnPlatform",
			Vector3.new(8, 1, 8),
			Vector3.new(0, -420, 0),
			Color3.fromRGB(80, 120, 90),
			1,
			Enum.Material.Concrete,
			false
		)
	end
	makeSpawnHelperNonObstructive(demoSpawnPlatform, Vector3.new(8, 1, 8), Vector3.new(0, -420, 0), false)

	local demoSpawnLocation = demoRoot:FindFirstChild("DemoSpawnLocation")
	if not demoSpawnLocation then
		demoSpawnLocation = Instance.new("SpawnLocation")
		demoSpawnLocation.Name = "DemoSpawnLocation"
		demoSpawnLocation.Shape = Enum.PartType.Block
		demoSpawnLocation.Size = Vector3.new(6, 1, 6)
		demoSpawnLocation.Position = Vector3.new(0, -414, 0)
		demoSpawnLocation.Color = Color3.fromRGB(60, 180, 80)
		demoSpawnLocation.Anchored = true
		demoSpawnLocation.CanCollide = false
		demoSpawnLocation.TopSurface = Enum.SurfaceType.Smooth
		demoSpawnLocation.BottomSurface = Enum.SurfaceType.Smooth
		demoSpawnLocation.Transparency = 1
		demoSpawnLocation.Material = Enum.Material.SmoothPlastic
		demoSpawnLocation.Neutral = true
		demoSpawnLocation.AllowTeamChangeOnTouch = false
		demoSpawnLocation.Enabled = true
		demoSpawnLocation.Duration = 0
		demoSpawnLocation.Parent = demoRoot
	end
	makeSpawnHelperNonObstructive(demoSpawnLocation, Vector3.new(6, 1, 6), Vector3.new(0, -414, 0), false)
	demoSpawnLocation.Enabled = true

	local demoSafetyFloor = demoRoot:FindFirstChild("DemoSafetyFloor")
	if not demoSafetyFloor then
		demoSafetyFloor = createPart(
			demoRoot,
			"DemoSafetyFloor",
			Vector3.new(80, 2, 80),
			Vector3.new(0, -540, 0),
			Color3.fromRGB(120, 40, 40),
			1,
			Enum.Material.SmoothPlastic,
			true
		)
	end
	makeSpawnHelperNonObstructive(demoSafetyFloor, Vector3.new(80, 2, 80), Vector3.new(0, -540, 0), true)

	local demoCameraTarget = demoRoot:FindFirstChild("DemoCameraTarget")
	if not demoCameraTarget then
		demoCameraTarget = createPart(
			demoRoot,
			"DemoCameraTarget",
			Vector3.new(2, 2, 2),
			Vector3.new(0, -408, 0),
			Color3.fromRGB(255, 220, 80),
			1,
			Enum.Material.SmoothPlastic,
			false
		)
	end
	makeSpawnHelperNonObstructive(demoCameraTarget, Vector3.new(2, 2, 2), Vector3.new(0, -408, 0), false)

	local demoDebugPole = demoRoot:FindFirstChild("DemoDebugPole")
	if not demoDebugPole then
		demoDebugPole = createPart(
			demoRoot,
			"DemoDebugPole",
			Vector3.new(1, 1, 1),
			Vector3.new(0, -406, 0),
			Color3.fromRGB(255, 0, 0),
			1,
			Enum.Material.SmoothPlastic,
			false
		)
	end
	makeSpawnHelperNonObstructive(demoDebugPole, Vector3.new(1, 1, 1), Vector3.new(0, -406, 0), false)

	self.spawnCFrame = getHubSpawnCFrame()

	local hubSpawnLocation = demoRoot:FindFirstChild("HubSpawnLocation")
	if not hubSpawnLocation then
		hubSpawnLocation = Instance.new("SpawnLocation")
		hubSpawnLocation.Name = "HubSpawnLocation"
		hubSpawnLocation.Shape = Enum.PartType.Block
		hubSpawnLocation.Anchored = true
		hubSpawnLocation.TopSurface = Enum.SurfaceType.Smooth
		hubSpawnLocation.BottomSurface = Enum.SurfaceType.Smooth
		hubSpawnLocation.Neutral = true
		hubSpawnLocation.AllowTeamChangeOnTouch = false
		hubSpawnLocation.Duration = 0
		hubSpawnLocation.Parent = demoRoot
	end
	makeSpawnHelperNonObstructive(hubSpawnLocation, Vector3.new(4, 0.4, 4), self.spawnCFrame.Position - Vector3.new(0, 3.5, 0), false)
	hubSpawnLocation.Enabled = true

	for _, player in ipairs(Players:GetPlayers()) do
		self:SetupPlayer(player)
	end

	Players.PlayerAdded:Connect(function(player)
		self:SetupPlayer(player)
	end)

	print("[PlayerSpawnService] Hub walking spawn ready")
end

return PlayerSpawnService
