import cv2 
import pygame
def fade_video(screen, video_file, fade_duration=2.0, initial_delay=0, scale_factor=0.8):
    """
    Play a video with fade in/out effects
    Args:
        screen: Pygame screen surface
        video_file: Path to video file
        fade_duration: Seconds for fade in/out (default: 2.0)
        initial_delay: Milliseconds to wait before starting (default: 0)
        scale_factor: Video scale (default: 0.8 = 80% size)
    Returns: True if video completed, False if interrupted
    """
    cap = cv2.VideoCapture(video_file)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_file}")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Scale video
    new_width = int(video_width * scale_factor)
    new_height = int(video_height * scale_factor)
    video_x = (1080 - new_width) // 2
    video_y = (1080 - new_height) // 2
    
    # Get video duration for fade out timing
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = total_frames / fps
    
    # Initial delay if specified
    if initial_delay > 0:
        pygame.time.wait(initial_delay)
    
    # Fade setup
    fade_surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
    start_time = pygame.time.get_ticks()
    
    video_playing = True
    clock = pygame.time.Clock()
    
    while video_playing:
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                video_playing = False
                pygame.mixer.music.stop()
                return False
        
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize frame
        frame_resized = cv2.resize(frame, (new_width, new_height))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        video_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
        
        # Calculate fade alpha
        if current_time < fade_duration:
            # Fade in
            fade_alpha = int(255 * (current_time / fade_duration))
        elif current_time > video_duration - fade_duration:
            # Fade out
            fade_alpha = int(255 * ((video_duration - current_time) / fade_duration))
        else:
            # Fully visible
            fade_alpha = 255
        
        fade_alpha = max(0, min(255, fade_alpha))
        
        # Apply fade
        fade_surface.fill((0, 0, 0, 0))
        fade_surface.blit(video_surface, (0, 0))
        fade_surface.set_alpha(fade_alpha)
        
        # Draw to screen
        screen.fill((0, 0, 0))
        screen.blit(fade_surface, (video_x, video_y))
        pygame.display.flip()
        
        clock.tick(fps)
    
    cap.release()
    
    # Wait for audio to finish
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.mixer.music.stop()
                return False
    
    return True