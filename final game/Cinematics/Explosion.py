import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nile Gambit - Cannon Fire")

# Colors
BLACK = (0, 0, 0)

# VERY RED flame colors - even more vibrant
FLAME_CORE = (255, 255, 150)    # Brighter yellow core
FLAME_HOT = (255, 160, 40)      # More vibrant orange-red
FLAME_MID_HOT = (255, 120, 25)  # Bright red-orange
FLAME_MID = (255, 80, 20)       # Intense red
FLAME_COOL = (240, 50, 15)      # Deep red
FLAME_EDGE = (200, 30, 10)      # Dark red

# Smoke colors - slightly lighter to stay behind flame
SMOKE_LIGHT = (140, 140, 140, 120)
SMOKE_MEDIUM = (110, 110, 110, 100)
SMOKE_DARK = (80, 80, 80, 80)
SMOKE_VOLUME = (60, 60, 60, 70)

# Cannon position
CANNON_X = 100
CANNON_Y = 500

class FlameParticle:
    def __init__(self, x, y, angle, size_multiplier):
        self.x = x
        self.y = y
        
        # Size controlled by explosion size
        base_size = random.uniform(5.0, 9.0) * size_multiplier
        self.size = base_size
        self.base_size = base_size
        
        # Speed controlled by explosion size
        base_speed = random.uniform(6, 11) * size_multiplier
        # Angle controlled by explosion angle with spread based on size
        angle_spread = 6 * size_multiplier  # Larger explosions have wider spread
        actual_angle = math.radians(angle + random.uniform(-angle_spread, angle_spread))
        
        self.speed_x = math.cos(actual_angle) * base_speed
        self.speed_y = math.sin(actual_angle) * base_speed
        
        # Start with brighter red colors immediately
        self.color_stage = random.randint(0, 2)
        self.color_progress = random.uniform(0, 0.3)
        
        # Decay affected by size (larger explosions last longer)
        self.life = 1.0
        self.decay = random.uniform(0.04, 0.08) / size_multiplier
        
    def update(self):
        self.x += self.speed_x + random.uniform(-0.08, 0.08)
        self.y += self.speed_y
        
        # Physics affected by size
        self.speed_y += 0.08
        self.speed_x *= 0.97
        
        # Life cycle
        self.life -= self.decay
        
        # Size changes
        if self.life > 0.7:
            self.size = self.base_size * (1.0 + 0.3 * (1 - self.life))
        else:
            self.size = self.base_size * self.life * 0.9
            
        # Color progression
        self.color_progress += 0.08
        if self.color_progress >= 1 and self.color_stage < 4:
            self.color_stage += 1
            self.color_progress = 0
            
    def get_color(self):
        if self.color_stage == 0:
            return self.interpolate_color(FLAME_CORE, FLAME_HOT, self.color_progress)
        elif self.color_stage == 1:
            return self.interpolate_color(FLAME_HOT, FLAME_MID_HOT, self.color_progress)
        elif self.color_stage == 2:
            return self.interpolate_color(FLAME_MID_HOT, FLAME_MID, self.color_progress)
        elif self.color_stage == 3:
            return self.interpolate_color(FLAME_MID, FLAME_COOL, self.color_progress)
        else:
            return FLAME_EDGE
            
    def interpolate_color(self, color1, color2, progress):
        r = int(color1[0] + (color2[0] - color1[0]) * progress)
        g = int(color1[1] + (color2[1] - color1[1]) * progress)
        b = int(color1[2] + (color2[2] - color1[2]) * progress)
        return (r, g, b)
        
    def draw(self, surface):
        if self.life > 0:
            color = self.get_color()
            alpha = int(255 * self.life)
            
            surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            radius = self.size
            pygame.draw.circle(surf, (*color, alpha), (int(self.size), int(self.size)), radius)
            
            if radius > 2.5:
                core_radius = radius * 0.7
                core_alpha = min(alpha + 60, 255)
                core_color = (min(color[0] + 50, 255), 
                            min(color[1] + 50, 255), 
                            min(color[2] + 40, 255))
                pygame.draw.circle(surf, (*core_color, core_alpha), 
                                 (int(self.size), int(self.size)), core_radius)
            
            surface.blit(surf, (self.x - self.size, self.y - self.size))

