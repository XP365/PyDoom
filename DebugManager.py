"""
Debug Manager for visualizing player position and hitboxes
"""

from OpenGL.GL import *
import pygame
from pygame.locals import K_p
from InputManager import inputManager
from PhysicsManager import physicsManager
from Camera import camera


class DebugManager:
    def __init__(self):
        self.debug_enabled = False
        self.player_collider_width = 0.5
        self.player_collider_height = 0.5
        
    def toggle_debug(self) -> None:
        """Toggle debug visualization on/off"""
        self.debug_enabled = not self.debug_enabled
        print(f"[DEBUG] Debug mode: {'ON' if self.debug_enabled else 'OFF'}")
    
    def update(self) -> None:
        """Check for debug toggle key"""
        if inputManager.is_key_pressed(K_p):
            self.toggle_debug()
    
    def draw_debug(self, player_pos: tuple) -> None:
        """Draw debug visualizations
        
        Args:
            player_pos: Tuple of (x, z) representing player position in world space
        """
        if not self.debug_enabled:
            return
        
        # Save the current GL state
        glPushMatrix()
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        
        # Disable texturing for debug geometry
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_CULL_FACE)
        
        # Draw player position marker
        # Player collider is created at position (x, z) with size 0.5x0.5
        # In the collision library: Poly(Vector(x, z), [vertices...])
        # So the collider occupies: (x, z) to (x+0.5, z+0.5)
        self._draw_player_position(player_pos)
        
        # Draw all active hitboxes
        self._draw_all_hitboxes()
        
        # Restore GL state
        glPopAttrib()
        glPopMatrix()
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_CULL_FACE)
    
    def _draw_player_position(self, player_pos: tuple) -> None:
        """Draw a visual indicator of the player position and collider
        
        Args:
            player_pos: Tuple of (x, z) representing player position
        """
        x, z = player_pos
        
        # Draw player collider as a green rectangle outline
        glColor4f(0.0, 1.0, 0.0, 1.0)  # Green
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        
        # Draw the rectangular collider in XZ plane
        glVertex3f(x - self.player_collider_width / 2, 0.1, z - self.player_collider_height / 2)
        glVertex3f(x + self.player_collider_width / 2, 0.1, z - self.player_collider_height / 2)
        glVertex3f(x + self.player_collider_width / 2, 0.1, z + self.player_collider_height / 2)
        glVertex3f(x - self.player_collider_width / 2, 0.1, z + self.player_collider_height / 2)
        
        glEnd()
        glLineWidth(1.0)
        
        # Draw a vertical line at player center for orientation
        glColor4f(0.0, 1.0, 1.0, 1.0)  # Cyan
        glBegin(GL_LINES)
        glVertex3f(x, -1.0, z)
        glVertex3f(x, 1.0, z)
        glEnd()
    
    def _draw_all_hitboxes(self) -> None:
        """Draw all active hitbox colliders from the physics manager"""
        collider_count = len(physicsManager.colliders)
        
        if collider_count == 0:
            return
        
        # Draw each collider polygon
        glColor4f(1.0, 0.0, 0.0, 1.0)  # Red for hitboxes
        glLineWidth(2.0)
        
        for i, collider in enumerate(physicsManager.colliders):
            self._draw_collider_polygon(collider, i)
        
        glLineWidth(1.0)
    
    def _draw_collider_polygon(self, polygon, index: int = 0) -> None:
        """Draw a single polygon collider
        
        Args:
            polygon: A Poly object from the collision library with vertices
            index: Collider index for debugging
        """
        try:
            # Access the polygon's vertices
            if not hasattr(polygon, 'points') or not polygon.points:
                return
            
            glBegin(GL_LINE_LOOP)
            
            # Draw each vertex directly as world coordinates
            # The collision library automatically adds position to vertices when storing,
            # so points are already in world space
            for point in polygon.points:
                # Points are in world space (x is X, y is Z)
                vertex_x = point.x
                vertex_z = point.y
                glVertex3f(vertex_x, 0.0, vertex_z)
            
            glEnd()
            
        except Exception as e:
            try:
                print(f"[DEBUG] Error drawing polygon {index}: {e}")
                import traceback
                traceback.print_exc()
            except:
                pass
    
    def draw_debug_text(self, player_pos: tuple) -> None:
        """Print debug text information to console
        
        Args:
            player_pos: Tuple of (x, z) representing player position
        """
        if not self.debug_enabled:
            return
        
        x, z = player_pos
        collider_count = len(physicsManager.colliders)
        
        print(f"[DEBUG] Player Pos: ({x:.2f}, {z:.2f}) | Colliders: {collider_count}")


# Debug manager singleton
debugManager = DebugManager()
