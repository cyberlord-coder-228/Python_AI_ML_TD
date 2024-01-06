# spaghetti warning
import pygame
import sys
import random
import math

pygame.init()

# Constants
PROGRAM_NAME = "Tower Defense"
LIVES = 20
WIDTH, HEIGHT = 800, 600
MENU_WIDTH = 25
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_RED = (255, 150, 150)
LIGHT_GREEN = (150, 255, 150)
LIGHT_BLUE = (150, 150, 255)
LIGHT_YELLOW = (255, 255, 100)
DARK_RED = (200, 0, 0)
DARK_GREEN = (50, 100, 50)
DARK_BLUE = (0, 0, 200)
DARK_GRAY = (32, 32, 32)
MID_GREY = (69, 69, 69)
LIGHT_GRAY = (200, 200, 200)

# Function that towers use to shoot slightly more precisely
def aim(origin, projectile_speed, target_loc, target_speed, target_angle):
    distance = math.hypot(origin[0]-target_loc[0], origin[1]-target_loc[1])
    interject_time = distance / (projectile_speed+target_speed)
    x = target_loc[0] + interject_time * target_speed * math.cos(target_angle) 
    y = target_loc[1] - interject_time * target_speed * math.sin(target_angle) 
    return (x, y)

# Classes
class Projectile(pygame.sprite.Sprite):
    def __init__(self, origin, goal):
        super().__init__()
        self.size = 3
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=origin)
        self.angle = -math.degrees(math.atan2(-(goal[1]-self.rect.center[1]), (goal[0] - self.rect.center[0])))
        self.speed = 200  # pixels per second

    def update(self):
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.kill()

        if len(units):
            for unit in units:
                if unit.rect.colliderect(self.rect):
                    unit.self_destroy()
                    self.kill()
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.rect.x += dx / FPS
        self.rect.y += dy / FPS

class Bomb(Projectile):
    def __init__(self, origin, goal, power=100, interval=3*FPS, speed=100):
        super().__init__(origin, goal)
        self.size = 10
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(BLACK)  # Use color from the Tower class
        self.rect = self.image.get_rect(center=origin)
        self.explosion_timer = 0
        self.explosion_interval = interval  # Explode after 3 seconds
        self.explosion_radius = power
        self.speed = speed

    def update(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.rect.x += dx / FPS
        self.rect.y += dy / FPS

        self.explosion_timer += 1
        if self.explosion_timer >= self.explosion_interval:
            explosion = Explosion(self.rect.center, self.explosion_radius)
            all_sprites.add(explosion)
            explosions.add(explosion)
            self.kill()
        elif len(units):
            for unit in units:
                if unit.rect.colliderect(self.rect):
                    explosion = Explosion(self.rect.center, self.explosion_radius)
                    all_sprites.add(explosion)
                    explosions.add(explosion)
                    self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, location, radius):
        super().__init__()
        self.size = radius
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=location)
        self.explosion_duration = 0.25 * FPS  # Display explosion for 0.5 seconds

    def update(self):
        self.explosion_duration -= 1
        if self.explosion_duration <= 0:
            for unit in units:
                if math.hypot(self.rect.center[0]-unit.rect.center[0], self.rect.center[1]-unit.rect.center[1]) < self.size:
                    unit.self_destroy()
            self.kill()  # Remove the explosion sprite after the duration


class Tower(pygame.sprite.Sprite):
    color_scheme = {'red': DARK_RED, 'green': DARK_GREEN, 'blue': DARK_BLUE}
    
    def __init__(self, x, y, color):
        super().__init__()
        self.size = 20
        self.color = color
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color_scheme[self.color])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.reload_time = 1 * FPS
        self.timer = self.reload_time

    def shoot(self):
        pass

class RedTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 'red')
        self.color = 'red'
        # self.image = pygame.Surface((self.size, self.size))
        self.image.fill(DARK_RED)
        self.reload_time = 0.05 * FPS
        self.timer = self.reload_time

    def shoot(self):
        if self.timer <= self.reload_time:
            self.timer += 1
        else:
            if len(units):

                target = random.choice(list(units))
                expected_interject_location = aim(
                    origin=self.rect.center,
                    projectile_speed=200,
                    target_loc=target.rect.center,
                    target_speed=target.speed,
                    target_angle=target.angle
                )
                projectile = Projectile(self.rect.center, expected_interject_location)
                all_sprites.add(projectile)
                projectiles.add(projectile)
            self.timer = 0

class GreenTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 'green')
        self.color = 'green'
        # self.image = pygame.Surface((self.size, self.size))
        self.image.fill(DARK_GREEN)
        self.reload_time = 2.5 * FPS
        self.timer = self.reload_time//2
        self.explosion_radius = 200

    def shoot(self):
        if self.timer <= self.reload_time:
            self.timer += 1
        else:
            if len(units):
                target = random.choice(list(units))
                bomb = Bomb(
                    origin=self.rect.center,
                    goal=target.rect.center,
                    power=self.explosion_radius,
                    speed=0
                )
                all_sprites.add(bomb)
                projectiles.add(bomb)
            self.timer = 0

class BlueTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 'blue')
        self.color = 'blue'
        # self.image = pygame.Surface((self.size, self.size))
        self.image.fill(DARK_BLUE)
        self.reload_time = 0.5 * FPS
        self.timer = self.reload_time//2

    def shoot(self):
        if self.timer <= self.reload_time:
            self.timer += 1
        else:
            if len(units):
                target = random.choice(list(units))
                expected_interject_location = aim(
                    origin=self.rect.center,
                    projectile_speed=100,
                    target_loc=target.rect.center,
                    target_speed=target.speed,
                    target_angle=target.angle
                )
                bomb = Bomb(self.rect.center, expected_interject_location, speed=100)
                all_sprites.add(bomb)
                projectiles.add(bomb)
            self.timer = 0

class Unit(pygame.sprite.Sprite):
    color_scheme = {'red': LIGHT_RED, 'green': LIGHT_GREEN, 'blue': LIGHT_BLUE, 'yellow': LIGHT_YELLOW}
    
    def __init__(self, x, y, color):
        super().__init__()
        self.size = 15

        self.origin = (x,y)
        self.image = pygame.Surface((self.size, self.size))
        self.color = color
        self.image.fill(self.color_scheme[self.color])
        self.rect = self.image.get_rect(center=(x, y))
        
        
        self.dispersion = 3
        self.angle = random.uniform(175, 185)
        self.speed = 100  # pixels per second

    def evaluate_fitness(self):
        distance_to_defender = self.rect.center[0]-defender_fortress.rect.center[0]
        fitness = WIDTH//2 - distance_to_defender  # The closer, the better

        # Penalize for collisions with projectiles and explosions
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                fitness *= 0.5  # Reduce fitness if hit by a projectile

        for explosion in explosions:
            if math.hypot(self.rect.center[0] - explosion.rect.center[0],
                          self.rect.center[1] - explosion.rect.center[1]) < explosion.size:
                fitness *= 0.5  # Reduce fitness if in the explosion radius

        return fitness

    def self_destroy(self):
        u_fit = self.evaluate_fitness()*0.5
        AGENT.update_color_value(self.color, u_fit)
        AGENT.update_position_value(self.origin, u_fit)
        self.kill()

    def update(self):
        # Reflect units from the sides of the board
        if self.rect.top <= MENU_WIDTH or self.rect.bottom >= HEIGHT or self.rect.right >= WIDTH:
            self.self_destroy()

        # Check for towers of the same color and move away
        for tower in towers:
            if tower.color == self.color:
                if self.rect.colliderect(tower.rect):
                    self.self_destroy()
                dx = tower.rect.center[0] - self.rect.center[0]
                dy = tower.rect.center[1] - self.rect.center[1]
                distance = math.hypot(dx, dy)
                if distance <= 50:
                    self.angle = -math.degrees(math.atan2(-dy, dx))
                
        # Calculate the movement vector
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.rect.x += dx / FPS
        self.rect.y += dy / FPS

        self.angle += random.uniform(-self.dispersion, self.dispersion)

class RedUnit(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 'red')
        self.size = 5
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color_scheme['red'])

class GreenUnit(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 'green')
        self.speed = 150

class BlueUnit(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 'blue')
        self.angle = 180
        self.dispersion = 10

class YellowUnit(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 'yellow')
        self.mutation_factor = 0.1

    def deviance(self):
        return random.uniform(1-self.mutation_factor, 1+self.mutation_factor)

    def set_params(self, size, speed, angle, dispersion):
        self.size = round(size * self.deviance())
        self.speed = speed * self.deviance()
        self.angle = angle * self.deviance()
        self.dispersion = dispersion * self.deviance()

    def self_destroy(self):
        try:
            YELLOW_POPULATION.pop(YELLOW_POPULATION.index(self))
        except:
            pass
        u_fit = self.evaluate_fitness()*0.5
        AGENT.update_color_value(self.color, u_fit)
        AGENT.update_position_value(self.origin, u_fit)
        self.kill()

