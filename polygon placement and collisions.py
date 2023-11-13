import pygame
import math
from random import randint, uniform

# Constants and Configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
COLLISION_DAMPING = 1  # Energy loss per collision

class Polygon:
    def __init__(self, screen_width, screen_height, existing_polygons):
        self.sides = randint(3, 8)
        self.pos = [randint(0, screen_width), randint(0, screen_height)]
        self.velocity = [uniform(-1, 1), uniform(-1, 1)]
        self.rotation = uniform(0, 360)
        self.size = self.sides  # Using sides as the mass

        # Ensure no initial overlap with existing polygons
        while self.check_initial_collision(existing_polygons):
            self.pos = [randint(0, screen_width), randint(0, screen_height)]

    def update(self, screen_width, screen_height, polygons):
        # Update position based on velocity
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        # Wrap around the screen
        self.pos[0] %= screen_width
        self.pos[1] %= screen_height

        # Check for collisions
        self.handle_collisions(polygons)

    def handle_collisions(self, polygons):
        for other_polygon in polygons:
            if other_polygon != self:
                if self.check_collision(other_polygon):
                    self.resolve_collision(other_polygon)

    def check_collision(self, other_polygon):
        # Check if any vertex of self is inside the other polygon
        for point in self.calculate_polygon_points():
            if point_in_polygon(point, other_polygon.calculate_polygon_points()):
                return True

        # Check if any vertex of other_polygon is inside self
        for point in other_polygon.calculate_polygon_points():
            if point_in_polygon(point, self.calculate_polygon_points()):
                return True

        return False

    def resolve_collision(self, other_polygon):
        # Calculate the collision normal
        collision_normal = [other_polygon.pos[0] - self.pos[0], other_polygon.pos[1] - self.pos[1]]
        magnitude = math.sqrt(collision_normal[0] ** 2 + collision_normal[1] ** 2)
        collision_normal = [collision_normal[0] / magnitude, collision_normal[1] / magnitude]

        # Calculate relative velocity
        relative_velocity = [
            other_polygon.velocity[0] - self.velocity[0],
            other_polygon.velocity[1] - self.velocity[1],
        ]

        # Calculate relative velocity along the collision normal
        vel_along_normal = (
            relative_velocity[0] * collision_normal[0] +
            relative_velocity[1] * collision_normal[1]
        )

        # If objects are moving away from each other, do not resolve the collision
        if vel_along_normal > 0:
            return

        # Calculate impulse (change in velocity) with restitution
        restitution = 0.9
        impulse = -(1 + restitution) * vel_along_normal / (1/self.size + 1/other_polygon.size)

        # Apply impulse to update velocities with restitution
        self.velocity[0] -= (impulse / self.size) * collision_normal[0]
        self.velocity[1] -= (impulse / self.size) * collision_normal[1]
        other_polygon.velocity[0] += (impulse / other_polygon.size) * collision_normal[0]
        other_polygon.velocity[1] += (impulse / other_polygon.size) * collision_normal[1]

        # Move the polygons away along the collision normal with restitution
        move_distance = 0.5

        self.pos[0] -= collision_normal[0] * move_distance
        self.pos[1] -= collision_normal[1] * move_distance
        other_polygon.pos[0] += collision_normal[0] * move_distance
        other_polygon.pos[1] += collision_normal[1] * move_distance

        # If the objects are still overlapping, move them
        if self.check_collision(other_polygon):
            separation_distance = 0.1
            self.pos[0] -= collision_normal[0] * separation_distance
            self.pos[1] -= collision_normal[1] * separation_distance
            other_polygon.pos[0] += collision_normal[0] * separation_distance
            other_polygon.pos[1] += collision_normal[1] * separation_distance

    def check_initial_collision(self, existing_polygons):
        # Check if any vertex of self is inside any existing polygon
        for other_polygon in existing_polygons:
            if self.check_collision(other_polygon):
                return True
        return False

    def draw(self, screen):
        # Draw the polygon based on its position, sides, and rotation
        points = self.calculate_polygon_points()
        pygame.draw.lines(screen, WHITE, True, points)

    def calculate_polygon_points(self):
        angle = 360 / self.sides
        # Scale factor to ensure equal side lengths for all polygons
        scale_factor = 20 * 2 / (2 * math.sin(math.radians(angle / 2)))
        points = []
        for i in range(self.sides):
            x = self.pos[0] + scale_factor * math.cos(math.radians(angle * i + self.rotation))
            y = self.pos[1] + scale_factor * math.sin(math.radians(angle * i + self.rotation))
            points.append((x, y))
        return points

def point_in_polygon(point, polygon_points):
    x, y = point
    n = len(polygon_points)
    inside = False

    p1x, p1y = polygon_points[0]
    for i in range(n + 1):
        p2x, p2y = polygon_points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Random Polygons Generator")

    polygons = []
    for _ in range(20):
        new_polygon = Polygon(SCREEN_WIDTH, SCREEN_HEIGHT, polygons)
        polygons.append(new_polygon)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update polygons
        for polygon in polygons:
            polygon.update(SCREEN_WIDTH, SCREEN_HEIGHT, polygons)

        screen.fill(BLACK)

        # Draw polygons
        for polygon in polygons:
            polygon.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
