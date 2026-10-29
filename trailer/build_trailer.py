#!/usr/bin/env python3
"""
Build a cinematic storyboard trailer for Valley of the Forgotten Wolves.
Uses ffmpeg (via imageio-ffmpeg) to:
- Apply Ken-Burns slow zoom/pan to each key frame
- Stitch scenes with cross-fade transitions
- Add a synthesized low-frequency cinematic drone bed
- Layer the narrator VO clips in time
- Add final title card
Outputs 16:9 1080p mp4.
"""
import os, subprocess, math, wave, struct, json, sys

FFMPEG = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = "/home/user/ELFATH-STATIO/trailer"
IMG  = os.path.join(ROOT, "images")
AUD  = os.path.join(ROOT, "audio")
OUT  = os.path.join(ROOT, "build")
os.makedirs(OUT, exist_ok=True)

W, H, FPS = 1920, 1080, 24

# ---------- Scene timeline (Version A, 88s) ----------
# Each scene: image, duration (s), VO file (or None), Ken-Burns mode, hold-first-black
# KB modes: "zoom_in", "zoom_out", "pan_right", "pan_left", "tilt_up", "tilt_down", "static"
scenes = [
    # 0:00-0:08 Hook - two moons
    {"img": "scene01_two_moons.jpg",     "dur": 8.0,  "vo": "vo_01_hook.mp3",       "kb": "tilt_up",   "start_black": 1.5},
    # 0:08-0:16 Valley
    {"img": "scene02_valley.jpg",        "dur": 8.0,  "vo": "vo_02_world.mp3",      "kb": "zoom_out"},
    # 0:16-0:24 Traveler
    {"img": "scene03_protagonist.jpg",   "dur": 8.0,  "vo": "vo_03_character.mp3",  "kb": "pan_left"},
    # 0:24-0:32 Warning
    {"img": "scene04_warning.jpg",       "dur": 8.0,  "vo": "vo_04_warning.mp3",    "kb": "zoom_in"},
    # 0:32-0:40 Reality breaks
    {"img": "scene05_reality_breaks.jpg","dur": 8.0,  "vo": "vo_05_breaks.mp3",     "kb": "zoom_in",  "shake": True},
    # 0:40-0:48 Wall of names
    {"img": "scene06_discovery.jpg",     "dur": 8.0,  "vo": "vo_06_discovery.mp3",  "kb": "zoom_in"},
    # 0:48-0:56 Pack
    {"img": "scene07_nightmare.jpg",     "dur": 8.0,  "vo": "vo_07_nightmare.mp3",  "kb": "pan_right"},
    # 0:56-1:04 Escalation
    {"img": "scene08_escalation.jpg",    "dur": 8.0,  "vo": "vo_08_escalation.mp3", "kb": "zoom_in",  "fast": True},
    # 1:04-1:12 Silence
    {"img": "scene09_silence.jpg",       "dur": 8.0,  "vo": "vo_09_silence.mp3",    "kb": "static",   "silence": True},
    # 1:12-1:20 Final horror - then fade to black
    {"img": "scene10_final_horror.jpg",  "dur": 6.0,  "vo": None,                    "kb": "zoom_in",  "end_black": 2.0},
]

# Total runtime calculation
TOTAL = sum(s["dur"] for s in scenes)  # 78s for visual scenes, then book reveal 10s
BOOK_DUR = 10.0
print(f"Scene total: {TOTAL}s + book reveal {BOOK_DUR}s = {TOTAL+BOOK_DUR}s")

