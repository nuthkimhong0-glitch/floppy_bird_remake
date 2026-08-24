import math
from PIL import Image, ImageDraw, ImageFont

#this is a tools for create pixel from text, and it generate from ai cuz im dumb

def generate_pixel_text(
    text="PRESS SPACE",
    font_path="custom_assets/PressStart2P-Regular.ttf",
    font_size=36,
    text_color="#FFFFFF",        # Main text fill color
    border_color="#000000",      # Outline color
    border_depth=1,              # Thickness of the outline in pixels
    shadow_color="#555555",      # Color of the drop shadow
    shadow_distance=0,           # Distance of shadow (0 = no shadow)
    shadow_angle=45,             # Angle in degrees (0=Right, 90=Down, 45=Bottom-Right)
    shadow_extrusion=False,      # True = Solid 3D trail, False = Floating shadow
    bg_color=(0, 0, 0, 0),       # Background color (default transparent)
    padding=10,                  # Empty space around the text
    output_filename="custom_assets/output.png"
):
    # 1. Load Font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        print(f"Error: Could not find '{font_path}'. Make sure it's in the same folder!")
        return

    # 2. Measure Text
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Calculate final shadow offset based on angle and distance
    # Math note: standard screen coords have +Y going down
    max_shadow_x = int(shadow_distance * math.cos(math.radians(shadow_angle)))
    max_shadow_y = int(shadow_distance * math.sin(math.radians(shadow_angle)))

    # 3. Calculate Canvas Size (ensuring nothing gets cut off)
    img_w = text_w + (padding * 2) + (border_depth * 2) + abs(max_shadow_x)
    img_h = text_h + (padding * 2) + (border_depth * 2) + abs(max_shadow_y)

    img = Image.new("RGBA", (img_w, img_h), bg_color)
    draw = ImageDraw.Draw(img)
    
    # CRITICAL: Disable anti-aliasing for sharp, blocky pixel edges
    draw.fontmode = "1"

    # Base starting coordinates
    # We add max(0, -max_shadow) to push the text inward if the shadow projects left/up
    start_x = padding + border_depth + max(0, -max_shadow_x) - bbox[0]
    start_y = padding + border_depth + max(0, -max_shadow_y) - bbox[1]

    # 4. Draw Drop Shadow (Drawn first so it sits at the back)
    if shadow_distance > 0:
        steps = shadow_distance if shadow_extrusion else 1
        step_multiplier = 1 if shadow_extrusion else shadow_distance
        
        for step in range(1, steps + 1):
            curr_x = int((step * step_multiplier) * math.cos(math.radians(shadow_angle)))
            curr_y = int((step * step_multiplier) * math.sin(math.radians(shadow_angle)))
            
            # Draw shadow silhouette (matching the shape of the bordered text)
            for dx in range(-border_depth, border_depth + 1):
                for dy in range(-border_depth, border_depth + 1):
                    draw.text((start_x + curr_x + dx, start_y + curr_y + dy), text, font=font, fill=shadow_color)
            draw.text((start_x + curr_x, start_y + curr_y), text, font=font, fill=shadow_color)

    # 5. Draw Outline / Border
    if border_depth > 0:
        for dx in range(-border_depth, border_depth + 1):
            for dy in range(-border_depth, border_depth + 1):
                if dx == 0 and dy == 0:
                    continue
                draw.text((start_x + dx, start_y + dy), text, font=font, fill=border_color)

    # 6. Draw Main Text Fill (Drawn last so it sits on top)
    draw.text((start_x, start_y), text, font=font, fill=text_color)

    # Save
    img.save(output_filename)
    print(f"Success! Image saved as {output_filename}")


# ==========================================
# EXAMPLES OF HOW TO USE YOUR NEW PARAMETERS
# ==========================================

# Example 1: Your original request (Pure white, 1px black edge, no shadow)
generate_pixel_text(
    text="SCORE:",
    border_depth=2,
    shadow_distance=2,
    output_filename="custom_assets/score.png",
    shadow_color="#000000"
)

# Example 2: Thick 2px border with a deep red floating drop shadow
# generate_pixel_text(
#     text="GAME OVER",
#     border_depth=2,
#     shadow_distance=8,
#     shadow_angle=45,       # Bottom-right
#     shadow_color="#FF0000",
#     shadow_extrusion=False,
#     output_filename="2_floating_shadow.png"
# )

# # Example 3: 3D Extruded Retro Arcade Style
# generate_pixel_text(
#     text="LEVEL UP!",
#     text_color="#FFFF00",  # Yellow text
#     border_depth=1,
#     shadow_distance=10,    # Long trail
#     shadow_angle=135,      # Bottom-left
#     shadow_color="#000088", # Dark blue shadow
#     shadow_extrusion=True, # Turns the shadow into a solid 3D block
#     output_filename="3_extruded_3D.png"
# )