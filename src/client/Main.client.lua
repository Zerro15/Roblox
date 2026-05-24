local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

print(string.format("[Client boot] %s v%s", GameConfig.GameName, GameConfig.Version))

local function setupDemoCamera()
	print("[Client] Waiting for GameRuntime/Map...")

	local gameRuntime = Workspace:WaitForChild("GameRuntime", 30)
	if not gameRuntime then
		print("[Client] Demo camera failed: GameRuntime not found")
		return
	end

	local mapFolder = gameRuntime:WaitForChild("Map", 30)
	if not mapFolder then
		print("[Client] Demo camera failed: Map not found")
		return
	end

	local groundOrPathNodes = mapFolder:WaitForChild("Ground", 5) or mapFolder:WaitForChild("PathNodes", 5)
	if not groundOrPathNodes then
		print("[Client] Demo camera warning: Ground/PathNodes not found, proceeding anyway")
	end

	local camera = Workspace.CurrentCamera
	local mapCenter = Vector3.new(0, 10, 0)
	local cameraPosition = Vector3.new(-70, 85, -70)

	camera.CameraType = Enum.CameraType.Scriptable
	camera.CFrame = CFrame.new(cameraPosition, mapCenter)
	print("[Client] Demo camera activated")

	task.wait(2)
	camera.CFrame = CFrame.new(cameraPosition, mapCenter)

	task.wait(3)
	camera.CFrame = CFrame.new(cameraPosition, mapCenter)

	task.wait(5)
	camera.CFrame = CFrame.new(cameraPosition, mapCenter)
end

task.spawn(setupDemoCamera)
