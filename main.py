import os
import json
import random
import math
import pygame

# ============================================================
# ATSARA OS ADVENTURE
# Bhutan-inspired educational operating systems adventure
# ============================================================

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1100, 700
FPS = 60
WORLD_W, WORLD_H = 2200, 1400

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(ROOT, "assets")
MUSIC = os.path.join(ASSET, "music")

SAVE_FILE = os.path.join(ROOT, "os_adventure_save.json")

# ============================================================
# MUSIC FILE
# ============================================================

WORLD_MUSIC = os.path.join(MUSIC, "world_music.mp3")

music_volume = 0.45
music_muted = False

# ============================================================
# DISPLAY
# ============================================================

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atsara OS Adventure")
clock = pygame.time.Clock()

# ============================================================
# COLOURS
# ============================================================

WHITE = (255, 255, 255)
BLACK = (20, 25, 35)
DARK = (24, 34, 47)
PANEL = (35, 49, 66)

GOLD = (255, 205, 75)
GREEN = (85, 205, 120)
RED = (230, 65, 65)
BLUE = (65, 135, 245)
GREY = (170, 180, 190)

# ============================================================
# FONTS
# ============================================================

font = pygame.font.SysFont("arial", 20)
small_font = pygame.font.SysFont("arial", 16)
medium_font = pygame.font.SysFont("arial", 27, bold=True)
large_font = pygame.font.SysFont("arial", 40, bold=True)

# ============================================================
# MUSIC SYSTEM
# ============================================================

def play_world_music():
    global music_muted

    if not os.path.isfile(WORLD_MUSIC):
        print("Music not found:", WORLD_MUSIC)
        return

    try:
        pygame.mixer.music.load(WORLD_MUSIC)

        if music_muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(music_volume)

        # -1 means loop forever
        pygame.mixer.music.play(-1)

        print("World music started.")

    except pygame.error as error:
        print("Could not play music:", error)


def update_music_volume():
    if music_muted:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(music_volume)


def toggle_music():
    global music_muted

    music_muted = not music_muted
    update_music_volume()


def increase_music_volume():
    global music_volume

    music_volume = min(1.0, music_volume + 0.05)
    update_music_volume()


def decrease_music_volume():
    global music_volume

    music_volume = max(0.0, music_volume - 0.05)
    update_music_volume()


# ============================================================
# ASSETS
# ============================================================

def load_image(filename, alpha=False):
    path = os.path.join(ASSET, filename)

    if not os.path.isfile(path):
        print("Image not found:", path)
        return None

    try:
        image = pygame.image.load(path)

        if alpha:
            return image.convert_alpha()

        return image.convert()

    except pygame.error as error:
        print("Could not load", filename, error)
        return None


def load_sprite_frames(filename, columns=5, rows=5):
    path = os.path.join(ASSET, filename)

    if not os.path.isfile(path):
        print("Sprite not found:", path)
        return []

    try:
        sheet = pygame.image.load(path).convert_alpha()

    except pygame.error as error:
        print("Could not load sprite:", filename, error)
        return []

    sheet_w, sheet_h = sheet.get_size()

    cell_w = sheet_w // columns
    cell_h = sheet_h // rows

    frames = []

    for row in range(rows):

        for col in range(columns):

            rect = pygame.Rect(
                col * cell_w,
                row * cell_h,
                cell_w,
                cell_h
            )

            frame = sheet.subsurface(rect).copy()

            bounds = frame.get_bounding_rect(min_alpha=1)

            if bounds.width and bounds.height:
                frames.append(
                    frame.subsurface(bounds).copy()
                )

    print(
        f"Loaded {len(frames)} frames from {filename}"
    )

    return frames


# ============================================================
# CHARACTER SPRITES
# ============================================================

atsara_frames = load_sprite_frames(
    "Atsara-idle-trimmed.png",
    5,
    5
)

aup_idle_frames = load_sprite_frames(
    "Aup Bokto-idle-trimmed.png",
    5,
    5
)

aup_walk_frames = load_sprite_frames(
    "aup_bokto_walk.png",
    5,
    4
)

aup_run_frames = load_sprite_frames(
    "aup_bokto_run.png",
    5,
    5
)

# ============================================================
# WORLD IMAGES
# ============================================================

forest_bg = load_image("forest.jpe")

forest_world_bg = None

if forest_bg:
    source_w, source_h = forest_bg.get_size()
    scale = max(
        WORLD_W / source_w,
        WORLD_H / source_h
    )
    scaled_size = (
        round(source_w * scale),
        round(source_h * scale)
    )
    scaled_forest = pygame.transform.smoothscale(
        forest_bg,
        scaled_size
    )
    crop_x = (scaled_size[0] - WORLD_W) // 2
    crop_y = (scaled_size[1] - WORLD_H) // 2
    forest_world_bg = scaled_forest.subsurface(
        (crop_x, crop_y, WORLD_W, WORLD_H)
    ).copy()

# ============================================================
# LEVEL QUESTIONS
# ============================================================

