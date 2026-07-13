local Lighting = game:GetService("Lighting")
local Workspace = game:GetService("Workspace")

local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local HubService = {
	isBuilt = false,
	isHidden = false,
	isAuthored = false,
	startDefenseCallback = nil,
	promptConnected = false,
	center = Vector3.new(155, 2, -92),
}

local function emitHubMarker(message)
	print("[Hub] " .. message)
	warn("[Hub] " .. message)
end

local function clearChildren(instance)
	for _, child in ipairs(instance:GetChildren()) do
		child:Destroy()
	end
end

local function createPart(parent, name, shape, size, cframe, color, material, transparency)
	local part = Instance.new("Part")
	part.Name = name
	part.Shape = shape or Enum.PartType.Block
	part.Size = size
	part.CFrame = cframe
	part.Color = color
	part.Material = material or Enum.Material.SmoothPlastic
	part.Transparency = transparency or 0
	part.Anchored = true
	part.CanCollide = true
	part.TopSurface = Enum.SurfaceType.Smooth
	part.BottomSurface = Enum.SurfaceType.Smooth
	part.Parent = parent
	return part
end

local function createFolder(parent, name)
	local folder = Instance.new("Folder")
	folder.Name = name
	folder.Parent = parent
	return folder
end

local function addPointLight(parent, color, brightness, range)
	local light = Instance.new("PointLight")
	light.Color = color
	light.Brightness = brightness
	light.Range = range
	light.Shadows = true
	light.Parent = parent
	return light
end

local function addBillboardLabel(parent, text, offset, color)
	local gui = Instance.new("BillboardGui")
	gui.Name = "Label"
	gui.Size = UDim2.new(0, 220, 0, 44)
	gui.StudsOffset = offset or Vector3.new(0, 6, 0)
	gui.AlwaysOnTop = true
	gui.Parent = parent

	local label = Instance.new("TextLabel")
	label.Name = "Text"
	label.Size = UDim2.new(1, 0, 1, 0)
	label.BackgroundColor3 = Color3.fromRGB(19, 13, 10)
	label.BackgroundTransparency = 0.18
	label.BorderSizePixel = 0
	label.Text = text
	label.TextColor3 = color or Color3.fromRGB(244, 210, 128)
	label.TextScaled = true
	label.Font = Enum.Font.GothamBold
	label.Parent = gui
	return gui
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

local function applyHubAtmosphere()
	Lighting.FogColor = Color3.fromRGB(32, 38, 48)
	Lighting.FogStart = 4
	Lighting.FogEnd = 175
	Lighting.Ambient = Color3.fromRGB(36, 35, 46)
	Lighting.OutdoorAmbient = Color3.fromRGB(28, 27, 36)
	Lighting.Brightness = 1.2
	Lighting.ClockTime = 22
end

local function createRing(parent, name, center, radius, height, color, material, transparency)
	local ringFolder = createFolder(parent, name)
	for index = 1, 24 do
		local angle = (math.pi * 2 / 24) * index
		local position = center + Vector3.new(math.cos(angle) * radius, height, math.sin(angle) * radius)
		local segment = createPart(
			ringFolder,
			string.format("%s_Segment_%02d", name, index),
			Enum.PartType.Block,
			Vector3.new(5.2, 0.14, 0.55),
			CFrame.new(position) * CFrame.Angles(0, -angle, 0),
			color,
			material,
			transparency
		)
		segment.CanCollide = false
	end
	return ringFolder
end

local function createGasLamp(parent, name, position)
	local lamp = createFolder(parent, name)
	createPart(
		lamp,
		"Base",
		Enum.PartType.Cylinder,
		Vector3.new(3.8, 0.65, 3.8),
		CFrame.new(position + Vector3.new(0, 0.3, 0)) * CFrame.Angles(0, 0, math.rad(90)),
		Color3.fromRGB(86, 61, 34),
		Enum.Material.Metal,
		0
	)
	createPart(
		lamp,
		"Post",
		Enum.PartType.Cylinder,
		Vector3.new(0.9, 9.5, 0.9),
		CFrame.new(position + Vector3.new(0, 5.2, 0)),
		Color3.fromRGB(74, 55, 38),
		Enum.Material.Metal,
		0
	)
	createPart(
		lamp,
		"BrassCap",
		Enum.PartType.Cylinder,
		Vector3.new(2.6, 0.7, 2.6),
		CFrame.new(position + Vector3.new(0, 10.1, 0)) * CFrame.Angles(0, 0, math.rad(90)),
		Color3.fromRGB(176, 128, 54),
		Enum.Material.Metal,
		0
	)
	local glow = createPart(
		lamp,
		"GasGlow",
		Enum.PartType.Ball,
		Vector3.new(2.3, 2.3, 2.3),
		CFrame.new(position + Vector3.new(0, 9.1, 0)),
		Color3.fromRGB(255, 188, 82),
		Enum.Material.Neon,
		0.08
	)
	glow.CanCollide = false
	addPointLight(glow, Color3.fromRGB(255, 184, 92), 2.4, 28)
	return lamp
