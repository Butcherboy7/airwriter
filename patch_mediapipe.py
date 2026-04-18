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
        lines = f.readlines()

    # Check if already patched
    is_patched = False
    for line in lines:
        if ('try:' in line and '_shared_lib.free.argtypes' in line and 'AttributeError' in line) or \
           ('_crt = ctypes.cdll.msvcrt' in line):
            is_patched = True
            break

    if is_patched:
        print("MediaPipe is already patched! No changes needed.")
        return

    # Find the load_raw_library function and its return statement
    new_lines = []
    found_load_raw = False
    patch_applied = False
    
    patch_code = [
        '\n',
        '  # Register "free()" — Python 3.13 may not expose \'free\' from the DLL directly.\n',
        '  # Fall back to loading it from the C runtime (msvcrt on Windows).\n',
        '  try:\n',
        '    _shared_lib.free.argtypes = [ctypes.c_void_p]\n',
        '    _shared_lib.free.restype = None\n',
        '  except AttributeError:\n',
        '    if os.name == "nt":\n',
        '      _crt = ctypes.cdll.msvcrt\n',
        '    else:\n',
        '      _crt = ctypes.CDLL(None)\n',
        '    _crt.free.argtypes = [ctypes.c_void_p]\n',
        '    _crt.free.restype = None\n',
        '    _shared_lib.free = _crt.free\n'
    ]

    for i in range(len(lines)):
        line = lines[i]
        if 'def load_raw_library' in line:
            found_load_raw = True
        
        # If we find the return statement of load_raw_library, insert the patch before it
        if found_load_raw and 'return _shared_lib' in line and not patch_applied:
            new_lines.extend(patch_code)
            patch_applied = True
        
        new_lines.append(line)

    if not patch_applied:
        print("Error: Could not find a suitable place to inject the patch. The library structure might be too different.")
        return

    with open(path, 'w') as f:
        f.writelines(new_lines)
    
    print("Success: MediaPipe C Bindings have been patched for Python 3.13!")

if __name__ == "__main__":
    patch_mediapipe()
