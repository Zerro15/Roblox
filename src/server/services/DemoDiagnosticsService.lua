local Workspace = game:GetService("Workspace")

local DemoDiagnosticsService = {}

local BEACONS = {
	ServerBootBeacon = {
		position = Vector3.new(-30, 45, 0),
		color = Color3.fromRGB(50, 140, 255),
	},
	PlayerSpawnBeacon = {
		position = Vector3.new(-15, 45, 0),
		color = Color3.fromRGB(60, 220, 90),
	},
	MapBuildBeacon = {
		position = Vector3.new(0, 45, 0),
		color = Color3.fromRGB(255, 230, 70),
	},
	WaveLoopBeacon = {
		position = Vector3.new(15, 45, 0),
		color = Color3.fromRGB(255, 70, 70),
	},
}

function DemoDiagnosticsService:GetRoot()
	local root = Workspace:FindFirstChild("DemoDiagnostics")
	if not root then
		root = Instance.new("Folder")
		root.Name = "DemoDiagnostics"
		root.Parent = Workspace
	end

	return root
end

function DemoDiagnosticsService:CreateBeacon(name, config)
	local root = self:GetRoot()
	local beacon = root:FindFirstChild(name)
	if not beacon then
		beacon = Instance.new("Part")
		beacon.Name = name
		beacon.Shape = Enum.PartType.Block
		beacon.Size = Vector3.new(8, 8, 8)
		beacon.Position = config.position
		beacon.Color = config.color
		beacon.Material = Enum.Material.Neon
		beacon.Anchored = true
		beacon.CanCollide = false
		beacon.Transparency = 0.65
		beacon.TopSurface = Enum.SurfaceType.Smooth
		beacon.BottomSurface = Enum.SurfaceType.Smooth
		beacon.Parent = root
	end

	beacon:SetAttribute("Marked", false)
	beacon:SetAttribute("StatusText", "created")
	return beacon
end

function DemoDiagnosticsService:Init()
	warn("[DemoDiagnostics] Init")

	for name, config in pairs(BEACONS) do
		self:CreateBeacon(name, config)
	end

	Workspace:SetAttribute("DemoDiagnosticsReady", true)
end

function DemoDiagnosticsService:Mark(name)
	local root = self:GetRoot()
	local beacon = root:FindFirstChild(name)
	if not beacon then
		local config = BEACONS[name]
		if not config then
			warn("[DemoDiagnostics] Unknown beacon: " .. tostring(name))
			return
		end
		beacon = self:CreateBeacon(name, config)
	end

	beacon.Transparency = 0
	beacon:SetAttribute("Marked", true)
	beacon:SetAttribute("MarkedAt", os.time())
	warn("[DemoDiagnostics] " .. name .. " marked")
end

function DemoDiagnosticsService:SetStatus(name, statusText)
	local root = self:GetRoot()
	local beacon = root:FindFirstChild(name)
	if beacon then
		beacon:SetAttribute("StatusText", statusText)
	end
end

return DemoDiagnosticsService