LEVELS = [

    {
        "name": "Level 1: Forest of Computer Basics",

        "lesson":
            "Discover what an operating system does.",

        "questions": [

            (
                "What does OS mean?",
                [
                    "Open Software",
                    "Operating System",
                    "Online Service",
                    "Output System"
                ],
                1
            ),

            (
                "What does an operating system do?",
                [
                    "Manage the computer's parts and programs",
                    "Print documents",
                    "Create electricity",
                    "Replace the CPU"
                ],
                0
            ),

            (
                "Which of these is an operating system?",
                [
                    "Microsoft Word",
                    "Windows",
                    "Google Chrome",
                    "PowerPoint"
                ],
                1
            ),

            (
                "Which computer part carries out instructions?",
                [
                    "Monitor",
                    "Keyboard",
                    "CPU",
                    "Printer"
                ],
                2
            ),

            (
                "What is computer hardware?",
                [
                    "Parts of a computer you can touch",
                    "A website",
                    "A password",
                    "An application"
                ],
                0
            ),

            (
                "Which device lets you enter information into a computer?",
                [
                    "Monitor",
                    "Speaker",
                    "Printer",
                    "Mouse"
                ],
                3
            ),

            (
                "What is computer software?",
                [
                    "Programs that tell a computer what to do",
                    "A cable",
                    "A screen",
                    "A desk"
                ],
                0
            ),

            (
                "Which device shows information from a computer?",
                [
                    "Keyboard",
                    "Mouse",
                    "Monitor",
                    "Scanner"
                ],
                2
            ),

            (
                "Why does a computer need an operating system?",
                [
                    "To manage the computer's parts and programs",
                    "To make rain",
                    "To replace the internet",
                    "To remove all files"
                ],
                0
            ),

            (
                "Which operating system is made for phones?",
                [
                    "Android",
                    "Excel",
                    "Photoshop",
                    "Bluetooth"
                ],
                0
            )
        ]
    },

    {
        "name": "Level 2: Chorten of Processes",

        "lesson":
            "Learn how an OS manages running programs.",

        "questions": [

            (
                "What do we call a program while it is running?",
                [
                    "A program that is running",
                    "A monitor",
                    "A cable",
                    "A printed page"
                ],
                0
            ),

            (
                "What does multitasking let an operating system do?",
                [
                    "Run several programs by sharing computer time",
                    "Deleting all programs",
                    "Turning off RAM",
                    "Using one file only"
                ],
                0
            ),

            (
                "What does the CPU scheduler choose?",
                [
                    "Which program gets CPU time next",
                    "The screen colour",
                    "The keyboard layout",
                    "The file extension"
                ],
                0
            ),

            (
                "What is a process doing when it is running?",
                [
                    "Using the CPU to run its instructions",
                    "Waiting forever",
                    "Printing by itself",
                    "Acting as hardware"
                ],
                0
            ),

            (
                "What happens when a process is finished?",
                [
                    "It stops running",
                    "It becomes a keyboard",
                    "It becomes RAM",
                    "It must always restart"
                ],
                0
            ),

            (
                "What is a process called when it is ready to run?",
                [
                    "Waiting for its turn to use the CPU",
                    "Already deleted",
                    "A broken device",
                    "A saved image"
                ],
                0
            ),

            (
                "What is a computer program?",
                [
                    "Instructions that tell a computer what to do",
                    "A computer desk",
                    "A power cable",
                    "A monitor stand"
                ],
                0
            ),

            (
                "Why does an operating system manage processes?",
                [
                    "To organize how programs use the CPU and memory",
                    "To clean the screen",
                    "To make paper",
                    "To replace the keyboard"
                ],
                0
            ),

            (
                "Can an operating system manage several processes at once?",
                [
                    "Yes",
                    "No",
                    "Only offline",
                    "Only on printers"
                ],
                0
            ),

            (
                "What is a thread inside a process?",
                [
                    "A smaller task that runs inside a process",
                    "A power supply",
                    "A screen",
                    "A folder"
                ],
                0
            )
        ]
    },

    {
        "name": "Level 3: Dzong of Memory",

        "lesson":
            "Explore RAM, ROM, storage, and memory management.",

        "questions": [

            (
                "What do the letters RAM stand for?",
                [
                    "Random Access Memory",
                    "Read Any Monitor",
                    "Rapid Application Machine",
                    "Remote Access Module"
                ],
                0
            ),

            (
                "Which type of memory loses its data when power is off?",
                [
                    "ROM",
                    "RAM",
                    "SSD",
                    "DVD"
                ],
                1
            ),

            (
                "What happens to information in RAM when power is lost?",
                [
                    "They are normally lost",
                    "They print automatically",
                    "They become permanent",
                    "They move to the mouse"
                ],
                0
            ),

            (
                "What is virtual memory used for?",
                [
                    "Using some storage space as extra memory",
                    "A type of monitor",
                    "A keyboard key",
                    "A virus"
                ],
                0
            ),

            (
                "Which is usually faster for a computer to use?",
                [
                    "RAM",
                    "Hard drive",
                    "Paper",
                    "Printer"
                ],
                0
            ),

            (
                "What do the letters ROM stand for?",
                [
                    "Read-Only Memory",
                    "Run Only Machine",
                    "Random Output Monitor",
                    "Read Online Module"
                ],
                0
            ),

            (
                "Which storage keeps data when the power is off?",
                [
                    "RAM",
                    "SSD",
                    "CPU register only",
                    "Cache only"
                ],
                1
            ),

            (
                "What does memory management mean?",
                [
                    "Giving programs memory and tracking its use",
                    "Changing wallpaper",
                    "Printing documents",
                    "Managing desk space"
                ],
                0
            ),

            (
                "Why do programs need memory while they run?",
                [
                    "To hold the information they need while running",
                    "To increase room temperature",
                    "To replace the CPU",
                    "To print paper"
                ],
                0
            ),

            (
                "What may happen if a computer runs low on RAM?",
                [
                    "The computer may slow down",
                    "The mouse disappears",
                    "The monitor becomes a CPU",
                    "Files turn into paper"
                ],
                0
            )
        ]
    },

    {
        "name": "Level 4: Bridge of Files",

        "lesson":
            "Learn how files and folders are organised.",

        "questions": [

            (
                "What does a file system do?",
                [
                    "A way the OS stores and organizes files",
                    "A CPU",
                    "A keyboard",
                    "A monitor"
                ],
                0
            ),

            (
                "Which file ending is common for a plain text file?",
                [
                    ".exe",
                    ".txt",
                    ".mp3",
                    ".png"
                ],
                1
            ),

            (
                "What is a directory, or folder, used for?",
                [
                    "A folder used to organize files",
                    "A processor",
                    "A network cable",
                    "A power supply"
                ],
                0
            ),

            (
                "Why should you back up your files?",
                [
                    "To restore files if the originals are lost",
                    "To increase screen size",
                    "To remove all folders",
                    "To change the keyboard"
                ],
                0
            ),

            (
                "What does a file path tell you?",
                [
                    "Where a file is saved",
                    "A CPU speed",
                    "A password",
                    "A monitor size"
                ],
                0
            ),

            (
                "Which of these is a storage device?",
                [
                    "SSD",
                    "Mouse pad",
                    "Monitor stand",
                    "Keyboard key"
                ],
                0
            ),

            (
                "What happens when you copy a file?",
                [
                    "Creates another copy",
                    "Always deletes the original",
                    "Turns it into hardware",
                    "Shuts down the computer"
                ],
                0
            ),

            (
                "What is a good way to organize your files?",
                [
                    "Give files clear names so you can find them",
                    "Never save work",
                    "Delete all folders",
                    "Share every password"
                ],
                0
            ),

            (
                "What happens when you rename a file?",
                [
                    "Changes a file's name",
                    "Changes the CPU",
                    "Adds RAM",
                    "Formats the monitor"
                ],
                0
            ),

            (
                "Which device keeps data when the power is off?",
                [
                    "SSD",
                    "RAM",
                    "CPU cache",
                    "A running process"
                ],
                0
            )
        ]
    },

    {
        "name": "Level 5: Temple of Security",

        "lesson":
            "Protect computers, accounts, and personal data.",

        "questions": [

            (
                "What do we call software made to harm a computer?",
                [
                    "Software made to harm or trick you",
                    "A safe backup",
                    "A monitor",
                    "A file system"
                ],
                0
            ),

            (
                "Which password is the safest to use?",
                [
                    "Use a long password you do not reuse",
                    "Use 123456 everywhere",
                    "Share it publicly",
                    "Use your password as your username"
                ],
                0
            ),

            (
                "What is phishing, an online trick to steal information?",
                [
                    "A fake message that tricks you into sharing information",
                    "Memory management",
                    "A file extension",
                    "A CPU process"
                ],
                0
            ),

            (
                "What can antivirus software help you do?",
                [
                    "Help find harmful programs",
                    "Replace the CPU",
                    "Increase desk space",
                    "Guarantee no attacks ever"
                ],
                0
            ),

            (
                "Why should you install operating system updates?",
                [
                    "They can fix problems and security holes",
                    "They always delete files",
                    "They replace hardware",
                    "They remove the need for passwords"
                ],
                0
            ),

            (
                "What does authentication check?",
                [
                    "Checking that you are really who you say you are",
                    "Deleting a folder",
                    "Formatting a disk",
                    "Changing a wallpaper"
                ],
                0
            ),

            (
                "What should you do if a link looks suspicious?",
                [
                    "Do not open it; check with the sender first",
                    "Enter all passwords",
                    "Forward it to everyone",
                    "Disable security"
                ],
                0
            ),

            (
                "What does access control decide?",
                [
                    "Who can use files or computer features",
                    "Increasing screen brightness",
                    "Printing files",
                    "Changing the desktop picture"
                ],
                0
            ),

            (
                "Why should you keep backup copies of your files?",
                [
                    "They help you get files back if something goes wrong",
                    "They stop every attack",
                    "They replace passwords",
                    "They increase CPU speed"
                ],
                0
            ),

            (
                "What does a firewall do?",
                [
                    "Checking network data and blocking unwanted connections",
                    "Cooling the computer",
                    "Printing pages",
                    "Editing photos"
                ],
                0
            )
        ]
    },

    {
        "name": "Level 6: Monastery of Networks",

        "lesson":
            "Discover how computers communicate.",

        "questions": [

            (
                "What is a computer network?",
                [
                    "Devices linked so they can send information",
                    "A single keyboard",
                    "A file extension",
                    "A RAM chip"
                ],
                0
            ),

            (
                "What do the letters LAN stand for?",
                [
                    "Local Area Network",
                    "Large Access Number",
                    "Long Archive Node",
                    "Linked Application Name"
                ],
                0
            ),

            (
                "What does a router do?",
                [
                    "Sends data between your device and other networks",
                    "Prints documents",
                    "Executes every program",
                    "Replaces RAM"
                ],
                0
            ),

            (
                "What does Wi-Fi let a device do?",
                [
                    "Connect to a network without a cable",
                    "Permanent storage",
                    "CPU cooling",
                    "A file extension"
                ],
                0
            ),

            (
                "What is a server on a network?",
                [
                    "A computer that shares information with other computers",
                    "A mouse button",
                    "A screen resolution",
                    "A keyboard"
                ],
                0
            ),

            (
                "What does cloud computing mean?",
                [
                    "Using storage or programs over the internet",
                    "Computing inside actual clouds",
                    "Removing all servers",
                    "A type of keyboard"
                ],
                0
            ),

            (
                "What does an IP address identify?",
                [
                    "A device on a network",
                    "A keyboard key",
                    "A monitor size",
                    "A file extension"
                ],
                0
            ),

            (
                "What does bandwidth tell you about a network?",
                [
                    "How much data a network can send at one time",
                    "A keyboard length",
                    "A file name",
                    "A CPU brand"
                ],
                0
            ),

            (
                "Why should you use a secure connection?",
                [
                    "To help keep data safe while it travels online",
                    "To delete all data",
                    "To remove the OS",
                    "To replace the keyboard"
                ],
                0
            ),

            (
                "What does a network firewall do?",
                [
                    "A tool that checks and blocks some network data",
                    "A storage drive",
                    "A screen",
                    "A text file"
                ],
                0
            )
        ]
    },

    {
        "name": "Level 7: Royal OS Challenge",

        "lesson":
            "Put your operating-system knowledge to the test.",

        "questions": [

            (
                "What is a deadlock in a computer?",
                [
                    "Programs wait for each other and get stuck",
                    "A fast CPU",
                    "A folder",
                    "A display"
                ],
                0
            ),

            (
                "What is the kernel in an operating system?",
                [
                    "The main part of the OS that controls the computer",
                    "A monitor component",
                    "A keyboard",
                    "A network cable"
                ],
                0
            ),

            (
                "What is a system call?",
                [
                    "A program asking the OS to do something",
                    "A phone call to a computer",
                    "A backup",
                    "A screen saver"
                ],
                0
            ),

            (
                "What is an interrupt in a computer?",
                [
                    "A signal that tells the CPU to handle something",
                    "A folder name",
                    "A power supply",
                    "A password"
                ],
                0
            ),

            (
                "What does a device driver do?",
                [
                    "Software that helps the OS control a device",
                    "A vehicle operator",
                    "A spreadsheet",
                    "A monitor"
                ],
                0
            ),

            (
                "What does CPU scheduling decide?",
                [
                    "Choosing which program gets a turn with the CPU",
                    "Organising desktop icons",
                    "Installing a monitor",
                    "Formatting every disk"
                ],
                0
            ),

            (
                "What does open-source software mean?",
                [
                    "Software whose code people can view and sometimes change",
                    "Software with no code",
                    "Only hardware",
                    "Software that must be used offline"
                ],
                0
            ),

            (
                "Why are user accounts helpful on a shared computer?",
                [
                    "Each person can have their own files and access settings",
                    "No need for an OS",
                    "All files become public",
                    "Hardware is no longer needed"
                ],
                0
            ),

            (
                "What does an operating system provide to apps?",
                [
                    "Tools and access to the computer's hardware",
                    "Only a screen",
                    "Only a keyboard",
                    "Only electricity"
                ],
                0
            ),

            (
                "What is the main job of an operating system?",
                [
                    "Manage computer parts and help programs work",
                    "Replace every application",
                    "Eliminate all files",
                    "Act only as a web browser"
                ],
                0
            )
        ]
    }
]

