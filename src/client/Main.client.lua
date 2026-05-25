local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Workspace = game:GetService("Workspace")
local Players = game:GetService("Players")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local PlaceTowerRequest = Remotes:WaitForChild("PlaceTowerRequest")
local SellTowerRequest = Remotes:WaitForChild("SellTowerRequest")
local TowerSelectedNotify = Remotes:WaitForChild("TowerSelectedNotify")

print(string.format("[Client boot] %s v%s", GameConfig.GameName, GameConfig.Version))
warn(string.format("[Client boot] %s v%s", GameConfig.GameName, GameConfig.Version))

local localPlayer = Players.LocalPlayer
local mouse = localPlayer:GetMouse()

local selectedPadName = nil
local selectedTowerRuntimeId = nil
local cameraFocus = Vector3.new(0, 5, 0)
local cameraZoom = 1
local cameraReady = false
local cameraRenderConnected = false
local cameraDragging = false
local lastDragPosition = nil

local DEFAULT_CAMERA_OFFSET = Vector3.new(-118, 122, -118)
local CAMERA_MIN_ZOOM = 0.65
local CAMERA_MAX_ZOOM = 1.55
local CAMERA_PAN_SPEED = 70
local CAMERA_DRAG_SPEED = 0.18

local function getRuntime()
	return Workspace:WaitForChild(GameConfig.RuntimeFolderName, 30)
end

local function getPathCenter()
	local gameRuntime = Workspace:FindFirstChild(GameConfig.RuntimeFolderName)
	local map = gameRuntime and gameRuntime:FindFirstChild("Map")
	local pathNodes = map and map:FindFirstChild("PathNodes")
	if not pathNodes then
		return Vector3.new(0, 0, 0)
	end

	local total = Vector3.zero
	local count = 0
	for _, child in ipairs(pathNodes:GetChildren()) do
		if child:IsA("BasePart") then
			total += child.Position
			count += 1
		end
	end

	if count == 0 then
		return Vector3.new(0, 0, 0)
	end

	return total / count
end

local function applyPlayableCamera()
	local camera = Workspace.CurrentCamera
	if not camera then
		return
	end

	camera.CameraType = Enum.CameraType.Scriptable
	camera.CFrame = CFrame.new(cameraFocus + (DEFAULT_CAMERA_OFFSET * cameraZoom), cameraFocus)
end

local function resetPlayableCamera()
	cameraFocus = getPathCenter() + Vector3.new(0, 5, 0)
	cameraZoom = 1
	cameraReady = true
	applyPlayableCamera()
end

local function panCamera(delta)
	if not cameraReady then
		return
	end

	cameraFocus += delta
	applyPlayableCamera()
end

local function setupPlayableCamera()
	for _ = 1, 20 do
		resetPlayableCamera()
		task.wait(0.25)
	end

	if not cameraRenderConnected then
		cameraRenderConnected = true
		RunService.RenderStepped:Connect(function(deltaTime)
			if not cameraReady then
				return
			end

			local pan = Vector3.zero
			if UserInputService:IsKeyDown(Enum.KeyCode.Up) then
				pan += Vector3.new(0, 0, -1)
			end
			if UserInputService:IsKeyDown(Enum.KeyCode.Down) then
				pan += Vector3.new(0, 0, 1)
			end
			if UserInputService:IsKeyDown(Enum.KeyCode.Left) then
				pan += Vector3.new(-1, 0, 0)
			end
			if UserInputService:IsKeyDown(Enum.KeyCode.Right) then
				pan += Vector3.new(1, 0, 0)
			end

			if pan.Magnitude > 0 then
				cameraFocus += pan.Unit * CAMERA_PAN_SPEED * deltaTime * cameraZoom
			end

			applyPlayableCamera()
		end)
	end

	print("[Playable] Camera ready")
	warn("[Playable] Camera ready")
end

local function createLabel(parent, name, position, text)
	local label = Instance.new("TextLabel")
	label.Name = name
	label.Size = UDim2.new(0, 300, 0, 38)
	label.Position = position
	label.BackgroundColor3 = Color3.fromRGB(10, 18, 26)
	label.BackgroundTransparency = 0.1
	label.BorderSizePixel = 0
	label.TextColor3 = Color3.fromRGB(245, 235, 190)
	label.TextScaled = true
	label.TextXAlignment = Enum.TextXAlignment.Left
	label.Font = Enum.Font.GothamBold
	label.Text = text
	label.Parent = parent
	return label
end

