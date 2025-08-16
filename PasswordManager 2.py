from cryptography.fernet import Fernet
from getpass import getpass
from pathlib import Path

class PasswordManager:
    def __init__(self):
        self.key: bytes | None = None
        self.password_dict: dict[str, str] = {}
        self.password_file: str | None = None

    # --- Key management ---
    def create_key(self, path: str) -> None:
        """Generate a new key and save it to 'path'."""
        self.key = Fernet.generate_key()
        Path(path).write_bytes(self.key)
        print(f"[OK] Key created and saved to: {path}")

    def load_key(self, path: str) -> None:
        """Load an existing key from 'path'."""
        self.key = Path(path).read_bytes()
        print(f"[OK] Key loaded from: {path}")

    # --- Vault / file management ---
    def create_password_file(self, path: str, initial_values: dict[str, str] | None = None) -> None:
        """Create/overwrite a password file. Optionally seed with initial values."""
        if self.key is None:
            raise RuntimeError("Load or create a key first (self.key is None).")
        self.password_file = path
        # Truncate/create new file
        Path(path).write_text("", encoding="utf-8")
        self.password_dict.clear()
        if initial_values:
            for site, pw in initial_values.items():
                self.add_password(site, pw)
        print(f"[OK] Password file created at: {path}")

    def load_password_file(self, path: str) -> None:
        """Load existing password file into memory."""
        if self.key is None:
            raise RuntimeError("Load key before loading password file.")
        self.password_file = path
        self.password_dict.clear()

        p = Path(path)
        if not p.exists():
            # If file doesn’t exist yet, just create an empty one.
            p.write_text("", encoding="utf-8")
            print(f"[OK] Created new empty password file at: {path}")
            return

        lines = p.read_text(encoding="utf-8").splitlines()
        for ln in lines:
            if not ln.strip():
                continue
            # Split at first ":" only, to allow ":" inside ciphertext
            if ":" not in ln:
                print(f"[WARN] Skipping malformed line: {ln!r}")
                continue
            site, encrypted = ln.split(":", 1)
            site = site.strip()
            encrypted = encrypted.strip()
            try:
                decrypted = Fernet(self.key).decrypt(encrypted.encode("utf-8")).decode("utf-8")
                self.password_dict[site] = decrypted
            except Exception as e:
                print(f"[WARN] Could not decrypt entry for site '{site}': {e}")

        print(f"[OK] Loaded {len(self.password_dict)} entries from: {path}")

    # --- Operations ---
    def add_password(self, site: str, password: str) -> None:
        if self.key is None:
            raise RuntimeError("Load or create a key first.")
        if self.password_file is None:
            raise RuntimeError("Create or load a password file first.")

        self.password_dict[site] = password
        encrypted = Fernet(self.key).encrypt(password.encode("utf-8")).decode("utf-8")
        with open(self.password_file, "a", encoding="utf-8") as f:
            f.write(f"{site}:{encrypted}\n")
        print(f"[OK] Added/updated password for: {site}")

    def get_password(self, site: str) -> str | None:
        return self.password_dict.get(site)

    def list_sites(self) -> list[str]:
        return sorted(self.password_dict.keys())

# ---------------- CLI for quick use ----------------
def main():
    pm = PasswordManager()

    MENU = """
==== Simple Encrypted Password Manager ====
1) Create new key file
2) Load key file
3) Create new password file (vault)
4) Load existing password file (vault)
5) Add / Update a password
6) Get password by site
7) List sites
0) Exit
Choose: """

    while True:
        choice = input(MENU).strip()
        try:
            if choice == "1":
                path = input("Key file path (e.g., key.key): ").strip()
                pm.create_key(path)

            elif choice == "2":
                path = input("Key file path to load: ").strip()
                pm.load_key(path)

            elif choice == "3":
                if pm.key is None:
                    print("[ERR] Load/create a key first (option 1 or 2)."); continue
                path = input("Password file path (e.g., vault.txt): ").strip()
                pm.create_password_file(path)

            elif choice == "4":
                if pm.key is None:
                    print("[ERR] Load/create a key first (option 1 or 2)."); continue
                path = input("Password file path to load: ").strip()
                pm.load_password_file(path)

            elif choice == "5":
                if pm.key is None or pm.password_file is None:
                    print("[ERR] Load key and password file first.")
                    continue
                site = input("Site/App name: ").strip()
                username = input("Username (optional, will be stored in notes or site name if you like): ").strip()
                pw = getpass("Password (hidden input): ").strip()
                # store "username:password" as the value (simple approach)
                value = f"{username}:{pw}" if username else pw
                pm.add_password(site, value)

            elif choice == "6":
                site = input("Site/App to fetch: ").strip()
                val = pm.get_password(site)
                if val is None:
                    print("[INFO] Not found.")
                else:
                    # If you stored "username:password", split it:
                    if ":" in val:
                        u, p = val.split(":", 1)
                        print(f"Username: {u}\nPassword: {p}")
                    else:
                        print(f"Password: {val}")

            elif choice == "7":
                sites = pm.list_sites()
                if not sites:
                    print("(empty)")
                else:
                    for s in sites:
                        print("-", s)

            elif choice == "0":
                print("Bye!")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"[ERR] {e}")

if __name__ == "__main__":
    main()
