"""Create the original fantasy scene and knight sprite sheet for this lesson."""

from math import cos, sin
import json
from pathlib import Path

from PIL import Image, ImageDraw


HERE = Path(__file__).parent
CELL = 128
ACTIONS = ('idle', 'walk', 'run', 'jump', 'attack')
ACTION_FRAME_COUNTS = {
    'idle': 4,
    'walk': 8,
    'run': 10,
    'jump': 6,
    'attack': 7,
}


def polygon(draw, points, fill, outline=(25, 24, 42, 255)):
    draw.polygon(points, fill=fill, outline=outline)


def make_knight_frame(action, frame, frame_count):
    image = Image.new('RGBA', (CELL, CELL), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    phase = frame * 2 * 3.14159 / frame_count
    bob = round(2 * sin(phase)) if action in ('idle', 'walk', 'run') else 0
    jump = round(18 * sin(frame * 3.14159 / (frame_count - 1))) if action == 'jump' else 0
    cx, base = 64, 105 - bob - jump
    outline = (28, 27, 43, 255)
    steel, steel_light, steel_dark = (94, 126, 160, 255), (190, 211, 226, 255), (54, 72, 102, 255)
    red, red_light = (139, 39, 59, 255), (205, 69, 72, 255)
    gold = (242, 190, 82, 255)

    # Ground shadow; separate from the transparent sprite background.
    if action != 'jump':
        d.ellipse((37, 101, 91, 113), fill=(17, 20, 35, 115))

    # Directional footstep dust and speed streaks, trailing behind the knight.
    if action == 'walk' and frame in (frame_count // 4, frame_count * 3 // 4):
        dust_x = 43 if frame == 1 else 77
        d.ellipse((dust_x - 9, 97, dust_x + 1, 103), fill=(208, 203, 179, 150))
        d.ellipse((dust_x - 5, 92, dust_x + 3, 98), fill=(226, 218, 192, 190))
        d.ellipse((dust_x + 2, 96, dust_x + 8, 101), fill=(194, 190, 171, 145))
    elif action == 'run':
        trail = 14 + (frame % 3) * 5
        for i, y in enumerate((base - 65, base - 51, base - 37)):
            end_x = 24 + (frame * 7 + i * 11) % 18
            d.line((end_x, y, end_x + trail, y - (i - 1) * 2),
                   fill=(150, 220, 244, 210), width=2 if i != 1 else 3)
        d.ellipse((42, 98, 52, 104), fill=(218, 208, 182, 170))
        d.ellipse((51, 94, 58, 100), fill=(232, 221, 194, 190))

    stride = 0
    if action in ('walk', 'run'):
        stride = round(sin(phase) * (12 if action == 'run' else 7))
    if action == 'jump':
        stride = (-7 if frame < frame_count // 2 else 7)
    if action == 'attack':
        stride = 4 if frame > frame_count // 3 else 0

    # Boots and articulated greaves.
    for side, offset in ((-1, -stride), (1, stride)):
        lx = cx + side * 11 + offset
        knee_y = base - 22
        foot_x = lx + (side * 8 if action in ('walk', 'run', 'jump') else 0)
        polygon(d, [(lx - 6, knee_y), (lx + 6, knee_y), (foot_x + 5, base - 4),
                    (foot_x + 4, base), (foot_x - 8, base), (foot_x - 7, base - 5)],
                steel, outline)
        d.line((lx - 5, knee_y - 2, lx + 5, knee_y - 2), fill=steel_light, width=2)
        polygon(d, [(foot_x - 8, base - 5), (foot_x + 5, base - 5),
                    (foot_x + 11, base), (foot_x - 9, base)], steel_dark, outline)

    # Side-on red tabard and breastplate, with the chest facing right.
    polygon(d, [(cx - 13, base - 59), (cx + 11, base - 61),
                (cx + 17, base - 53), (cx + 13, base - 27),
                (cx + 7, base - 20), (cx - 13, base - 23),
                (cx - 17, base - 31)], red, outline)
    polygon(d, [(cx - 9, base - 58), (cx + 9, base - 59),
                (cx + 14, base - 52), (cx + 9, base - 40),
                (cx - 8, base - 39)], steel, outline)
    d.line((cx - 3, base - 56, cx + 7, base - 42), fill=steel_light, width=3)
    d.ellipse((cx + 3, base - 51, cx + 9, base - 45), fill=gold, outline=outline)

    # Cape swings with the action.
    cape_swing = round(sin(phase) * 7) if action in ('walk', 'run') else 0
    polygon(d, [(cx - 10, base - 57), (cx - 21, base - 52),
                (cx - 27 - cape_swing, base - 30), (cx - 12, base - 35)], red_light, outline)

    # Helmet, visor slit, plume.
    polygon(d, [(cx - 12, base - 78), (cx - 7, base - 83),
                (cx + 7, base - 81), (cx + 13, base - 74),
                (cx + 20, base - 69), (cx + 14, base - 65),
                (cx + 10, base - 59), (cx - 7, base - 60),
                (cx - 14, base - 67)], steel, outline)
    # Open side visor, cheek guard, and a red plume swept behind the helmet.
    polygon(d, [(cx + 7, base - 72), (cx + 17, base - 69),
                (cx + 11, base - 66), (cx + 4, base - 68)],
            (35, 45, 62, 255), outline)
    d.line((cx - 8, base - 72, cx + 8, base - 73), fill=steel_light, width=2)
    d.line((cx + 10, base - 64, cx + 15, base - 68), fill=gold, width=2)
    polygon(d, [(cx - 6, base - 81), (cx - 18, base - 96),
                (cx - 22, base - 84), (cx - 12, base - 77)], red_light, outline)
    d.line((cx - 9, base - 78, cx + 5, base - 78), fill=steel_light, width=2)

    # Left arm and kite shield.
    arm_y = base - 49
    d.line((cx - 11, arm_y, cx - 20, arm_y + 12), fill=steel_dark, width=8)
    d.ellipse((cx - 24, arm_y + 8, cx - 16, arm_y + 16), fill=steel_light, outline=outline)
    polygon(d, [(cx - 28, arm_y + 9), (cx - 15, arm_y + 11),
                (cx - 16, arm_y + 28), (cx - 22, arm_y + 35),
                (cx - 29, arm_y + 27)], steel, outline)
    d.line((cx - 22, arm_y + 12, cx - 22, arm_y + 29), fill=gold, width=2)

    # Right arm and sword. Attack raises and sweeps the blade through six poses.
    d.line((cx + 10, arm_y, cx + 20, arm_y + 7), fill=steel_dark, width=8)
    hand = (cx + 22, arm_y + 8)
    d.ellipse((hand[0] - 4, hand[1] - 4, hand[0] + 4, hand[1] + 4), fill=gold, outline=outline)
    if action == 'attack':
        # A forward overhead slash: the blade stays in front of the side-facing knight.
        attack_progress = frame / (frame_count - 1)
        angle = 0.95 + 0.96 * attack_progress
    elif action == 'jump':
        angle = 1.05
    else:
        angle = 1.15 + 0.08 * sin(phase)
    sx, sy = hand
    ex, ey = sx + 39 * sin(angle), sy - 39 * cos(angle)
    d.line((sx, sy, sx + 4 * sin(angle), sy - 4 * cos(angle)), fill=gold, width=5)
    d.line((sx + 4 * sin(angle), sy - 4 * cos(angle), ex, ey), fill=steel_light, width=5)
    d.line((sx + 5 * sin(angle), sy - 5 * cos(angle), ex, ey), fill=(239, 247, 250, 255), width=2)

    # Bright crescent trail and impact glint make the sword attack read clearly.
    if action == 'attack':
        # The arc drops with the blade instead of staying fixed in place.
        attack_progress = frame / (frame_count - 1)
        arc_drop = round(attack_progress * 15)
        arc_box = (cx + 4, base - 99 + arc_drop,
                   cx + 61, base - 42 + arc_drop)
        d.arc(arc_box, start=205, end=326, fill=(178, 76, 255, 170), width=9)
        d.arc(arc_box, start=205, end=326, fill=(85, 225, 255, 255), width=5)
        d.arc(arc_box, start=210, end=322, fill=(244, 255, 255, 255), width=2)
        if frame >= frame_count - 3:
            impact_progress = frame - (frame_count - 3)
            ix, iy = cx + 44 + impact_progress * 4, base - 63 + impact_progress * 4
            d.ellipse((ix - 10, iy - 10, ix + 10, iy + 10),
                      outline=(255, 201, 91, 240), width=3)
            d.ellipse((ix - 5, iy - 5, ix + 5, iy + 5), fill=(255, 248, 195, 240))
            for dx, dy in ((-12, -8), (12, -9), (-10, 11), (11, 10)):
                d.line((ix + dx, iy + dy, ix + dx * 1.65, iy + dy * 1.65),
                       fill=(255, 224, 131, 255), width=2)
    return image


def make_sprite_sheet():
    max_frame_count = max(ACTION_FRAME_COUNTS.values())
    sheet = Image.new('RGBA', (max_frame_count * CELL, len(ACTIONS) * CELL), (0, 0, 0, 0))
    # Rows have different active frame counts; unused cells at row ends stay transparent.
    for row, action in enumerate(ACTIONS):
        for frame in range(ACTION_FRAME_COUNTS[action]):
            sheet.alpha_composite(
                make_knight_frame(action, frame, ACTION_FRAME_COUNTS[action]),
                (frame * CELL, row * CELL),
            )
    sheet.save(HERE / 'fantasy_knight_spritesheet.png')


def make_variable_atlas():
    """Pack tightly cropped, variable-sized frames and save their atlas metadata."""
    padding = 4
    atlas_width = 768
    x = y = row_height = 0
    packed_frames = []

    for action in ACTIONS:
        frame_count = ACTION_FRAME_COUNTS[action]
        for frame_index in range(frame_count):
            cell = make_knight_frame(action, frame_index, frame_count)
            bounds = cell.getchannel('A').getbbox()
            crop = cell.crop(bounds)
            width, height = crop.size
            if x + width > atlas_width:
                x = 0
                y += row_height + padding
                row_height = 0
            packed_frames.append({
                'action': action,
                'frame': frame_index,
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'source_left': bounds[0],
                'source_top': bounds[1],
                'image': crop,
            })
            x += width + padding
            row_height = max(row_height, height)

    atlas_height = y + row_height
    atlas = Image.new('RGBA', (atlas_width, atlas_height), (0, 0, 0, 0))
    frame_data = {}
    for item in packed_frames:
        atlas.alpha_composite(item.pop('image'), (item['x'], item['y']))
        action = item.pop('action')
        frame_index = item.pop('frame')
        frame_data.setdefault(action, []).append({
            'index': frame_index,
            **item,
        })

    atlas.save(HERE / 'fantasy_knight_variable_atlas.png')
    metadata = {
        'atlas_width': atlas_width,
        'atlas_height': atlas_height,
        'source_cell_width': CELL,
        'source_cell_height': CELL,
        'actions': {
            action: {
                'frame_count': ACTION_FRAME_COUNTS[action],
                'frames': frame_data[action],
            }
            for action in ACTIONS
        },
    }
    (HERE / 'fantasy_knight_frames.json').write_text(
        json.dumps(metadata, indent=2), encoding='utf-8'
    )


def make_background():
    width, height = 960, 640
    image = Image.new('RGB', (width, height), (13, 20, 48))
    pix = image.load()
    for y in range(height):
        t = y / height
        color = (int(16 + 27 * t), int(24 + 27 * t), int(58 + 29 * t))
        for x in range(width):
            pix[x, y] = color
    d = ImageDraw.Draw(image, 'RGBA')

    # Stars and moon.
    for i in range(95):
        x = (i * 137 + 31) % width
        y = (i * 71 + 17) % 340
        r = 1 + (i % 3 == 0)
        d.ellipse((x-r, y-r, x+r, y+r), fill=(217, 230, 255, 210))
    d.ellipse((730, 66, 812, 148), fill=(255, 231, 174, 255))
    d.ellipse((755, 48, 824, 125), fill=(23, 30, 65, 255))

    # Distant mountains and a castle silhouette.
    d.polygon([(0, 350), (115, 222), (220, 348), (354, 190), (515, 360), (660, 240), (820, 359), (960, 215), (960, 460), (0, 460)], fill=(37, 53, 91, 255))
    d.polygon([(0, 395), (168, 292), (302, 404), (478, 270), (630, 410), (806, 285), (960, 395), (960, 475), (0, 475)], fill=(29, 69, 78, 255))
    d.rectangle((398, 238, 568, 372), fill=(54, 58, 84, 255), outline=(22, 27, 46, 255), width=4)
    d.rectangle((421, 190, 459, 372), fill=(67, 69, 94, 255), outline=(22, 27, 46, 255), width=3)
    d.rectangle((501, 205, 544, 372), fill=(67, 69, 94, 255), outline=(22, 27, 46, 255), width=3)
    d.polygon([(412, 191), (440, 154), (468, 191)], fill=(121, 52, 64, 255), outline=(22, 27, 46, 255))
    d.polygon([(490, 207), (522, 163), (555, 207)], fill=(121, 52, 64, 255), outline=(22, 27, 46, 255))
    for wx in (434, 515):
        d.rectangle((wx, 224, wx + 8, 243), fill=(255, 207, 116, 255))
    for wx in (420, 450, 487, 530):
        d.rectangle((wx, 280, wx + 11, 301), fill=(255, 201, 111, 220))
    d.rectangle((469, 318, 497, 372), fill=(27, 34, 54, 255))

    # Forest silhouettes on both sides, leaving a clear path for the knight.
    for side in (0, 1):
        for i in range(8):
            x = i * 55 if side == 0 else width - i * 55
            top = 280 + (i % 3) * 24
            d.rectangle((x - 5, top + 70, x + 7, 480), fill=(49, 43, 51, 255))
            d.polygon([(x, top - 45), (x - 37, top + 35), (x - 19, top + 30),
                       (x - 45, top + 75), (x + 44, top + 75),
                       (x + 18, top + 31), (x + 38, top + 38)],
                      fill=(24 + i % 3 * 4, 75 + i % 2 * 8, 68, 255))
            d.polygon([(x, top - 10), (x - 22, top + 37), (x + 24, top + 37)], fill=(42, 104, 79, 255))

    # Grassy path and scattered luminous stones.
    d.rectangle((0, 474, width, height), fill=(30, 55, 53, 255))
    d.polygon([(215, 474), (745, 474), (960, 640), (0, 640)], fill=(84, 77, 69, 255))
    d.line((260, 493, 62, 640), fill=(137, 120, 92, 255), width=5)
    d.line((700, 493, 897, 640), fill=(137, 120, 92, 255), width=5)
    for i in range(34):
        x, y = (i * 149 + 57) % width, 490 + (i * 47) % 140
        d.ellipse((x, y, x + 4, y + 3), fill=(157, 202, 136, 180))
    image.save(HERE / 'fantasy_forest_background.png')


if __name__ == '__main__':
    make_sprite_sheet()
    make_variable_atlas()
    make_background()