end

local function createPortal(parent, center)
	local portal = createFolder(parent, "CentralPortal")
	local brass = Color3.fromRGB(168, 118, 45)
	local teal = Color3.fromRGB(36, 222, 208)
	local violet = Color3.fromRGB(112, 62, 168)

	createPart(portal, "LeftPillar", Enum.PartType.Cylinder, Vector3.new(4.5, 18, 4.5), CFrame.new(center + Vector3.new(-12, 9, 0)), brass, Enum.Material.Metal, 0)
	createPart(portal, "RightPillar", Enum.PartType.Cylinder, Vector3.new(4.5, 18, 4.5), CFrame.new(center + Vector3.new(12, 9, 0)), brass, Enum.Material.Metal, 0)

	for index = 0, 12 do
		local angle = math.pi - (math.pi * index / 12)
		local position = center + Vector3.new(math.cos(angle) * 12, 18 + math.sin(angle) * 10, 0)
		local stone = createPart(
			portal,
			string.format("ArchStone_%02d", index),
			Enum.PartType.Ball,
			Vector3.new(4.8, 4.8, 4.8),
			CFrame.new(position),
			index % 2 == 0 and brass or Color3.fromRGB(55, 54, 68),
			index % 2 == 0 and Enum.Material.Metal or Enum.Material.Slate,
			0
		)
		stone.CanCollide = false
	end

	local surface = createPart(
		portal,
		"GlowingPortalSurface",
		Enum.PartType.Block,
		Vector3.new(18, 18, 0.4),
		CFrame.new(center + Vector3.new(0, 10, 0)),
		teal,
		Enum.Material.Neon,
		0.34
	)
	surface.CanCollide = false
	addPointLight(surface, teal, 3.2, 45)

	createRing(portal, "PortalRuneRing", center + Vector3.new(0, 10, -0.45), 11, 0, violet, Enum.Material.Neon, 0.12)
	for index = 1, 10 do
		local angle = (math.pi * 2 / 10) * index
		local rune = createPart(
			portal,
			string.format("FloatingRune_%02d", index),
			Enum.PartType.Block,
			Vector3.new(1.2, 1.2, 0.25),
			CFrame.new(center + Vector3.new(math.cos(angle) * 8, 10 + math.sin(angle) * 8, -0.7)) * CFrame.Angles(0, 0, angle),
			index % 2 == 0 and teal or Color3.fromRGB(232, 181, 83),
			Enum.Material.Neon,
			0.05
		)
		rune.CanCollide = false
	end

	local mist = Instance.new("ParticleEmitter")
	mist.Name = "SpiritMist"
	mist.Color = ColorSequence.new(teal, violet)
	mist.LightEmission = 0.45
	mist.Rate = 10
	mist.Lifetime = NumberRange.new(2.2, 4.2)
	mist.Speed = NumberRange.new(0.8, 2.1)
	mist.SpreadAngle = Vector2.new(18, 18)
	mist.Size = NumberSequence.new({
		NumberSequenceKeypoint.new(0, 1.2),
		NumberSequenceKeypoint.new(1, 4.5),
	})
	mist.Transparency = NumberSequence.new({
		NumberSequenceKeypoint.new(0, 0.25),
		NumberSequenceKeypoint.new(1, 1),
	})
	mist.Parent = surface

	addBillboardLabel(surface, "Врата обороны", Vector3.new(0, 16, 0), Color3.fromRGB(112, 255, 236))
	print("[Hub] Portal ready")
	warn("[Hub] Portal ready")
	return portal
end