LEVEL_REVIEW_NOTES = [
    [
        "An operating system manages computer parts and helps apps run.",
        "Windows, macOS, Linux, Android, and iOS are operating systems."
    ],
    [
        "A process is a program that is running.",
        "The OS shares CPU time so active programs can take turns."
    ],
    [
        "RAM holds information programs are using right now.",
        "RAM clears when power is off; SSD storage keeps saved files."
    ],
    [
        "File systems organize data into files and folders.",
        "A backup is another copy you can use if a file is lost."
    ],
    [
        "Strong, unique passwords help protect your accounts.",
        "Updates fix problems and can close security gaps."
    ],
    [
        "Networks let devices send and receive information.",
        "Routers connect local devices to other networks."
    ],
    [
        "The kernel is the core part of an operating system.",
        "Drivers help the OS control devices; system calls let apps request help."
    ]
]

# ============================================================
# GAME STATE
# ============================================================

player = pygame.Rect(180, 610, 42, 60)

atsara = pygame.Rect(150, 650, 42, 60)

# ============================================================
# LEARNING STATIONS
#
# All stations are placed along the main straight road.
# ============================================================

stations = [
    (250, 650),    # Level 1
    (550, 650),    # Level 2
    (850, 650),    # Level 3
    (1150, 650),   # Level 4
    (1450, 650),   # Level 5
    (1750, 650),   # Level 6
    (2050, 650)    # Level 7
]

WALKABLE_PATHS = [
    (842, 295),
    (1232, 350),
    (1510, 390),
    (420, 820),
    (955, 900)
]

LANDMARKS = [
    {
        "kind": "chorten",
        "x": 780,
        "y": 170,
        "width": 125,
        "height": 125,
        "name": "Chorten",
        "notes": [
            "An operating system runs each open program as a process.",
            "It shares CPU time between processes so several apps can keep working.",
            "Task Manager or Activity Monitor can show and manage running processes."
        ]
    },
    {
        "kind": "dzong",
        "x": 1170,
        "y": 160,
        "width": 125,
        "height": 190,
        "name": "Dzong",
        "notes": [
            "An operating system gives programs room in RAM while they run.",
            "It tracks memory use and helps prevent programs from overwriting one another.",
            "When RAM is full, the OS may move less-used data to storage, which is slower."
        ]
    },
    {
        "kind": "bridge",
        "x": 1460,
        "y": 425,
        "width": 100,
        "height": 225,
        "name": "Bridge",
        "notes": [
            "File systems organize data into named files and folders.",
            "The OS tracks where file data is stored and helps apps read or save it.",
            "File permissions can control who may open, change, or delete data."
        ]
    },
    {
        "kind": "chorten",
        "x": 1460,
        "y": 300,
        "width": 100,
        "height": 90,
        "name": "Note station",
        "notes": [
            "An operating system is the main software that manages a computer.",
            "It helps applications use hardware such as the CPU, memory, and storage.",
            "It also provides common services, files, security, and ways to interact with the device."
        ]
    },
    {
        "kind": "temple",
        "x": 360,
        "y": 700,
        "width": 120,
        "height": 120,
        "name": "Temple",
        "notes": [
            "Operating systems protect devices with accounts, sign-in checks, and permissions.",
            "Security updates fix weaknesses in system software.",
            "Built-in protections can help block unsafe apps and network activity."
        ]
    },
    {
        "kind": "monastery",
        "x": 900,
        "y": 745,
        "width": 110,
        "height": 165,
        "name": "Monastery",
        "notes": [
            "Network drivers help the OS communicate with Wi-Fi and Ethernet hardware.",
            "The OS manages connections and moves data using shared network protocols.",
            "Firewall and sharing settings help control how a device communicates."
        ]
    }
]

unlocked_level = 0
completed_levels = set()
crystals = 0
tutorial_seen = False

state = "title"
reset_confirmation = False

show_help = False
manual_page = 0

dialogue_lines = []
dialogue_index = 0
dialogue_return_state = "world"
dialogue_title = "ATSARA"
dialogue_marks_tutorial = False

current_level = 0

questions = []
question_index = 0

score = 0

feedback = ""
feedback_notes = []
feedback_timer = 0

walk_frame = 0
animation_timer = 0

facing_left = False
facing_up = False
facing_down = True

# ============================================================
# SAVE / LOAD
# ============================================================

def save_game():

    data = {
        "unlocked_level": unlocked_level,
        "completed_levels": sorted(completed_levels),
        "crystals": crystals,
        "tutorial_seen": tutorial_seen,
        "music_volume": music_volume,
        "music_muted": music_muted
    }

    try:

        with open(
            SAVE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=2
            )

        print("Progress saved.")

    except OSError as error:

        print(
            "Could not save progress:",
            error
        )


def load_game():

    global unlocked_level
    global completed_levels
    global crystals
    global tutorial_seen
    global music_volume
    global music_muted

    if not os.path.isfile(SAVE_FILE):
        return

    try:

        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        unlocked_level = max(
            0,
            min(
                int(
                    data.get(
                        "unlocked_level",
                        0
                    )
                ),
                len(LEVELS) - 1
            )
        )

        completed_levels = {
            int(level)

            for level in data.get(
                "completed_levels",
                []
            )

            if str(level).isdigit()
            and 0 <= int(level) < len(LEVELS)
        }

        crystals = max(
            0,
            int(
                data.get(
                    "crystals",
                    0
                )
            )
        )

        tutorial_seen = bool(
            data.get(
                "tutorial_seen",
                False
            )
        )

        music_volume = float(
            data.get(
                "music_volume",
                0.45
            )
        )

        music_volume = max(
            0.0,
            min(
                1.0,
                music_volume
            )
        )

        music_muted = bool(
            data.get(
                "music_muted",
                False
            )
        )

        print("Progress loaded.")

    except (
        OSError,
        ValueError,
        TypeError,
        json.JSONDecodeError
    ) as error:

        print(
            "Could not load progress:",
            error
        )


def reset_progress():

    global unlocked_level
    global completed_levels
    global crystals
    global tutorial_seen
    global state
    global show_help
    global manual_page
    global dialogue_lines
    global dialogue_index
    global dialogue_title
    global dialogue_marks_tutorial
    global current_level
    global questions
    global question_index
    global score
    global feedback
    global feedback_notes
    global feedback_timer
    global reset_confirmation

    unlocked_level = 0
    completed_levels.clear()
    crystals = 0
    tutorial_seen = False
    state = "title"
    show_help = False
    manual_page = 0
    dialogue_lines = []
    dialogue_index = 0
    dialogue_title = "ATSARA"
    dialogue_marks_tutorial = False
    current_level = 0
    questions = []
    question_index = 0
    score = 0
    feedback = ""
    feedback_notes = []
    feedback_timer = 0
    reset_confirmation = False
    player.topleft = (180, 610)

    save_game()


load_game()

# Start the Bhutan-inspired background music.
play_world_music()

# ============================================================
# DRAWING HELPERS
# ============================================================

def draw_text(
    text,
    x,
    y,
    colour=WHITE,
    selected_font=font
):

    image = selected_font.render(
        str(text),
        True,
        colour
    )

    screen.blit(
        image,
        (int(x), int(y))
    )


def center_text(
    text,
    y,
    colour=WHITE,
    selected_font=font
):

    image = selected_font.render(
        str(text),
        True,
        colour
    )

    screen.blit(
        image,
        (
            WIDTH // 2
            - image.get_width() // 2,
            y
        )
    )


def panel(
    rect,
    colour=PANEL,
    border=GOLD
):

    pygame.draw.rect(
        screen,
        colour,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        border,
        rect,
        2,
        border_radius=12
    )


def wrap_text(
    text,
    max_width,
    selected_font=font
):

    words = text.split()

    lines = []

    current = ""

    for word in words:

        candidate = (
            current
            + " "
            + word
        ).strip()

        if (
            selected_font.size(
                candidate
            )[0] > max_width
            and current
        ):

            lines.append(current)

            current = word

        else:

            current = candidate

    if current:
        lines.append(current)

    return lines


# ============================================================
# CHARACTER DRAWING
# ============================================================

def draw_character(
    frames,
    rect,
    camx,
    camy,
    frame_index=0,
    height=90,
    fallback=(50, 120, 240),
    flip_left=False
):

    x = int(
        rect.centerx
        - camx
    )

    y = int(
        rect.bottom
        - camy
    )

    # Character shadow
    pygame.draw.ellipse(
        screen,
        (35, 45, 30),
        (
            x - 20,
            y - 7,
            40,
            12
        )
    )

    if frames:

        frame = frames[
            frame_index
            % len(frames)
        ]

        fw, fh = frame.get_size()

        if fh > 0:

            new_w = max(
                1,
                int(
                    fw
                    * height
                    / fh
                )
            )

            image = pygame.transform.smoothscale(
                frame,
                (
                    new_w,
                    height
                )
            )

            if flip_left:

                image = pygame.transform.flip(
                    image,
                    True,
                    False
                )

            screen.blit(
                image,
                (
                    x - new_w // 2,
                    y - height
                )
            )

            return

    # Fallback character
    pygame.draw.circle(
        screen,
        fallback,
        (
            x,
            y - 70
        ),
        14
    )

    pygame.draw.rect(
        screen,
        fallback,
        (
            x - 15,
            y - 56,
            30,
            36
        ),
        border_radius=5
    )

    pygame.draw.line(
        screen,
        fallback,
        (
            x - 8,
            y - 22
        ),
        (
            x - 12,
            y - 2
        ),
        6
    )

    pygame.draw.line(
        screen,
        fallback,
        (
            x + 8,
            y - 22
        ),
        (
            x + 12,
            y - 2
        ),
        6
    )

    pygame.draw.line(
        screen,
        fallback,
        (
            x - 12,
            y - 47
        ),
        (
            x - 26,
            y - 32
        ),
        5
    )

    pygame.draw.line(
        screen,
        fallback,
        (
            x + 12,
            y - 47
        ),
        (
            x + 26,
            y - 32
        ),
        5
    )


