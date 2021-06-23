import psutil  # For killing processes
import winreg  # For Windows Regedit
import shutil  # For deleting folder contents
import os  # For checking if folder exists

subkey_names = []
folders = ["appcache", "config", "dumps", "logs", "userdata", "traces"]
steam_path = ""


def kill_process(name) -> None:
    for process in psutil.process_iter():
        if process.name() == name:
            process.kill()


def get_exe_path() -> str:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Valve\\Steam") as key:
        for idx in range(winreg.QueryInfoKey(key)[0]):
            val = winreg.EnumValue(key, idx)
            if val[0] == "SteamPath":
                return str(val[1]).replace('/', '\\')

    return ""


def main() -> None:
    # Kill steam
    print("Killing steam...")
    kill_process("steam.exe")

    # Get SteamPath from registry
    steam_path = get_exe_path()

    print(f"Steam path is: {steam_path}")

    for folder in folders:
        f = os.path.join(steam_path, folder)

        if os.path.exists(f):
            print(f"Deleting folder: {f}...")

            try:
                shutil.rmtree(f)
            except OSError:
                pass  # Pass if file could not be deleted.

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Valve\\Steam\\Users") as key:
        for idx in range(winreg.QueryInfoKey(key)[0]):
            subkey_names.append(winreg.EnumKey(key, idx))
            print(f"Deleting key: {subkey_names[idx]}")
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER,
                                 f"SOFTWARE\\Valve\\Steam\\Users\\{subkey_names[idx]}")
            except OSError:
                pass  # Pass if not enough permissions to delete key.

    print("Done.")


if __name__ == '__main__':
    main()
