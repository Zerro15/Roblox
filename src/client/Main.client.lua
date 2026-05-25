local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")
local Players = game:GetService("Players")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

print(string.format("[Client boot] %s v%s", GameConfig.GameName, GameConfig.Version))
warn(string.format("[Client boot] %s v%s", GameConfig.GameName, GameConfig.Version))

local function createDemoStatusGui()
	local localPlayer = Players.LocalPlayer
	if not localPlayer then
		return
	end

	local playerGui = localPlayer:FindFirstChildOfClass("PlayerGui") or localPlayer:WaitForChild("PlayerGui", 10)
	if not playerGui then
		return
	end

	local existing = playerGui:FindFirstChild("DemoStatusGui")
	if existing then
		existing:Destroy()
	end

	local screenGui = Instance.new("ScreenGui")
	screenGui.Name = "DemoStatusGui"
	screenGui.ResetOnSpawn = false
	screenGui.IgnoreGuiInset = true
	screenGui.Parent = playerGui

	local label = Instance.new("TextLabel")
	label.Name = "DemoStatusLabel"
	label.Size = UDim2.new(0, 420, 0, 56)
	label.Position = UDim2.new(0, 24, 0, 24)
	label.BackgroundColor3 = Color3.fromRGB(10, 20, 30)
	label.BackgroundTransparency = 0.15
	label.BorderSizePixel = 0
	label.Text = "DEMO SPECTATOR CAMERA ACTIVE"
	label.TextColor3 = Color3.fromRGB(255, 230, 120)
	label.TextScaled = true
	label.Font = Enum.Font.GothamBold
	label.Parent = screenGui
end

local function getPathCenter()
	local gameRuntime = Workspace:FindFirstChild("GameRuntime")
	local map = gameRuntime and gameRuntime:FindFirstChild("Map")
	local pathNodes = map and map:FindFirstChild("PathNodes")
	if not pathNodes then
		return nil
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
		return nil
	end

	return total / count
end

local function resolveLookAt()
	local pathCenter = getPathCenter()
	if pathCenter then
		warn("[Client] Demo camera path center found")
		return pathCenter + Vector3.new(0, 10, 0)
	end

	local demoRoot = Workspace:FindFirstChild("DemoPlayerSpawnRoot")
	local demoCameraTarget = demoRoot and demoRoot:FindFirstChild("DemoCameraTarget")
	if demoCameraTarget and demoCameraTarget:IsA("BasePart") then
		warn("[Client] Demo camera target found")
		return demoCameraTarget.Position
	end

	warn("[Client] Demo camera fallback lookAt used")
	return Vector3.new(0, 35, 0)
end

local function setupDemoCamera()
	warn("[Client] Demo spectator camera starting")

	local camera = Workspace.CurrentCamera
	local cameraPosition = Vector3.new(-120, 130, -120)

	for _ = 1, 40 do
		local lookAt = resolveLookAt()
		camera.CameraType = Enum.CameraType.Scriptable
		camera.CFrame = CFrame.new(cameraPosition, lookAt)
		task.wait(0.5)
	end

	createDemoStatusGui()
	warn("[Client] Demo spectator camera activated")
end

task.spawn(setupDemoCamera)
