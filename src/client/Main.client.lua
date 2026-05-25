local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

print(string.format("[Client boot] %s v%s", GameConfig.GameName, GameConfig.Version))

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
	local demoRoot = Workspace:FindFirstChild("DemoPlayerSpawnRoot")
	local demoCameraTarget = demoRoot and demoRoot:FindFirstChild("DemoCameraTarget")
	if demoCameraTarget and demoCameraTarget:IsA("BasePart") then
		print("[Client] Demo camera target found")
		return demoCameraTarget.Position
	end

	local pathCenter = getPathCenter()
	if pathCenter then
		return pathCenter
	end

	print("[Client] Demo camera fallback lookAt used")
	return Vector3.new(0, 35, 0)
end

local function setupDemoCamera()
	print("[Client] Demo spectator camera starting")

	local camera = Workspace.CurrentCamera
	local cameraPosition = Vector3.new(-100, 110, -100)

	for _ = 1, 40 do
		local lookAt = resolveLookAt()
		camera.CameraType = Enum.CameraType.Scriptable
		camera.CFrame = CFrame.new(cameraPosition, lookAt)
		task.wait(0.5)
	end

	print("[Client] Demo spectator camera activated")
end

task.spawn(setupDemoCamera)
