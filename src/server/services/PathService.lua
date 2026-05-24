local RuntimeService = require(script.Parent:WaitForChild("RuntimeService"))

local PathService = {
	currentPath = {},
}

local PATH_POINTS = {
	Vector3.new(-48, 1.5, -82),
	Vector3.new(-48, 1.5, -46),
	Vector3.new(-38, 1.5, -10),
	Vector3.new(-10, 1.5, 14),
	Vector3.new(22, 1.5, 40),
	Vector3.new(48, 1.5, 68),
	Vector3.new(66, 1.5, 102),
}

local function ensurePathFolder()
	local mapFolder = RuntimeService:GetContainer("Map")
	local existing = mapFolder:FindFirstChild("PathNodes")
	if existing and existing:IsA("Folder") then
		return existing
	end

	local folder = Instance.new("Folder")
	folder.Name = "PathNodes"
	folder.Parent = mapFolder
	return folder
end

function PathService:GetPathFolder()
	return ensurePathFolder()
end

function PathService:ClearPath()
	local pathFolder = self:GetPathFolder()
	for _, child in ipairs(pathFolder:GetChildren()) do
		child:Destroy()
	end
	self.currentPath = {}
end

function PathService:BuildBacklundPath()
	self:ClearPath()

	local pathFolder = self:GetPathFolder()
	local builtPath = {}

	for index, point in ipairs(PATH_POINTS) do
		local node = Instance.new("Part")
		node.Name = string.format("Node_%d", index)
		node.Size = Vector3.new(2.4, 2.4, 2.4)
		node.Position = point
		node.Anchored = true
		node.CanCollide = false
		node.Material = Enum.Material.Neon
		node.Color = Color3.new(0.15, 0.92, 1.0)
		node.Transparency = 0.2
		node.TopSurface = Enum.SurfaceType.Smooth
		node.BottomSurface = Enum.SurfaceType.Smooth
		node:SetAttribute("PathIndex", index)
		node.Parent = pathFolder

		table.insert(builtPath, point)
	end

	self.currentPath = builtPath
	print(string.format("[PathService] Built Backlund path with %d nodes", #builtPath))
	return builtPath
end

function PathService:GetPathPoints()
	if #self.currentPath > 0 then
		return self.currentPath
	end

	local points = {}
	local nodes = {}
	for _, child in ipairs(self:GetPathFolder():GetChildren()) do
		if child:IsA("BasePart") then
			table.insert(nodes, child)
		end
	end

	table.sort(nodes, function(a, b)
		return (a:GetAttribute("PathIndex") or 0) < (b:GetAttribute("PathIndex") or 0)
	end)

	for _, node in ipairs(nodes) do
		table.insert(points, node.Position)
	end

	self.currentPath = points
	return points
end

function PathService:Init()
	self:GetPathFolder()
	print("[PathService] Ready at Workspace/GameRuntime/Map/PathNodes")
end

return PathService