# ============================================================
# LANDMARK DRAWING
# ============================================================

def draw_projected_box(
    x,
    y,
    width,
    height,
    depth,
    front_colour,
    side_colour,
    top_colour
):

    depth_offset = depth // 2

    pygame.draw.polygon(
        screen,
        side_colour,
        [
            (x + width, y),
            (x + width + depth, y - depth_offset),
            (x + width + depth, y + height - depth_offset),
            (x + width, y + height)
        ]
    )

    pygame.draw.polygon(
        screen,
        top_colour,
        [
            (x, y),
            (x + depth, y - depth_offset),
            (x + width + depth, y - depth_offset),
            (x + width, y)
        ]
    )

    pygame.draw.polygon(
        screen,
        front_colour,
        [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height)
        ]
    )


def draw_bhutan_roof(center_x, roof_y, width, depth, rise):

    left_x = center_x - width // 2
    right_x = center_x + width // 2
    depth_offset = depth // 2

    pygame.draw.polygon(
        screen,
        (111, 43, 35),
        [
            (center_x, roof_y),
            (right_x, roof_y + rise),
            (right_x + depth, roof_y + rise - depth_offset),
            (center_x + depth, roof_y - depth_offset)
        ]
    )

    pygame.draw.polygon(
        screen,
        (157, 53, 42),
        [
            (left_x, roof_y + rise),
            (center_x, roof_y),
            (right_x, roof_y + rise),
            (right_x - 5, roof_y + rise + 5),
            (left_x + 5, roof_y + rise + 5)
        ]
    )

    pygame.draw.line(
        screen,
        (238, 190, 83),
        (left_x + 3, roof_y + rise + 3),
        (right_x - 3, roof_y + rise + 3),
        3
    )

    pygame.draw.line(
        screen,
        (194, 139, 55),
        (right_x, roof_y + rise),
        (right_x + depth, roof_y + rise - depth_offset),
        3
    )


