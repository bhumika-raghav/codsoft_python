krishna_premium_video.py
# Original Python recreation inspired by the visual style in the reference:
# Krishna + glowing Earth + cosmic background + particles + cinematic camera motion.
#
# Install:
#   pip install pillow opencv-python numpy
#
# Run:
#   python krishna_premium_video.py
#
# Output:
#   krishna_premium.mp4   (1080x1920, 9:16)

import math
import random
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
FPS = 30
SECONDS = 12
TOTAL = FPS * SECONDS
random.seed(42)

OUT = "krishna_premium.mp4"

# ---------- helpers ----------

def lerp(a, b, t):
    return a + (b - a) * t

def glow_layer(base, draw_fn, blur=25):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_fn(d)
    glow = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base, glow), layer

# ---------- cosmic background ----------

def make_background():
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]

    # Cinematic blue/purple radial gradient
    cx, cy = 0.52, 0.40
    dist = np.sqrt(((x - cx) / 0.75) ** 2 + ((y - cy) / 0.80) ** 2)
    glow = np.clip(1 - dist, 0, 1)

    r = 3 + 12 * glow
    g = 10 + 35 * glow
    b = 28 + 75 * glow

    arr = np.dstack([r.repeat(H, 0), g.repeat(W, 1), b.repeat(W, 1)])
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB").convert("RGBA")

BG = make_background()

# Stars are deterministic so the animation is stable.
stars = []
for _ in range(520):
    stars.append({
        "x": random.randint(0, W - 1),
        "y": random.randint(0, H - 1),
        "r": random.choice([1, 1, 1, 2, 2, 3]),
        "speed": random.uniform(0.2, 1.4),
        "phase": random.uniform(0, math.tau),
    })

# ---------- Earth ----------

def earth_layer(t):
    # Earth center and radius. Slight vertical camera movement gives depth.
    ex = W * 0.50
    ey = H * 0.91 + math.sin(t * 0.7) * 10
    R = W * 0.39

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    a = np.zeros((H, W, 4), dtype=np.uint8)

    yy, xx = np.ogrid[:H, :W]
    dx = xx - ex
    dy = yy - ey
    inside = dx * dx + dy * dy <= R * R

    # Spherical shading
    z = np.zeros_like(dx, dtype=np.float32)
    z[inside] = np.sqrt(np.maximum(R * R - dx[inside] ** 2 - dy[inside] ** 2, 0))
    nx = np.zeros_like(dx, dtype=np.float32)
    ny = np.zeros_like(dy, dtype=np.float32)
    nz = np.zeros_like(z)
    nx[inside] = dx[inside] / R
    ny[inside] = dy[inside] / R
    nz[inside] = z[inside] / R

    # Moving procedural "continents" / clouds.
    lon = np.arctan2(nx, nz + 1e-6) + t * 0.10
    lat = np.arcsin(np.clip(ny, -1, 1))

    n1 = (np.sin(lon * 5.0 + lat * 3.2) +
          np.sin(lon * 11.0 - lat * 5.0) * 0.45 +
          np.sin(lon * 19.0 + lat * 8.0) * 0.20) / 1.65

    clouds = (np.sin(lon * 18 + lat * 12 + t * 0.7) +
              np.sin(lon * 31 - lat * 9)) * 0.25

    ocean = np.clip(0.72 + 0.20 * nz, 0, 1)
    land = np.clip((n1 - 0.28) * 2.2, 0, 1)
    cloud = np.clip(clouds + 0.35, 0, 1) * 0.42

    rr = 5 + 20 * ocean + 18 * land + 28 * cloud
    gg = 35 + 85 * ocean + 58 * land + 50 * cloud
    bb = 75 + 125 * ocean + 30 * land + 45 * cloud

    # Rim lighting
    rim = np.clip((1 - nz) * 1.8, 0, 1)
    rr += 20 * rim
    gg += 40 * rim
    bb += 80 * rim

    a[inside, 0] = np.clip(rr[inside], 0, 255)
    a[inside, 1] = np.clip(gg[inside], 0, 255)
    a[inside, 2] = np.clip(bb[inside], 0, 255)
    a[inside, 3] = 255

    earth = Image.fromarray(a, "RGBA")

    # Atmosphere glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((ex-R-15, ey-R-15, ex+R+15, ey+R+15),
               outline=(80, 180, 255, 170), width=12)
    glow = glow.filter(ImageFilter.GaussianBlur(22))

    return glow, earth

