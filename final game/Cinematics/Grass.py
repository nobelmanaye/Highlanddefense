import pygame
import random
import math

class GrassBlade:
    def __init__(self, x, y, is_yellow=False):
        self.x = x
        self.y = y
        self.is_yellow = is_yellow
        
        if is_yellow:
            self.height = random.randint(8, 14)
            self.width = random.randint(1, 2)
        else:
            self.height = random.randint(16, 24)
            self.width = random.randint(2, 4)
            
        self.color = self.get_grass_color()
        self.lean_angle = random.uniform(-0.3, 0.3)
        self.wind_offset = random.uniform(0, 2 * math.pi)
        self.current_angle = self.lean_angle
        
    def get_grass_color(self):
        if self.is_yellow:
            return (random.randint(180, 220), random.randint(160, 200), random.randint(40, 80))
        else:
            base_green = (34, 139, 34)
            return (base_green[0] + random.randint(-10, 10),
                    base_green[1] + random.randint(-20, 20), 
                    base_green[2] + random.randint(-10, 10))
    
    def update(self, time, wind_strength=0.0, wind_direction=0.0):
        # Enhanced wind effects
        wind_sway = math.sin(time * 3.0 + self.wind_offset) * wind_strength * 1.5
        random_wobble = math.sin(time * 5.0 + self.wind_offset * 2) * wind_strength * 0.3
        self.current_angle = self.lean_angle + wind_sway * math.sin(wind_direction) + random_wobble
    
    def draw(self, surface, time):
        tip_x = self.x + math.sin(self.current_angle) * self.height
        tip_y = self.y - math.cos(self.current_angle) * self.height
        pygame.draw.line(surface, self.color, (self.x, self.y), (tip_x, tip_y), self.width)
    
    def draw_shadow(self, surface):
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
    def __init__(self, center_x, center_y, num_grasses=25, patch_radius=15, yellow_ratio=0.4):
        self.grasses = []
        self.center_x = center_x
        self.center_y = center_y
        
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
        gust_factor = 1.0 + math.sin(time * 2.0) * 0.3
        for grass in self.grasses:
            grass.update(time, wind_strength * gust_factor, wind_direction)
    
    def draw(self, surface, shadow_surface, time):
        for grass in self.grasses:
            grass.draw_shadow(shadow_surface)
        for grass in self.grasses:
            grass.draw(surface, time)

class GrassArea:
    def __init__(self, screen_size, grass_rects=None):
        """
        Initialize GrassArea with optional list of rectangular boundaries
        
        Args:
            screen_size: Tuple (width, height) of the screen
            grass_rects: List of pygame.Rect or tuples (x, y, width, height) defining grass areas
                        If None, uses entire screen
        """
        self.screen_size = screen_size
        
        # Set grass area boundaries
        if grass_rects:
            self.grass_rects = []
            for rect in grass_rects:
                if isinstance(rect, pygame.Rect):
                    self.grass_rects.append(rect)
                else:
                    self.grass_rects.append(pygame.Rect(rect))
        else:
            # Use entire screen if no rects provided
            self.grass_rects = [pygame.Rect(0, 0, screen_size[0], screen_size[1])]
        
        # Wind properties
        self.wind_strength = 0.5  # Default medium wind
        self.wind_direction = 0.0
        
        # Create shadow surface
        self.shadow_surface = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.grass_patches = []
    
    def create_grass_patches(self, num_patches=40, grasses_per_patch=25, patch_radius=15, yellow_ratio=0.4):
        """Create grass patches within the defined rectangular areas"""
        self.grass_patches = []
        
        # Distribute patches evenly among the rectangles
        patches_per_rect = max(1, num_patches // len(self.grass_rects))
        
        for grass_rect in self.grass_rects:
            for i in range(patches_per_rect):
                # Generate patch position within the current grass rectangle boundaries
                patch_x = random.randint(
                    grass_rect.left + patch_radius, 
                    grass_rect.right - patch_radius
                )
                patch_y = random.randint(
                    grass_rect.top + patch_radius, 
                    grass_rect.bottom - patch_radius
                )
                self.grass_patches.append(GrassPatch(patch_x, patch_y, grasses_per_patch, patch_radius, yellow_ratio))
        
        # Add any remaining patches to random rectangles
        remaining_patches = num_patches - (patches_per_rect * len(self.grass_rects))
        for i in range(remaining_patches):
            grass_rect = random.choice(self.grass_rects)
            patch_x = random.randint(
                grass_rect.left + patch_radius, 
                grass_rect.right - patch_radius
            )
            patch_y = random.randint(
                grass_rect.top + patch_radius, 
                grass_rect.bottom - patch_radius
            )
            self.grass_patches.append(GrassPatch(patch_x, patch_y, grasses_per_patch, patch_radius, yellow_ratio))
            
        return self.grass_patches
    
    def set_grass_areas(self, grass_rects):
        """Change the grass area rectangles"""
        self.grass_rects = []
        for rect in grass_rects:
            if isinstance(rect, pygame.Rect):
                self.grass_rects.append(rect)
            else:
                self.grass_rects.append(pygame.Rect(rect))
    
    def add_grass_area(self, grass_rect):
        """Add a new grass area rectangle"""
        if isinstance(grass_rect, pygame.Rect):
            self.grass_rects.append(grass_rect)
        else:
            self.grass_rects.append(pygame.Rect(grass_rect))
    
    def clear_grass_areas(self):
        """Clear all grass areas"""
        self.grass_rects = []
    
    def set_wind(self, strength, direction):
        """Set wind strength and direction"""
        self.wind_strength = max(0.0, min(2.0, strength))  # Clamp between 0-2
        self.wind_direction = direction
    
    def update(self, time):
        """Update all grass patches with current wind settings"""
        self.shadow_surface.fill((0, 0, 0, 0))  # Clear shadow surface
        for patch in self.grass_patches:
            patch.update(time, self.wind_strength, self.wind_direction)
    
    def draw(self, surface, time):
        """Draw all grass patches with shadows"""
        # Draw grass to main surface
        for patch in self.grass_patches:
            patch.draw(surface, self.shadow_surface, time)
        
        # Draw shadows
        surface.blit(self.shadow_surface, (0, 0))