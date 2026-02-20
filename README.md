# Caesar Modulo Tool (Stream/File + Key/Crack)

This project implements a generalized Caesar cipher using modulo arithmetic over a user-defined alphabet (character set). It supports both file-based processing and UNIX-style pipelines (stdin → stdout), and it is designed to handle large inputs by processing data in chunks instead of loading entire files into memory.

---

## Features

- Custom alphabet/charset input (not limited to `a-z`)
- Automatic modulo base: `m = len(alphabet)`
- Key-based encryption/decryption (`encrypt`, `decrypt`)
- Brute-force cracking (`crack`) for attacker-style analysis
- Stream processing (stdin/stdout) for pipeline chaining

---

## Requirements

- Python 3.9+ (any modern Python 3 should work)

---

## Usage

### Encrypt (stdin → stdout)

```bash
echo "hello world" | python tool.py encrypt -k 3
```

**Expected output:**

```
khoor zruog
```

**Decrypt text:**

```bash
echo "khoor zruog" | python tool.py decrypt -k 3
```

**Expected output:**

```
hello world
```

### File-Based Usage

**Encrypt a file and print result:**

```bash
python tool.py encrypt -k 5 -f input.txt
```

**Encrypt and save to file:**

```bash
python tool.py encrypt -k 5 -f input.txt -o encrypted.txt
```

**Decrypt a file:**

```bash
python tool.py decrypt -k 5 -f encrypted.txt
```

### Crack Mode (Brute Force)

Crack mode attempts all possible keys and prints candidate plaintexts.

```bash
echo "khoor" | python tool.py crack
```

**Sample output:**

```
k= 0 | khoor
k= 1 | jgnnq
k= 2 | ifmmp
k= 3 | hello
...
```

After identifying the correct key, decrypt fully:

```bash
python tool.py decrypt -k 3 -f cipher.txt
```

### Pipeline Examples (UNIX Chaining)

**Decrypt and filter for a keyword:**

```bash
cat cipher.txt | python tool.py decrypt -k 20 | grep today
```

### Custom Alphabet Example

**Default alphabet:**

```
abcdefghijklmnopqrstuvwxyz
```

**Example including digits:**

```bash
echo "abc123" | python tool.py encrypt -k 2 --alphabet "abcdefghijklmnopqrstuvwxyz0123456789"
```

Here: `m = 36` (modulo base automatically adjusts)

---

### Example using our Assignment/In-class activity

**Ciphertext:**

```
cz sio zyff xiqh symnylxus mnuhx oj nixus
```

**Step 1: Identify key**

```bash
echo "cz sio zyff xiqh symnylxus mnuhx oj nixus" | python tool.py crack
```

**Step 2: Decrypt with discovered key (k = 20)**

```bash
echo "cz sio zyff xiqh symnylxus mnuhx oj nixus" | python tool.py decrypt -k 20
```

**Plaintext:**

```
if you fell down yesterday stand up today
```

_Attributed author: H. G. Wells_

---

**Author:** Bryan Jesus Mangapit
**Subject:** MIT 281