def draw_landmark(
    kind,
    wx,
    wy,
    w,
    h,
    camx,
    camy
):

    sx = int(
        wx - camx
    )

    sy = int(
        wy - camy
    )

    if (
        sx + w < -50
        or sx > WIDTH + 50
    ):
        return

    if (
        sy + h < -50
        or sy > HEIGHT + 50
    ):
        return

    pygame.draw.ellipse(
        screen,
        (20, 25, 18, 100),
        (
            sx + 8,
            sy + h - 27,
            w - 4,
            26
        )
    )

    center_x = sx + w // 2

    if kind in ("chorten", "temple"):
        pygame.draw.polygon(
            screen,
            (125, 77, 50),
            [
                (sx + 18, sy + h - 30),
                (sx + w - 18, sy + h - 30),
                (sx + w - 10, sy + h - 15),
                (sx + 10, sy + h - 15)
            ]
        )
        draw_projected_box(
            sx + 27,
            sy + h - 43,
            w - 54,
            12,
            12,
            (223, 204, 160),
            (142, 116, 77),
            (247, 230, 190)
        )
        draw_projected_box(
            sx + 35,
            sy + h - 53,
            w - 70,
            10,
            9,
            (238, 224, 190),
            (161, 133, 87),
            (255, 242, 207)
        )

        dome_width = int(w * 0.43)
        dome_height = int(h * 0.43)
        dome_x = center_x - dome_width // 2
        dome_y = sy + int(h * 0.30)
        pygame.draw.ellipse(
            screen,
            (174, 153, 117),
            (dome_x + 5, dome_y + 7, dome_width, dome_height)
        )
        pygame.draw.ellipse(
            screen,
            (239, 228, 198),
            (dome_x, dome_y, dome_width, dome_height)
        )
        pygame.draw.ellipse(
            screen,
            (255, 246, 220),
            (dome_x + 5, dome_y + 4, dome_width - 13, dome_height // 2)
        )
        pygame.draw.ellipse(
            screen,
            (177, 52, 43),
            (dome_x - 2, dome_y + dome_height - 13, dome_width + 4, 17)
        )
        draw_projected_box(
            center_x - 12,
            dome_y + 4,
            24,
            13,
            8,
            (211, 185, 133),
            (143, 111, 64),
            (244, 224, 174)
        )
        pygame.draw.line(
            screen,
            (226, 176, 55),
            (center_x, dome_y + 4),
            (center_x, sy + 10),
            4
        )
        for tier in range(4):
            tier_y = sy + 15 + tier * 5
            tier_width = 15 - tier * 3
            pygame.draw.ellipse(
                screen,
                (239, 193, 72),
                (
                    center_x - tier_width // 2,
                    tier_y,
                    tier_width,
                    4
                )
            )
        pygame.draw.circle(
            screen,
            (255, 220, 106),
            (center_x, sy + 9),
            4
        )

    elif kind in ("dzong", "monastery"):
        scale_x = w / 125
        scale_y = h / 190
        front_x = sx + int(25 * scale_x)
        lower_y = sy + int(95 * scale_y)
        lower_width = int(76 * scale_x)
        lower_height = int(60 * scale_y)
        depth = max(8, int(15 * scale_x))

        draw_projected_box(
            front_x,
            lower_y,
            lower_width,
            lower_height,
            depth,
            (225, 215, 187),
            (150, 117, 75),
            (246, 231, 197)
        )
        draw_projected_box(
            sx + int(37 * scale_x),
            sy + int(58 * scale_y),
            int(52 * scale_x),
            int(43 * scale_y),
            max(7, int(11 * scale_x)),
            (235, 222, 193),
            (158, 119, 72),
            (250, 235, 200)
        )

        pygame.draw.rect(
            screen,
            (157, 51, 42),
            (front_x, lower_y + int(14 * scale_y), lower_width, max(4, int(7 * scale_y)))
        )
        pygame.draw.rect(
            screen,
            (190, 146, 65),
            (front_x, lower_y + int(21 * scale_y), lower_width, max(2, int(3 * scale_y)))
        )

        for window_x in (0.34, 0.50, 0.66):
            window_width = max(5, int(8 * scale_x))
            pygame.draw.rect(
                screen,
                (95, 49, 39),
                (
                    front_x + int(lower_width * window_x) - window_width // 2,
                    lower_y + int(34 * scale_y),
                    window_width,
                    max(9, int(15 * scale_y))
                )
            )
            pygame.draw.rect(
                screen,
                (231, 190, 106),
                (
                    front_x + int(lower_width * window_x) - window_width // 2 - 2,
                    lower_y + int(33 * scale_y),
                    window_width + 4,
                    2
                )
            )

        pygame.draw.rect(
            screen,
            (110, 53, 40),
            (
                front_x + lower_width // 2 - 6,
                lower_y + lower_height - int(23 * scale_y),
                12,
                int(23 * scale_y)
            )
        )

        upper_x = sx + int(37 * scale_x)
        upper_y = sy + int(58 * scale_y)
        upper_width = int(52 * scale_x)
        for window_x in (0.35, 0.68):
            pygame.draw.rect(
                screen,
                (100, 48, 38),
                (
                    upper_x + int(upper_width * window_x) - 3,
                    upper_y + int(17 * scale_y),
                    6,
                    max(8, int(11 * scale_y))
                )
            )

        draw_bhutan_roof(
            center_x,
            sy + int(72 * scale_y),
            int(112 * scale_x),
            max(10, int(18 * scale_x)),
            max(15, int(22 * scale_y))
        )
        draw_bhutan_roof(
            center_x,
            sy + int(43 * scale_y),
            int(82 * scale_x),
            max(9, int(14 * scale_x)),
            max(13, int(18 * scale_y))
        )
        pygame.draw.line(
            screen,
            (239, 193, 77),
            (center_x, sy + int(43 * scale_y)),
            (center_x, sy + int(32 * scale_y)),
            3
        )
        pygame.draw.circle(
            screen,
            (248, 205, 91),
            (center_x, sy + int(30 * scale_y)),
            3
        )

    elif kind == "bridge":
        deck_x = sx + 23
        deck_y = sy + 7
        deck_width = w - 46
        deck_height = h - 14

        for support_y in (sy + 75, sy + 145):
            draw_projected_box(
                sx + w // 2 - 13,
                support_y,
                26,
                38,
                8,
                (126, 112, 91),
                (79, 76, 67),
                (165, 149, 121)
            )

        draw_projected_box(
            deck_x,
            deck_y,
            deck_width,
            deck_height,
            12,
            (151, 91, 52),
            (91, 54, 39),
            (190, 130, 76)
        )

        for plank_y in range(deck_y + 12, deck_y + deck_height - 3, 14):
            pygame.draw.line(
                screen,
                (112, 67, 43),
                (deck_x + 3, plank_y),
                (deck_x + deck_width - 3, plank_y),
                1
            )

        for rail_x in (deck_x - 7, deck_x + deck_width + 6):
            pygame.draw.line(
                screen,
                (112, 48, 39),
                (rail_x, deck_y + 5),
                (rail_x, deck_y + deck_height - 5),
                4
            )
            pygame.draw.line(
                screen,
                (216, 164, 85),
                (rail_x - 1, deck_y + 5),
                (rail_x - 1, deck_y + deck_height - 5),
                2
            )
            for post_y in range(deck_y + 10, deck_y + deck_height - 5, 22):
                pygame.draw.line(
                    screen,
                    (131, 57, 42),
                    (deck_x - 4, post_y),
                    (deck_x + deck_width + 4, post_y),
                    3
                )

def draw_station_icon(station_index, center_x, center_y):

    pygame.draw.circle(
        screen,
        (34, 45, 43),
        (center_x, center_y),
        21
    )

    pygame.draw.circle(
        screen,
        (226, 210, 165),
        (center_x, center_y),
        21,
        2
    )

    if station_index == 0:
        pygame.draw.polygon(
            screen,
            (68, 145, 91),
            [(center_x - 14, center_y + 10), (center_x - 7, center_y - 10), (center_x, center_y + 10)]
        )
        pygame.draw.polygon(
            screen,
            (91, 174, 105),
            [(center_x - 3, center_y + 10), (center_x + 6, center_y - 14), (center_x + 15, center_y + 10)]
        )
        pygame.draw.rect(screen, (135, 90, 55), (center_x + 4, center_y + 5, 4, 8))

    elif station_index == 1:
        pygame.draw.rect(screen, (238, 230, 205), (center_x - 11, center_y + 7, 22, 5))
        pygame.draw.ellipse(screen, (248, 242, 220), (center_x - 8, center_y - 4, 16, 13))
        pygame.draw.rect(screen, (178, 55, 48), (center_x - 5, center_y - 10, 10, 7))
        pygame.draw.line(screen, (238, 190, 62), (center_x, center_y - 10), (center_x, center_y - 17), 2)
        pygame.draw.circle(screen, (238, 190, 62), (center_x, center_y - 17), 2)

    elif station_index == 2:
        pygame.draw.rect(screen, (235, 222, 190), (center_x - 12, center_y - 2, 24, 14))
        pygame.draw.polygon(
            screen,
            (151, 54, 45),
            [(center_x - 15, center_y - 2), (center_x, center_y - 11), (center_x + 15, center_y - 2)]
        )
        pygame.draw.line(
            screen,
            (237, 191, 70),
            (center_x - 12, center_y),
            (center_x + 12, center_y),
            2
        )
        for window_x in (center_x - 7, center_x, center_x + 7):
            pygame.draw.rect(screen, (130, 48, 42), (window_x - 2, center_y + 3, 4, 5))

    elif station_index == 3:
        pygame.draw.line(screen, (220, 174, 101), (center_x - 15, center_y + 7), (center_x + 15, center_y + 7), 4)
        pygame.draw.line(screen, (150, 73, 52), (center_x - 12, center_y + 10), (center_x - 12, center_y - 4), 2)
        pygame.draw.line(screen, (150, 73, 52), (center_x + 12, center_y + 10), (center_x + 12, center_y - 4), 2)
        pygame.draw.lines(
            screen,
            (233, 202, 143),
            False,
            [(center_x - 13, center_y - 4), (center_x, center_y + 2), (center_x + 13, center_y - 4)],
            2
        )
        pygame.draw.line(screen, (150, 73, 52), (center_x - 12, center_y + 11), (center_x + 12, center_y + 11), 2)

    elif station_index == 4:
        pygame.draw.rect(screen, (238, 225, 194), (center_x - 9, center_y - 1, 18, 13))
        pygame.draw.polygon(
            screen,
            (188, 69, 48),
            [(center_x - 14, center_y - 1), (center_x, center_y - 10), (center_x + 14, center_y - 1)]
        )
        pygame.draw.line(
            screen,
            (242, 190, 67),
            (center_x - 12, center_y + 1),
            (center_x + 12, center_y + 1),
            2
        )
        pygame.draw.rect(screen, (116, 62, 45), (center_x - 2, center_y + 5, 4, 7))

    elif station_index == 5:
        pygame.draw.polygon(
            screen,
            (93, 151, 91),
            [(center_x - 17, center_y + 12), (center_x - 5, center_y + 2), (center_x + 5, center_y + 12)]
        )
        pygame.draw.rect(screen, (234, 224, 194), (center_x - 8, center_y - 5, 17, 15))
        pygame.draw.polygon(
            screen,
            (145, 52, 45),
            [(center_x - 11, center_y - 5), (center_x, center_y - 13), (center_x + 12, center_y - 5)]
        )
        pygame.draw.rect(screen, (125, 48, 42), (center_x - 4, center_y - 1, 4, 5))
        pygame.draw.rect(screen, (125, 48, 42), (center_x + 3, center_y - 1, 3, 5))

    else:
        flag_points = [
            (center_x - 13, center_y - 11),
            (center_x + 13, center_y - 11),
            (center_x + 13, center_y + 11),
            (center_x - 13, center_y + 11)
        ]
        pygame.draw.polygon(screen, (242, 190, 58), [flag_points[0], flag_points[1], flag_points[2]])
        pygame.draw.polygon(screen, (226, 112, 47), [flag_points[0], flag_points[2], flag_points[3]])
        pygame.draw.lines(
            screen,
            (250, 245, 224),
            False,
            [(center_x - 8, center_y + 6), (center_x - 2, center_y + 1), (center_x + 3, center_y + 5), (center_x + 8, center_y - 4)],
            3
        )
        pygame.draw.line(screen, (250, 245, 224), (center_x + 4, center_y - 5), (center_x + 11, center_y - 7), 2)


def draw_station_lock(center_x, center_y):

    lock_x = center_x + 9
    lock_y = center_y - 15
    outline = (35, 40, 42)
    body = (246, 235, 206)

    pygame.draw.rect(
        screen,
        body,
        (lock_x, lock_y + 5, 11, 9),
        border_radius=2
    )

    pygame.draw.lines(
        screen,
        outline,
        False,
        [
            (lock_x + 2, lock_y + 6),
            (lock_x + 2, lock_y + 3),
            (lock_x + 9, lock_y + 3),
            (lock_x + 9, lock_y + 6)
        ],
        2
    )

    pygame.draw.circle(
        screen,
        outline,
        (lock_x + 5, lock_y + 9),
        1
    )


# ============================================================
# WORLD BACKGROUND
# ============================================================

def draw_world_background(
    camx,
    camy
):

    # ========================================================
    # FOREST
    # ========================================================

    screen.fill(
        (91, 145, 93)
    )

    if forest_world_bg:
        screen.blit(
            forest_world_bg,
            (
                -camx,
                -camy
            )
        )

    else:

        screen.fill(
            (100, 155, 100)
        )

    # ========================================================
    # MAIN STRAIGHT ROAD
    # ========================================================

    road_y = 650

    # Dark road border
    pygame.draw.rect(
        screen,
        (125, 105, 75),
        (
            -camx,
            road_y - 75 - camy,
            WORLD_W,
            150
        )
    )

    # Road surface
    pygame.draw.rect(
        screen,
        (194, 165, 117),
        (
            -camx,
            road_y - 60 - camy,
            WORLD_W,
            120
        )
    )

    # Upper road edge
    pygame.draw.line(
        screen,
        (225, 200, 155),
        (
            -camx,
            road_y - 60 - camy
        ),
        (
            WORLD_W - camx,
            road_y - 60 - camy
        ),
        4
    )

    # Lower road edge
    pygame.draw.line(
        screen,
        (225, 200, 155),
        (
            -camx,
            road_y + 60 - camy
        ),
        (
            WORLD_W - camx,
            road_y + 60 - camy
        ),
        4
    )

    # Centre road markings
    for wx in range(
        0,
        WORLD_W,
        100
    ):

        pygame.draw.line(
            screen,
            (235, 215, 170),
            (
                wx - camx,
                road_y - camy
            ),
            (
                wx + 55 - camx,
                road_y - camy
            ),
            5
        )

    # ========================================================
    # RIVER
    # ========================================================

    river_y = 500

    pygame.draw.rect(
        screen,
        (27, 103, 139),
        (
            1250 - camx,
            river_y - camy,
            950,
            100
        )
    )

    pygame.draw.rect(
        screen,
        (48, 157, 184),
        (
            1250 - camx,
            river_y + 15 - camy,
            950,
            65
        )
    )

    # Water highlights
    for i in range(10):

        x = (
            1280
            + i * 85
            - camx
        )

        y = (
            535
            + int(
                math.sin(
                    i * 1.7
                ) * 10
            )
            - camy
        )

        pygame.draw.line(
            screen,
            (170, 230, 225),
            (
                x,
                y
            ),
            (
                x + 35,
                y
            ),
            2
        )

    # ========================================================
    # WALKWAYS TO LANDMARKS
    # ========================================================

    for path_x, landmark_y in WALKABLE_PATHS:
        pygame.draw.line(
            screen,
            (145, 120, 85),
            (path_x - camx, landmark_y - camy),
            (path_x - camx, road_y - camy),
            45
        )
        pygame.draw.line(
            screen,
            (210, 180, 130),
            (path_x - camx, landmark_y - camy),
            (path_x - camx, road_y - camy),
            34
        )

    # ========================================================
    # LANDMARKS
    # ========================================================

    for landmark in LANDMARKS:
        draw_landmark(
            landmark["kind"],
            landmark["x"],
            landmark["y"],
            landmark["width"],
            landmark["height"],
            camx,
            camy
        )

    # ========================================================
    # LEARNING STATIONS
    # ========================================================

    for i, (wx, wy) in enumerate(
        stations
    ):

        sx = int(
            wx - camx
        )

        sy = int(
            wy - camy
        )

        if not (
            -50 <= sx <= WIDTH + 50
            and
            -50 <= sy <= HEIGHT + 50
        ):
            continue

        draw_station_icon(
            i,
            sx,
            sy - 52
        )

        if i == unlocked_level:

            colour = GOLD

        elif i in completed_levels:

            colour = GREEN

        elif i < unlocked_level:

            colour = GREY

        else:

            colour = (
                95,
                100,
                110
            )

        pygame.draw.circle(
            screen,
            (25, 30, 35),
            (
                sx,
                sy + 4
            ),
            31
        )

        pygame.draw.circle(
            screen,
            (20, 30, 40),
            (
                sx,
                sy
            ),
            30
        )

        pygame.draw.circle(
            screen,
            colour,
            (
                sx,
                sy
            ),
            24
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (
                sx,
                sy
            ),
            24,
            2
        )

        number = medium_font.render(
            str(i + 1),
            True,
            BLACK
        )

        screen.blit(
            number,
            number.get_rect(
                center=(
                    sx,
                    sy
                )
            )
        )

        if i > unlocked_level:
            draw_station_lock(sx, sy)

        if i in completed_levels:

            draw_text(
                "DONE",
                sx - 20,
                sy + 29,
                WHITE,
                small_font
            )

    # ========================================================
    # ATSARA
    # ========================================================

    draw_character(
        atsara_frames,
        atsara,
        camx,
        camy,
        frame_index=0,
        height=90,
        fallback=RED
    )

    # ========================================================
    # AUP BOKTO
    # ========================================================

    keys = pygame.key.get_pressed()

    moving = any(
        keys[k]
        for k in (
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_w,
            pygame.K_a,
            pygame.K_s,
            pygame.K_d
        )
    )

    running_fast = (
        keys[pygame.K_LSHIFT]
        or
        keys[pygame.K_RSHIFT]
    )

    if (
        running_fast
        and
        aup_run_frames
    ):

        frames = aup_run_frames

    elif (
        moving
        and
        aup_walk_frames
    ):

        frames = aup_walk_frames

    else:

        frames = aup_idle_frames

    draw_character(
        frames,
        player,
        camx,
        camy,
        frame_index=walk_frame,
        height=100,
        fallback=BLUE,
        flip_left=facing_left
    )


# ============================================================
# HUD
# ============================================================

def draw_hud():

    pygame.draw.rect(
        screen,
        (20, 30, 42),
        (
            0,
            0,
            WIDTH,
            76
        )
    )

    draw_text(
        "ATSARA OS ADVENTURE",
        20,
        8,
        GOLD,
        medium_font
    )

    draw_text(
        f"Level unlocked: {unlocked_level + 1}/7",
        530,
        12
    )

    draw_text(
        f"Crystals: {crystals}",
        800,
        12,
        GOLD
    )

    draw_text(
        "WASD/Arrows: Move | Shift: Run | E: Interact | H: Manual | M: Music | +/-: Volume",
        20,
        48,
        WHITE,
        small_font
    )

    # Music indicator
    draw_text(
        f"Music: {'OFF' if music_muted else 'ON'} {music_volume:.0%}",
        930,
        48,
        RED if music_muted else GREEN,
        small_font
    )


# ============================================================
# DIALOGUE
# ============================================================

def start_dialogue(
    lines,
    return_state="world",
    mark_tutorial=False,
    title="ATSARA"
):

    global state
    global dialogue_lines
    global dialogue_index
    global dialogue_return_state
    global dialogue_marks_tutorial
    global dialogue_title

    dialogue_lines = lines

    dialogue_index = 0

    dialogue_return_state = return_state
    dialogue_marks_tutorial = mark_tutorial
    dialogue_title = title

    state = "dialogue"


def close_dialogue():

    global state
    global tutorial_seen
    global dialogue_marks_tutorial

    if dialogue_marks_tutorial and not tutorial_seen:
        tutorial_seen = True
        save_game()

    dialogue_marks_tutorial = False
    state = dialogue_return_state


def near_atsara():

    distance = math.hypot(
        player.centerx
        - atsara.centerx,

        player.centery
        - atsara.centery
    )

    return distance < 115


def talk_to_atsara():

    global tutorial_seen

    if not tutorial_seen:

        lines = [

            "Kuzuzangpo, Aup Bokto! Welcome to our adventure!",

            "We have an important mission: discover how operating systems help computers work.",

            "Use WASD or the arrow keys to walk. Hold Shift to run.",

            "Walk close to a numbered learning station and press E to begin its challenge.",

            "Each level has ten questions. You need at least 80 percent to pass.",

            "Pass a level to earn five crystals and unlock the next challenge.",

            "Press H whenever you need the game manual. Are you ready? Let's explore!"
        ]

    else:

        lines = [

            "Kuzuzangpo, Aup Bokto! How is your adventure going?",

            "Explore the forest and visit the numbered learning stations.",

            "Remember: you need 80 percent to pass a quiz.",

            "If you need help with the controls, press H to open your field guide.",

            "Good luck! I will be here if you need guidance."
        ]

    start_dialogue(
        lines,
        mark_tutorial=not tutorial_seen
    )


def show_landmark_notes(landmark):

    start_dialogue(
        landmark["notes"],
        title="NOTE"
    )


def draw_dialogue():

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            0,
            0,
            0,
            95
        )
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    box = pygame.Rect(
        45,
        HEIGHT - 205,
        WIDTH - 90,
        165
    )

    panel(
        box,
        (35, 43, 54),
        GOLD
    )

    portrait = pygame.Rect(
        box.x + 14,
        box.y + 14,
        100,
        120
    )

    pygame.draw.rect(
        screen,
        (67, 87, 92),
        portrait,
        border_radius=12
    )

    if atsara_frames:

        frame = atsara_frames[0]

        fw, fh = frame.get_size()

        scale = min(
            90 / max(1, fw),
            110 / max(1, fh)
        )

        image = pygame.transform.smoothscale(
            frame,
            (
                max(
                    1,
                    int(fw * scale)
                ),
                max(
                    1,
                    int(fh * scale)
                )
            )
        )

        screen.blit(
            image,
            image.get_rect(
                center=portrait.center
            )
        )

    else:

        pygame.draw.circle(
            screen,
            RED,
            (
                portrait.centerx,
                portrait.y + 35
            ),
            18
        )

        pygame.draw.rect(
            screen,
            RED,
            (
                portrait.centerx - 18,
                portrait.y + 53,
                36,
                48
            ),
            border_radius=6
        )

    draw_text(
        dialogue_title,
        box.x + 135,
        box.y + 12,
        GOLD,
        medium_font
    )

    if dialogue_lines:

        message = dialogue_lines[
            min(
                dialogue_index,
                len(dialogue_lines) - 1
            )
        ]

        lines = wrap_text(
            message,
            box.width - 170,
            font
        )

        for i, line in enumerate(
            lines[:3]
        ):

            draw_text(
                line,
                box.x + 135,
                box.y + 49 + i * 26,
                WHITE,
                font
            )

    draw_text(
        "SPACE / E: Continue",
        box.right - 220,
        box.bottom - 30,
        GOLD,
        small_font
    )


