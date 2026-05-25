local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))
local WaveConfig = require(Shared:WaitForChild("configs"):WaitForChild("WaveConfig"))

local EnemyService = require(script.Parent:WaitForChild("EnemyService"))
local PathService = require(script.Parent:WaitForChild("PathService"))

local WaveService = {
	currentWave = 0,
	isWaveRunning = false,
	wavesCompleted = 0,
	intermissionSeconds = 5,
}

local function toVector3(values)
	return Vector3.new(values[1], values[2], values[3])
end

function WaveService:StartWave(waveNumber)
	if self.isWaveRunning then
		warn(string.format("[WaveService] Cannot start wave %s while wave %s is still running", tostring(waveNumber), tostring(self.currentWave)))
		return false
	end

	local waveEntries = WaveConfig[waveNumber]
	if not waveEntries then
		warn(string.format("[WaveService] Unknown wave: %s", tostring(waveNumber)))
		return false
	end

	self.currentWave = waveNumber
	self.isWaveRunning = true
	print("[WaveService] Starting wave " .. waveNumber)
	warn("[WaveService] Runtime marker: Starting wave " .. waveNumber)

	local spawnedEnemies = {}
	local pathPoints = PathService:GetPathPoints()
	local startPosition = pathPoints[1] or toVector3(GameConfig.DefaultEnemySpawn)

	local offsetX = 0

	for _, entry in ipairs(waveEntries) do
		for _ = 1, entry.count do
			local spawnPosition = startPosition + Vector3.new(offsetX, 1.5, 0)
			local enemy = EnemyService:SpawnEnemy(entry.enemyType, spawnPosition)
			if enemy then
				table.insert(spawnedEnemies, enemy)
				EnemyService:StartEnemyMovement(enemy, pathPoints)
				print(string.format("[WaveService] Spawned moving enemy %s", enemy.Name))
				warn(string.format("[WaveService] Runtime marker: Spawned moving enemy %s", enemy.Name))
			end

			offsetX += 4
			task.wait(entry.interval or 0.5)
		end
	end

	print(string.format("[WaveService] Wave %d spawned %d enemies", waveNumber, #spawnedEnemies))
	warn(string.format("[WaveService] Runtime marker: Wave %d spawned %d enemies", waveNumber, #spawnedEnemies))
	self:WaitForWaveClear()
	self.isWaveRunning = false
	self.wavesCompleted += 1
	print("[WaveService] Wave completed " .. waveNumber)
	warn("[WaveService] Runtime marker: Wave completed " .. waveNumber)
	return true
end

function WaveService:SpawnTestWave()
	print("[WaveService] Starting test wave ...")
	return self:StartWave(1)
end

function WaveService:GetCurrentWave()
	return self.currentWave
end

function WaveService:IsWaveRunning()
	return self.isWaveRunning
end

function WaveService:GetWaveStatus()
	return {
		currentWave = self.currentWave,
		isWaveRunning = self.isWaveRunning,
		wavesCompleted = self.wavesCompleted,
		intermissionSeconds = self.intermissionSeconds,
		aliveEnemies = self:CountAliveEnemies(),
	}
end

function WaveService:CountAliveEnemies()
	local aliveCount = 0

	for _ in pairs(EnemyService:GetActiveEnemies()) do
		aliveCount += 1
	end

	return aliveCount
end

function WaveService:WaitForWaveClear()
	local timeoutAt = os.clock() + 120

	while self:CountAliveEnemies() > 0 do
		if os.clock() >= timeoutAt then
			warn("[WaveService] Wave clear wait timed out")
			return false
		end

		task.wait(0.5)
	end

	return true
end

function WaveService:StartNextWave()
	return self:StartWave(self.currentWave + 1)
end

function WaveService:StartWaveLoop(maxWaves)
	task.spawn(function()
		local totalWaves = math.min(maxWaves or #WaveConfig, #WaveConfig)

		for waveNumber = 1, totalWaves do
			local started = self:StartWave(waveNumber)
			if not started then
				break
			end

			if waveNumber < totalWaves then
				task.wait(self.intermissionSeconds)
			end
		end

		print("[WaveService] Wave loop completed")
		warn("[WaveService] Runtime marker: Wave loop completed")
	end)
end

function WaveService:Init()
	local count = 0
	for _ in pairs(WaveConfig) do
		count += 1
	end

	print(string.format("[WaveService] Loaded %d wave definitions", count))
	warn(string.format("[WaveService] Runtime marker: Loaded %d wave definitions", count))
end

return WaveService