local function createCommandTable(parent, center)
	local tableFolder = createFolder(parent, "CommandTable")
	createPart(tableFolder, "OakTableTop", Enum.PartType.Block, Vector3.new(20, 1.2, 12), CFrame.new(center + Vector3.new(0, 3.1, 0)), Color3.fromRGB(86, 48, 28), Enum.Material.WoodPlanks, 0)
	createPart(tableFolder, "ParchmentMap", Enum.PartType.Block, Vector3.new(15, 0.18, 8), CFrame.new(center + Vector3.new(0, 3.8, 0)), Color3.fromRGB(202, 172, 116), Enum.Material.Sand, 0)

	for index, offset in ipairs({
		Vector3.new(-7, 1.6, -4),
		Vector3.new(7, 1.6, -4),
		Vector3.new(-7, 1.6, 4),
		Vector3.new(7, 1.6, 4),
	}) do
		createPart(tableFolder, "BrassLeg_" .. index, Enum.PartType.Cylinder, Vector3.new(1.1, 3.2, 1.1), CFrame.new(center + offset), Color3.fromRGB(139, 96, 36), Enum.Material.Metal, 0)
	end

	for index = 1, 6 do
		local x = -6 + index * 2
		createPart(tableFolder, "DistrictLine_" .. index, Enum.PartType.Block, Vector3.new(0.22, 0.12, 6.5), CFrame.new(center + Vector3.new(x, 3.95, 0)) * CFrame.Angles(0, math.rad(18), 0), Color3.fromRGB(94, 68, 48), Enum.Material.Wood, 0)
	end

	for index, offset in ipairs({
		Vector3.new(-4, 4.45, -1.5),
		Vector3.new(0, 4.45, 1),
		Vector3.new(4, 4.45, -2),
	}) do
		local marker = createPart(tableFolder, "MiniTowerMarker_" .. index, Enum.PartType.Cylinder, Vector3.new(1.1, 1.2, 1.1), CFrame.new(center + offset), Color3.fromRGB(48, 126, 150), Enum.Material.Metal, 0)
		marker.CanCollide = false
	end

	local labelAnchor = createPart(tableFolder, "MapLabelAnchor", Enum.PartType.Block, Vector3.new(1, 1, 1), CFrame.new(center + Vector3.new(0, 6, 0)), Color3.fromRGB(202, 172, 116), Enum.Material.SmoothPlastic, 1)
	labelAnchor.CanCollide = false
	addBillboardLabel(labelAnchor, "Карта района", Vector3.new(0, 2, 0), Color3.fromRGB(244, 210, 128))
	return tableFolder
end

local function createTowerPreview(parent, center)
	local preview = createFolder(parent, "TowerPreview")
	createPart(preview, "PreviewPedestal", Enum.PartType.Cylinder, Vector3.new(12, 1, 12), CFrame.new(center + Vector3.new(0, 0.7, 0)) * CFrame.Angles(0, 0, math.rad(90)), Color3.fromRGB(38, 38, 45), Enum.Material.Slate, 0)
	createPart(preview, "LanternWardenPreviewBody", Enum.PartType.Cylinder, Vector3.new(4.5, 7, 4.5), CFrame.new(center + Vector3.new(0, 4.4, 0)), Color3.fromRGB(158, 115, 52), Enum.Material.Metal, 0)
	createPart(preview, "PreviewLens", Enum.PartType.Ball, Vector3.new(3.3, 3.3, 3.3), CFrame.new(center + Vector3.new(0, 8.3, 0)), Color3.fromRGB(65, 218, 232), Enum.Material.Neon, 0.1).CanCollide = false
	local ring = createPart(preview, "RangeGlow", Enum.PartType.Cylinder, Vector3.new(24, 0.12, 24), CFrame.new(center + Vector3.new(0, 0.9, 0)) * CFrame.Angles(0, 0, math.rad(90)), Color3.fromRGB(38, 170, 255), Enum.Material.Neon, 0.83)
	ring.CanCollide = false
	addPointLight(preview.PreviewLens, Color3.fromRGB(65, 218, 232), 1.8, 26)
	addBillboardLabel(preview.PreviewLens, "Агенты Завесы", Vector3.new(0, 6, 0), Color3.fromRGB(112, 255, 236))

	local sealed = createPart(preview, "SealedPrototype", Enum.PartType.Cylinder, Vector3.new(3.2, 5.5, 3.2), CFrame.new(center + Vector3.new(18, 3.4, 0)), Color3.fromRGB(70, 56, 86), Enum.Material.Marble, 0.15)
	createPart(preview, "SealedChain", Enum.PartType.Block, Vector3.new(7, 0.35, 0.5), CFrame.new(center + Vector3.new(18, 5.5, 0)) * CFrame.Angles(0, math.rad(45), 0), Color3.fromRGB(130, 105, 62), Enum.Material.Metal, 0)
	addBillboardLabel(sealed, "Запечатано", Vector3.new(0, 5, 0), Color3.fromRGB(201, 166, 255))
	return preview
