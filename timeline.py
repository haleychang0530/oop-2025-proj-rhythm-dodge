from obstacle import *
from particle import Particle
import effect

def update_obstacles(screen,screen_rect,particles,events, player, obstacles, spawned, time_now,prev_obs,bpm_scale,time_skip):
    # 障礙物生成（依時間）
    for i, evt in enumerate(events):
        if evt["time"] + 50 > time_now + time_skip * bpm_scale * 1000 >= evt["time"] and i not in spawned:
            if evt.get("type") == "sin":
                obs = SinObstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"], amplitude=evt.get("amplitude", 50), frequency=evt.get("frequency", 0.01))
            elif evt.get("type") == "follow":
                obs = FollowObstacle(evt["x"], evt["y"], evt["w"], evt["h"],player , speed=evt.get("speed", 15))
            elif evt.get("type") == "laser":
                obs = LaserObstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"], charge_time=evt.get("charge", 1000)/ bpm_scale) 
            
            # === 圓形類型 ===
            elif evt.get("type") == "circle":
                obs = CircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"]
                )

            elif evt.get("type") == "circle_sin":
                obs = SinCircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"],
                    amplitude=evt.get("amplitude", 50),
                    frequency=evt.get("frequency", 0.01)
                )

            elif evt.get("type") == "circle_follow":
                obs = FollowCircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    player, speed=evt.get("speed", 15)
                )

            elif evt.get("type") == "circle_laser":
                obs = LaserCircleObstacle(
                    evt["x"], evt["y"], evt.get("radius",25),
                    evt["vx"], evt["vy"],
                    charge_time= evt.get("charge", 1000) / bpm_scale,
                    sound = evt.get("sound", True)
                )
            elif evt.get("type") == "gear":
                obs = GearObstacle(
                    evt["x"], evt["y"], evt.get("radius",40),
                    evt["vx"], evt["vy"],
                    teeth=evt.get("teeth", 8),
                    rotation_speed=evt.get("rot_speed", 2)
            )
            elif evt.get("type") == "gear_follow":
                obs = FollowGearObstacle(
                    evt["x"], evt["y"], evt.get("radius",40),
                    player, speed=evt.get("speed", 15),
                    teeth=evt.get("teeth", 8),
                    rotation_speed=evt.get("rot_speed", 2)
                )
            elif evt.get("type") == "gear_sin":
                obs = SinGearObstacle(
                    evt["x"], evt["y"], evt.get("radius",40),
                    evt["vx"], evt["vy"],
                    amplitude=evt.get("amplitude", 50),
                    frequency=evt.get("frequency", 0.01),
                    teeth=evt.get("teeth", 8),
                    rotation_speed=evt.get("rot_speed", 2)
                )
            elif evt.get("type") == "cannon":
                obs = CannonObstacle(
                    evt["x"], evt["y"], evt["w"], evt["h"],
                    evt["vx"], evt["vy"], evt.get("amplitude", 300)
                    ,evt.get("wave", 2040), evt.get("bar", 51)
                    
                )
            elif evt.get("type") == "ring":
                obs = RingObstacle(
                evt["x"],evt["y"],
                evt.get("radius", 700),        
                evt.get("duration", 400),                
                evt.get("thickness", 40),
                evt.get("vx", 0), evt.get("vy", 0), evt.get("fade", 1)
                )
            else:
                obs = Obstacle(evt["x"], evt["y"], evt["w"], evt["h"], evt["vx"], evt["vy"])
            obstacles.append(obs)
            spawned.add(i)
    
    # 更新障礙物
    all_pass = True

    for o in obstacles:
        # 如果有碰撞，讓全部障礙物震動
        if not all_pass:
            o.shake(20,10)  # (10,10)是(震動時長,震動幅度)
            ###################
        if isinstance(o, CannonObstacle):
            o.update(screen_rect, player)
        else:
            o.update()    
        if ( isinstance(o, LaserObstacle) or isinstance(o, LaserCircleObstacle) or isinstance(o, RingObstacle)) and o.expired:
            obstacles.remove(o)
        if not screen.get_rect().colliderect(o.rect):
            obstacles.remove(o)
        # 檢查玩家與障礙物碰撞
        if player.alive and not player.dashing:
            if ( isinstance(o,CircleObstacle) or isinstance(o, SinCircleObstacle) or isinstance(o, FollowCircleObstacle) or isinstance(o, LaserCircleObstacle) 
                or isinstance(o, GearObstacle) or isinstance(o, SinGearObstacle) or isinstance(o, FollowGearObstacle) or isinstance(o, RingObstacle)):
                # 圓形障礙物的碰撞檢查
                if o.collide(player):
                    if isinstance(o, LaserCircleObstacle) and not o.activated:
                        continue  # 預熱中的雷射不造成傷害
                    if o not in prev_obs and player.blood > 0:
                        all_pass=False
                        damage = effect.hurt(o)
                        o.shake(20,10)
                        player.blood = player.blood - damage
                        prev_obs.append(o)
                    elif player.blood > 0 and isinstance(o, LaserCircleObstacle):
                        all_pass=False
                        o.shake(20,10)
                        player.blood = player.blood - effect.hurt(o)
                    for _ in range(30):
                        particles.append(Particle(player.rect.centerx, player.rect.centery))
            elif player.rect.colliderect(o.rect):
                if ( isinstance(o, LaserObstacle) and not o.activated or (isinstance(o, CannonObstacle) and o.expired)):
                    continue  # 預熱中的雷射不造成傷害
                if o not in prev_obs and player.blood > 0:
                    all_pass=False
                    o.shake(20,10)
                    player.blood = player.blood - effect.hurt(o)
                    prev_obs.append(o)
                elif player.blood > 0 and isinstance(o, LaserObstacle):
                    all_pass=False
                    o.shake(20,10)
                    player.blood = player.blood - effect.hurt(o)
                for _ in range(30):
                    particles.append(Particle(player.rect.centerx, player.rect.centery))

 
    return prev_obs