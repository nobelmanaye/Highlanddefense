import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Optimized Grass Simulation")

# Pre-create shadow surface (DO THIS ONCE)
shadow_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

class GrassBlade:
    def __init__(self, x, y, is_yellow=False):
        self.x = x
        self.y = y
        self.is_yellow = is_yellow
        
        # Yellow grass is shorter, green is taller
        if is_yellow:
            self.height = random.randint(8, 14)
            self.width = random.randint(1, 2)
        else:
            self.height = random.randint(16, 24)
            self.width = random.randint(2, 4)
            
        self.color = self.get_grass_color()
        self.highlight_pos = random.uniform(0.3, 0.7)
        self.lean_angle = random.uniform(-0.3, 0.3)
        self.wind_offset = random.uniform(0, 2 * math.pi)
        self.current_angle = self.lean_angle  # Initialize current angle
        
    def get_grass_color(self):
        """Generate grass color - optimized"""
        if self.is_yellow:
            return (random.randint(180, 220), random.randint(160, 200), random.randint(40, 80))
        else:
            base_green = (34, 139, 34)
            return (base_green[0] + random.randint(-10, 10),
                    base_green[1] + random.randint(-20, 20), 
                    base_green[2] + random.randint(-10, 10))
    
    def update(self, time, wind_strength=0.0, wind_direction=0.0):
        """Optimized wind update"""
        wind_sway = math.sin(time * 2.0 + self.wind_offset) * wind_strength
        self.current_angle = self.lean_angle + wind_sway * math.sin(wind_direction)
    
    def draw(self, surface, time):
        """Optimized draw - no highlight for speed"""
        tip_x = self.x + math.sin(self.current_angle) * self.height
        tip_y = self.y - math.cos(self.current_angle) * self.height
        
        pygame.draw.line(surface, self.color, (self.x, self.y), (tip_x, tip_y), self.width)
    
    def draw_shadow(self, surface):
        """Optimized shadow - use pre-created surface"""
        shadow_angle = self.current_angle + 0.2
        shadow_length = self.height * 0.8
        
        shadow_start_x = self.x + 2
        shadow_start_y = self.y + 1
        shadow_tip_x = shadow_start_x + math.sin(shadow_angle) * shadow_length
        shadow_tip_y = shadow_start_y - math.cos(shadow_angle) * shadow_length * 0.7
        
        pygame.draw.line(surface, (0, 0, 0, 50),
                        (shadow_start_x, shadow_start_y),
                        (shadow_tip_x, shadow_tip_y),
                        max(1, self.width - 1))

class GrassPatch:
    def __init__(self, center_x, center_y, num_grasses=12, patch_radius=20, yellow_ratio=0.3):
        self.grasses = []
        self.center_x = center_x
        self.center_y = center_y
        
        # Create grass blades - reduced count for performance
        yellow_count = int(num_grasses * yellow_ratio)
        green_count = num_grasses - yellow_count
        
        for i in range(yellow_count):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, patch_radius * 0.4)
            x = center_x + math.cos(angle) * distance
            y = center_y + math.sin(angle) * distance
            self.grasses.append(GrassBlade(x, y, is_yellow=True))
        
        for i in range(green_count):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(patch_radius * 0.3, patch_radius * 0.8)
            x = center_x + math.cos(angle) * distance
            y = center_y + math.sin(angle) * distance
            self.grasses.append(GrassBlade(x, y, is_yellow=False))
    
    def update(self, time, wind_strength=0.0, wind_direction=0.0):
        """Batch update all grass blades"""
        for grass in self.grasses:
            grass.update(time, wind_strength, wind_direction)
    
    def draw(self, surface, shadow_surface, time):
        """Optimized draw - batch shadows"""
        # Draw shadows to shadow surface
        for grass in self.grasses:
            grass.draw_shadow(shadow_surface)
        
        # Draw grass blades
        for grass in self.grasses:
            grass.draw(surface, time)

def apply_wind_to_grass(grass_patches, time, wind_strength=0.0, wind_direction=0.0):
    """Batch apply wind to all patches"""
    for patch in grass_patches:
        patch.update(time, wind_strength, wind_direction)

def create_yellow_centered_cluster(center_x, center_y, num_grasses=12, patch_radius=20, yellow_ratio=0.4):
    """Create optimized cluster"""
    return GrassPatch(center_x, center_y, num_grasses, patch_radius, yellow_ratio)

