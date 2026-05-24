local TowerConfig = {
	BasicTower = {
		displayName = "Basic Tower",
		cost = 100,
		damage = 20,
		range = 42,
		fireRate = 1.0,
		color = { 0.2, 0.55, 1.0 },
		size = { 4, 10, 4 },
	},
	SniperTower = {
		displayName = "Sniper Tower",
		cost = 180,
		damage = 45,
		range = 40,
		fireRate = 0.5,
		color = { 0.6, 0.4, 1.0 },
		size = { 3, 14, 3 },
	},
	SplashTower = {
		displayName = "Splash Tower",
		cost = 220,
		damage = 30,
		range = 18,
		fireRate = 0.8,
		color = { 1.0, 0.45, 0.15 },
		size = { 5, 8, 5 },
	},
}

return TowerConfig
