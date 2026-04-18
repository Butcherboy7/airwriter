import os
import sys

def patch_mediapipe():
    # Detect path to the bindings file
    path = os.path.join('venv', 'Lib', 'site-packages', 'mediapipe', 'tasks', 'python', 'core', 'mediapipe_c_bindings.py')
    
    if not os.path.exists(path):
        print(f"Error: Could not find the file at {path}")
        print("Make sure you have created the virtual environment (venv) and installed mediapipe.")
        return

    with open(path, 'r') as f:
        content = f.read()

    old_code = '_shared_lib.free.argtypes = [ctypes.c_void_p]'
    
    # Check if already patched
    if 'try:' in content and '_shared_lib.free.argtypes' in content and 'AttributeError' in content:
        print("MediaPipe is already patched! No changes needed.")
        return

    if old_code not in content:
        print("Error: Could not find the specific line to patch. The library version might be different.")
        return

    new_code = """try:
    _shared_lib.free.argtypes = [ctypes.c_void_p]
    _shared_lib.free.restype = None
  except AttributeError:
    import ctypes as _ct; _crt = _ct.cdll.msvcrt if os.name == "nt" else _ct.CDLL(None); _crt.free.argtypes = [_ct.c_void_p]; _crt.free.restype = None; _shared_lib.free = _crt.free"""

    new_content = content.replace(old_code, new_code)

    with open(path, 'w') as f:
        f.write(new_content)
    
    print("Success: MediaPipe C Bindings have been patched for Python 3.13!")

if __name__ == "__main__":
    patch_mediapipe()
