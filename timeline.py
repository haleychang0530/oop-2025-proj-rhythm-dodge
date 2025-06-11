import obstacle

def update_obstacles(events, player, obstacles, spawned, time_now):
    # 障礙物生成（依時間）
    for i, evt in enumerate(events):
        if time_now >= evt["time"]*1.02564 and i not in spawned: # 1.02564 是時間縮放因子 for bpm 234
            if evt.get("type") == "sin":
                obs = obstacle.SinObstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"], amplitude=evt.get("amplitude", 50), frequency=evt.get("frequency", 0.01))
            elif evt.get("type") == "follow":
                obs = obstacle.FollowObstacle(evt["x"], evt["y"], evt["w"], evt["h"],player , speed=evt.get("speed", 15))
            elif evt.get("type") == "laser":
                obs = obstacle.LaserObstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"], charge_time=evt.get("charge", 1000)*1.02564)
            
            # === 圓形類型 ===
            elif evt.get("type") == "circle":
                obs = obstacle.CircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"]
                )

            elif evt.get("type") == "circle_sin":
                obs = obstacle.SinCircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"],
                    amplitude=evt.get("amplitude", 50),
                    frequency=evt.get("frequency", 0.01)
                )

            elif evt.get("type") == "circle_follow":
                obs = obstacle.FollowCircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    player, speed=evt.get("speed", 15)
                )

            elif evt.get("type") == "circle_laser":
                obs = obstacle.LaserCircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"],
                    charge_time=evt.get("charge", 1000) * 1.02564
                )
            elif evt.get("type") == "gear":
                obs = obstacle.GearObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"],
                    teeth=evt.get("teeth", 8),
                    rotation_speed=evt.get("rot_speed", 2)
            )
            elif evt.get("type") == "gear_follow":
                obs = obstacle.FollowGearObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    player, speed=evt.get("speed", 15),
                    teeth=evt.get("teeth", 8),
                    rotation_speed=evt.get("rot_speed", 2)
                )
            elif evt.get("type") == "gear_sin":
                obs = obstacle.SinGearObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"],
                    amplitude=evt.get("amplitude", 50),
                    frequency=evt.get("frequency", 0.01),
                    teeth=evt.get("teeth", 8),
                    rotation_speed=evt.get("rot_speed", 2)
                )
            elif evt.get("type") == "cannon":
                obs = obstacle.CannonObstacle(
                    evt["x"], evt["y"], evt["w"], evt["h"],
                    evt["vx"], evt["vy"]
                )
            else:
                obs = obstacle.Obstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"])
            obstacles.append(obs)
            spawned.add(i)
    return obstacles, spawned