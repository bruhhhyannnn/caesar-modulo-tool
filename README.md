# Caesar Modulo Tool (Stream/File + Key/Crack)

This project implements a generalized Caesar cipher using modulo arithmetic over a user-defined alphabet (character set). It supports both file-based processing and UNIX-style pipelines (stdin → stdout), and it is designed, hopefully, to handle large inputs efficiently without loading entire files into memory.

---

## Features

- Custom alphabet/charset input (not limited to `a-z`)
- Automatic modulo base: `m = len(alphabet)`
- Key-based encryption/decryption (`encrypt`, `decrypt`)
- Brute-force cracking (`crack`) for attacker-style analysis
- Stream processing (stdin/stdout) for pipeline chaining
- Error handling for missing files

---

## Requirements

- Python 3.9+ (any modern Python 3 should work)

---

## How It Works

The Caesar cipher shifts each character in the input by a fixed key `k` within the given alphabet:

```
encrypted_index = (original_index + k) % m
decrypted_index = (original_index - k) % m
```

Where `m` is the length of the alphabet. Characters not found in the alphabet (spaces, punctuation, etc.) are passed through unchanged.

---

## Usage

### Encrypt (stdin → stdout)

```bash
echo "hello world" | python tool.py encrypt -k 3
```

**Expected output:**

> khoor zruog

**Decrypt text:**

```bash
echo "khoor zruog" | python tool.py decrypt -k 3
```

**Expected output:**

> hello world

### File-Based Usage

**Encrypt a file and print result:**

```bash
python tool.py encrypt -k 5 -f cipher.txt
```

**Encrypt/Decrypt and save to file:**

```bash
python tool.py encrypt -k 5 -f cipher.txt -o encrypted.txt
```

**Decrypt a file:**

```bash
python tool.py decrypt -k 5 -f encrypted.txt
```

### Crack Mode (Brute Force)

Crack mode attempts all possible keys and prints candidate plaintexts. Useful when the key is unknown.

```bash
echo "khoor" | python tool.py crack
```

**Sample output:**

```
k=  0 | khoor
k=  1 | jgnnq
k=  2 | ifmmp
k=  3 | hello
...
```

### Pipeline Examples (UNIX Chaining)

**Decrypt and filter for a keyword:**

```bash
cat cipher.txt | python tool.py decrypt -k 20 | grep today
```

**Encrypt and immediately inspect output:**

```bash
echo "hello world" | python tool.py encrypt -k 7 | cat -A
```

**Chain crack into a file for review:**

```bash
echo "khoor zruog" | python tool.py crack > candidates.txt
```

### Custom Alphabet Example

**Default alphabet:**

> abcdefghijklmnopqrstuvwxyz

**Example including digits** — note that `--alphabet` must come before the subcommand:

```bash
echo "abc123" | python tool.py --alphabet "abcdefghijklmnopqrstuvwxyz0123456789" encrypt -k 2
```

**Expected output:**

> cde345

Here: `m = 36` (modulo base automatically adjusts)

---

### Example using our Assignment/In-class activity

**Ciphertext:**

> cz sio zyff xiqh symnylxus mnuhx oj nixus

**Step 1: Identify key**

```bash
echo "cz sio zyff xiqh symnylxus mnuhx oj nixus" | python tool.py crack
```

**Step 2: Decrypt with discovered key (k = 20)**

```bash
echo "cz sio zyff xiqh symnylxus mnuhx oj nixus" | python tool.py decrypt -k 20
```

**Plaintext:**

> if you fell down yesterday stand up today

_Attributed author: H. G. Wells_

---

## Error Reference

| Scenario                         | Output                                                        |
| -------------------------------- | ------------------------------------------------------------- |
| Input file not found             | `Error: input file 'x.txt' not found.`                        |
| Invalid/empty alphabet           | `ValueError` with a descriptive message                       |
| Duplicate characters in alphabet | `ValueError: Alphabet must not contain duplicate characters.` |

---

**Author:** Bryan Jesus Mangapit
**Subject:** MIT 281
