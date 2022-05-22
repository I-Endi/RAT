# Creating Windows executable

## 0: Edit IP and HOST in client_main.py
Change IP and HOST at bottom of file

## 1: Merge project files together
### In Linux:

```bash
cat file1.py file2.py ... > client_all.py
```

### In Windows:

```python
import shutil

with open('client_all.py','wb') as wfd:
    for f in ['file1.py','file2.py','file3.py']:
        with open(f,'rb') as fd:
            shutil.copyfileobj(fd, wfd)
```

## 2: Remove imports

Remove imports like:

```python
from client.connection import Connection
from client.rev_shell import Shell
```

## 3: Create .exe with pyinstaller

```bash
pyinstaller --noconfirm --onefile --windowed  "client_all.py"
```
