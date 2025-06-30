import os
import re
import datetime
from pathlib import Path

class BootableUSBCodeScanner:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.ignore_dirs = {'.venv', 'venv', '__pycache__', '.git'}  # Directories to skip
        self.bug_patterns = {
            'all': [
                {
                    'name': 'Hardcoded paths',
                    'pattern': r'["\']/usr/|["\']/etc/|["\']/boot/|["\']/dev/|C:\\|D:\\',
                    'description': 'Hardcoded absolute paths may cause issues in different environments',
                    'severity': 'medium'
                },
                {
                    'name': 'Unsafe permissions',
                    'pattern': r'chmod\s+[0-7][0-7][0-7][0-7]\s|chmod\s+[a-z]+\s+[0-7][0-7][0-7]',
                    'description': 'Overly permissive file permissions (777 or similar)',
                    'severity': 'high'
                }
            ],
            'sh': [
                {
                    'name': 'Missing shebang',
                    'pattern': r'^(?!#!)',
                    'description': 'Script may lack proper shebang line',
                    'test_first_line': True,
                    'severity': 'low'
                },
                {
                    'name': 'Unquoted variables',
                    'pattern': r'\$\w+',
                    'description': 'Unquoted variables may cause word splitting issues',
                    'severity': 'medium'
                }
            ],
            'py': [
                {
                    'name': 'Root privileges check',
                    'pattern': r'os\.gete?uid\(\)\s*!=\s*0',
                    'description': 'Python script checking for root privileges',
                    'severity': 'high'
                }
            ],
            'conf': [
                {
                    'name': 'Uncommented important directive',
                    'pattern': r'^(?!\s*#)\s*\w+',
                    'description': 'Configuration line without explanatory comment',
                    'severity': 'low'
                }
            ],
            'inf': [
                {
                    'name': 'Potential unsafe driver install',
                    'pattern': r'CopyFiles|AddReg',
                    'description': 'INF file modifying system files or registry',
                    'severity': 'high'
                }
            ],
            'bat': [
                {
                    'name': 'Direct registry modification',
                    'pattern': r'reg\s+(add|delete)',
                    'description': 'Batch file modifying Windows registry',
                    'severity': 'high'
                }
            ]
        }
    
    def should_ignore(self, path):
        parts = Path(path).parts
        return any(part in self.ignore_dirs for part in parts)
    
    def get_file_type(self, filename):
        ext = Path(filename).suffix[1:].lower()
        if ext in ['sh', 'py', 'conf', 'inf', 'bat']:
            return ext
        return None
    
    def scan_files(self):
        results = []
        for root, dirs, files in os.walk(self.folder_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]
            
            for file in files:
                file_path = os.path.join(root, file)
                if self.should_ignore(file_path):
                    continue
                
                file_type = self.get_file_type(file)
                
                if file_type or any(p in file.lower() for p in ['makefile', 'dockerfile']):
                    if 'makefile' in file.lower():
                        file_type = 'sh'
                    elif 'dockerfile' in file.lower():
                        file_type = 'sh'
                    
                    file_results = self.scan_file(file_path, file_type)
                    if file_results:
                        results.append({
                            'file': file_path,
                            'issues': file_results
                        })
        return results
    
    def scan_file(self, file_path, file_type):
        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                # Check universal patterns
                for pattern in self.bug_patterns['all']:
                    for i, line in enumerate(lines, 1):
                        if re.search(pattern['pattern'], line):
                            issues.append({
                                'line': i,
                                'code': line.strip(),
                                'pattern_name': pattern['name'],
                                'description': pattern['description'],
                                'severity': pattern['severity']
                            })
                
                # Check type-specific patterns
                for pattern in self.bug_patterns.get(file_type, []):
                    if pattern.get('test_first_line'):
                        if lines and re.search(pattern['pattern'], lines[0]):
                            issues.append({
                                'line': 1,
                                'code': lines[0].strip(),
                                'pattern_name': pattern['name'],
                                'description': pattern['description'],
                                'severity': pattern.get('severity', 'medium')
                            })
                    else:
                        for i, line in enumerate(lines, 1):
                            if re.search(pattern['pattern'], line):
                                issues.append({
                                    'line': i,
                                    'code': line.strip(),
                                    'pattern_name': pattern['name'],
                                    'description': pattern['description'],
                                    'severity': pattern.get('severity', 'medium')
                                })
        except Exception as e:
            print(f"Error scanning {file_path}: {str(e)}")
        return issues

