local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local GameConfig = require(Shared:WaitForChild("GameConfig"))

-- UI bootstrap will be added later after the core gameplay loop is in place.
print(string.format("[Client boot] %s v%s", GameConfig.GameName, GameConfig.Version))
