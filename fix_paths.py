import os
import re
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Scan and fix hardcoded absolute paths in source files.")
    parser.add_argument("root", help="Root folder to scan for source files.")
    parser.add_argument("--apply", action="store_true",
                        help="Apply fixes to files (otherwise, dry-run only).")
    parser.add_argument("--ext", action="append",
                        help="Limit scanning to these file extensions (e.g. --ext py --ext sh).")
    args = parser.parse_args()

    root_path = args.root
    apply_changes = args.apply
    # File extensions to include
    exts_filter = [ext.lower().lstrip('.') for ext in (args.ext or [])]
    if not exts_filter:
        exts_filter = ["py", "sh", "bat", "conf", "inf"]

    # Directories to ignore during recursion
    ignore_dirs = {".venv", "venv", "__pycache__", ".git"}  # common environmentos.path.join(os.sep, 'cache') folders:contentReference[oaicite:9]{index=9}

    # Regex patterns to identify absolute paths
    pattern_quoted = re.compile(r'(?P<prefix>r?|f?)(?P<quote>["\'])(?P<path>(?:[A-Za-z]:[\\os.path.join(os.sep, ']|', ')[^')"\']*)(?P=quote)')
    pattern_unquoted = re.compile(r'(?P<path>(?:[A-Za-z]:[\\os.path.join(os.sep, ']|', ')[^\')'"\s]+)')

    files_scanned = 0
    issues_found = 0
    issues_fixed = 0
    issues_skipped = 0

    for root, dirs, files in os.walk(root_path):
        # Prune ignored directories from traversal
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for filename in files:
            file_ext = Path(filename).suffix[1:].lower()
            if file_ext in exts_filter:
                file_path = os.path.join(root, filename)
                # Double-check if any ignored dir in the full path
                if any(part in ignore_dirs for part in Path(file_path).parts):
                    continue
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")
                    continue

                files_scanned += 1
                file_changed = False
                new_lines = []
                for lineno, line in enumerate(lines, start=1):
                    stripped = line.lstrip()
                    # Skip full-line comments in supported file types
                    if (file_ext in {"py", "sh", "conf", "inf"} and stripped.startswith("#")) or \
                       (file_ext == "bat" and (stripped.lower().startswith("rem") or stripped.startswith("::"))):
                        new_lines.append(line)
                        continue
                    # Skip lines that appear to define regex patterns for hardcoded paths (to avoid false positives)
                    if 'pattern' in line and any(x in line for x in ("/usr/", "/etc/", "/boot/", "/dev/", "C:\\", "D:\\")):
                        new_lines.append(line)
                        continue

                    # Function to generate replacement code for a found path
                    def generate_code(p: str) -> str:
                        if file_ext != "py":
                            # Only auto-rewrite code in Python files; other file types remain unchanged in apply.
                            return p
                        # For Python, build a dynamic path expression
                        # Windows absolute path (with drive letter):
                        if len(p) >= 2 and p[1] == ':':
                            drive = p[:2]  # e.g., "C:"
                            parts = re.split(r'[\\os.path.join(os.sep, ']')', p)[1:]
                            if parts and parts[0] == '':
                                parts = parts[1:]
                            if parts and parts[0].lower() == 'users':
                                # Replace "C:\Users\Name\..." with Path.home():contentReference[oaicite:10]{index=10}
                                remaining = parts[2:] if len(parts) >= 2 else []
                                code = "Path.home()"
                                for part in remaining:
                                    code += f" / '{part}'"
                                return code
                            if parts and parts[0].lower().startswith('program files'):
                                # Replace "C:\Program Files\..." with environment variable:contentReference[oaicite:11]{index=11}
                                env_key = 'ProgramFiles'
                                if parts[0].lower().startswith('program files (x86'):
                                    env_key = 'ProgramFiles(x86)'
                                default_path = f"{drive}\\{parts[0]}"
                                remaining = parts[1:]
                                if remaining:
                                    inner = "', '".join(remaining)
                                    return f"os.path.join(os.environ.get('{env_key}', '{default_path}'), '{inner}')"
                                else:
                                    return f"os.environ.get('{env_key}', '{default_path}')"
                            if parts and parts[0].lower() == 'windows':
                                # Replace "C:\Windows\..." with %SystemRoot%
                                env_key = 'SystemRoot'
                                default_path = f"{drive}\\Windows"
                                remaining = parts[1:]
                                if remaining:
                                    inner = "', '".join(remaining)
                                    return f"os.path.join(os.environ.get('{env_key}', '{default_path}'), '{inner}')"
                                else:
                                    return f"os.environ.get('{env_key}', '{default_path}')"
                            # Generic Windows path: use os.path.join with drive and parts
                            if parts:
                                inner = "', '".join(parts)
                                return f"os.path.join('{drive}\\', '{inner}')"
                            else:
                                return f"r'{drive}\\'"  # just a drive (rare case)

                        elif p.startswith(os.sep):
                            parts = [pt for pt in p.split(os.sep) if pt]  # split and remove empty elements
                            if parts and parts[0] == 'home' and len(parts) >= 2:
                                # Replace "/home/<user>/..." with Path.home():contentReference[oaicite:12]{index=12}
                                remaining = parts[2:] if len(parts) >= 2 else []
                                code = "Path.home()"
                                for part in remaining:
                                    code += f" / '{part}'"
                                return code
                            if parts and parts[0] == 'root':
                                # Replace "/root/..." with Path.home() (root's home directory)
                                remaining = parts[1:]
                                code = "Path.home()"
                                for part in remaining:
                                    code += f" / '{part}'"
                                return code
                            # If path is within the project tree, make it relative to the current file
                            try:
                                target_path = Path(p)
                                file_dir = Path(file_path).parent
                                common = Path(os.path.commonpath([file_dir, target_path]))
                            except Exception:
                                common = None
                            if common and common != Path(os.sep):
                                # Compute relative path from this file to the target path
                                rel_path = os.path.relpath(p, file_dir)
                                rel_parts = Path(rel_path).parts
                                # Build Path(__file__) with appropriate parents
                                code = "Path(__file__)"
                                ups = sum(1 for part in rel_parts if part == os.pardir)
                                if ups > 0:
                                    code += "".join(".parent" * ups)
                                else:
                                    code += ".parent"
                                for part in rel_parts[ups:]:
                                    code += f" / '{part}'"
                                return code
                            # Otherwise, use os.path.join with os.sep for absolute path
                            if parts:
                                inner = "', '".join(parts)
                                return f"os.path.join(os.sep, '{inner}')"
                            else:
                                return "os.sep"  # path was os.sep (root)

                        # If none of the above, return as-is
                        return p

                    # Prepare to find and replace paths in the current line
                    line_out = line
                    matches = list(pattern_quoted.finditer(line))
                    if matches:
                        issues_found += len(matches)
                        # In dry-run, do not actually replace yet; in apply, perform substitution
                        if apply_changes and file_ext == "py":
                            line_out = pattern_quoted.sub(lambda m: generate_code(m.group('path')), line_out)
                            issues_fixed += len(matches)
                            file_changed = True
                        else:
                            issues_skipped += len(matches)
                        # Log each occurrence
                        for m in matches:
                            print(f"{'[Fixed]' if (apply_changes and file_ext == 'py') else '[Found]'} "
                                  f"{file_path}:{lineno}: {m.group('path')}")

                    # Handle unquoted paths (if any) on the line (excluding those already handled)
                    line_temp = line_out if (apply_changes and file_ext == "py") else line  # consider original if not replaced
                    if matches and not apply_changes:
                        # Mask out quoted matches to avoid double-counting in dry-run
                        line_temp = pattern_quoted.sub('', line_temp)
                    matches2 = list(pattern_unquoted.finditer(line_temp))
                    if matches2:
                        issues_found += len(matches2)
                        if apply_changes and file_ext == "py":
                            line_out = pattern_unquoted.sub(lambda m: generate_code(m.group('path')), line_out)
                            issues_fixed += len(matches2)
                            file_changed = True
                        else:
                            issues_skipped += len(matches2)
                        for m in matches2:
                            print(f"{'[Fixed]' if (apply_changes and file_ext == 'py') else '[Found]'} "
                                  f"{file_path}:{lineno}: {m.group('path')}")

                    new_lines.append(line_out)
                # Write changes back to file if any fixes were made
                if apply_changes and file_changed and file_ext == "py":
                    try:
                        with open(file_path, 'w', encoding='utf-8') as wf:
                            wf.writelines(new_lines)
                    except Exception as e:
                        print(f"Error writing changes to {file_path}: {e}")
                else:
                    # If no changes or not applying, just keep original lines (no write needed for dry-run)
                    new_lines = lines

    # Print summary report
    if apply_changes:
        print(f"\nScan complete. Files scanned: {files_scanned}, Issues fixed: {issues_fixed}, Issues skipped: {issues_skipped}")
    else:
        print(f"\nScan complete (dry-run). Files scanned: {files_scanned}, Issues found: {issues_found}")

if __name__ == "__main__":
    main()
