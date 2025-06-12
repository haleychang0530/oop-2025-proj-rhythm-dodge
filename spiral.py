import pygame
import math

class SpiralPath:
    def __init__(self, center, start_radius, thickness, angle_speed=0.1, radius_speed=0.8, color=(0, 0, 0)):
        self.center = center
        self.radius = start_radius
        self.thickness = thickness
        self.angle = 0
        self.angle_speed = angle_speed
        self.radius_speed = radius_speed
        self.color = color
        self.outer_points = []
        self.inner_points = []
        self.rotation_offset = 0  # additional rotation in radians

    def update(self):
        if self.radius > self.thickness:
            angle_rad = self.angle
            # Outer point
            x1 = self.center[0] + self.radius * math.cos(angle_rad)
            y1 = self.center[1] + self.radius * math.sin(angle_rad)
            self.outer_points.append((x1, y1))
            
            # Inner point
            inner_r = self.radius - self.thickness
            x2 = self.center[0] + inner_r * math.cos(angle_rad)
            y2 = self.center[1] + inner_r * math.sin(angle_rad)
            self.inner_points.append((x2, y2))

            # Spiral parameters
            self.angle += self.angle_speed
            self.radius -= self.radius_speed

    def rotate(self, delta_angle_rad):
        """Add a rotation offset (in radians)."""
        self.rotation_offset += delta_angle_rad

    def _apply_rotation(self, point):
        """Rotate a single point around center."""
        cx, cy = self.center
        x, y = point
        dx, dy = x - cx, y - cy
        r = math.hypot(dx, dy)
        theta = math.atan2(dy, dx) + self.rotation_offset
        return (cx + r * math.cos(theta), cy + r * math.sin(theta))

    def draw(self, surface):
        if len(self.outer_points) > 1:
            # Apply rotation to all points
            rotated_outer = [self._apply_rotation(p) for p in self.outer_points]
            rotated_inner = [self._apply_rotation(p) for p in reversed(self.inner_points)]
            full_path = rotated_outer + rotated_inner
            pygame.draw.polygon(surface, self.color, full_path)

    def is_finished(self):
        return self.radius <= self.thickness



pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create spiral object
spiral = SpiralPath(center=(400, 300), start_radius=400, thickness=20, color=(255, 0, 100))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Background

    if not spiral.is_finished():
        spiral.update()
    else:
        spiral.rotate(0.01)  # slowly rotates every frame

    spiral.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

