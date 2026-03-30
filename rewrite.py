import re
from pathlib import Path

file_path = r'c:\Users\kj anand\Downloads\Form 9A\form.html'
text = Path(file_path).read_text(encoding='utf-8')

text = text.replace('class="form-card"', 'class="form-container"')

# We want to find each section starting with <div class="section-divider">...</div>
parts = re.split(r'<!-- ═══ SECTION \d+:[^=]+═══ -->', text)

if len(parts) > 1:
    out = [parts[0]]
    for i in range(1, len(parts)):
        sec_content = parts[i]
        
        # Check if the submit-bar is in this section (last one)
        rest = ""
        if 'class="submit-bar"' in sec_content:
            split_sec = sec_content.split('<!-- ═══ Submit ═══ -->')
            if len(split_sec) > 1:
                sec_content = split_sec[0]
                rest = '<!-- ═══ Submit ═══ -->' + split_sec[1]
            else:
                last_idx = sec_content.rfind('<div class="submit-bar">')
                rest = sec_content[last_idx:]
                sec_content = sec_content[:last_idx]
        
        match = re.search(r'<div class="section-divider">([^<]+)</div>', sec_content)
        if match:
            sec_title = match.group(1)
            sec_content = re.sub(r'<div class="section-divider">[^<]+</div>', '', sec_content, 1)
        else:
            sec_title = "Section Details"
            
        sec_content = sec_content.replace('class="form-row"', 'class="form-group"')
        
        new_sec = f'''
        <div class="gov-section">
            <div class="gov-section-left">
                <div class="section-title">{sec_title}</div>
{sec_content.rstrip()}
            </div>
            <div class="gov-section-right">
                <strong>Instructions:</strong><br><br>
                Please fill all the mandatory fields marked with an asterisk (*).<br><br>
                Ensure data matches your proof documents exactly.
            </div>
        </div>
{rest}'''
        out.append(new_sec)

    Path(file_path).write_text(''.join(out), encoding='utf-8')
    print('Converted layout successfully')
else:
    print('No sections found')
