# Debug Manager - Player Position and Hitbox Visualization

## Overview
The `DebugManager` provides real-time visualization of the player position and all active hitbox colliders in the game world.

## How to Use

### Toggle Debug Mode
Press **D** to toggle the debug visualization on/off. You'll see a console message confirming the state:
```
[DEBUG] Debug mode: ON
[DEBUG] Debug mode: OFF
```

### Visual Indicators

When debug mode is enabled, you will see:

#### Player Position (Green)
- **Green Rectangle Outline**: Shows the player's collision box in the XZ plane
- **Cyan Vertical Line**: Indicates the player's center position and vertical axis

#### Hitbox Colliders (Red)
- **Red Line Outlines**: Shows all active wall and environmental colliders as polygon outlines
- Each polygon is drawn at ground level (Y = 0) in world space

## Features

- **Toggle with D key**: Simple one-key enable/disable
- **Real-time visualization**: Updates every frame
- **Automatic scaling**: Works with camera transformations
- **Console logging**: Optional debug text output with player coordinates and collider count
- **Non-invasive**: Debug geometry doesn't affect gameplay or physics

## Technical Details

### What Gets Drawn

1. **Player Collider**: A 0.5 × 0.5 unit rectangle based on current player position
2. **Physics Colliders**: All polygons registered in the physics manager
3. **Orientation markers**: Cyan line for visual orientation reference

### Color Coding

- **Green (0, 1, 0, 1)**: Player collision box
- **Cyan (0, 1, 1, 1)**: Player center/orientation
- **Red (1, 0, 0, 1)**: Wall and environment colliders

## Files Modified

- `DebugManager.py` - New debug visualization module
- `Renderer.py` - Integrated debug drawing into render pipeline
- `InputManager.py` - Added key press detection for toggle

## Future Enhancements

Potential improvements for the debug system:
- Display collider information (polygon vertex count, positions)
- Show collision test results in real-time
- Visualize other physics properties (velocity, acceleration)
- Toggle individual collider visibility
- Export collider geometry to file
