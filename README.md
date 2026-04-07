# Patient Portal - Hardened Version

## Environment Setup

### Step 1: Verify Python and Setup Virtual Environment

``` bash
python3 --version
python3 -m venv venv
```

Windows:

```bash
.\venv\Scripts\activate.bat
```

macOS/Linux:

```bash
source venv/bin/activate
```

### Step 2: Install Requirements

```bash
python3 -m pip install -r requirements.txt
```

### Step 3: Run Flask

```bash
python3 app.py
```

Then open your browser and go to: `http://localhost:5000`