end

function HubService:GetHubFolder()
	return RuntimeService:GetContainer("Hub")
end

function HubService:GetAuthoredHubFolder()
	local hub = Workspace:FindFirstChild("Hub")
	if hub and hub:IsA("Folder") then
		return hub
	end

	return nil
end

function HubService:GetHubSpawnCFrame()
	local authoredHub = self:GetAuthoredHubFolder()
	local spawnPart = findDescendantByName(authoredHub, "HubSpawn")
	if spawnPart and spawnPart:IsA("BasePart") then
		return CFrame.new(spawnPart.Position + Vector3.new(0, 4, 0))
	end

	return CFrame.new(self.center + Vector3.new(0, 6, 62))
end

function HubService:SetStartDefenseCallback(callback)
	self.startDefenseCallback = callback
end

function HubService:EnsureStartDefensePrompt(hubFolder)
	local promptPart = findDescendantByName(hubFolder, "PortalStartDefense")
	if not promptPart or not promptPart:IsA("BasePart") then
		promptPart = findDescendantByName(hubFolder, "PortalSurface")
	end

	if not promptPart or not promptPart:IsA("BasePart") then
		warn("[Hub] Start defense prompt anchor missing")
		return nil
	end

	local prompt = promptPart:FindFirstChild("StartDefensePrompt")
	if not prompt or not prompt:IsA("ProximityPrompt") then
		if prompt then
			prompt:Destroy()
		end

		prompt = Instance.new("ProximityPrompt")
		prompt.Name = "StartDefensePrompt"
		prompt.Parent = promptPart
	end

	prompt.ActionText = "Начать оборону"
	prompt.ObjectText = "Врата обороны"
	prompt.KeyboardKeyCode = Enum.KeyCode.E
	prompt.HoldDuration = 0.15
	prompt.MaxActivationDistance = 16
	prompt.RequiresLineOfSight = false
	prompt.Enabled = true

	if not self.promptConnected then
		self.promptConnected = true
		prompt.Triggered:Connect(function(player)
			emitHubMarker("Start defense clicked")
			if self.startDefenseCallback then
				self.startDefenseCallback(player)
			else
				warn("[Hub] Start defense callback is not registered")
			end
		end)
	end

	emitHubMarker("Start defense prompt ready")
	return prompt
end