# ============================================================
# FIELD MANUAL
# ============================================================

MANUAL_PAGES = [

    (
        "WELCOME, ADVENTURER",
        [
            "You are Aup Bokto, exploring a Bhutan-inspired world.",
            "Atsara will teach you about operating systems.",
            "Explore the forest, chorten, dzong and bridge.",
            "Visit learning stations to begin each level.",
            "Complete all seven levels to finish your adventure."
        ]
    ),

    (
        "MOVEMENT AND CONTROLS",
        [
            "W / A / S / D or arrow keys: Move",
            "Hold LEFT SHIFT: Run",
            "E: Talk to Atsara or use a learning station",
            "E: Read a landmark summary when nearby",
            "SPACE: Continue dialogue",
            "H: Open or close this manual",
            "F5: Save your progress",
            "M: Mute or unmute music",
            "+ / -: Change music volume",
            "ESC: Close a screen or return to the title"
        ]
    ),

    (
        "LEARNING AND QUIZZES",
        [
            "Walk close to a numbered learning station.",
            "Press E to start an unlocked level.",
            "Choose an answer using keys 1, 2, 3 or 4.",
            "Each level contains ten questions.",
            "You need at least 80 percent to pass.",
            "Read feedback when you get an answer wrong.",
            "You can retry a level you have not passed."
        ]
    ),

    (
        "LEVELS AND CRYSTALS",
        [
            "1. Computer basics — the forest",
            "2. Processes — the chorten",
            "3. Memory — the dzong",
            "4. Files — the bridge",
            "5. Security — the temple",
            "6. Networks — the monastery",
            "7. Advanced OS concepts — the final challenge",
            "Pass a level to earn five crystals and unlock the next."
        ]
    ),

    (
        "SAVING AND GETTING HELP",
        [
            "Press F5 to save unlocked levels and crystals.",
            "Your progress is saved in os_adventure_save.json.",
            "Press H anytime in the world to open this manual.",
            "Find Atsara and press E when you need guidance.",
            "If a level is locked, finish the previous level first.",
            "Good luck, Aup Bokto!"
        ]
    )
]


def draw_manual():

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            8,
            15,
            22,
            220
        )
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    box = pygame.Rect(
        80,
        55,
        WIDTH - 160,
        HEIGHT - 110
    )

    panel(
        box,
        (48, 43, 35),
        GOLD
    )

    title, instructions = MANUAL_PAGES[
        manual_page
    ]

    draw_text(
        "FIELD GUIDE",
        box.x + 30,
        box.y + 20,
        GOLD,
        large_font
    )

    draw_text(
        title,
        box.x + 30,
        box.y + 82,
        WHITE,
        medium_font
    )

    y = box.y + 135

    for line in instructions:

        draw_text(
            "• " + line,
            box.x + 35,
            y,
            WHITE,
            font
        )

        y += 37

    draw_text(
        f"Page {manual_page + 1} of {len(MANUAL_PAGES)}",
        box.x + 30,
        box.bottom - 45,
        GOLD,
        small_font
    )

    draw_text(
        "LEFT / RIGHT: Pages     H or ESC: Close",
        box.right - 395,
        box.bottom - 45,
        WHITE,
        small_font
    )


# ============================================================
# PLAYER MOVEMENT
# ============================================================

def is_walkable_surface(center_x, foot_y):

    if 590 <= foot_y <= 710:
        return True

    for path_x, landmark_y in WALKABLE_PATHS:
        if (
            abs(center_x - path_x) <= 22
            and min(landmark_y, 650) <= foot_y <= max(landmark_y, 650)
        ):
            return True

    return (
        1418 <= center_x <= 1577
        and 502 <= foot_y <= 535
    )