local function createButton(parent, name, position, size, text, bgColor)
	local btn = Instance.new("TextButton")
	btn.Name = name
	btn.Size = size
	btn.Position = position
	btn.BackgroundColor3 = bgColor
	btn.BorderSizePixel = 0
	btn.TextColor3 = Color3.fromRGB(255, 245, 210)
	btn.TextScaled = true
	btn.Font = Enum.Font.GothamBold
	btn.Text = text
	btn.Parent = parent
	return btn
end

local function findAncestorInFolder(part, folderName)
	local current = part
	while current do
		if current.Parent and current.Parent.Name == folderName and current:IsA("BasePart") then
			return current
		end
		current = current.Parent
	end
	return nil
end

local function findRuntimeTowerId(part)
	local current = part
	while current do
		local runtimeId = current:GetAttribute("RuntimeTowerId")
		if runtimeId then
			return runtimeId
		end
		current = current.Parent
	end
	return nil
end

local function findTowerRoot(runtimeId)
	local runtime = Workspace:FindFirstChild(GameConfig.RuntimeFolderName)
	local towersFolder = runtime and runtime:FindFirstChild("Towers")
	if not towersFolder then
		return nil
	end

	for _, child in ipairs(towersFolder:GetChildren()) do
		if child:GetAttribute("RuntimeTowerId") == runtimeId and child:GetAttribute("TowerType") then
			return child
		end
	end

	return nil
end

local function raycastScreenPosition(screenPosition)
	local camera = Workspace.CurrentCamera
	if not camera then
		return nil
	end

	local ray = camera:ViewportPointToRay(screenPosition.X, screenPosition.Y)
	local result = Workspace:Raycast(ray.Origin, ray.Direction * 1000)
	return result and result.Instance or nil
end

