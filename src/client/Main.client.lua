local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

print(string.format("[Client boot] %s v%s", GameConfig.GameName, GameConfig.Version))

local function setupDemoCamera()
	print("[Client] Waiting for DemoPlayerSpawnRoot")

	local demoRoot = Workspace:WaitForChild("DemoPlayerSpawnRoot", 15)
	if not demoRoot then
		warn("[Client] DemoPlayerSpawnRoot not found")
		return
	end

	local demoCameraTarget = demoRoot:WaitForChild("DemoCameraTarget", 5)
	if not demoCameraTarget then
		warn("[Client] DemoCameraTarget not found")
		return
	end

	print("[Client] Demo camera target found")

	local camera = Workspace.CurrentCamera
	local cameraPosition = Vector3.new(-80, 90, -80)

	for i = 1, 20 do
		camera.CameraType = Enum.CameraType.Scriptable
		camera.CFrame = CFrame.new(cameraPosition, demoCameraTarget.Position)
		task.wait(0.5)
	end

	print("[Client] Demo camera activated")
end

task.spawn(setupDemoCamera)

