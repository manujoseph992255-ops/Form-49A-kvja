import re
from pathlib import Path

file_path = r'c:\Users\kj anand\Downloads\Form 9A\form.html'
text = Path(file_path).read_text(encoding='utf-8')

# Extract the existing Javascript block so we don't destroy custom logic
js_match = re.search(r'<script>(.*)</script>', text, flags=re.DOTALL)
js_content = js_match.group(1) if js_match else ''

# Extract Address state options as they are long
state_match = re.search(r'<select class="sel" id="addrState">(.*?)</select>', text, flags=re.DOTALL)
addr_state_options = state_match.group(1) if state_match else '<option value="">-Select-</option>'

html_head = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Online PAN Application</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
</head>
<body>
    <a href="index.html" class="logout-btn" onclick="sessionStorage.removeItem('loggedIn')">
        <i class="fa-solid fa-right-from-bracket"></i> Logout
    </a>

    <div class="form-wrap">
        
        <!-- Top App Selection Block -->
        <div class="protean-box" style="margin-bottom: 20px;">
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Select PAN Application Type<span class="star">*</span><br><span style="font-size:11px; font-weight:normal;">(New or Change Request)</span></div>
                    <select class="sel" id="appType">
                        <option value="">---Please Select---</option>
                        <option value="New PAN - Indian Citizen">New PAN - Indian Citizen (Form 49A)</option>
                    </select>
                </div>
                <div class="box-col">
                    <div class="lbl">Select Applicant Category<span class="star">*</span><br><span style="font-size:11px; font-weight:normal;">(Individual,Trust,HUF,...)</span></div>
                    <select class="sel" id="applicantStatus">
                        <option value="">---Please Select---</option>
                        <option value="Individual">Individual</option>
                        <option value="Hindu Undivided Family">Hindu Undivided Family</option>
                        <option value="Company">Company</option>
                        <option value="Firm / LLP">Firm / LLP</option>
                        <option value="Association of Persons">Association of Persons</option>
                        <option value="Body of Individuals">Body of Individuals</option>
                        <option value="Local Authority">Local Authority</option>
                        <option value="Artificial Juridical Person">Artificial Juridical Person</option>
                        <option value="Trust">Trust</option>
                    </select>
                </div>
            </div>
        </div>

        <div class="sec-hdr">Applicant information <i class="fa fa-info-circle"></i></div>
        
        <!-- Applicant Information Block -->
        <div class="protean-box">
            <div class="box-row">
                <div class="box-col" style="max-width: 33%;">
                    <div class="lbl">Title<span class="star">*</span></div>
                    <!-- Make the title select since we changed it from radio to select -->
                    <select class="sel" id="title">
                        <option value="">---Please Select---</option>
                        <option value="Shri">Shri</option>
                        <option value="Smt">Smt.</option>
                        <option value="Kumari">Kumari</option>
                        <option value="Ms">M/s</option>
                    </select>
                </div>
            </div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Last Name / Surname<span class="star">*</span></div>
                    <input type="text" class="inp" id="lastName">
                </div>
                <div class="box-col">
                    <div class="lbl">First Name</div>
                    <input type="text" class="inp" id="firstName">
                </div>
                <div class="box-col">
                    <div class="lbl">Middle Name</div>
                    <input type="text" class="inp" id="middleName">
                </div>
            </div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Date of Birth / Incorporation / Formation (DD/MM/YYYY)<span class="star">*</span></div>
                    <input type="text" class="inp" id="dob" placeholder="DD / MM / YYYY">
                </div>
                <div class="box-col">
                    <div class="lbl">Email ID<span class="star">*</span></div>
                    <input type="email" class="inp" id="email">
                </div>
                <div class="box-col">
                    <div class="lbl">Mobile Number<span class="star">*</span></div>
                    <input type="text" class="inp" id="mobile" maxlength="10">
                </div>
            </div>
            <div class="box-row" style="margin-top: 15px;">
                <div class="box-col full" style="display:flex; align-items:start; gap: 8px;">
                    <input type="checkbox" id="consentCheck" style="margin-top: 3px;">
                    <div class="disclaimer">
                        By submitting data to us and/or using our Protean e-Gov TIN web site <a href="#">https://onlineservices.proteantech.in/paam/endUserRegisterContact.html</a> you give your consent that all personal data/information that you submit to avail tax related services from Protean eGov Technologies Limited may be received, stored, processed, transmitted and or made available for view /use as mandated by law or otherwise, shall be dealt with by us in the manner and for the purposes specified / as described in the privacy policy or as mandated by law. I have also read, understood and expressly agree to be bound by the Privacy Policy <a href="#">https://tinpan.proteantech.in/privacy-policy</a>, Disclaimer and web-site usage guidelines as published by Protean on its website from time to time.
                    </div>
                </div>
            </div>
        </div>

        <div class="sec-hdr">Detailed Form Entries</div>
        
        <!-- Other Details Block (Father, Address, Source of Income, etc) -->
        <div class="protean-box">
            <div class="section-sub-hdr" style="margin-top: 5px;">Name on PAN Card</div>
            <div class="box-row">
                <div class="box-col full">
                    <div class="lbl">Abbreviated Name for PAN card<span class="star">*</span></div>
                    <input type="text" class="inp" id="abbrName">
                </div>
            </div>

            <div class="section-sub-hdr">Other Name Details</div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Have you ever been known by any other name?<span class="star">*</span></div>
                    <div class="radios">
                        <label><input type="radio" name="otherName" value="Yes"> Yes</label>
                        <label><input type="radio" name="otherName" value="No"> No</label>
                    </div>
                </div>
            </div>
            <div class="box-row" id="otherNameDetails" style="display:none;">
                <div class="box-col">
                    <div class="lbl">Other Last Name</div>
                    <input type="text" class="inp" id="otherLastName">
                </div>
                <div class="box-col">
                    <div class="lbl">Other First Name</div>
                    <input type="text" class="inp" id="otherFirstName">
                </div>
                <div class="box-col">
                    <div class="lbl">Other Middle Name</div>
                    <input type="text" class="inp" id="otherMiddleName">
                </div>
            </div>

            <div class="section-sub-hdr">Gender</div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Gender<span class="star">*</span></div>
                    <div class="radios">
                        <label><input type="radio" name="gender" value="Male"> Male</label>
                        <label><input type="radio" name="gender" value="Female"> Female</label>
                        <label><input type=\"radio\" name=\"gender\" value=\"Transgender\"> Transgender</label>
                    </div>
                </div>
            </div>

            <div class="section-sub-hdr">Parents Details</div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Father's Last Name<span class="star">*</span></div>
                    <input type="text" class="inp" id="fatherLast">
                </div>
                <div class="box-col">
                    <div class="lbl">Father's First Name<span class="star">*</span></div>
                    <input type="text" class="inp" id="fatherFirst">
                </div>
                <div class="box-col">
                    <div class="lbl">Father's Middle Name</div>
                    <input type="text" class="inp" id="fatherMiddle">
                </div>
            </div>
            <div class="box-row">
                <div class="box-col full">
                    <div class="lbl">Single Parent (Mother's name only)?</div>
                    <div class="radios">
                        <label><input type="radio" name="singleParent" value="Yes"> Yes</label>
                        <label><input type="radio" name="singleParent" value="No"> No</label>
                    </div>
                </div>
            </div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Mother's Last Name</div>
                    <input type="text" class="inp" id="motherLast">
                </div>
                <div class="box-col">
                    <div class="lbl">Mother's First Name</div>
                    <input type="text" class="inp" id="motherFirst">
                </div>
                <div class="box-col">
                    <div class="lbl">Mother's Middle Name</div>
                    <input type="text" class="inp" id="motherMiddle">
                </div>
            </div>

            <div class="section-sub-hdr">Residence Address</div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Flat / Room / Block No.<span class="star">*</span></div>
                    <input type="text" class="inp" id="addrFlat">
                </div>
                <div class="box-col">
                    <div class="lbl">Building / Village<span class="star">*</span></div>
                    <input type="text" class="inp" id="addrBuilding">
                </div>
                <div class="box-col">
                    <div class="lbl">Road / Street</div>
                    <input type="text" class="inp" id="addrRoad">
                </div>
            </div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Area / Locality</div>
                    <input type="text" class="inp" id="addrArea">
                </div>
                <div class="box-col">
                    <div class="lbl">Town / City / District<span class="star">*</span></div>
                    <input type="text" class="inp" id="addrCity">
                </div>
                <div class="box-col">
                    <div class="lbl">State / UT<span class="star">*</span></div>
                    <select class="sel" id="addrState">
                        ''' + addr_state_options + '''
                    </select>
                </div>
            </div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Pincode<span class="star">*</span></div>
                    <input type="text" class="inp" id="addrPincode" maxlength="6">
                </div>
                <div class="box-col">
                    <div class="lbl">Country</div>
                    <input type="text" class="inp" id="addrCountry" value="India">
                </div>
            </div>

            <div class="section-sub-hdr">Document Proofs</div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Proof of Identity<span class="star">*</span></div>
                    <select class="sel" id="proofId"><option value="">-Select-</option><option>Aadhaar Card</option><option>Passport</option><option>Voter ID</option></select>
                </div>
                <div class="box-col">
                    <div class="lbl">Proof of Address<span class="star">*</span></div>
                    <select class="sel" id="proofAddr"><option value="">-Select-</option><option>Aadhaar Card</option><option>Passport</option><option>Electricity Bill</option></select>
                </div>
                <div class="box-col">
                    <div class="lbl">Proof of Date of Birth<span class="star">*</span></div>
                    <select class="sel" id="proofDob"><option value="">-Select-</option><option>Aadhaar Card</option><option>Birth Certificate</option><option>Passport</option></select>
                </div>
            </div>

            <div class="section-sub-hdr">Source of Income</div>
            <div class="box-row">
                <div class="box-col">
                    <div class="lbl">Primary Source of Income<span class="star">*</span></div>
                    <select class="sel" id="incomeSource"><option value="">-Select-</option><option>Salary</option><option>Business</option><option>Other Sources</option><option>No Income</option></select>
                </div>
            </div>

            <div class="section-sub-hdr">Assessing Officer (AO) Code</div>
            <div class="box-row">
                <div class="box-col" style="max-width:200px">
                    <div class="lbl">AO Area Code<span class="star">*</span></div>
                    <input type="text" class="inp" id="aoArea" maxlength="3">
                </div>
                <div class="box-col" style="max-width:200px">
                    <div class="lbl">AO Type<span class="star">*</span></div>
                    <input type="text" class="inp" id="aoType" maxlength="2">
                </div>
                <div class="box-col" style="max-width:200px">
                    <div class="lbl">Range Code<span class="star">*</span></div>
                    <input type="text" class="inp" id="aoRange" maxlength="3">
                </div>
                <div class="box-col" style="max-width:200px">
                    <div class="lbl">AO No.<span class="star">*</span></div>
                    <input type="text" class="inp" id="aoNo" maxlength="2">
                </div>
            </div>

            <div class="box-row" style="margin-top:30px; justify-content:center;">
                <div class="box-col full" style="text-align:center;">
                    <button class="submit-btn" onclick="validateForm()">Submit</button>
                    <button class="reset-btn" onclick="location.reload()" style="background:#e5e7eb; border:1px solid #ccc; padding:12px 30px; margin-left:15px; cursor:pointer; font-size:15px; font-weight:bold; border-radius:3px; color:#333;">Reset</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    ''' + js_content + '''
    
    // Custom overriding fixes for the Protean structural changes:
    // Since title is now a select, update validate function hook:
    const oldVal = validateForm;
    validateForm = function() {
        // Enforce the consent check
        const chk = document.getElementById('consentCheck');
        if (chk && !chk.checked) {
            alert("⚠️ Please accept the privacy policy checkbox under Applicant Information before submitting.");
            return;
        }

        // Overwrite how title is checked since we made it a <select>
        if (!document.getElementById('title').value) {
            document.getElementById('title').classList.add('err');
            alert("⚠️ Please select Title.");
            document.getElementById('title').scrollIntoView();
            return;
        } else {
            document.getElementById('title').classList.remove('err');
        }

        // Call base logic 
        oldVal();
    }
    </script>
</body>
</html>'''

Path(file_path).write_text(html_head, encoding='utf-8')
print('Protean layout completely applied to form.html')

css_code = '''@import url('https://fonts.googleapis.com/css2?family=Arial:wght@400;500;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif; }

body { background: #ffffff; min-height: 100vh; padding: 40px 20px; }

.form-wrap { max-width: 1000px; margin: 0 auto; }

/* Logout button top-right */
.logout-btn {
    position: absolute; top: 15px; right: 20px; z-index: 999;
    padding: 8px 15px; font-size: 13px; font-weight: 500; color: #555; text-decoration: underline;
}

.protean-box { background: #efece0; padding: 25px 35px; margin-bottom: 30px; }
.box-row { display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 20px; }
.box-col { flex: 1; min-width: 250px; }
.box-col.full { flex: 1 1 100%; }

.sec-hdr { color: #0076a3; font-size: 18px; font-weight: normal; margin-bottom: 12px; margin-top: 30px; display: flex; align-items: center; gap: 8px; }
.sec-hdr i { font-size: 16px; }

.section-sub-hdr { color: #555; font-size: 14px; font-weight: bold; margin-bottom: 18px; margin-top: 35px; border-bottom: 1px dotted #ccc; padding-bottom: 5px; text-transform:uppercase; }

.lbl { font-size: 13px; color: #666; margin-bottom: 7px; display: block; line-height: 1.4; }
.lbl .star { color: #d00; margin-left: 2px; }

.inp, .sel { 
    width: 100%; padding: 8px 10px; border: 1px solid #ccc; background: #fff; 
    font-size: 13px; color: #333; height: 36px; border-radius: 2px;
}
.inp:focus, .sel:focus { outline: none; border-color: #0076a3; box-shadow: 0 0 3px rgba(0,118,163,0.3); }
.inp.err, .sel.err { border-color: red; }
.inp::placeholder { color: #aaa; }

.disclaimer { font-size: 12.5px; line-height: 1.6; color: #666; display: inline; }
.disclaimer a { color: #0000ee; text-decoration: underline; }

.radios { display: flex; gap: 18px; flex-wrap: wrap; align-items: center; margin-top: 8px; }
.radios label { font-size: 13.5px; color: #555; display: flex; align-items: center; gap: 5px; cursor: pointer; }
.radios input[type="radio"] { margin: 0; cursor: pointer; }

.submit-btn { background: #0076a3; color: #fff; border: none; padding: 12px 40px; border-radius: 3px; cursor: pointer; font-size: 15px; font-weight: bold; }
.submit-btn:hover { background: #005a7d; }

.field-error { color: #d00; font-size: 11px; margin-top: 5px; }

/* Modal tweaks */
.overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 9999; }
.sbox { background: white; border-radius: 5px; padding: 40px 50px; text-align: center; }
'''

Path(r'c:\Users\kj anand\Downloads\Form 9A\style.css').write_text(css_code, encoding='utf-8')
print('CSS applied successfully')
