local WaveConfig = {
	[1] = {
		{ enemyType = "Basic", count = 4, interval = 1.0 },
	},
	[2] = {
		{ enemyType = "Basic", count = 5, interval = 0.9 },
		{ enemyType = "Fast", count = 2, interval = 0.8 },
	},
	[3] = {
		{ enemyType = "Basic", count = 6, interval = 0.8 },
		{ enemyType = "Fast", count = 4, interval = 0.7 },
	},
	[4] = {
		{ enemyType = "Tank", count = 2, interval = 1.2 },
		{ enemyType = "Fast", count = 5, interval = 0.7 },
	},
	[5] = {
		{ enemyType = "Basic", count = 5, interval = 0.8 },
		{ enemyType = "Fast", count = 5, interval = 0.6 },
		{ enemyType = "Tank", count = 3, interval = 1.4 },
	},
}

return WaveConfig