# ---------- Step 1: build a low-frequency drone bed (WAV) ----------
def build_drone(path, total_dur, sr=44100):
    n = int(sr * total_dur)
    samples = []
    # A low drone at 44Hz, layered with 55Hz + 82.4Hz (ominous chord), very slow amplitude envelope
    # Plus a higher shimmer that builds in second half
    import math
    for i in range(n):
        t = i / sr
        # Pressure envelope: starts low, builds, drops to SILENCE at silence scene, rebuilds
        # Silence scene sits at second 64-72
        phase_pressure = 1.0
        if 63 < t < 65:
            phase_pressure = max(0.0, 1.0 - (t - 63) / 2.0)
        elif 65 <= t <= 72:
            phase_pressure = 0.0  # total silence
        elif 72 < t < 75:
            phase_pressure = min(0.8, (t - 72) / 3.0) * 0.6
        else:
            # Slow crescendo
            phase_pressure = 0.25 + 0.55 * min(1.0, t / 55.0)

        # Fade in
        if t < 2.0:
            phase_pressure *= t / 2.0

        # Fade out at end (after book reveal ends)
        fade_start = total_dur - 3.0
        if t > fade_start:
            phase_pressure *= max(0.0, 1.0 - (t - fade_start) / 3.0)

        # Heartbeat pulse in last 16s (silence + final horror)
        pulse = 0.0
        if t >= 55:
            beat_freq = 1.1 if t < 72 else 0.7  # slower in final scene
            beat_phase = (t * beat_freq) % 1.0
            if beat_phase < 0.08:
                pulse = math.sin(beat_phase / 0.08 * math.pi) * 0.35

        # Slow LFO
        lfo = 0.5 + 0.5 * math.sin(2*math.pi*0.07*t)
        s  = 0.50 * math.sin(2*math.pi*44*t + 0.3*lfo)
        s += 0.35 * math.sin(2*math.pi*55*t + 0.2*math.sin(2*math.pi*0.05*t))
        s += 0.22 * math.sin(2*math.pi*82.4*t)
        s += 0.10 * math.sin(2*math.pi*110*t)  # harmonic
        s += pulse * math.sin(2*math.pi*35*t)  # sub kick

        # Soft distortion for "growl"
        s = math.tanh(s * 0.9) * 0.5
        s *= phase_pressure * 0.35

        # Fade to silence over 2 seconds at 64s (hard cut after ramp)
        samples.append(int(s * 32767))

    with wave.open(path, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b''.join(struct.pack('<h', s) for s in samples))

drone_path = os.path.join(OUT, "drone.wav")
build_drone(drone_path, TOTAL + BOOK_DUR)
print(f"[drone] {drone_path}")

# ---------- Step 2: build title-card image from book cover ----------
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import glob

