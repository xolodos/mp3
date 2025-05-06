import os
import pygame
import time
from pathlib import Path
import msvcrt
from colorama import init, Fore, Style

init(autoreset=True)

pygame.mixer.init()

SCRIPT_DIR = Path(__file__).parent.absolute()

MUSIC_FOLDERS = {
    "1": SCRIPT_DIR / "jumpstyle",
    "2": SCRIPT_DIR / "funk"
}

def print_slow(text, color=Fore.GREEN, delay=0.03):
    """Печатает текст с эффектом плавного появления."""
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()

def draw_progress_bar(current, total, length=20):
    """Рисует прогресс-бар."""
    progress = min(1.0, current / total)
    filled = int(progress * length)
    return f"[{'=' * filled}{' ' * (length - filled)}] {format_time(current)} / {format_time(total)}"

def format_time(seconds):
    """Форматирует время в MM:SS."""
    return f"{int(seconds // 60)}:{int(seconds % 60):02d}"

def get_user_input():
    """Неблокирующий ввод для Windows."""
    if msvcrt.kbhit():
        return msvcrt.getch().decode().lower()
    return None

def play_music_from_folder(folder):
    """Воспроизведение треков с управлением."""
    if not folder.exists():
        print(Fore.RED + f"❌ Папка '{folder}' не найдена!")
        return

    track_list = sorted([f for f in folder.glob("*") if f.suffix.lower() in ('.mp3', '.wav', '.ogg')])
    if not track_list:
        print(Fore.RED + f"❌ В папке '{folder}' нет аудиофайлов!")
        return

    current_idx = 0
    while current_idx < len(track_list):
        track = track_list[current_idx]
        try:
            os.system("mode con cols-180 lines-68")
            pygame.mixer.music.load(str(track))
            pygame.mixer.music.play()
            length = pygame.mixer.Sound(track).get_length()
            
            os.system('cls' if os.name == 'nt' else 'clear')
            print_slow(f"▶️ Трек {current_idx + 1}/{len(track_list)}: {track.name}")
            
            while pygame.mixer.music.get_busy():
                pos = pygame.mixer.music.get_pos() / 1000
                print(f"\r{Fore.GREEN}{draw_progress_bar(pos, length)}", end='', flush=True)
                
                cmd = get_user_input()
                if cmd == 'n':  
                    current_idx += 1
                    pygame.mixer.music.stop()
                    break
                elif cmd == 'p' and current_idx > 0:  
                    current_idx -= 1
                    pygame.mixer.music.stop()
                    break
                elif cmd == 'q':  
                    pygame.mixer.music.stop()
                    return
                
                time.sleep(0.1)
            
        except Exception as e:
            print(Fore.RED + f"❌ праблем: {e}")
            break

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_slow("=== 🎵 me.arbuzz.su ===")
    print_slow("1. jumpstyle", delay=0.05)
    print_slow("2. funk", delay=0.05)
    print_slow("0. выход", delay=0.05)

    while True:
        choice = input(Fore.GREEN + "(?): ").strip()
        
        if choice == "0":
            print_slow("👋 ну покеда")
            break
        elif choice in MUSIC_FOLDERS:
            play_music_from_folder(MUSIC_FOLDERS[choice])
        else:
            print(Fore.RED + "❌ чет не то!")

if __name__ == "__main__":
    main()