function HubService:BuildHub()
	local authoredHub = self:GetAuthoredHubFolder()
	if authoredHub then
		self.isBuilt = true
		self.isHidden = false
		self.isAuthored = true
		applyHubAtmosphere()
		self:EnsureStartDefensePrompt(authoredHub)
		emitHubMarker("Authored hub found")
		emitHubMarker("Walkable hub ready")
		emitHubMarker("Defense portal ready")
		emitHubMarker("Hub ready")
		emitHubMarker("Portal ready")
		return authoredHub
	end

	local hubFolder = self:GetHubFolder()
	clearChildren(hubFolder)
	self.isHidden = false
	self.isAuthored = false

	applyHubAtmosphere()
	emitHubMarker("Generated fallback hub")

	local center = self.center
	local platform = createFolder(hubFolder, "OccultCommandPlatform")
	createPart(platform, "MainStoneDais", Enum.PartType.Cylinder, Vector3.new(92, 2.2, 92), CFrame.new(center) * CFrame.Angles(0, 0, math.rad(90)), Color3.fromRGB(34, 36, 44), Enum.Material.Slate, 0)
	createPart(platform, "RaisedBrassRim", Enum.PartType.Cylinder, Vector3.new(98, 0.55, 98), CFrame.new(center + Vector3.new(0, 1.25, 0)) * CFrame.Angles(0, 0, math.rad(90)), Color3.fromRGB(129, 91, 38), Enum.Material.Metal, 0.2).CanCollide = false

	for index = 1, 8 do
		local angle = (math.pi * 2 / 8) * index
		local position = center + Vector3.new(math.cos(angle) * 52, 0.1, math.sin(angle) * 52)
		createPart(platform, "OuterStone_" .. index, Enum.PartType.Block, Vector3.new(18, 1.4, 8), CFrame.new(position) * CFrame.Angles(0, -angle, 0), Color3.fromRGB(45, 43, 52), Enum.Material.Cobblestone, 0)
	end

	local ritual = createFolder(hubFolder, "RitualFloor")
	createRing(ritual, "OuterSeal", center, 34, 1.28, Color3.fromRGB(31, 202, 194), Enum.Material.Neon, 0.25)
	createRing(ritual, "MiddleGoldSeal", center, 23, 1.32, Color3.fromRGB(219, 164, 70), Enum.Material.Neon, 0.34)
	createRing(ritual, "InnerVioletSeal", center, 12, 1.36, Color3.fromRGB(126, 70, 194), Enum.Material.Neon, 0.32)
	createPart(ritual, "CentralSeal", Enum.PartType.Cylinder, Vector3.new(8, 0.16, 8), CFrame.new(center + Vector3.new(0, 1.45, 0)) * CFrame.Angles(0, 0, math.rad(90)), Color3.fromRGB(35, 231, 218), Enum.Material.Neon, 0.18).CanCollide = false

	for index = 1, 12 do
		local angle = (math.pi * 2 / 12) * index
		local stone = createPart(
			ritual,
			string.format("RuneStone_%02d", index),
			Enum.PartType.Block,
			Vector3.new(2.6, 0.55, 1.2),
			CFrame.new(center + Vector3.new(math.cos(angle) * 29, 1.65, math.sin(angle) * 29)) * CFrame.Angles(0, -angle, 0),
			index % 3 == 0 and Color3.fromRGB(125, 73, 184) or Color3.fromRGB(45, 222, 204),
			Enum.Material.Neon,
			0.08
		)
		stone.CanCollide = false
	end

	createPortal(hubFolder, center + Vector3.new(0, 1.2, -33))
	createCommandTable(hubFolder, center + Vector3.new(-28, 0, 18))
	createTowerPreview(hubFolder, center + Vector3.new(26, 0, 18))

	for index, position in ipairs({
		center + Vector3.new(-42, 0, -30),
		center + Vector3.new(42, 0, -30),
		center + Vector3.new(-44, 0, 34),
		center + Vector3.new(44, 0, 34),
		center + Vector3.new(0, 0, 46),
	}) do
		createGasLamp(hubFolder, "GasLamp_" .. index, position)
	end

	for index, offset in ipairs({
		Vector3.new(-52, 4, -8),
		Vector3.new(52, 4, -8),
		Vector3.new(-16, 3, 48),
		Vector3.new(16, 3, 48),
	}) do
		local candle = createPart(hubFolder, "Candle_" .. index, Enum.PartType.Cylinder, Vector3.new(1.1, 2.2, 1.1), CFrame.new(center + offset), Color3.fromRGB(210, 188, 141), Enum.Material.SmoothPlastic, 0)
		local flame = createPart(hubFolder, "CandleFlame_" .. index, Enum.PartType.Ball, Vector3.new(1, 1.4, 1), CFrame.new(center + offset + Vector3.new(0, 1.7, 0)), Color3.fromRGB(255, 159, 64), Enum.Material.Neon, 0.05)
		flame.CanCollide = false
		addPointLight(flame, Color3.fromRGB(255, 156, 70), 0.8, 12)
		candle.CanCollide = false
	end

	self.isBuilt = true
	self:EnsureStartDefensePrompt(hubFolder)
	emitHubMarker("Hub ready")
	return hubFolder
end

function HubService:HideHub()
	if self.isHidden then
		return
	end

	self.isHidden = true
	local hubFolder = self.isAuthored and self:GetAuthoredHubFolder() or self:GetHubFolder()
	if not hubFolder then
		return
	end
	for _, descendant in ipairs(hubFolder:GetDescendants()) do
		if descendant:IsA("BasePart") then
			descendant.Transparency = math.max(descendant.Transparency, 0.88)
			descendant.CanCollide = false
		elseif descendant:IsA("PointLight") then
			descendant.Enabled = false
		elseif descendant:IsA("ParticleEmitter") then
			descendant.Enabled = false
		elseif descendant:IsA("BillboardGui") then
			descendant.Enabled = false
		end
	end
end

function HubService:StartDefense(playerName)
	self:HideHub()
	print(string.format("[Hub] Defense started%s", playerName and (" by " .. playerName) or ""))
	warn("[Hub] Defense started")
end

return HubService