cover_src = os.path.join(ROOT, "book_cover.jpg")
title_path = os.path.join(OUT, "title_card.jpg")
cover = Image.open(cover_src).convert("RGB")
# Fit cover into 1920x1080 with dark letterbox + text
card = Image.new("RGB", (W, H), (6, 8, 14))
# Scale cover to center with breathing room
cw, ch = cover.size
scale = min(W*0.55 / cw, H*0.9 / ch)
nw, nh = int(cw*scale), int(ch*scale)
cover_r = cover.resize((nw, nh), Image.LANCZOS)
# Apply vignette-ish glow behind cover
glow = Image.new("RGB", (W, H), (0,0,0))
gd = ImageDraw.Draw(glow)
cx, cy = W//2, H//2 - 30
gd.ellipse((cx-450, cy-350, cx+450, cy+350), fill=(40, 50, 80))
glow = glow.filter(ImageFilter.GaussianBlur(80))
# Additive blend glow onto dark card
card_pix = card.load(); glow_pix = glow.load()
for y in range(H):
    for x in range(W):
        r,g,b = card_pix[x,y]
        gr,gg,gb = glow_pix[x,y]
        card_pix[x,y] = (min(255,r+gr//3), min(255,g+gg//3), min(255,b+gb//3))
card.paste(cover_r, (W//2 - nw//2, H//2 - nh//2 - 60))

# Add text - look for a font that supports Arabic
import subprocess as sp
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
for p in ["/usr/share/fonts", "/usr/local/share/fonts"]:
    for root, dirs, files in os.walk(p):
        for f in files:
            if f.lower().endswith(".ttf") and ("arab" in f.lower() or "noto" in f.lower() and "arab" in f.lower()):
                font_paths.insert(0, os.path.join(root,f))
print("Fonts found:", font_paths[:5])

try:
    font_big = ImageFont.truetype(font_paths[0], 72)
    font_med = ImageFont.truetype(font_paths[0], 44)
    font_sm  = ImageFont.truetype(font_paths[0], 32)
except Exception as e:
    print("font load failed, default", e)
    font_big = ImageFont.load_default()
    font_med = font_big; font_sm = font_big

draw = ImageDraw.Draw(card)
# English title (safer than depending on Arabic font availability in PIL)
title = "VALLEY OF THE FORGOTTEN WOLVES"
sub   = "LAND OF ZIKOLA · BOOK 3"
auth  = "Amr Abdel Hamid"
tag   = "\"They know your name.\""
cta   = "AVAILABLE NOW"
subcta= "Read the terrifying story"

def center_text(text, y, font, fill):
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, y), text, font=font, fill=fill)

y = H - nh//2 - 60 + nh + 20
center_text(sub, y, font_sm, (180,200,220)); y += 48
center_text(title, y, font_big, (230,235,240)); y += 86
center_text(auth, y, font_med, (180,200,220)); y += 56
center_text(tag, y, font_sm, (140,160,180)); y += 46
center_text(cta, y, font_big, (255, 100, 60)); y += 80
center_text(subcta, y, font_sm, (200,200,200))

# Subtle vignette overlay
vig = Image.new("L", (W,H), 0)
vd = ImageDraw.Draw(vig)
for i in range(60):
    alpha = int(200 * (i/60)**2)
    vd.rectangle((i, i, W-i, H-i), outline=alpha)
card.putalpha(255)  # ensure RGBA for composite
vig_inv = Image.eval(vig, lambda a: 255 - a)
black_vig = Image.new("RGB", (W,H), (0,0,0))
card = Image.composite(card, black_vig, vig_inv)

card.convert("RGB").save(title_path, quality=92)
print(f"[title card] {title_path}")

# ---------- Step 3: render each scene to a video clip with Ken Burns ----------
def ken_burns_filter(dur, mode, fps, fast=False, shake=False):
    """Returns an ffmpeg filter chain producing slow zoom/pan on the input."""
    # Start and end zoom factors
    speed = 1.0 if not fast else 1.6
    z_start = 1.0
    z_end = 1.18 if mode in ("zoom_in",) else (0.95 if mode == "zoom_out" else 1.08)
    # We'll use the 'zoompan' filter for pan/zoom, combined with a scale.
    # Simpler approach: use zoompan with zoom expression and x/y expressions.
    n_frames = int(dur * fps)
    # zoom expression: linear interpolation over frames
    z_expr = f"'if(eq(on,1),{z_start},{z_start}+({z_end}-{z_start})*on/{n_frames})'"
    # Pan offsets to keep subject centered; adjust per mode
    if mode == "tilt_up":
        x_expr = "'iw/2-(iw/zoom/2)'"
        y_expr = f"'ih-(ih/zoom)-on*ih/{n_frames}/3'"
    elif mode == "pan_left":
        x_expr = f"'(iw-iw/zoom)*on/{n_frames}'"
        y_expr = "'ih/2-(ih/zoom/2)'"
    elif mode == "pan_right":
        x_expr = f"'(iw-iw/zoom)*(1-on/{n_frames})'"
        y_expr = "'ih/2-(ih/zoom/2)'"
    elif mode == "zoom_out":
        # swap z to start closer, end wide
        z_lo, z_hi = 1.20, 1.0
        z_expr = f"'{z_lo}+({z_hi}-{z_lo})*on/{n_frames}'"
        x_expr = "'iw/2-(iw/zoom/2)'"
        y_expr = "'ih/2-(ih/zoom/2)'"
    else:  # zoom_in / static
        x_expr = "'iw/2-(iw/zoom/2)'"
        y_expr = "'ih/2-(ih/zoom/2)'"

    filt = (f"scale=3840:2160:flags=lanczos,"
            f"zoompan=z={z_expr}:x={x_expr}:y={y_expr}:d={n_frames}:s={W+40}x{H+40}:fps={fps}")
    if shake:
        # Add subtle camera shake using 'n' (frame counter after zoompan)
        filt += ",crop=w="+str(W)+":h="+str(H)+f":x=20+15*sin(2*PI*n/8):y=20+15*sin(2*PI*n/13)"
    else:
        filt += f",crop={W}:{H}"
    # Slight contrast / grade: push teal shadows, warm highlights
    filt += (",eq=contrast=1.08:saturation=0.85:brightness=-0.02,"
             "curves=r='0/0 0.25/0.20 0.75/0.78 1/1':"
                     "g='0/0 0.25/0.22 0.75/0.75 1/1':"
                     "b='0/0 0.25/0.30 0.75/0.75 1/1'")
    # Subtle film grain
    filt += ",noise=c0s=6:c0f=t+u"
    return filt, n_frames

clip_paths = []
for idx, s in enumerate(scenes):
    img_path = os.path.join(IMG, s["img"])
    clip_out = os.path.join(OUT, f"clip_{idx:02d}.mp4")
    filt, n_frames = ken_burns_filter(s["dur"], s["kb"], FPS, s.get("fast", False), s.get("shake", False))
    # If VO exists, mux silence + VO so the clip carries audio we can later merge
    vo_file = s.get("vo")
    if vo_file and os.path.exists(os.path.join(AUD, vo_file)):
        # Concat approach: combine VO with matching video duration as silent bed
        # Simpler: render video only, we'll mix audio globally later
        pass
    cmd = [
        FFMPEG, "-y", "-loop", "1", "-i", img_path,
        "-t", str(s["dur"]),
        "-vf", filt,
        "-an",  # no audio here; we add globally
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        clip_out,
    ]
    print(f"[scene {idx}] {s['img']} ({s['dur']}s, {s['kb']})")
    r = sp.run(cmd, capture_output=True)
    if r.returncode != 0:
        print("FFMPEG ERR:", r.stderr.decode()[-1000:])
        sys.exit(1)
    clip_paths.append(clip_out)

# Render title clip (slow zoom in on book card)
title_clip = os.path.join(OUT, "clip_title.mp4")
n_frames = int(BOOK_DUR * FPS)
filt = (f"scale=3840:2160:flags=lanczos,"
        f"zoompan=z='1+0.12*on/{n_frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={n_frames}:s={W}x{H}:fps={FPS}")
cmd = [FFMPEG, "-y", "-loop", "1", "-i", title_path, "-t", str(BOOK_DUR),
       "-vf", filt, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
       "-pix_fmt", "yuv420p", "-r", str(FPS), title_clip]
sp.run(cmd, check=True, capture_output=True)
clip_paths.append(title_clip)

# ---------- Step 4: build silence clip for the 2s pre-hook black ----------
black_clip = os.path.join(OUT, "clip_black.mp4")
cmd = [FFMPEG, "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d=1.5",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", black_clip]
sp.run(cmd, check=True, capture_output=True)

# Build a black-out clip for the "sudden silence" cut? We'll instead splice a 2s black
# between clip 7 (escalation) and clip 8 (silence).
black2 = os.path.join(OUT, "clip_black2.mp4")
cmd = [FFMPEG, "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d=2.0",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", black2]
sp.run(cmd, check=True, capture_output=True)

# Build end black (0.5s) after book reveal
black_end = os.path.join(OUT, "clip_black_end.mp4")
cmd = [FFMPEG, "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d=1.0",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", black_end]
sp.run(cmd, check=True, capture_output=True)

# ---------- Step 5: concat with crossfades using xfade filter ----------
# Build ordered clip list with black insertions
ordered = [black_clip] + clip_paths[:8] + [black2] + clip_paths[8:10] + [clip_paths[10]] + [black_end]

# Concat via ffmpeg concat demuxer for simplicity (no xfade on first pass; will add simple fade in/out per clip)
list_file = os.path.join(OUT, "concat.txt")
with open(list_file, "w") as f:
    for c in ordered:
        f.write(f"file '{c}'\n")

concat_v = os.path.join(OUT, "video_only.mp4")
cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", list_file,
       "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", concat_v]
sp.run(cmd, check=True, capture_output=True)
print(f"[concat video] {concat_v}")

# ---------- Step 6: mix VO tracks onto drone ----------
# We need to know final total video duration.
total_dur_out = TOTAL + BOOK_DUR + 1.5 + 2.0 + 1.0  # black intro + black2 + black end
print(f"Final duration: {total_dur_out}s")

# Build VO mix: place each VO at its time offset
# Offsets (seconds into final timeline):
# Black intro: 1.5s
# Then scenes start at t=1.5
# Scene 0 (hook)   : VO at 1.5+3 = 4.5 (let VO start ~3s into hook scene, after the initial look)
# Scene 1 (valley) : starts 1.5+8  = 9.5, VO at 9.5+2
# Scene 2 (trav)   : starts 17.5,   VO at 17.5+1
# Scene 3 (warning): starts 25.5,   VO at 25.5+1
# Scene 4 (breaks) : starts 33.5,   VO at 33.5+1
# Scene 5 (names)  : starts 41.5,   VO at 41.5+2
# Scene 6 (pack)   : starts 49.5,   VO at 49.5+1
# Scene 7 (esc)    : starts 57.5,   VO at 57.5+1
# black2: 65.5-67.5
# Scene 8 (silence): starts 67.5,   VO at 67.5+5 ("you thought you were alone" after stillness)
# Scene 9 (final)  : starts 75.5,   no VO (whisper as text-on-screen)
# Title clip       : starts 81.5,   VO at 81.5+1 (final CTA)

vo_timeline = [
    ("vo_01_hook.mp3",       4.5),
    ("vo_02_world.mp3",      11.0),
    ("vo_03_character.mp3",  18.0),
    ("vo_04_warning.mp3",    26.0),
    ("vo_05_breaks.mp3",     34.0),
    ("vo_06_discovery.mp3",  42.5),
    ("vo_07_nightmare.mp3",  50.5),
    ("vo_08_escalation.mp3", 58.5),
    ("vo_09_silence.mp3",    72.5),
    ("vo_10_final.mp3",      83.0),
]

# Build an ffmpeg command that takes drone as 0, each VO as -i 1..N, and amixes them with adelay
inputs = ["-i", drone_path]
filter_parts = []
for i,(vo,off) in enumerate(vo_timeline):
    inputs += ["-i", os.path.join(AUD, vo)]
    delay_ms = int(off*1000)
    filter_parts.append(f"[{i+1}:a]adelay={delay_ms}|{delay_ms},apad[a{i}];")
# Mix all: drone + all VOs
mix_inputs = "[0:a]" + "".join(f"[a{i}]" for i in range(len(vo_timeline)))
filter_parts.append(f"{mix_inputs}amix=inputs={1+len(vo_timeline)}:duration=first:dropout_transition=2[aout];")
filter_parts.append(f"[aout]loudnorm=I=-16:TP=-2:LRA=11[aout]")
af = "".join(filter_parts)

mixed_audio = os.path.join(OUT, "mixed_audio.m4a")
cmd = [FFMPEG, "-y"] + inputs + [
    "-filter_complex", af,
    "-map", "[aout]",
    "-c:a", "aac", "-b:a", "192k",
    mixed_audio,
]
r = sp.run(cmd, capture_output=True)
if r.returncode != 0:
    print("AUDIO MIX ERR:", r.stderr.decode()[-2000:])
    sys.exit(1)
print(f"[audio mix] {mixed_audio}")

# ---------- Step 7: mux final video + audio ----------
final_path = os.path.join(ROOT, "ValleyOfTheForgottenWolves_Trailer.mp4")
cmd = [FFMPEG, "-y", "-i", concat_v, "-i", mixed_audio,
       "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
       "-shortest", final_path]
sp.run(cmd, check=True, capture_output=True)
print(f"\n[FINAL] {final_path}")
print(f"Size: {os.path.getsize(final_path)/1024/1024:.1f} MB")
