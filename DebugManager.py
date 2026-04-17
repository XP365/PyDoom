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
        """Draw debug visualizations (player and hitboxes)."""
        if not self.debug_enabled:
            return
        
        glPushMatrix()
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_CULL_FACE)
        
        self._draw_player_position(player_pos)
        self._draw_all_hitboxes()
        
        glPopAttrib()
        glPopMatrix()
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_CULL_FACE)
    
    def _draw_player_position(self, player_pos: tuple) -> None:
        """Draw player collider as green box with cyan center line."""
        x, z = player_pos
        
        glColor4f(0.0, 1.0, 0.0, 1.0)
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glVertex3f(x - self.player_collider_width / 2, 0.1, z - self.player_collider_height / 2)
        glVertex3f(x + self.player_collider_width / 2, 0.1, z - self.player_collider_height / 2)
        glVertex3f(x + self.player_collider_width / 2, 0.1, z + self.player_collider_height / 2)
        glVertex3f(x - self.player_collider_width / 2, 0.1, z + self.player_collider_height / 2)
        glEnd()
        glLineWidth(1.0)
        
        glColor4f(0.0, 1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        glVertex3f(x, -1.0, z)
        glVertex3f(x, 1.0, z)
        glEnd()
    
    def _draw_all_hitboxes(self) -> None:
        """Draw all wall colliders in red."""
        if not physicsManager.colliders:
            return
        
        glColor4f(1.0, 0.0, 0.0, 1.0)
        glLineWidth(2.0)
        
        for collider in physicsManager.colliders:
            self._draw_collider_polygon(collider)
        
        glLineWidth(1.0)
    
    def _draw_collider_polygon(self, polygon) -> None:
        """Draw a single polygon collider outline."""
        if not hasattr(polygon, 'points') or not polygon.points:
            return
        
        glBegin(GL_LINE_LOOP)
        for point in polygon.points:
            glVertex3f(point.x, 0.0, point.y)
        glEnd()


# Debug manager singleton
debugManager = DebugManager()
