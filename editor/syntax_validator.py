import re

class SyntaxValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate(self, code):
        self.errors = []
        self.warnings = []
        
        lines = code.split('\n')
        
        self._check_version_declaration(lines)
        self._check_declaration_statement(lines)
        self._check_bracket_matching(code)
        self._check_indentation(lines)
        self._check_common_mistakes(lines)
        
        return self.errors + self.warnings
    
    def _check_version_declaration(self, lines):
        if not lines:
            return
        
        found = False
        for i, line in enumerate(lines[:5]):
            if re.match(r'^\s*//@version\s*=\s*6', line):
                found = True
                break
            elif re.match(r'^\s*//@version\s*=\s*[1-5]', line):
                self.warnings.append({
                    'line': i + 1,
                    'message': f'Obsolete Pine Script version. Use //@version=6',
                    'severity': 'warning'
                })
                found = True
                break
        
        if not found and any(line.strip() and not line.strip().startswith('//') for line in lines[:10]):
            self.warnings.append({
                'line': 1,
                'message': 'Missing version declaration //@version=6',
                'severity': 'warning'
            })
    
    def _check_declaration_statement(self, lines):
        code = '\n'.join(lines)
        code_no_comments = re.sub(r'//.*', '', code)
        
        if not re.search(r'\b(indicator|strategy|library)\s*\(', code_no_comments):
            self.warnings.append({
                'line': 1,
                'message': 'Missing declaration: indicator(), strategy() or library()',
                'severity': 'warning'
            })
    
    def _check_bracket_matching(self, code):
        stack = []
        brackets = {'(': ')', '[': ']', '{': '}'}
        closing = {')': '(', ']': '[', '}': '{'}
        
        code_clean = re.sub(r'"[^"]*"', '', code)
        code_clean = re.sub(r"'[^']*'", '', code_clean)
        code_clean = re.sub(r'//.*', '', code_clean)
        
        line_num = 1
        for char in code_clean:
            if char == '\n':
                line_num += 1
            elif char in brackets:
                stack.append((char, line_num))
            elif char in closing:
                if not stack:
                    self.errors.append({
                        'line': line_num,
                        'message': f'Closing bracket "{char}" without matching opening',
                        'severity': 'error'
                    })
                else:
                    open_bracket, open_line = stack.pop()
                    if brackets[open_bracket] != char:
                        self.errors.append({
                            'line': line_num,
                            'message': f'Mismatched brackets: "{open_bracket}" opened at line {open_line}, but found "{char}"',
                            'severity': 'error'
                        })
        
        for bracket, line_num in stack:
            self.errors.append({
                'line': line_num,
                'message': f'Unclosed bracket "{bracket}"',
                'severity': 'error'
            })
    
    def _check_indentation(self, lines):
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            
            spaces = len(line) - len(line.lstrip(' '))
            
            if spaces % 4 != 0 and line.strip():
                self.warnings.append({
                    'line': i + 1,
                    'message': f'Non-standard indentation (use multiples of 4 spaces)',
                    'severity': 'warning'
                })
    
    def _check_common_mistakes(self, lines):
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            if 'transp' in line and not line_stripped.startswith('//'):
                self.errors.append({
                    'line': i + 1,
                    'message': 'Parameter "transp" removed in v6. Use color.new(color, transparency)',
                    'severity': 'error'
                })
            
            if re.search(r'strategy\.(entry|order|exit|close|cancel).*\bwhen\s*=', line):
                self.errors.append({
                    'line': i + 1,
                    'message': 'Parameter "when" removed in v6. Use if-statement instead',
                    'severity': 'error'
                })
            
            if re.search(r'\b\d+\s*/\s*\d+\b', line) and not line_stripped.startswith('//'):
                self.warnings.append({
                    'line': i + 1,
                    'message': 'In v6, integer division can return decimals. Use int() if needed',
                    'severity': 'info'
                })
            
            if re.search(r'\bbool\s+\w+\s*=\s*na\b', line):
                self.errors.append({
                    'line': i + 1,
                    'message': 'In v6, bool variables cannot be na. Use true or false',
                    'severity': 'error'
                })
            
            if re.search(r'timeframe\.period\s*==\s*["\']([DWMH])["\']', line):
                match = re.search(r'timeframe\.period\s*==\s*["\']([DWMH])["\']', line)
                if match:
                    tf = match.group(1)
                    self.warnings.append({
                        'line': i + 1,
                        'message': f'In v6, timeframe.period always includes multiplier. Use "1{tf}" instead of "{tf}"',
                        'severity': 'warning'
                    })
            
            if re.search(r'(true|false|na|\d+|"[^"]*"|\'[^\']*\')[[\d+\]]', line):
                self.errors.append({
                    'line': i + 1,
                    'message': 'In v6, cannot use [] on literal values or constants',
                    'severity': 'error'
                })
            
            if re.search(r'plot\s*\([^)]*offset\s*=\s*[a-zA-Z_]\w*', line):
                self.warnings.append({
                    'line': i + 1,
                    'message': 'Parameter offset must be "simple" value, not "series"',
                    'severity': 'warning'
                })