# ---------- Krishna vector figure ----------

def krishna_layer(t):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Floating position / subtle breathing.
    bob = math.sin(t * 2.0) * 7
    cx = W * 0.50
    top = H * 0.17 + bob
    s = W / 1080.0

    # Aura behind Krishna
    aura = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ad = ImageDraw.Draw(aura)
    for rr, aa in [(190, 35), (155, 55), (125, 75)]:
        ad.ellipse((cx-rr, top-rr, cx+rr, top+rr),
                   fill=(80, 190, 255, aa))
    aura = aura.filter(ImageFilter.GaussianBlur(45))
    layer = Image.alpha_composite(layer, aura)
    d = ImageDraw.Draw(layer)

    # Colors â visible blue skin rather than a black silhouette.
    skin = (45, 125, 205, 255)
    skin_light = (75, 165, 235, 255)
    gold = (245, 190, 70, 255)
    gold_hi = (255, 225, 125, 255)
    dhoti = (245, 218, 145, 255)
    dark_blue = (20, 55, 105, 255)
    hair = (15, 20, 35, 255)

    # Head
    head_r = 52 * s
    d.ellipse((cx-head_r, top-head_r, cx+head_r, top+head_r),
              fill=skin, outline=(130, 205, 255, 255), width=max(2, int(3*s)))

    # Hair
    d.pieslice((cx-head_r, top-head_r-8*s, cx+head_r, top+25*s),
               180, 360, fill=hair)

    # Tilak
    d.line((cx, top-25*s, cx, top-5*s), fill=(255, 240, 220, 255), width=max(2, int(4*s)))

    # Peacock feather
    feather = [(cx+8*s, top-45*s),
               (cx+20*s, top-105*s),
               (cx+35*s, top-135*s),
               (cx+42*s, top-95*s),
               (cx+28*s, top-58*s)]
    d.polygon(feather, fill=(30, 150, 90, 255))
    d.ellipse((cx+27*s, top-112*s, cx+48*s, top-91*s), fill=(30, 120, 200, 255))
    d.ellipse((cx+33*s, top-106*s, cx+43*s, top-96*s), fill=(20, 30, 70, 255))

    # Neck
    d.rounded_rectangle((cx-18*s, top+35*s, cx+18*s, top+70*s),
                        radius=10*s, fill=skin)

    # Torso
    d.polygon([(cx-45*s, top+62*s),
               (cx+45*s, top+62*s),
               (cx+65*s, top+185*s),
               (cx-65*s, top+185*s)],
              fill=skin)

    # Yellow/gold cloth across torso
    d.polygon([(cx-40*s, top+72*s),
               (cx+42*s, top+70*s),
               (cx+28*s, top+112*s),
               (cx-30*s, top+116*s)],
              fill=gold)

    # Arms â flute-playing pose
    d.line((cx-35*s, top+75*s, cx-105*s, top+105*s),
           fill=skin_light, width=int(22*s))
    d.line((cx+35*s, top+75*s, cx+92*s, top+55*s),
           fill=skin_light, width=int(22*s))

    # Hands
    d.ellipse((cx-118*s, top+95*s, cx-92*s, top+121*s), fill=skin_light)
    d.ellipse((cx+82*s, top+42*s, cx+108*s, top+68*s), fill=skin_light)

    # Flute
    d.line((cx-105*s, top+87*s, cx+105*s, top+58*s),
           fill=gold_hi, width=max(3, int(7*s)))
    for k in [-65, -30, 5, 40, 75]:
        x = cx + k*s
        y = top + (87 - k*0.14)*s
        d.ellipse((x-3*s, y-3*s, x+3*s, y+3*s), fill=(120, 75, 20, 255))

    # Waist sash
    d.polygon([(cx-55*s, top+170*s),
               (cx+55*s, top+170*s),
               (cx+35*s, top+205*s),
               (cx-35*s, top+205*s)],
              fill=gold)

    # Dhoti
    d.polygon([(cx-55*s, top+190*s),
               (cx+55*s, top+190*s),
               (cx+78*s, top+300*s),
               (cx+20*s, top+340*s),
               (cx, top+250*s),
               (cx-20*s, top+340*s),
               (cx-78*s, top+300*s)],
              fill=dhoti)

    # Dhoti folds
    for off in [-45, -20, 20, 45]:
        d.line((cx+off*s, top+205*s,
                cx+off*0.65*s, top+320*s),
               fill=(185, 150, 80, 180), width=max(2, int(3*s)))

    # Scarf / stole
    d.line((cx-52*s, top+85*s, cx-100*s, top+245*s),
           fill=(40, 100, 175, 230), width=max(7, int(18*s)))
    d.line((cx+52*s, top+85*s, cx+112*s, top+245*s),
           fill=(40, 100, 175, 230), width=max(7, int(18*s)))

    # Anklets / feet
    d.ellipse((cx-62*s, top+327*s, cx-20*s, top+345*s), fill=skin_light)
    d.ellipse((cx+20*s, top+327*s, cx+62*s, top+345*s), fill=skin_light)
    d.arc((cx-70*s, top+320*s, cx-15*s, top+350*s), 0, 180,
          fill=gold_hi, width=max(2, int(4*s)))
    d.arc((cx+15*s, top+320*s, cx+70*s, top+350*s), 0, 180,
          fill=gold_hi, width=max(2, int(4*s)))

    # Jewelry highlights
    d.ellipse((cx-8*s, top+53*s, cx+8*s, top+69*s), fill=gold_hi)
    d.arc((cx-48*s, top+45*s, cx+48*s, top+95*s), 10, 170,
          fill=gold_hi, width=max(2, int(4*s)))

    return layer

