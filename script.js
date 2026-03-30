// Modern Form Validation for CRM-style Form 9A
function validateModernForm() {
    const form = document.getElementById('modernForm');
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    let firstErrorField = null;

    // Reset styles
    inputs.forEach(input => {
        input.style.borderColor = '#ccd0d7';
    });

    // Check individual inputs
    inputs.forEach(input => {
        if (!input.value.trim() || (input.type === 'radio' && !isRadioGroupChecked(input.name))) {
            isValid = false;
            input.style.borderColor = '#d93025';
            if (!firstErrorField) firstErrorField = input;
        }
    });

    if (isValid) {
        showSuccessModal();
    } else {
        if (firstErrorField) {
            firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstErrorField.focus();
        }
        alert('Please complete all mandatory fields marked with an asterisk (*).');
    }
}

function isRadioGroupChecked(name) {
    const radios = document.getElementsByName(name);
    for (const r of radios) {
        if (r.checked) return true;
    }
    return false;
}

function showSuccessModal() {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
        display: flex; justify-content: center; align-items: center;
        z-index: 10000; animation: fadeIn 0.3s ease;
    `;
    
    modal.innerHTML = `
        <div style="background: white; padding: 40px; border-radius: 12px; text-align: center; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);">
            <div style="width: 80px; height: 80px; background: #e6f4ea; color: #1e8e3e; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 20px;">
                <i class="fa-solid fa-check" style="font-size: 40px;"></i>
            </div>
            <h2 style="color: #1a1a1b; margin-bottom: 10px;">Details Validated</h2>
            <p style="color: #5f6368; margin-bottom: 30px;">The Form 49A details have been successfully recorded in the CRM system.</p>
            <button onclick="location.reload()" style="background: #0b57d0; color: white; border: none; padding: 12px 30px; border-radius: 6px; font-weight: 600; cursor: pointer;">
                Close & Restart
            </button>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// Inline animation
const style = document.createElement('style');
style.innerHTML = `
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(style);
