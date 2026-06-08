import locale
import os
import struct
import urllib.request

ZW_ZERO = "\u200b"
ZW_ONE = "\u200c"

LOCALES = {
    "ru": {
        "err_not_found": "[-] Ошибка: '{path}' не найден.",
        "success_embed": "[+] Секрет успешно растворен в {path} ({size} байт)",
        "err_decode": "[-] Ошибка: скрытых данных не обнаружено или заголовок поврежден.",
        "success_extract": "[+] Успешно извлечено ({size} байт):\n",
        "err_empty_url": "[-] Ссылка не может быть пустой.",
        "downloading": "[i] Скачиваю данные с {url} ...",
        "err_download": "[-] Не удалось скачать файл. Код ответа сервера: {code}",
        "err_network": "[-] Ошибка сети/доступа: {error}",
        "err_choice": "[-] Введите число (0, 1, 2 или 3).",
        "err_invalid": "[-] Неверный выбор. Введите число от 0 до 3.",
        "menu_title": " Выберите действие: ",
        "menu_1": " 1 - Растворить секрет в README.md",
        "menu_2": " 2 - Извлечь секрет из локального файла",
        "menu_3": " 3 - Извлечь секрет из GitHub по ссылке",
        "menu_0": " 0 - Выход",
        "input_readme": "Путь к исходному README [README.md]: ",
        "input_secret": "Введите секретное сообщение: ",
        "input_output": "Путь для результата [README_hidden.md]: ",
        "input_local": "Путь к локальному файлу [README_hidden.md]: ",
        "input_url": "Ссылка на репозиторий или RAW файл GitHub: ",
        "exit": "Выход...",
    },
    "en": {
        "err_not_found": "[-] Error: '{path}' not found.",
        "success_embed": "[+] Secret successfully dissolved in {path} ({size} bytes)",
        "err_decode": "[-] Error: no hidden data found or header is corrupted.",
        "success_extract": "[+] Successfully extracted ({size} bytes):\n",
        "err_empty_url": "[-] URL cannot be empty.",
        "downloading": "[i] Downloading data from {url} ...",
        "err_download": "[-] Failed to download file. Server response code: {code}",
        "err_network": "[-] Network/Access error: {error}",
        "err_choice": "[-] Enter a number (0, 1, 2, or 3).",
        "err_invalid": "[-] Invalid choice. Enter a number from 0 to 3.",
        "menu_title": " Select action: ",
        "menu_1": " 1 - Dissolve secret in README.md",
        "menu_2": " 2 - Extract secret from local file",
        "menu_3": " 3 - Extract secret from GitHub via link",
        "menu_0": " 0 - Exit",
        "input_readme": "Path to original README [README.md]: ",
        "input_secret": "Enter secret message: ",
        "input_output": "Path for result [README_hidden.md]: ",
        "input_local": "Path to local file [README_hidden.md]: ",
        "input_url": "Link to GitHub repository or RAW file: ",
        "exit": "Exit...",
    },
}


def get_msg(key: str, **kwargs) -> str:
    try:
        lang = locale.getlocale()[0][:2].lower()
    except Exception:
        lang = "en"
    if lang not in LOCALES:
        lang = "en"
    return LOCALES[lang][key].format(**kwargs)


def embed_ghost(readme_path: str, secret_text: str, output_path: str):
    if not os.path.exists(readme_path):
        print(get_msg("err_not_found", path=readme_path))
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        public_text = f.read()

    secret_bytes = secret_text.encode("utf-8")
    payload = struct.pack(">I", len(secret_bytes)) + secret_bytes
    binary = "".join(format(b, "08b") for b in payload)
    ghost_tail = "".join(ZW_ONE if bit == "1" else ZW_ZERO for bit in binary)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(public_text + ghost_tail)

    print(get_msg("success_embed", path=output_path, size=len(secret_bytes)))


def extract_ghost_from_text(full_text: str) -> bytes:
    binary = "".join(
        "1" if char == ZW_ONE else "0" for char in full_text if char in (ZW_ZERO, ZW_ONE)
    )

    if not binary or len(binary) < 32:
        return b""

    byte_arr = bytes(
        int(binary[i : i + 8], 2) for i in range(0, len(binary), 8)
    )
    secret_size = struct.unpack(">I", byte_arr[:4])[0]

    if secret_size > len(byte_arr) - 4:
        return b""

    return byte_arr[4 : 4 + secret_size]


def convert_to_raw_url(url: str) -> str:
    if "raw.githubusercontent.com" in url:
        return url

    url = url.rstrip("/")
    if "github.com" in url and "blob" not in url:
        return url.replace("github.com", "raw.githubusercontent.com") + "/main/README.md"

    if "github.com" in url and "/blob/" in url:
        url = url.replace("github.com", "raw.githubusercontent.com")
        return url.replace("/blob/", "/")

    return url


def fetch_url(url: str) -> str:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read().decode("utf-8")


def main():
    while True:
        print("\n" + "=" * 45)
        print(get_msg("menu_1"))
        print(get_msg("menu_2"))
        print(get_msg("menu_3"))
        print(get_msg("menu_0"))
        print("=" * 45)

        try:
            choice = int(input(get_msg("menu_title")))
        except ValueError:
            print(get_msg("err_choice"))
            continue

        if choice == 0:
            print(get_msg("exit"))
            break

        elif choice == 1:
            readme_in = (
                input(get_msg("input_readme")).strip() or "README.md"
            )
            secret_in = input(get_msg("input_secret"))
            out_readme = (
                input(get_msg("input_output")).strip() or "README_hidden.md"
            )
            embed_ghost(readme_in, secret_in, out_readme)

        elif choice == 2:
            readme_path = (
                input(get_msg("input_local")).strip() or "README_hidden.md"
            )
            if not os.path.exists(readme_path):
                print(get_msg("err_not_found", path=readme_path))
                continue

            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            secret_bytes = extract_ghost_from_text(content)
            if not secret_bytes:
                print(get_msg("err_decode"))
            else:
                print(get_msg("success_extract", size=len(secret_bytes)))
                print(secret_bytes.decode("utf-8", errors="replace"))

        elif choice == 3:
            url_in = input(get_msg("input_url")).strip()
            if not url_in:
                print(get_msg("err_empty_url"))
                continue

            raw_url = convert_to_raw_url(url_in)
            print(get_msg("downloading", url=raw_url))

            try:
                try:
                    text = fetch_url(raw_url)
                except urllib.error.HTTPError as e:
                    if e.code == 404 and "/main/" in raw_url:
                        raw_url = raw_url.replace("/main/", "/master/")
                        text = fetch_url(raw_url)
                    else:
                        raise e

                secret_bytes = extract_ghost_from_text(text)
                if not secret_bytes:
                    print(get_msg("err_decode"))
                else:
                    print(get_msg("success_extract", size=len(secret_bytes)))
                    print(secret_bytes.decode("utf-8", errors="replace"))

            except urllib.error.HTTPError as e:
                print(get_msg("err_download", code=e.code))
            except Exception as e:
                print(get_msg("err_network", error=str(e)))

        else:
            print(get_msg("err_invalid"))


if __name__ == "__main__":
    main()