def move_player(keys):

    global walk_frame
    global animation_timer

    global facing_left
    global facing_up
    global facing_down

    dx = 0
    dy = 0

    if (
        keys[pygame.K_LEFT]
        or
        keys[pygame.K_a]
    ):

        dx -= 1

    if (
        keys[pygame.K_RIGHT]
        or
        keys[pygame.K_d]
    ):

        dx += 1

    if (
        keys[pygame.K_UP]
        or
        keys[pygame.K_w]
    ):

        dy -= 1

    if (
        keys[pygame.K_DOWN]
        or
        keys[pygame.K_s]
    ):

        dy += 1

    moving = (
        dx != 0
        or
        dy != 0
    )

    speed = (
        7
        if (
            keys[pygame.K_LSHIFT]
            or
            keys[pygame.K_RSHIFT]
        )
        else 4
    )

    if dx < 0:

        facing_left = True

    elif dx > 0:

        facing_left = False

    if dy < 0:

        facing_up = True
        facing_down = False

    elif dy > 0:

        facing_down = True
        facing_up = False

    if dx and dy:

        speed = max(
            1,
            int(
                speed * 0.7071
            )
        )

    next_x = max(
        0,
        min(
            player.x + dx * speed,
            WORLD_W - player.width
        )
    )

    if is_walkable_surface(
        next_x + player.width // 2,
        player.bottom
    ):
        player.x = next_x

    next_y = max(
        0,
        min(
            player.y + dy * speed,
            WORLD_H - player.height
        )
    )

    if is_walkable_surface(
        player.centerx,
        next_y + player.height
    ):
        player.y = next_y

    if moving:

        animation_timer += 1

        if animation_timer >= 8:

            walk_frame += 1

            animation_timer = 0


# ============================================================
# STATION DETECTION
# ============================================================

def nearest_station():

    closest = None

    best = float("inf")

    for i, (x, y) in enumerate(
        stations
    ):

        distance = math.hypot(
            player.centerx - x,
            player.centery - y
        )

        if distance < best:

            best = distance
            closest = i

    if best <= 100:

        return closest

    return None


def nearest_landmark():

    closest = None
    best = float("inf")

    for landmark in LANDMARKS:
        distance = math.hypot(
            player.centerx - (landmark["x"] + landmark["width"] / 2),
            player.centery - (landmark["y"] + landmark["height"])
        )

        if distance < best:
            best = distance
            closest = landmark

    if best <= 145:
        return closest

    return None


def draw_landmark_prompt(landmark):

    rect = pygame.Rect(
        100,
        HEIGHT - 78,
        900,
        44
    )

    panel(
        rect,
        (24, 35, 48),
        GOLD
    )

    center_text(
        "Press E to read a note",
        HEIGHT - 66,
        WHITE,
        small_font
    )


# ============================================================
# QUIZ SYSTEM
# ============================================================

def start_quiz(level_number):

    global state
    global current_level
    global questions
    global question_index
    global score
    global feedback
    global feedback_notes

    if level_number > unlocked_level:

        return

    current_level = level_number

    questions = []

    for question, options, correct in LEVELS[level_number]["questions"]:
        shuffled_options = list(enumerate(options))
        random.shuffle(shuffled_options)

        shuffled_correct = next(
            index
            for index, (original_index, _) in enumerate(shuffled_options)
            if original_index == correct
        )

        questions.append(
            (
                question,
                [option for _, option in shuffled_options],
                shuffled_correct
            )
        )

    random.shuffle(
        questions
    )

    question_index = 0

    score = 0

    feedback = ""

    feedback_notes = []

    state = "quiz"


def answer_question(choice):

    global score
    global state
    global feedback
    global feedback_notes
    global feedback_timer

    question, options, correct = questions[
        question_index
    ]

    if choice == correct:

        score += 1

        feedback = (
            "Good Job!"
        )

    else:

        feedback = (
            "OH NO!!"
        )

    feedback_notes = [
        f"Correct answer: {options[correct]}.",
        *LEVEL_REVIEW_NOTES[current_level]
    ]

    state = "feedback"

    feedback_timer = 240


def finish_quiz():

    global state
    global unlocked_level
    global crystals

    percentage = (
        score
        / len(questions)
        * 100
    )

    if percentage >= 80:

        if current_level not in completed_levels:

            crystals += 5

        completed_levels.add(
            current_level
        )

        if current_level < len(LEVELS) - 1:

            unlocked_level = max(
                unlocked_level,
                current_level + 1
            )

        save_game()

        state = "passed"

    else:

        state = "failed"


# ============================================================
# QUIZ DRAWING
# ============================================================

def draw_quiz():

    screen.fill(DARK)

    level = LEVELS[
        current_level
    ]

    total = len(questions)

    draw_text(
        level["name"],
        35,
        22,
        GOLD,
        medium_font
    )

    draw_text(
        level["lesson"],
        40,
        61,
        WHITE,
        small_font
    )

    draw_text(
        f"Question {question_index + 1} of {total}",
        40,
        94,
        WHITE
    )

    draw_text(
        f"Score: {score}",
        920,
        94,
        GREEN
    )

    # Progress bar
    pygame.draw.rect(
        screen,
        GREY,
        (
            40,
            130,
            1020,
            10
        )
    )

    progress = int(
        1020
        * question_index
        / max(
            1,
            total
        )
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (
            40,
            130,
            progress,
            10
        )
    )

    question, options, correct = questions[
        question_index
    ]

    panel(
        pygame.Rect(
            40,
            160,
            1020,
            125
        )
    )

    q_lines = wrap_text(
        question,
        950,
        medium_font
    )

    for i, line in enumerate(
        q_lines[:2]
    ):

        draw_text(
            line,
            65,
            190 + i * 34,
            WHITE,
            medium_font
        )

    # Answer buttons
    for i, option in enumerate(
        options
    ):

        col = i % 2
        row = i // 2

        x = 55 + col * 510
        y = 320 + row * 100

        rect = pygame.Rect(
            x,
            y,
            485,
            76
        )

        panel(
            rect,
            (43, 59, 78),
            BLUE
        )

        option_lines = wrap_text(
            f"{i + 1}. {option}",
            450,
            small_font
        )

        for j, line in enumerate(
            option_lines[:2]
        ):

            draw_text(
                line,
                x + 16,
                y + 19 + j * 23,
                WHITE,
                small_font
            )

    center_text(
        "Press 1, 2, 3 or 4 to answer",
        540,
        GOLD
    )

    center_text(
        "Pass mark: 80%",
        580,
        WHITE,
        small_font
    )

    center_text(
        "ESC: Return to the world",
        615,
        GREY,
        small_font
    )


# ============================================================
# FEEDBACK
# ============================================================

def draw_feedback():

    draw_quiz()

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            0,
            0,
            0,
            175
        )
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    colour = GREEN if feedback == "Good Job!" else RED

    box = pygame.Rect(
        95,
        220,
        910,
        260
    )

    panel(
        box,
        (30, 43, 57),
        colour
    )

    draw_text(
        feedback,
        box.x + 25,
        box.y + 25,
        colour,
        medium_font
    )

    note_y = box.y + 75

    for note in feedback_notes:
        for line in wrap_text(note, 840, font):
            draw_text(
                f"- {line}",
                box.x + 25,
                note_y,
                WHITE,
                font
            )
            note_y += 27

    draw_text(
        "Next question loading...",
        box.x + 25,
        box.bottom - 38,
        GREY,
        small_font
    )


# ============================================================
# RESULTS
# ============================================================

def draw_result(passed):

    screen.fill(DARK)

    if passed:

        center_text(
            "LEVEL COMPLETED!",
            95,
            GREEN,
            large_font
        )

        center_text(
            "Atsara: Wonderful work, Aup Bokto!",
            155,
            GOLD,
            medium_font
        )

        center_text(
            "You earned crystals!",
            195,
            GOLD
        )

    else:

        center_text(
            "LET'S TRY AGAIN!",
            95,
            RED,
            large_font
        )

        center_text(
            "Atsara: Every mistake helps us learn.",
            155,
            WHITE,
            medium_font
        )

        center_text(
            "You need at least 80% to pass.",
            195,
            WHITE
        )

    percentage = (
        score
        / len(questions)
        * 100
    )

    panel(
        pygame.Rect(
            280,
            250,
            540,
            145
        )
    )

    center_text(
        f"Score: {score}/{len(questions)}",
        275,
        WHITE,
        medium_font
    )

    center_text(
        f"Percentage: {percentage:.0f}%",
        325,
        GOLD,
        medium_font
    )

    if (
        passed
        and
        current_level < len(LEVELS) - 1
    ):

        center_text(
            "The next level is unlocked!",
            430,
            GREEN
        )

    elif passed:

        center_text(
            "Congratulations! All seven levels completed!",
            430,
            GREEN
        )

    center_text(
        "Press ENTER to return to the world",
        500,
        WHITE
    )

    center_text(
        "Press H for the manual after returning",
        540,
        GREY,
        small_font
    )

    center_text(
        "Press ESC to quit",
        575,
        GREY,
        small_font
    )


# ============================================================
# STATION PROMPT
# ============================================================

def draw_station_prompt():

    station = nearest_station()

    if station is None:

        return

    rect = pygame.Rect(
        100,
        HEIGHT - 78,
        900,
        44
    )

    panel(
        rect,
        (24, 35, 48),
        GOLD
    )

    if station <= unlocked_level:

        message = (
            f"Press E to play: "
            f"{LEVELS[station]['name']}"
        )

    else:

        message = (
            "This station is locked. "
            "Complete the previous level first."
        )

    center_text(
        message,
        HEIGHT - 66,
        WHITE,
        small_font
    )


