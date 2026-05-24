local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))
local WaveConfig = require(Shared:WaitForChild("configs"):WaitForChild("WaveConfig"))

local EnemyService = require(script.Parent:WaitForChild("EnemyService"))
local PathService = require(script.Parent:WaitForChild("PathService"))

local WaveService = {
	currentWave = 0,
}

local function toVector3(values)
	return Vector3.new(values[1], values[2], values[3])
end

function WaveService:StartWave(waveNumber)
	local waveEntries = WaveConfig[waveNumber]
	if not waveEntries then
		warn(string.format("[WaveService] Unknown wave: %s", tostring(waveNumber)))
		return {}
	end

	self.currentWave = waveNumber

	local spawnedEnemies = {}
	local pathPoints = PathService:GetPathPoints()
	local startPosition = pathPoints[1] or toVector3(GameConfig.DefaultEnemySpawn)

	task.spawn(function()
		local offsetX = 0

		for _, entry in ipairs(waveEntries) do
			for _ = 1, entry.count do
				local spawnPosition = startPosition + Vector3.new(offsetX, 1.5, 0)
				local enemy = EnemyService:SpawnEnemy(entry.enemyType, spawnPosition)
				if enemy then
					table.insert(spawnedEnemies, enemy)
					EnemyService:StartEnemyMovement(enemy, pathPoints)
					print(string.format("[WaveService] Spawned moving enemy %s", enemy.Name))
				end

				offsetX += 4
				task.wait(entry.interval or 0.5)
			end
		end

		print(string.format("[WaveService] Test wave spawned %d enemies", #spawnedEnemies))
	end)

	print(string.format("[WaveService] Started wave %d with %d planned enemies", waveNumber, #spawnedEnemies))
	return spawnedEnemies
end

function WaveService:SpawnTestWave()
	print("[WaveService] Starting test wave ...")
	return self:StartWave(1)
end

function WaveService:Init()
	local count = 0
	for _ in pairs(WaveConfig) do
		count += 1
	end

	print(string.format("[WaveService] Loaded %d wave definitions", count))
end

return WaveService
