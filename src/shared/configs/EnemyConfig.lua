local EnemyConfig = {
	Basic = {
		displayName = "Basic Drone",
		maxHealth = 100,
		speed = 8,
		reward = 15,
		color = { 0.35, 0.8, 0.35 },
		size = { 4, 4, 4 },
	},
	Fast = {
		displayName = "Fast Runner",
		maxHealth = 65,
		speed = 13,
		reward = 18,
		color = { 1, 0.85, 0.2 },
		size = { 3, 3, 3 },
	},
	Tank = {
		displayName = "Tank Core",
		maxHealth = 250,
		speed = 5,
		reward = 35,
		color = { 0.8, 0.3, 0.3 },
		size = { 6, 6, 6 },
	},
}

return EnemyConfig