# ============================================================
# TITLE SCREEN
# ============================================================

RESET_BUTTON_RECT = pygame.Rect(
    WIDTH // 2 - 120,
    620,
    240,
    44
)

RESET_CONFIRM_YES_RECT = pygame.Rect(
    WIDTH // 2 - 180,
    365,
    160,
    48
)

RESET_CONFIRM_NO_RECT = pygame.Rect(
    WIDTH // 2 + 20,
    365,
    160,
    48
)

def draw_title():

    screen.fill(DARK)

    if forest_bg:

        bg = pygame.transform.smoothscale(
            forest_bg,
            (
                WIDTH,
                HEIGHT
            )
        )

        screen.blit(
            bg,
            (0, 0)
        )

        shade = pygame.Surface(
            (
                WIDTH,
                HEIGHT
            ),
            pygame.SRCALPHA
        )

        shade.fill(
            (
                10,
                20,
                25,
                135
            )
        )

        screen.blit(
            shade,
            (0, 0)
        )

    center_text(
        "ATSARA OS ADVENTURE",
        85,
        GOLD,
        large_font
    )

    center_text(
        "Explore Bhutan. Learn Operating Systems.",
        145,
        WHITE,
        medium_font
    )

    panel(
        pygame.Rect(
            165,
            210,
            770,
            270
        ),
        (28, 40, 50)
    )

    center_text(
        "Join Aup Bokto and Atsara on a learning adventure.",
        245,
        WHITE
    )

    center_text(
        "Explore seven levels and answer 70 questions.",
        290,
        WHITE
    )

    center_text(
        "Pass each quiz with at least 80%.",
        335,
        GOLD
    )

    center_text(
        "Atsara will teach you how to play.",
        380,
        WHITE
    )

    center_text(
        "Press ENTER to begin",
        510,
        GREEN,
        medium_font
    )

    center_text(
        "Press L to load saved progress",
        552,
        WHITE
    )

    center_text(
        "Press ESC to quit",
        590,
        GREY,
        small_font
    )

    if not reset_confirmation:
        panel(
            RESET_BUTTON_RECT,
            (60, 42, 40),
            RED
        )
        center_text(
            "Restart Progress",
            RESET_BUTTON_RECT.y + 13,
            WHITE,
            small_font
        )
        return

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )
    overlay.fill((0, 0, 0, 190))
    screen.blit(overlay, (0, 0))

    confirmation_box = pygame.Rect(
        WIDTH // 2 - 270,
        260,
        540,
        190
    )
    panel(
        confirmation_box,
        (35, 43, 54),
        GOLD
    )
    center_text(
        "Restart all progress?",
        286,
        GOLD,
        medium_font
    )
    center_text(
        "Levels, crystals, and tutorial progress will reset.",
        326,
        WHITE,
        small_font
    )

    panel(RESET_CONFIRM_YES_RECT, (62, 48, 40), RED)
    yes_label = small_font.render(
        "Yes, restart",
        True,
        WHITE
    )
    screen.blit(
        yes_label,
        yes_label.get_rect(center=RESET_CONFIRM_YES_RECT.center)
    )

    panel(RESET_CONFIRM_NO_RECT, (43, 59, 78), BLUE)
    no_label = small_font.render(
        "Cancel",
        True,
        WHITE
    )
    screen.blit(
        no_label,
        no_label.get_rect(center=RESET_CONFIRM_NO_RECT.center)
    )

# ============================================================
# MAIN LOOP
# ============================================================

running = True

while running:

    dt = clock.tick(FPS)

    for event in pygame.event.get():

        # ====================================================
        # WINDOW CLOSE
        # ====================================================

        if event.type == pygame.QUIT:

            save_game()

            running = False

            continue

        if event.type == pygame.MOUSEBUTTONDOWN:

            if state == "title":

                if reset_confirmation:

                    if RESET_CONFIRM_YES_RECT.collidepoint(event.pos):
                        reset_progress()

                    elif RESET_CONFIRM_NO_RECT.collidepoint(event.pos):
                        reset_confirmation = False

                elif RESET_BUTTON_RECT.collidepoint(event.pos):
                    reset_confirmation = True

            continue

        if event.type != pygame.KEYDOWN:

            continue

        if event.key == pygame.K_m:
            toggle_music()
            save_game()
            continue

        if event.key in (
            pygame.K_EQUALS,
            pygame.K_PLUS,
            pygame.K_KP_PLUS
        ):
            increase_music_volume()
            save_game()
            continue

        if event.key in (
            pygame.K_MINUS,
            pygame.K_KP_MINUS
        ):
            decrease_music_volume()
            save_game()
            continue

        # ====================================================
        # TITLE
        # ====================================================

        if state == "title":

            if reset_confirmation:

                if event.key in (
                    pygame.K_y,
                    pygame.K_RETURN
                ):
                    reset_progress()

                elif event.key in (
                    pygame.K_n,
                    pygame.K_ESCAPE
                ):
                    reset_confirmation = False

                continue

            if event.key == pygame.K_RETURN:

                if not tutorial_seen:

                    talk_to_atsara()

                else:

                    state = "world"

            elif event.key == pygame.K_l:

                load_game()

                if not tutorial_seen:

                    talk_to_atsara()

                else:

                    state = "world"

            elif event.key == pygame.K_ESCAPE:

                running = False

        # ====================================================
        # WORLD
        # ====================================================

        elif state == "world":

            # Manual is open
            if show_help:

                if (
                    event.key == pygame.K_h
                    or
                    event.key == pygame.K_ESCAPE
                ):

                    show_help = False

                elif event.key == pygame.K_RIGHT:

                    manual_page = (
                        manual_page + 1
                    ) % len(MANUAL_PAGES)

                elif event.key == pygame.K_LEFT:

                    manual_page = (
                        manual_page - 1
                    ) % len(MANUAL_PAGES)

                continue

            # Exit world
            if event.key == pygame.K_ESCAPE:

                save_game()

                state = "title"

            # Manual
            elif event.key == pygame.K_h:

                show_help = True

            # Save
            elif event.key == pygame.K_F5:

                save_game()

            # Interact
            elif event.key == pygame.K_e:

                if near_atsara():

                    talk_to_atsara()

                else:

                    station = nearest_station()
                    landmark = nearest_landmark()

                    if (
                        station is not None
                        and station <= unlocked_level
                    ):

                        start_quiz(station)

                    elif landmark is not None:

                        show_landmark_notes(landmark)

        # ====================================================
        # DIALOGUE
        # ====================================================

        elif state == "dialogue":

            if event.key in (
                pygame.K_SPACE,
                pygame.K_e,
                pygame.K_RETURN
            ):

                dialogue_index += 1

                if (
                    dialogue_index
                    >= len(dialogue_lines)
                ):

                    close_dialogue()

            elif event.key == pygame.K_h:

                show_help = True

                state = "world"

            elif event.key == pygame.K_ESCAPE:

                close_dialogue()

        # ====================================================
        # QUIZ
        # ====================================================

        elif state == "quiz":

            if event.key == pygame.K_ESCAPE:

                state = "world"

            elif event.key in (
                pygame.K_1,
                pygame.K_2,
                pygame.K_3,
                pygame.K_4
            ):

                answer_question(
                    event.key - pygame.K_1
                )

        # ====================================================
        # FEEDBACK
        # ====================================================

        elif state == "feedback":

            if event.key == pygame.K_ESCAPE:

                state = "world"

        # ====================================================
        # RESULTS
        # ====================================================

        elif state in (
            "passed",
            "failed"
        ):

            if event.key == pygame.K_RETURN:

                state = "world"

            elif event.key == pygame.K_ESCAPE:

                save_game()

                running = False

    # ========================================================
    # PLAYER MOVEMENT
    # ========================================================

    if (
        state == "world"
        and
        not show_help
    ):

        move_player(
            pygame.key.get_pressed()
        )

    # ========================================================
    # CAMERA
    # ========================================================

    camx = max(
        0,
        min(
            player.centerx - WIDTH // 2,
            WORLD_W - WIDTH
        )
    )

    camy = max(
        0,
        min(
            player.centery - HEIGHT // 2,
            WORLD_H - HEIGHT
        )
    )

    # ========================================================
    # DRAW STATES
    # ========================================================

    if state == "title":

        draw_title()

    elif state == "world":

        draw_world_background(
            camx,
            camy
        )

        draw_hud()

        if not show_help:

            station = nearest_station()
            landmark = nearest_landmark()

            if near_atsara():

                prompt = pygame.Rect(
                    250,
                    HEIGHT - 78,
                    600,
                    44
                )

                panel(
                    prompt,
                    (24, 35, 48),
                    GOLD
                )

                center_text(
                    "Press E to talk to Atsara",
                    HEIGHT - 66,
                    WHITE,
                    small_font
                )

            elif (
                station is not None
                and station <= unlocked_level
            ):

                draw_station_prompt()

            elif landmark is not None:

                draw_landmark_prompt(landmark)

            else:

                draw_station_prompt()

        if show_help:

            draw_manual()

    elif state == "dialogue":

        draw_world_background(
            camx,
            camy
        )

        draw_hud()

        draw_dialogue()

    elif state == "quiz":

        draw_quiz()

    elif state == "feedback":

        draw_feedback()

        feedback_timer -= 1

        if feedback_timer <= 0:

            question_index += 1

            if (
                question_index
                >= len(questions)
            ):

                finish_quiz()

            else:

                state = "quiz"

    elif state == "passed":

        draw_result(True)

    elif state == "failed":

        draw_result(False)

    # ========================================================
    # DISPLAY
    # ========================================================

    pygame.display.flip()

# ============================================================
# EXIT
# ============================================================

pygame.mixer.music.stop()

pygame.quit()