# ---------- frame ----------

def make_frame(frame_no):
    t = frame_no / FPS

    img = BG.copy()

    # Animated star field / parallax
    star_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(star_layer)

    for st in stars:
        x = (st["x"] + t * st["speed"] * 18) % W
        y = (st["y"] + t * st["speed"] * 5) % H
        pulse = 0.55 + 0.45 * math.sin(t * 2.2 + st["phase"])
        alpha = int(80 + 170 * pulse)
        r = st["r"]
        sd.ellipse((x-r, y-r, x+r, y+r), fill=(210, 235, 255, alpha))

    img = Image.alpha_composite(img, star_layer)

    # Central cosmic nebula
    neb = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nd = ImageDraw.Draw(neb)
    for i in range(9):
        rr = 80 + i * 34
        aa = max(5, 55 - i * 5)
        nd.ellipse((W*.5-rr, H*.38-rr, W*.5+rr, H*.38+rr),
                   fill=(55, 145, 235, aa))
    neb = neb.filter(ImageFilter.GaussianBlur(60))
    img = Image.alpha_composite(img, neb)

    # Earth
    earth_glow, earth = earth_layer(t)
    img = Image.alpha_composite(img, earth_glow)
    img = Image.alpha_composite(img, earth)

    # Krishna
    krishna = krishna_layer(t)
    img = Image.alpha_composite(img, krishna)

    # Foreground floating particles
    p = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(p)
    for i in range(55):
        x = (i * 137 + t * (15 + i % 8)) % W
        y = (i * 71 - t * (10 + i % 5)) % H
        rr = 1 + (i % 3)
        pd.ellipse((x-rr, y-rr, x+rr, y+rr),
                   fill=(120, 220, 255, 120))
    img = Image.alpha_composite(img, p)

    # Cinematic vignette
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    dx = (xx - W/2) / (W/2)
    dy = (yy - H/2) / (H/2)
    vignette = 1 - 0.42 * np.clip((dx*dx + dy*dy) / 1.7, 0, 1)
    arr *= vignette[..., None]

    # Subtle film-like exposure breathing
    exposure = 0.96 + 0.04 * math.sin(t * 0.45)
    arr *= exposure

    return np.clip(arr, 0, 255).astype(np.uint8)

# ---------- render ----------

def main():
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(OUT, fourcc, FPS, (W, H))

    if not writer.isOpened():
        raise RuntimeError("Could not open video writer. Try installing/reinstalling opencv-python.")

    print(f"Rendering {SECONDS}s video...")
    for i in range(TOTAL):
        frame = make_frame(i)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        writer.write(frame_bgr)

        if (i + 1) % FPS == 0:
            print(f"{i + 1}/{TOTAL} frames")

    writer.release()
    print(f"Done: {OUT}")

if __name__ == "__main__":
    main()