class Fortress(pygame.sprite.Sprite):
    def __init__(self, x, color):
        super().__init__()
        self.image = pygame.Surface((30, HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 0)
        self.health = LIVES

    def decrease_health(self):
        self.health -= 1

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(PROGRAM_NAME)
clock = pygame.time.Clock()

# Groups
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
explosions = pygame.sprite.Group()
towers = pygame.sprite.Group()
units = pygame.sprite.Group()
fortress_group = pygame.sprite.Group()

# Create Fortresses
defender_fortress = Fortress(0, DARK_GRAY)
attacker_fortress = Fortress(WIDTH - 30, WHITE)

all_sprites.add(defender_fortress, attacker_fortress)
fortress_group.add(defender_fortress, attacker_fortress)

def is_valid_tower_position(x, y):
    # Check if the position is in the left half of the board and not on the panel
    if x >= WIDTH // 2 or y <= 25:
        return False

    # Check for collisions with the fortresses
    for fortress in fortress_group:
        if fortress.rect.collidepoint(x, y):
            return False
    
    # Check for collisions with existing towers
    for tower in towers:
        if tower.rect.collidepoint(x, y):
            return False
    
    return True

def place_tower(x, y, color):
    if is_valid_tower_position(x, y):
        if len(towers) >= 4:
            # If there are already 6 towers, remove the oldest one
            oldest_tower = towers.sprites()[0]
            towers.remove(oldest_tower)
            all_sprites.remove(oldest_tower)
        
        if color == 'red':
            tower = RedTower(x, y)
        elif color == 'blue':
            tower = BlueTower(x, y)
        elif color == 'green':
            tower = GreenTower(x, y)
        else:
            tower = Tower(x, y, color)
        all_sprites.add(tower)
        towers.add(tower)


# Unit spawning logic
UNIT_SPAWN_TIMER = 0
UNIT_SPAWN_INTERVAL = 0.001 * FPS
class SelectionAgent:
    def __init__(self):
        self.color_options = {'red':0, 'green':0, 'blue':0, 'yellow':0}
        self.y_pos_options = {y: val for y, val in zip(range(10, HEIGHT-10), [0]*(HEIGHT-20))}

    def update_color_value(self, color, delta=1):
        self.color_options[color] += delta

    def update_position_value(self, origin, delta=1):
        self.y_pos_options[round(origin[1])]

    def select_best_unit_spawning_options(self):
        if random.uniform(0, 1) < 0.1:  # Exploration: 10% of the time, choose a random action
            return (
                random.choice(list(self.color_options)),
                random.choice(list(self.y_pos_options))
            )
        else:
            # Exploitation: Choose the action with the highest Q-value for the current state
            max_color_value = max(list(self.color_options.values()))
            best_colors = [color for color in self.color_options if self.color_options[color] == max_color_value]
            max_pos_value = max(list(self.y_pos_options.values()))
            best_positions = [y for y in self.y_pos_options if self.y_pos_options[y] == max_pos_value]
            result = (random.choice(best_colors), random.choice(best_positions))
            return result

# Main game loop
AGENT = SelectionAgent()
YELLOW_POPULATION = []
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                place_tower(*pygame.mouse.get_pos(), 'red')
            elif event.button == 2:  # Middle mouse button
                place_tower(*pygame.mouse.get_pos(), 'green')
            elif event.button == 3:  # Right mouse button
                place_tower(*pygame.mouse.get_pos(), 'blue')

    # Check for collisions between units and the fortresses
    hits_defender = pygame.sprite.spritecollide(defender_fortress, units, True)
    hits_attacker = pygame.sprite.spritecollide(attacker_fortress, units, False)
    
    for hit in hits_defender:
        print(f'{hit}, size: {hit.size}, speed: {hit.speed}, angle: {round(hit.angle)}, d: {hit.dispersion}')
        AGENT.update_color_value(hit.color, 1000)
        AGENT.update_position_value(hit.origin, 1000)
        defender_fortress.decrease_health()
        if defender_fortress.health <= 0:
            running = False

    all_sprites.update()
    screen.fill(WHITE)

    # Draw light grey on the left and mid-grey on the right
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, WIDTH // 2, HEIGHT))
    pygame.draw.rect(screen, MID_GREY, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))

    # Draw white panel at the top
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, MENU_WIDTH))

    # Display remaining health on the white panel
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {defender_fortress.health}", True, DARK_GRAY)
    screen.blit(health_text, (50, 0))

    # Spawn units every 3 seconds
    UNIT_SPAWN_TIMER
    # global UNIT_SPAWN_INTERVAL
    if UNIT_SPAWN_TIMER < UNIT_SPAWN_INTERVAL:
        UNIT_SPAWN_TIMER += 1
    else:
        x_pos = WIDTH-30
        color, y_pos = AGENT.select_best_unit_spawning_options()
        match color:
            case 'red':
                new_unit = RedUnit(x_pos, y_pos)
            case 'green':
                new_unit = GreenUnit(x_pos, y_pos)
            case 'blue':
                new_unit = BlueUnit(x_pos, y_pos)
            case 'yellow':
                if len(YELLOW_POPULATION) <= 4:
                    new_unit = YellowUnit(x_pos, y_pos)
                    YELLOW_POPULATION.append(new_unit)

                else:
                    YELLOW_POPULATION = sorted(YELLOW_POPULATION, key=lambda x: x.evaluate_fitness(), reverse=True)
                    PARENTS = YELLOW_POPULATION[:len(YELLOW_POPULATION)//2]
                    parent1, parent2 = random.sample(PARENTS, 2)

                    new_unit=YellowUnit(x_pos, y_pos)

                    new_unit.set_params(
                        size=(parent1.size + parent2.size) / 2,
                        speed=(parent1.speed + parent2.speed) / 2,
                        angle=(parent1.angle + parent2.angle) / 2,
                        dispersion=(parent1.dispersion + parent2.dispersion) / 2
                    )
                    YELLOW_POPULATION.append(new_unit)

        
        units.add(new_unit)
        all_sprites.add(new_unit)
        UNIT_SPAWN_TIMER = 0

    for tower in towers:
        tower.shoot()

    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
