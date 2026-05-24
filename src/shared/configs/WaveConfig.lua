local WaveConfig = {
	[1] = {
		{ enemyType = "Basic", count = 4, interval = 1.0 },
	},
	[2] = {
		{ enemyType = "Basic", count = 6, interval = 0.9 },
	},
	[3] = {
		{ enemyType = "Fast", count = 5, interval = 0.7 },
	},
	[4] = {
		{ enemyType = "Basic", count = 4, interval = 0.8 },
		{ enemyType = "Fast", count = 3, interval = 0.7 },
	},
	[5] = {
		{ enemyType = "Tank", count = 2, interval = 1.4 },
		{ enemyType = "Fast", count = 3, interval = 0.7 },
	},
}

return WaveConfig
