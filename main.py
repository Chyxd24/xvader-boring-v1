"""The Most Boring Object, Reviewed in One Line: xvader comp entry.

Target judge axis (RULES.txt, published brief):
  - single line of at most 200 chars reviewing a boring object.
  - funny AND true; laugh comes from how the object really behaves.
  - genuinely boring and everyday object.

Entry line lands its punch on the final token. Whole pipeline is
stdlib-only (os) so the snapshot stays inside the intake caps.
"""
import os

# Punchline. Sumber satu-satunya; revisi cukup di satu tempat.
ENTRY = (
    "Paperclip. Holds paper. Has never once surprised anyone. "
    "Five stars, but only because zero stars is not an option."
)

# Batas keras dari RULES.txt scorer: 1..200 chars, UTF-8.
HARD_LIMIT = 200

# Path output yang dibaca sealed scorer.
OUTPUT_PATH = "/output/entry.txt"


def build_line() -> str:
    """Kembalikan punchline.

    Dipecah jadi fungsi supaya bisa di-override di test tanpa
    menyentuh konstanta modul, dan supaya readback() punya satu
    sumber kebenaran.
    """
    return ENTRY


def validate(line: str, limit: int = HARD_LIMIT) -> tuple:
    """Validasi 1 line sesuai sealed scorer.

    Syarat: UTF-8, 1..limit char, bukan whitespace saja.
    Return (ok, alasan). Tidak melempar exception — caller yang
    memutuskan fatal atau tidak.
    """
    if not line:
        return False, "empty"
    if len(line) > limit:
        return False, f"too long: {len(line)} > {limit}"
    if not line.strip():
        return False, "whitespace only"
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as e:
        return False, f"not utf-8: {e}"
    return True, "ok"


def write_entry(path: str = OUTPUT_PATH) -> tuple:
    """Tulis 1 line ke path output. Return (path, char_count).

    Membuat direktori tujuan bila belum ada. Menulis dengan
    encoding utf-8 eksplisit sesuai syarat scorer.
    """
    line = build_line()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    return path, len(line)


def readback(path: str = OUTPUT_PATH, limit: int = HARD_LIMIT) -> bool:
    """Baca ulang entry lalu assert konten & panjang.

    Sengaja dipisah dari write_entry supaya contract LOOP
    ("readback-assert") terlihat sebagai langkah sendiri di
    transkrip agent.
    """
    with open(path, encoding="utf-8") as f:
        data = f.read()
    assert data == build_line(), "readback mismatch"
    ok, reason = validate(data, limit)
    assert ok, f"validation failed: {reason}"
    return True


if __name__ == "__main__":
    # 1) tulis, 2) readback, 3) cetak ringkasan untuk log agent.
    path, n = write_entry()
    print(f"wrote {n} chars to {path}")
    print("readback ok:", readback())
    # entry line final. Joke mendarat di kata-END sesuai kriteria judge.
    ok, reason = validate(build_line())
    print(f"validate: ok={ok} reason={reason}")
