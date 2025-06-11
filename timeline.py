import obstacle
import effect
from particle import Particle
from obstacle import CannonObstacle, LaserObstacle, LaserCircleObstacle, CircleObstacle, SinCircleObstacle, FollowCircleObstacle, GearObstacle, SinGearObstacle, FollowGearObstacle

def update_obstacles(screen,screen_rect,particles,events, player, obstacles, spawned, time_now,prev_obs):
    # 障礙物生成（依時間）
    # prev_obstacles
    
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
    # 更新障礙物
    all_pass = True
    for o in obstacles:
        if isinstance(o, CannonObstacle):
            o.update(screen_rect, player)
        else:
            o.update()    
        if ( isinstance(o, LaserObstacle) or isinstance(o, LaserCircleObstacle)) and o.expired:
            obstacles.remove(o)

        if not screen.get_rect().colliderect(o.rect):
            obstacles.remove(o)

        # 檢查玩家與障礙物碰撞
        if player.alive and not player.dashing:
            if ( isinstance(o,CircleObstacle) or isinstance(o, SinCircleObstacle) or isinstance(o, FollowCircleObstacle) or isinstance(o, LaserCircleObstacle) 
                or isinstance(o, GearObstacle) or isinstance(o, SinGearObstacle) or isinstance(o, FollowGearObstacle) ):
                # 圓形障礙物的碰撞檢查
                if o.collide(player):
                    if isinstance(o, LaserCircleObstacle) and not o.activated:
                        continue  # 預熱中的雷射不造成傷害
                    if prev_obs != o and player.blood > 0:
                        all_pass=False
                        player.blood = player.blood - 1
                        prev_obs = o
                        effect.hurt(o)
                        o.shake()
                    for _ in range(30):
                        particles.append(Particle(player.rect.centerx, player.rect.centery))
            elif player.rect.colliderect(o.rect):
                if ( isinstance(o, LaserObstacle) and not o.activated or (isinstance(o, CannonObstacle) and o.expired)):
                    continue  # 預熱中的雷射不造成傷害
                if prev_obs != o and player.blood > 0:
                    all_pass=False
                    player.blood = player.blood - 1
                    prev_obs = o
                    effect.hurt(o)
                    o.shake()
                for _ in range(30):
                    particles.append(Particle(player.rect.centerx, player.rect.centery))
            
    if all_pass:
        prev_obs = None
    return prev_obs