def main():
    clock = pygame.time.Clock()
    running = True
    
    # FEWER patches for better performance (6 vs 12)
    grass_patches = [
        create_yellow_centered_cluster(200, 480, 12, 20, 0.4),
        create_yellow_centered_cluster(350, 520, 10, 18, 0.3),
        create_yellow_centered_cluster(500, 490, 14, 22, 0.5),
        create_yellow_centered_cluster(650, 510, 11, 19, 0.35),
        create_yellow_centered_cluster(300, 550, 13, 21, 0.4),
        create_yellow_centered_cluster(550, 530, 12, 20, 0.45),
    ]
    
    # Wind control
    wind_strength = 0.0
    wind_direction = 0.0
    
    def draw_background():
        screen.fill((135, 206, 235))
        pygame.draw.rect(screen, (139, 69, 19), (0, 400, SCREEN_WIDTH, 200))
        pygame.draw.rect(screen, (34, 139, 34), (0, 400, SCREEN_WIDTH, 15))
    
    def draw_wind_indicator():
        center_x, center_y = 50, 50
        radius = 30
        
        pygame.draw.circle(screen, (200, 200, 200), (center_x, center_y), radius, 2)
        
        if wind_strength > 0:
            arrow_length = radius * wind_strength
            end_x = center_x + math.cos(wind_direction) * arrow_length
            end_y = center_y - math.sin(wind_direction) * arrow_length
            
            pygame.draw.line(screen, (255, 0, 0), (center_x, center_y), (end_x, end_y), 3)
    
    start_time = pygame.time.get_ticks()
    
    while running:
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Add new cluster (but limit total)
                    if len(grass_patches) < 8:  # Limit total patches
                        new_x = random.randint(50, SCREEN_WIDTH - 50)
                        new_y = random.randint(420, SCREEN_HEIGHT - 50)
                        grass_patches.append(create_yellow_centered_cluster(new_x, new_y, 40, 20, random.uniform(0.2, 0.5)))
        
        # Wind controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            wind_strength = min(1.0, wind_strength + 0.05)
        if keys[pygame.K_DOWN]:
            wind_strength = max(0.0, wind_strength - 0.05)
        if keys[pygame.K_LEFT]:
            wind_direction += 0.1
        if keys[pygame.K_RIGHT]:
            wind_direction -= 0.1
        if keys[pygame.K_r]:
            wind_strength = 0.0
            wind_direction = 0.0
        
        # Apply wind
        apply_wind_to_grass(grass_patches, current_time, wind_strength, wind_direction)
        
        # Clear shadow surface once per frame (NOT per blade)
        shadow_surface.fill((0, 0, 0, 0))
        
        # Draw everything
        draw_background()
        
        # Draw all patches with shared shadow surface
        for patch in grass_patches:
            patch.draw(screen, shadow_surface, current_time)
        
        # Blit shadow surface once
        screen.blit(shadow_surface, (0, 0))
        
        # Draw UI
        draw_wind_indicator()
        
        # Simple controls display
        font = pygame.font.Font(None, 24)
        controls = [
            "UP/DOWN: Wind Strength",
            "LEFT/RIGHT: Wind Direction", 
            "R: Reset Wind",
            "SPACE: Add Grass",
            f"Strength: {wind_strength:.2f}",
            f"Patches: {len(grass_patches)}"
        ]
        
        for i, text in enumerate(controls):
            rendered = font.render(text, True, (255, 255, 255))
            screen.blit(rendered, (10, 10 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
class GrassArea:
    def __init__(self):
        # Define the rectangular area boundaries
        self.left_x1, self.left_y1 = 33, 29
        self.left_x2, self.left_y2 = 33, 661
        self.right_x1, self.right_y1 = 492, 20
        self.right_x2, self.right_y2 = 446, 61
        
        # Calculate the rectangle dimensions
        self.min_x = min(self.left_x1, self.left_x2, self.right_x1, self.right_x2)
        self.max_x = max(self.left_x1, self.left_x2, self.right_x1, self.right_x2)
        self.min_y = min(self.left_y1, self.left_y2, self.right_y1, self.right_y2)
        self.max_y = max(self.left_y1, self.left_y2, self.right_y1, self.right_y2)
    
    def create_grass_patches(self, num_patches=40, grasses_per_patch=25, patch_radius=15, yellow_ratio=0.4):
        grass_patches = []
        for i in range(num_patches):
            patch_x = random.randint(self.min_x + 10, self.max_x - 10)
            patch_y = random.randint(self.min_y + 10, self.max_y - 10)
            grass_patches.append(GrassPatch(patch_x, patch_y, grasses_per_patch, patch_radius, yellow_ratio))
        return grass_patches
if __name__ == "__main__":
    main()