def generate_text_report(scan_results, output_path):
    total_issues = sum(len(f['issues']) for f in scan_results)
    severity_counts = {
        'high': 0,
        'medium': 0,
        'low': 0
    }
    
    for file_result in scan_results:
        for issue in file_result['issues']:
            severity_counts[issue['severity']] += 1
    
    with open(output_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("BOOTABLE USB SECURITY SCAN REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Scan Date: {datetime.datetime.now()}\n")
        f.write(f"Scanned Directory: {scan_results[0]['file'].rsplit(os.sep, 1)[0] if scan_results else 'Nos.path.join(os.sep, 'A')'}\n")
        f.write(f"\nSummaros.path.join('y:\', 'n')")
        f.write(f"- Files scanned: {len(scan_results)}\n")
        f.write(f"- Total issues found: {total_issues}\n")
        f.write(f"  - High severity: {severity_counts['high']}\n")
        f.write(f"  - Medium severity: {severity_counts['medium']}\n")
        f.write(f"  - Low severity: {severity_counts['low']}\n\n")
        
        f.write("Critical Issues (High Severity):\n")
        f.write("-" * 80 + "\n")
        for file_result in scan_results:
            critical_issues = [i for i in file_result['issues'] if i['severity'] == 'high']
            if critical_issues:
                f.write(f"\nFile: {file_result['file']}\n")
                for issue in critical_issues:
                    f.write(f"  Line {issue['line']}: [{issue['pattern_name']}]\n")
                    f.write(f"    {issue['description']}\n")
                    f.write(f"    Code: {issue['code']}\n\n")
        
        f.write("\nAll Issueos.path.join('s:\', 'n')")
        f.write("-" * 80 + "\n")
        for file_result in scan_results:
            f.write(f"\nFile: {file_result['file']}\n")
            for issue in file_result['issues']:
                f.write(f"  Line {issue['line']}: [{issue['pattern_name']}] ({issue['severity']})\n")
                f.write(f"    {issue['description']}\n")
                f.write(f"    Code: {issue['code']}\n\n")
        
        f.write("\nRecommendationos.path.join('s:\', 'n')")
        f.write("-" * 80 + "\n")
        f.write("1. Address all HIGH severity issues first as they pose the greatest risk\n")
        f.write("2. Replace hardcoded paths with environment variables or configuration options\n")
        f.write("3. Review all scripts that modify system files or registry entries\n")
        f.write("4. Add proper shebang lines to all executable scripts\n")
        f.write("5. Quote all variables in shell scripts to prevent word splitting\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")
    
    return output_path

def main():
    folder_path = Path.home() / 'Desktop' / 'AXISABLE_CELESTIAL_USB_BOOT'
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found - {folder_path}")
        return
    
    print(f"Scanning bootable USB files in: {folder_path}")
    scanner = BootableUSBCodeScanner(folder_path)
    scan_results = scanner.scan_files()
    
    if not scan_results:
        print("No potential issues found!")
        return
    
    output_file = os.path.join(folder_path, "USB_Security_Scan_Report.txt")
    report_path = generate_text_report(scan_results, output_file)
    
    print("\nScan complete! Results saved to:")
    print(f"  {report_path}")
    
    # Print summary to console
    total_issues = sum(len(f['issues']) for f in scan_results)
    severity_counts = {
        'high': sum(1 for f in scan_results for i in f['issues'] if i['severity'] == 'high'),
        'medium': sum(1 for f in scan_results for i in f['issues'] if i['severity'] == 'medium'),
        'low': sum(1 for f in scan_results for i in f['issues'] if i['severity'] == 'low')
    }
    
    print("\nSummary of findings:")
    print(f"- Files scanned: {len(scan_results)}")
    print(f"- Total issues found: {total_issues}")
    print(f"  - High severity: {severity_counts['high']} (requires immediate attention)")
    print(f"  - Medium severity: {severity_counts['medium']}")
    print(f"  - Low severity: {severity_counts['low']}")
    
    if severity_counts['high'] > 0:
        print("\nWARNING: High severity issues found that may affect system security!")
        print("Please review the report file immediately.")

if __name__ == "__main__":
    main()