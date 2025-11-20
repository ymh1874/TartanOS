# TartanOS Desktop & Terminal Environment

**Author:** Yousef Hussein

## Project Description

**TartanOS** is a simulated desktop operating system built using **CMU Graphics**. It features a login screen, a customizable desktop with icons, and a fully functional terminal that supports navigation, file management, and command execution. The system aims to recreate core OS interactions within the constraints of 15-112.

The project includes:

* A login interface with dynamic UI scaling.
* A desktop environment containing icons, wallpapers, and system elements.
* A command‑line terminal supporting commands such as `cd`, `ls`, `cat`, `mkdir`, `touch`, and more.
* A simulated file system.
* A mode‑based UI system switching between desktop and terminal modes.

---

## Competitive Analysis


This project is inspired by eDEX-UI, a futuristic terminal-based interface. Like eDEX-UI, it combines a terminal, system-style panels, and navigation elements in one unified screen. The similarity is mainly in the clean, immersive layout and the idea of interacting with an OS-like interface rather than a simple terminal.

However, this project differs by including a full desktop environment (icons, wallpaper, login page) and by using a simulated file system built entirely in CMU Graphics. 

---

## Structural Plan

The codebase is modularized to separate UI, core mode management, and system logic so features can scale independently. Below is the current layout and responsibilities (map local paths to responsibilities):

- `main.py`
   - App bootstrap: initialize `app` fields, create `FileSystem` and `UserAuth`, set `app.tick`, and register mode manager and top-level UI objects.

- `config.py`
   - Centralized configuration values (colors, default sizes, constants).

- `core/` (mode + rendering orchestration)
   - `appModes.py`: mode manager that switches between `desktop` and `terminal` modes and dispatches key/ redraw events.
   - `inputHandler.py`, `renderer.py`: helpers for global input handling and rendering orchestration where applicable.

- `systems/` (non-UI system logic)
   - `fileSystem.py`: the simulated file system implementation.
   - `pathUtils.py`: path resolution helpers (join, normalize, parent path logic).
   - `commandRegistry.py`: command handlers moved out of UI; each `cmd*` (ls, cat, cd, touch, etc.) lives here and operates against the terminal and `FileSystem`.
   - `userAuth.py`: authentication logic.

- `ui/` (visual components)
   - `ui/desktop/` — desktop view implementation (`desktop.py`, `widgets.py`) and icon widgets.
   - `ui/terminal/` — terminal UI and input handling split into `terminal.py` and rendering helpers (`terminalRenderer.py`). The terminal UI should be thin: it draws labels and forwards command execution to `systems.commandRegistry` and filesystem operations to `systems.fileSystem`.

- `assets/` — images and icons used by the UI and desktop.


This structural plan reflects the current repository layout and the modularization work already performed.
---

## Algorithmic Plan

The trickiest component is **path resolution and file‑system navigation in the terminal**.

### **Goal:** Process commands like

```
cd ../../home/user/projects
ls /home/shared
cat notes.txt
```

### **Algorithmic Breakdown:**

1. **Parse Input:**

   * Split command and arguments.
   * Normalize multiple slashes or spaces.

2. **Resolve Path:**

   * If path starts with `/`, treat as absolute.
   * Otherwise treat as relative to `currPath`.
   * Split into components using `/`.
   * Use a stack to resolve:

     * `..` → pop
     * `.` → ignore
     * folder names → push
   * Join stack into final path.

3. **Validate:**

   * Check existence in `fileSys` dictionary.
   * Check if target is file or folder depending on command.

4. **Execute Command:**

   * `cd` updates `currPath`.
   * `ls` lists keys in dictionary.
   * `cat` prints file contents.

This approach ensures correctness and avoids edge cases such as root navigation, double slashes, or invalid paths.

**More to be added later...**

---

## Timeline Plan

### **Week 1:**

* Finalize proposal
* Basic app structure + modes
* Login screen implementation

### **Week 2:**

* Desktop UI complete
* Icons, wallpaper scaling, click interactions

### **Week 3:**

* Terminal base system
* Text input, history, scrolling
* Basic file system (static)

### **Week 4:**

* Full command implementation (`cd`, `ls`, `cat`, `mkdir`, `touch`, etc.)
* Dynamic file system
* Polish, error handling, edge cases
* UI refinement
* Final demo recording

---

## Module List

The project will only use:

* **cmu_graphics** (required and permitted)
* **math** (standard library; allowed)
* **random** (for optional wallpaper variations)

No external modules, hardware, networking,
 or non‑approved libraries will be used.

---

