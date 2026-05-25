local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

local RuntimeService = {}

local RUNTIME_CHILDREN = {
	"Enemies",
	"Towers",
	"Projectiles",
	"Map",
	"Debug",
}

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

function RuntimeService:GetRuntimeFolder()
	return Workspace:FindFirstChild(GameConfig.RuntimeFolderName)
end

function RuntimeService:GetOrCreateRuntimeFolder()
	local runtimeFolder = self:GetRuntimeFolder()
	if runtimeFolder then
		return runtimeFolder
	end

	runtimeFolder = Instance.new("Folder")
	runtimeFolder.Name = GameConfig.RuntimeFolderName
	runtimeFolder.Parent = Workspace
	return runtimeFolder
end

function RuntimeService:GetContainer(name)
	local runtimeFolder = self:GetOrCreateRuntimeFolder()
	return ensureFolder(runtimeFolder, name)
end

function RuntimeService:GetRemoteEvent(name)
	local remotesFolder = ensureFolder(ReplicatedStorage, "Remotes")
	local existing = remotesFolder:FindFirstChild(name)
	if existing and existing:IsA("RemoteEvent") then
		return existing
	end

	if existing then
		existing:Destroy()
	end

	local remote = Instance.new("RemoteEvent")
	remote.Name = name
	remote.Parent = remotesFolder
	return remote
end

function RuntimeService:Init()
	local runtimeFolder = self:GetOrCreateRuntimeFolder()

	for _, childName in ipairs(RUNTIME_CHILDREN) do
		ensureFolder(runtimeFolder, childName)
	end

	self:GetRemoteEvent("PlaceTowerRequest")
	self:GetRemoteEvent("SellTowerRequest")
	self:GetRemoteEvent("TowerSelectedNotify")
	print(string.format("[RuntimeService] Ready at Workspace/%s", runtimeFolder.Name))
end

return RuntimeService