class SmokeParticle:
    def __init__(self, x, y, angle, size_multiplier, cluster_id=0, delay=0):
        self.x = x
        self.y = y
        self.cluster_id = cluster_id
        self.delay = delay
        self.active = False
        
        # Size controlled by explosion size
        self.size = random.uniform(1, 3) * size_multiplier
        self.max_size = random.uniform(8, 14) * size_multiplier
        
        # Phase tracking
        self.phase = "delayed"
        self.phase_timer = 0
        self.forward_duration = random.uniform(0.15, 0.3)
        
        # Movement based on explosion angle and size
        base_speed = random.uniform(2, 4) * size_multiplier
        
        # Smoke clusters follow the explosion angle
        cluster_angles = {
            0: angle - 7,  # Left of main angle
            1: angle - 3,  # Slight left
            2: angle,      # Main angle
            3: angle + 3,  # Slight right
            4: angle + 7   # Right of main angle
        }
        
        base_angle = cluster_angles[cluster_id % 5]
        actual_angle = math.radians(base_angle + random.uniform(-3, 3))
        
        self.speed_x = math.cos(actual_angle) * base_speed
        self.speed_y = math.sin(actual_angle) * base_speed
        
        # Store initial direction for curve
        self.initial_angle = actual_angle
        self.curve_progress = 0
        self.curve_speed = random.uniform(0.025, 0.04)
        
        self.decay = random.uniform(0.004, 0.008) / size_multiplier
        self.life = 1.0
        self.color = SMOKE_LIGHT
        
        self.cluster_offset_x = random.uniform(-2, 2) * size_multiplier
        self.cluster_offset_y = random.uniform(-1, 1) * size_multiplier
        
    def update(self):
        self.phase_timer += 0.016
        
        if self.phase == "delayed":
            if self.phase_timer > self.delay:
                self.phase = "following"
                self.phase_timer = 0
                self.active = True
                
        elif self.phase == "following" and self.active:
            self.x += self.speed_x + self.cluster_offset_x * 0.05
            self.y += self.speed_y + self.cluster_offset_y * 0.05
            
            self.speed_y += 0.02
            self.speed_x *= 0.99
            
            if self.phase_timer > self.forward_duration:
                self.phase = "forward"
                self.phase_timer = 0
                
        elif self.phase == "forward" and self.active:
            self.x += self.speed_x
            self.y += self.speed_y
            
            self.speed_x *= 0.88
            self.speed_y *= 0.88
            
            if self.phase_timer > 0.1:
                self.phase = "curving"
                self.curve_progress = 0
                
        elif self.phase == "curving" and self.active:
            self.curve_progress += self.curve_speed
            
            curve_strength = 0.35
            curve_angle = self.initial_angle + (math.pi * curve_strength * self.curve_progress)
            
            current_speed = max(0.2, 1.5 * (1 - self.curve_progress * 0.7))
            
            self.speed_x = math.cos(curve_angle) * current_speed
            self.speed_y = math.sin(curve_angle) * current_speed
            
            self.x += self.speed_x
            self.y += self.speed_y
            
            self.speed_y += 0.005
        
        if self.active:
            self.life -= self.decay
            
            if self.size < self.max_size:
                expansion_rate = 0.04 if self.phase == "following" else 0.03
                self.size += expansion_rate
                
            if self.phase == "curving":
                if self.color == SMOKE_LIGHT and self.curve_progress > 0.3:
                    self.color = SMOKE_MEDIUM
                elif self.curve_progress > 0.6:
                    self.color = random.choice([SMOKE_DARK, SMOKE_VOLUME])
            
    def draw(self, surface):
        if self.life > 0 and self.active:
            alpha = int(self.color[3] * self.life * 0.8)
            color = (*self.color[:3], alpha)
            
            surf_size = int(self.size * 2)
            surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
            
            center = (surf_size // 2, surf_size // 2)
            pygame.draw.circle(surf, color, center, int(self.size))
            
            surface.blit(surf, (self.x - self.size, self.y - self.size))

class Explosion:
    def __init__(self, x, y, angle=-75, size=1.0):
        self.x = x
        self.y = y
        self.angle = angle
        self.size = size
        
        # Particle systems
        self.flame_particles = []
        self.smoke_particles = []
        
        # Explosion timing
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.duration = 400
        
        # Animation timing
        self.last_smoke_burst = 0
        self.last_spatter = 0
        self.smoke_interval = 250
        self.spatter_interval = 150
        
        # Constants
        self.FLAME_PARTICLE_COUNT = 25
        self.SMOKE_PARTICLE_COUNT = 10
        
        # Create initial explosion
        self.create_initial_explosion()
    
    def create_initial_explosion(self):
        """Create the main explosion particles"""
        # Create flame particles with controlled angle and size
        flame_count = int(self.FLAME_PARTICLE_COUNT * self.size)
        for _ in range(flame_count):
            self.flame_particles.append(FlameParticle(self.x, self.y, self.angle, self.size))
        
        # Create smoke particles with controlled angle and size
        smoke_delays = [0, 0.1, 0.15, 0.2, 0.25]
        cluster_count = max(1, int(3 * self.size))  # More clusters for larger explosions
        particles_per_cluster = int(self.SMOKE_PARTICLE_COUNT * self.size)
        
        for cluster_id in range(cluster_count):
            for i in range(particles_per_cluster):
                delay = random.choice(smoke_delays)
                self.smoke_particles.append(SmokeParticle(self.x, self.y, self.angle, self.size, cluster_id, delay))
    
    def create_spatter_flames(self):
        """Create additional flame spatter effects"""
        for _ in range(max(1, int(3 * self.size))):
            offset_range = 6 * self.size
            particle = FlameParticle(self.x + random.uniform(-offset_range, offset_range), 
                                   self.y + random.uniform(-offset_range/2, offset_range/2), 
                                   self.angle, self.size)
            particle.speed_x *= 1.05
            particle.speed_y *= 1.02
            self.flame_particles.append(particle)
    
    def create_additional_smoke(self):
        """Create additional smoke effects"""
        for cluster_id in range(max(1, int(2 * self.size))):
            for _ in range(max(1, int(3 * self.size))):
                delay = random.uniform(0.05, 0.15)
                self.smoke_particles.append(SmokeParticle(self.x, self.y, self.angle, self.size, cluster_id + 3, delay))
    
    def update(self):
        """Update the explosion state and all particles"""
        current_time = pygame.time.get_ticks()
        
        if self.active:
            explosion_elapsed = current_time - self.start_time
            
            if explosion_elapsed < 200:
                if current_time - self.last_spatter > self.spatter_interval:
                    self.create_spatter_flames()
                    self.last_spatter = current_time
            
            elif explosion_elapsed < self.duration:
                if current_time - self.last_smoke_burst > self.smoke_interval:
                    self.create_additional_smoke()
                    self.last_smoke_burst = current_time
            
            if explosion_elapsed > self.duration:
                self.active = False
        
        # Update particles
        for particle in self.flame_particles[:]:
            particle.update()
            if particle.life <= 0 or particle.size <= 0:
                self.flame_particles.remove(particle)
                
        for particle in self.smoke_particles[:]:
            particle.update()
            if particle.life <= 0:
                self.smoke_particles.remove(particle)
    
    def draw(self, surface):
        """Draw all explosion particles"""
        # Draw smoke first (behind flames)
        for particle in self.smoke_particles:
            particle.draw(surface)
        
        # Draw flames on top
        for particle in self.flame_particles:
            particle.draw(surface)
    
    def is_finished(self):
        """Check if the explosion has completed its lifecycle"""
        return not self.active and len(self.flame_particles) == 0 and len(self.smoke_particles) == 0

# Main game loop
clock = pygame.time.Clock()
explosions = []  # List to track multiple explosions

# CONTROL INSTRUCTIONS
font = pygame.font.Font(None, 36)

running = True
while running:
    current_time = pygame.time.get_ticks()
    
    # Handle events
    size = 1
    position = [300, 300]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = event.pos
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                size = 0.4
            if event.key == pygame.K_d:
                size = 1
            if event.key == pygame.K_f:
                size = 3
            if event.key == pygame.K_l:
                size = 8
            
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Default explosion at cannon position
                explosions.append(Explosion(CANNON_X + 67, CANNON_Y - 25))
            elif event.key == pygame.K_1:
                # High angle explosion at mouse position
                explosions.append(Explosion(position[0], position[1], 0, size))
            elif event.key == pygame.K_2:
                # Low angle explosion at mouse position
                explosions.append(Explosion(position[0], position[1], 45, size))
            elif event.key == pygame.K_3:
                # Small explosion at mouse position
                explosions.append(Explosion(position[0], position[1], 90, size))
            elif event.key == pygame.K_4:
                # Large explosion at mouse position
                explosions.append(Explosion(position[0], position[1], 135, size))
            elif event.key == pygame.K_5:
                # Very large explosion at mouse position
                explosions.append(Explosion(position[0], position[1], 180, size))
            elif event.key == pygame.K_6:
                # Wide angle explosion at mouse position
                explosions.append(Explosion(position[0], position[1], 225, size))
            elif event.key == pygame.K_7:
                # Narrow upward explosion at mouse position
                explosions.append(Explosion(position[0], position[1], 270, size))
    
    # Update all explosions
    for explosion in explosions[:]:
        explosion.update()
        if explosion.is_finished():
            explosions.remove(explosion)
    
    # Draw everything
    screen.fill(BLACK)
    
    # Draw cannon
    pygame.draw.rect(screen, (139, 69, 19), (CANNON_X, CANNON_Y - 20, 60, 20))
    pygame.draw.rect(screen, (80, 80, 80), (CANNON_X + 40, CANNON_Y - 15, 40, 10))
    
    # Draw all explosions
    for explosion in explosions:
        explosion.draw(screen)
    
    # Draw control instructions
    instructions = [
        "SPACE: Default explosion",
        "1: High angle (0°)",
        "2: Low angle (45°)", 
        "3: Small (0.5x)",
        "4: Large (1.5x)",
        "5: Very large (2.0x)",
        "6: Wide angle (225°)",
        "7: Narrow upward (270°)",
        "Click + Number: Explosion at mouse"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, (255, 255, 255))
        screen.blit(text, (10, 10 + i * 30))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()