local function setupPlayableUi()
	local runtime = getRuntime()
	if not runtime then
		return
	end

	local playerGui = localPlayer:FindFirstChildOfClass("PlayerGui") or localPlayer:WaitForChild("PlayerGui", 10)
	if not playerGui then
		return
	end

	local existing = playerGui:FindFirstChild("PlayableHud")
	if existing then
		existing:Destroy()
	end

	local screenGui = Instance.new("ScreenGui")
	screenGui.Name = "PlayableHud"
	screenGui.ResetOnSpawn = false
	screenGui.IgnoreGuiInset = true
	screenGui.Parent = playerGui

	local moneyLabel = createLabel(screenGui, "MoneyLabel", UDim2.new(0, 24, 0, 24), "Деньги: ...")
	local waveLabel = createLabel(screenGui, "WaveLabel", UDim2.new(0, 24, 0, 68), "Волна: ...")
	local baseLabel = createLabel(screenGui, "BaseLabel", UDim2.new(0, 24, 0, 112), "База: ...")
	local stateLabel = createLabel(screenGui, "StateLabel", UDim2.new(0, 24, 0, 156), "Состояние: ...")

	local controls = Instance.new("TextLabel")
	controls.Name = "ControlsLabel"
	controls.Size = UDim2.new(0, 560, 0, 44)
	controls.Position = UDim2.new(0, 24, 1, -68)
	controls.BackgroundColor3 = Color3.fromRGB(13, 25, 20)
	controls.BackgroundTransparency = 0.08
	controls.BorderSizePixel = 0
	controls.TextColor3 = Color3.fromRGB(160, 245, 190)
	controls.TextScaled = true
	controls.Font = Enum.Font.GothamBold
	controls.Text = "Нажми синюю площадку. B - построить, S - продать, ESC - снять выбор, R - камера, колесо - зум."
	controls.Parent = screenGui

	-- Selection panel (right side)
	local selectionPanel = Instance.new("Frame")
	selectionPanel.Name = "SelectionPanel"
	selectionPanel.Size = UDim2.new(0, 280, 0, 260)
	selectionPanel.Position = UDim2.new(1, -304, 0, 24)
	selectionPanel.BackgroundColor3 = Color3.fromRGB(12, 20, 30)
	selectionPanel.BackgroundTransparency = 0.08
	selectionPanel.BorderSizePixel = 0
	selectionPanel.Visible = false
	selectionPanel.Parent = screenGui

	local selTitle = Instance.new("TextLabel")
	selTitle.Name = "SelectionTitle"
	selTitle.Size = UDim2.new(1, -16, 0, 32)
	selTitle.Position = UDim2.new(0, 8, 0, 8)
	selTitle.BackgroundTransparency = 1
	selTitle.TextColor3 = Color3.fromRGB(255, 240, 180)
	selTitle.TextScaled = true
	selTitle.TextXAlignment = Enum.TextXAlignment.Left
	selTitle.Font = Enum.Font.GothamBold
	selTitle.Text = ""
	selTitle.Parent = selectionPanel

	local selInfo = Instance.new("TextLabel")
	selInfo.Name = "SelectionInfo"
	selInfo.Size = UDim2.new(1, -16, 0, 48)
	selInfo.Position = UDim2.new(0, 8, 0, 44)
	selInfo.BackgroundTransparency = 1
	selInfo.TextColor3 = Color3.fromRGB(200, 210, 220)
	selInfo.TextScaled = true
	selInfo.TextXAlignment = Enum.TextXAlignment.Left
	selInfo.TextYAlignment = Enum.TextYAlignment.Top
	selInfo.Font = Enum.Font.Gotham
	selInfo.Text = ""
	selInfo.Parent = selectionPanel

	local buildBasicBtn = createButton(
		selectionPanel, "BuildBasicBtn",
		UDim2.new(0, 8, 0, 100),
		UDim2.new(1, -16, 0, 40),
		"Построить базовую башню ($100)",
		Color3.fromRGB(25, 92, 185)
	)
	buildBasicBtn.Visible = false

	local sellBtn = createButton(
		selectionPanel, "SellBtn",
		UDim2.new(0, 8, 0, 148),
		UDim2.new(1, -16, 0, 40),
		"Продать башню (50% возврат)",
		Color3.fromRGB(180, 60, 40)
	)
	sellBtn.Visible = false

	local upgradeBtn = createButton(
		selectionPanel, "UpgradeBtn",
		UDim2.new(0, 8, 0, 196),
		UDim2.new(1, -16, 0, 40),
		"Улучшение скоро",
		Color3.fromRGB(60, 60, 70)
	)
	upgradeBtn.Visible = false
	upgradeBtn.Active = false
	upgradeBtn.AutoButtonColor = false

	-- Quick build button (B key fallback)
	local quickBuildBtn = createButton(
		screenGui, "QuickBuildBtn",
		UDim2.new(1, -280, 1, -68),
		UDim2.new(0, 250, 0, 44),
		"Быстрая постройка (B)",
		Color3.fromRGB(25, 92, 185)
	)

	local selectedPadBox = Instance.new("SelectionBox")
	selectedPadBox.Name = "SelectedPadBox"
	selectedPadBox.Color3 = Color3.fromRGB(80, 210, 255)
	selectedPadBox.LineThickness = 0.08
	selectedPadBox.SurfaceTransparency = 0.85
	selectedPadBox.Parent = Workspace.CurrentCamera or Workspace

	local selectedTowerBox = Instance.new("SelectionBox")
	selectedTowerBox.Name = "SelectedTowerBox"
	selectedTowerBox.Color3 = Color3.fromRGB(255, 218, 90)
	selectedTowerBox.LineThickness = 0.08
	selectedTowerBox.SurfaceTransparency = 0.85
	selectedTowerBox.Parent = Workspace.CurrentCamera or Workspace

	local function updateHud()
		moneyLabel.Text = string.format("Деньги: $%s", tostring(runtime:GetAttribute("Money") or 0))
		waveLabel.Text = string.format("Волна: %s", tostring(runtime:GetAttribute("Wave") or 0))
		baseLabel.Text = string.format(
			"База: %s/%s",
			tostring(runtime:GetAttribute("BaseHealth") or 0),
			tostring(runtime:GetAttribute("MaxBaseHealth") or 0)
		)
		stateLabel.Text = string.format("Состояние: %s", tostring(runtime:GetAttribute("GameState") or "Ready"))
	end

	updateHud()
	runtime.AttributeChanged:Connect(updateHud)

	local function clearSelection()
		selectedPadName = nil
		selectedTowerRuntimeId = nil
		selectedPadBox.Adornee = nil
		selectedTowerBox.Adornee = nil
		selectionPanel.Visible = false
		buildBasicBtn.Visible = false
		sellBtn.Visible = false
		upgradeBtn.Visible = false
		selTitle.Text = ""
		selInfo.Text = ""
	end

	local function selectPad(buildPad)
		clearSelection()
		if not buildPad then
			return
		end
		local occupied = buildPad:GetAttribute("Occupied") or false
		if occupied then
			return
		end
		selectedPadName = buildPad.Name
		selectedPadBox.Adornee = buildPad
		selectionPanel.Visible = true
		selTitle.Text = "Площадка: " .. buildPad.Name
		selInfo.Text = "Выбери башню для постройки."
		buildBasicBtn.Visible = true
	end

	local function selectTower(runtimeId)
		clearSelection()
		if not runtimeId then
			return
		end
		local towerPart = findTowerRoot(runtimeId)
		if not towerPart then
			return
		end
		selectedTowerRuntimeId = runtimeId
		selectedTowerBox.Adornee = towerPart
		selectionPanel.Visible = true
		selTitle.Text = towerPart:GetAttribute("DisplayName") or towerPart.Name
		local cost = towerPart:GetAttribute("Cost") or 0
		local dmg = towerPart:GetAttribute("Damage") or 0
		local rng = towerPart:GetAttribute("Range") or 0
		selInfo.Text = string.format("Урон: %d  Радиус: %d  Цена: $%d", dmg, rng, cost)
		sellBtn.Visible = true
		upgradeBtn.Visible = true
		TowerSelectedNotify:FireServer(runtimeId)
	end

	buildBasicBtn.MouseButton1Click:Connect(function()
		if selectedPadName then
			PlaceTowerRequest:FireServer("BasicTower", selectedPadName)
			clearSelection()
		end
	end)

	sellBtn.MouseButton1Click:Connect(function()
		if selectedTowerRuntimeId then
			SellTowerRequest:FireServer(selectedTowerRuntimeId)
			clearSelection()
		end
	end)

	quickBuildBtn.MouseButton1Click:Connect(function()
		PlaceTowerRequest:FireServer("BasicTower", nil)
	end)

	local function buildSelectedOrQuick()
		PlaceTowerRequest:FireServer("BasicTower", selectedPadName)
		if selectedPadName then
			clearSelection()
		end
	end

	local function sellSelectedTower()
		if selectedTowerRuntimeId then
			SellTowerRequest:FireServer(selectedTowerRuntimeId)
			clearSelection()
		end
	end

	local function selectTarget(target)
		if not target then
			clearSelection()
			return
		end

		local buildPad = findAncestorInFolder(target, "BuildPads")
		if buildPad then
			selectPad(buildPad)
			return
		end

		local runtimeId = findRuntimeTowerId(target)
		if runtimeId then
			selectTower(runtimeId)
			return
		end

		clearSelection()
	end

	UserInputService.InputBegan:Connect(function(input, gameProcessed)
		if gameProcessed then
			return
		end

		if input.KeyCode == Enum.KeyCode.B then
			buildSelectedOrQuick()
		elseif input.KeyCode == Enum.KeyCode.S then
			sellSelectedTower()
		elseif input.KeyCode == Enum.KeyCode.Escape then
			clearSelection()
		elseif input.KeyCode == Enum.KeyCode.R then
			resetPlayableCamera()
		elseif input.UserInputType == Enum.UserInputType.MouseButton2 then
			cameraDragging = true
			lastDragPosition = input.Position
		end
	end)

	UserInputService.InputChanged:Connect(function(input, gameProcessed)
		if gameProcessed then
			return
		end

		if input.UserInputType == Enum.UserInputType.MouseWheel then
			cameraZoom = math.clamp(cameraZoom - (input.Position.Z * 0.08), CAMERA_MIN_ZOOM, CAMERA_MAX_ZOOM)
			applyPlayableCamera()
		elseif cameraDragging and input.UserInputType == Enum.UserInputType.MouseMovement and lastDragPosition then
			local delta = input.Position - lastDragPosition
			lastDragPosition = input.Position
			panCamera(Vector3.new(delta.X, 0, delta.Y) * CAMERA_DRAG_SPEED * cameraZoom)
		end
	end)

	UserInputService.InputEnded:Connect(function(input)
		if input.UserInputType == Enum.UserInputType.MouseButton2 then
			cameraDragging = false
			lastDragPosition = nil
		end
	end)

	UserInputService.TouchTap:Connect(function(touchPositions, gameProcessed)
		if gameProcessed then
			return
		end

		local firstTouch = touchPositions and touchPositions[1]
		selectTarget(firstTouch and raycastScreenPosition(firstTouch) or nil)
	end)

	mouse.Button1Down:Connect(function()
		selectTarget(mouse.Target)
	end)

	print("[Playable] UI ready")
	warn("[Playable] UI ready")
end

task.spawn(setupPlayableCamera)
task.spawn(setupPlayableUi)
