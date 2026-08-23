# ParaView MCP Tools Reference

This document describes the tools available through the ParaView MCP Server for integration with Claude Desktop or other MCP clients.

## Overview

The ParaView MCP Server enables natural language control of ParaView visualizations. It connects to a running pvserver and exposes ParaView functionality through the Model Context Protocol.

> **Known limitation:** this connects the client GUI to pvserver via a synchronization mechanism that upstream (`llnl/paraview_mcp`) documents as deprecated in recent ParaView versions, which "may not display content from the pvserver instance correctly, and overall stability issues may occur." Prefer the headless `pvpython` scripting workflow when interactive GUI feedback isn't required.

## Setup

### Prerequisites

1. ParaView installed (with pvserver and pvpython)
2. Python 3.10+ with mcp and httpx packages
3. Claude Desktop or compatible MCP client

### Starting the Server

```bash
# 1. Start pvserver
$PARAVIEW_HOME/bin/pvserver --multi-clients --server-port=11111 &

# 2. Connect ParaView GUI (optional but recommended for visual feedback)
$PARAVIEW_HOME/bin/paraview --server-url=cs://localhost:11111 &

# 3. The MCP server connects automatically when Claude Desktop starts
```

### Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ParaView": {
      "command": "/path/to/python",
      "args": [
        "/path/to/paraview_mcp/paraview_mcp_server.py",
        "--server", "localhost",
        "--port", "11111"
      ]
    }
  }
}
```

---

## Tool Reference

### Data Loading

#### `load_data(file_path: str) -> str`

Load data from a file into ParaView.

**Arguments:**
- `file_path`: Path to the data file (supports VTK, EXODUS, CSV, RAW, etc.)

**Returns:** Status message with registered source name.

**Example:**
```
load_data("/path/to/volume.vtk")
# Returns: "Successfully loaded data from /path/to/volume.vtk. Source registered as 'volume.vtk'."
```

**Notes:**
- RAW files automatically parse dimensions from filename (e.g., `data_256x256x256_uint8.raw`)
- EXODUS files are read using IOSSReader

---

### Isosurface Creation

#### `create_isosurface(value: float, field: str = None) -> str`

Create an isosurface visualization of the active source.

**Arguments:**
- `value`: Isovalue for the contour
- `field`: Optional field name to contour by (defaults to first available)

**Returns:** Status message with filter name.

**Example:**
```
create_isosurface(0.5, "density")
# Returns: "Created isosurface at value 0.5. Filter registered as 'Contour1'."
```

---

### Slice Creation

#### `create_slice(origin_x, origin_y, origin_z, normal_x, normal_y, normal_z) -> str`

Create a slice through the loaded volume data.

**Arguments:**
- `origin_x, origin_y, origin_z`: Slice plane origin (None defaults to data center)
- `normal_x, normal_y, normal_z`: Slice plane normal (default: [0, 0, 1])

**Returns:** Status message with slice filter name.

**Example:**
```
create_slice(None, None, None, 1, 0, 0)
# Creates a Y-Z plane slice through the data center
```

---

### Volume Rendering

#### `toggle_volume_rendering(enable: bool = True) -> str`

Toggle volume rendering visibility for the active source.

**Arguments:**
- `enable`: True to show, False to hide volume rendering

**Returns:** Status message.

**Notes:**
- When disabled, preserves volume representation settings
- Works only with the original loaded data source

---

### Visibility Control

#### `toggle_visibility(enable: bool = True) -> str`

Toggle visibility for the active source.

**Arguments:**
- `enable`: True to show, False to hide

**Returns:** Status message.

---

### Source Management

#### `set_active_source(name: str) -> str`

Set the active pipeline object by its registered name.

**Arguments:**
- `name`: Name of the source (e.g., "Contour1", "Slice1")

**Returns:** Status message.

**Example:**
```
set_active_source("Contour1")
```

#### `get_active_source_names_by_type(source_type: str = None) -> str`

Get a list of source names filtered by type.

**Arguments:**
- `source_type`: Filter by type (e.g., "Contour", "Slice"). None returns all.

**Returns:** List of source names.

---

### Transfer Functions

#### `edit_volume_opacity(field_name: str, opacity_points: list[dict]) -> str`

Edit the opacity transfer function for a field.

**Arguments:**
- `field_name`: The scalar field to modify
- `opacity_points`: List of dicts: `[{"value": float, "alpha": float}, ...]`

**Example:**
```json
{
  "field_name": "density",
  "opacity_points": [
    {"value": 0.0, "alpha": 0.0},
    {"value": 50.0, "alpha": 0.3},
    {"value": 100.0, "alpha": 1.0}
  ]
}
```

#### `set_color_map(field_name: str, color_points: list[dict]) -> str`

Set the color transfer function for a field.

**Arguments:**
- `field_name`: The scalar field to modify
- `color_points`: List of dicts: `[{"value": float, "rgb": [r, g, b]}, ...]`

**Example:**
```json
{
  "field_name": "density",
  "color_points": [
    {"value": 0.0, "rgb": [0.0, 0.0, 1.0]},
    {"value": 50.0, "rgb": [1.0, 1.0, 1.0]},
    {"value": 100.0, "rgb": [1.0, 0.0, 0.0]}
  ]
}
```

**Tips:**
- Lower values typically correspond to lower density/background
- Higher values indicate higher physical density
- Take screenshots after adjusting to verify results

---

### Coloring

#### `color_by(field: str, component: int = -1) -> str`

Color the active visualization by a specific field.

**Arguments:**
- `field`: Field name to color by
- `component`: Component to color by (-1 for magnitude)

**Returns:** Status message.

**Notes:**
- Not applicable for volume rendering
- Cannot be used with 'Outline' or 'Wireframe' representations

---

### Representation

#### `set_representation_type(rep_type: str) -> str`

Set the representation type for the active source.

**Arguments:**
- `rep_type`: One of "Surface", "Wireframe", "Points", "Volume", "Outline", "Surface With Edges"

**Notes:**
- Do not use for volume rendering (use `toggle_volume_rendering` instead)

---

### Pipeline Information

#### `get_pipeline() -> str`

Get the current pipeline structure.

**Returns:** List of all sources in the pipeline with their types.

#### `get_available_arrays() -> str`

Get a list of available arrays in the active source.

**Returns:** Lists of point data and cell data arrays with component counts.

---

### Streamlines

#### `create_streamline(seed_point_number: int, vector_field: str = None, integration_direction: str = "BOTH", max_steps: int = 1000, initial_step: float = 0.1, maximum_step: float = 50.0) -> str`

Create streamlines with tube visualization.

**Arguments:**
- `seed_point_number`: Number of seed points to generate
- `vector_field`: Vector field name (auto-detected if None)
- `integration_direction`: "FORWARD", "BACKWARD", or "BOTH"
- `max_steps`: Maximum integration steps
- `initial_step`: Initial step length
- `maximum_step`: Maximum streamline length

**Returns:** Status message with tube filter name.

---

### Camera Control

#### `rotate_camera(azimuth: float = 30.0, elevation: float = 0.0) -> str`

Rotate the camera by specified angles.

**Arguments:**
- `azimuth`: Rotation around vertical axis in degrees
- `elevation`: Rotation around horizontal axis in degrees

#### `reset_camera() -> str`

Reset the camera to show all data.

---

### Screenshot

#### `get_screenshot() -> Image`

Capture a screenshot of the current view.

**Returns:** Image data for display in chat.

**Notes:**
- Requires ParaView GUI connected to see the rendered view
- Uses the active GUI view

---

### Analysis Tools

#### `plot_over_line(point1: list[float] = None, point2: list[float] = None, resolution: int = 100) -> str`

Create a plot over line filter to sample data along a line.

**Arguments:**
- `point1`: Start point [x, y, z] (None uses data bounds)
- `point2`: End point [x, y, z] (None uses data bounds)
- `resolution`: Number of sample points

#### `warp_by_vector(vector_field: str = None, scale_factor: float = 1.0) -> str`

Apply warp by vector filter to the active source.

**Arguments:**
- `vector_field`: Vector field name (auto-detected if None)
- `scale_factor`: Scale factor for the warp

#### `compute_surface_area() -> str`

Compute the surface area of the active surface mesh.

**Returns:** Computed area value.

**Notes:**
- Active source must be a surface mesh
- Use after creating a contour/isosurface

---

### Export

#### `save_contour_as_stl(stl_filename: str = "contour.stl") -> str`

Save the active contour or surface as an STL file.

**Arguments:**
- `stl_filename`: Output filename (saved in same folder as loaded data)

**Returns:** Path to saved file.

---

## Best Practices

1. **Limit function calls per reply** - Execute operations incrementally
2. **Take screenshots after changes** - Verify visualization results
3. **Use appropriate functions for representation type**:
   - Volume rendering: `toggle_volume_rendering`, `set_color_map`, `edit_volume_opacity`
   - Surface rendering: `color_by`, `set_representation_type`
4. **Check available arrays** before coloring by field
5. **Use `get_pipeline()`** to understand current state
