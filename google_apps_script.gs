/* 
   FORM 49A - GOOGLE APPS SCRIPT BACKEND (VER-8 FIXED)
   Safety Check added for empty sheets.
*/

const SHEET_ID   = '1X85-75wsZG7ZFJp5KQ_VV3zRRoYw9DjBdRJ62JRFgyc'; 
const SHEET_NAME = 'Users';

function doGet(e) {
  var p = e.parameter;
  var callback = p.callback || 'callback';
  var result;
  try {
    if (p.action === 'signup') result = handleSignup(p);
    else if (p.action === 'login') result = handleLogin(p);
    else if (p.action === 'submitForm') result = handleSubmitForm(p);
    else result = { success: false, message: 'Unknown action.' };
  } catch(err) {
    result = { success: false, message: 'Server error: ' + err.message };
  }
  return ContentService.createTextOutput(callback + '(' + JSON.stringify(result) + ')').setMimeType(ContentService.MimeType.JAVASCRIPT);
}

function handleSignup(p) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) sheet.appendRow(['Name', 'Email', 'Username', 'Password', 'RegisteredAt']);
  var data = sheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    if (data[i][2].toString().toLowerCase() === p.username.toLowerCase()) return { success: false, message: 'Username already exists.' };
  }
  sheet.appendRow([p.name, p.email, p.username, p.password, new Date().toLocaleString()]);
  return { success: true };
}

function handleLogin(p) {
  var sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  if (!sheet) return { success: false, message: 'No users found.' };
  var data = sheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    if (data[i][2].toString() === p.username && data[i][3].toString() === p.password) return { success: true, name: data[i][0] };
  }
  return { success: false, message: 'Invalid credentials.' };
}

function handleSubmitForm(p) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheetName = 'Applications';
  var sheet = ss.getSheetByName(sheetName);

  var config = [
    { id: 'username',          lbl: 'Username (Typist)' },
    { id: 'timestamp',         lbl: 'Timestamp' },
    { id: 'timeTaken',         lbl: 'Time Taken' },
    { id: 'title',             lbl: 'Title' },
    { id: 'lastName',          lbl: 'Last Name / Surname' },
    { id: 'firstName',         lbl: 'First Name' },
    { id: 'middleName',        lbl: 'Middle Name' },
    { id: 'abbrName',          lbl: 'Name on PAN Card' },
    { id: 'otherName',         lbl: 'Ever known by other name?' },
    { id: 'otherLastName',     lbl: 'Other: Last Name' },
    { id: 'otherFirstName',    lbl: 'Other: First Name' },
    { id: 'otherMiddleName',   lbl: 'Other: Middle Name' },
    { id: 'gender',            lbl: 'Gender' },
    { id: 'dob',               lbl: 'Date of Birth' },
    { id: 'fatherLast',        lbl: "Father's Last Name" },
    { id: 'fatherFirst',       lbl: "Father's First Name" },
    { id: 'fatherMiddle',      lbl: "Father's Middle Name" },
    { id: 'singleParent',      lbl: 'Single Parent?' },
    { id: 'motherLast',        lbl: "Mother's Last Name" },
    { id: 'motherFirst',       lbl: "Mother's First Name" },
    { id: 'motherMiddle',      lbl: "Mother's Middle Name" },
    { id: 'addrFlat',          lbl: 'Flat / Door / Block' },
    { id: 'addrBuilding',      lbl: 'Building / Village' },
    { id: 'addrRoad',          lbl: 'Road / Street / PO' },
    { id: 'addrArea',          lbl: 'Area / Locality' },
    { id: 'addrCity',          lbl: 'Town / City / District' },
    { id: 'addrState',         lbl: 'State / Union Territory' },
    { id: 'addrPincode',       lbl: 'Pincode' },
    { id: 'addrCountry',       lbl: 'Country' },
    { id: 'officeName',        lbl: 'Office Name' },
    { id: 'officeFlat',        lbl: 'Office Flat / Door' },
    { id: 'officeCity',        lbl: 'Office Town / District' },
    { id: 'officeState',       lbl: 'Office State / UT' },
    { id: 'officePincode',     lbl: 'Office Pincode' },
    { id: 'phoneRes',          lbl: 'Phone (Residence)' },
    { id: 'phoneOff',          lbl: 'Phone (Office)' },
    { id: 'mobile',            lbl: 'Mobile Number' },
    { id: 'email',             lbl: 'Email Address' },
    { id: 'applicantStatus',   lbl: 'Applicant Status' },
    { id: 'regNo',             lbl: 'Registration Number' },
    { id: 'incomeSource',      lbl: 'Source of Income' },
    { id: 'aoArea',            lbl: 'AO Area Code' },
    { id: 'aoType',            lbl: 'AO Type' },
    { id: 'aoRange',           lbl: 'AO Range Code' },
    { id: 'aoNo',              lbl: 'AO No.' },
    { id: 'proofId',           lbl: 'Proof of Identity' },
    { id: 'proofAddr',         lbl: 'Proof of Address' },
    { id: 'proofDob',          lbl: 'Proof of Date of Birth' }
  ];

  var formData = JSON.parse(p.data);
  formData.username  = p.username || 'Guest';
  formData.timestamp = new Date().toLocaleString();

  // Safety Check: If sheet is broken or missing Time Taken, reset it
  if (sheet) {
    var lastCol = sheet.getLastColumn();
    var hasTimeTaken = false;
    if (lastCol > 0) {
      var headers = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
      hasTimeTaken = (headers.indexOf('Time Taken') !== -1);
    }
    
    if (!hasTimeTaken) {
      ss.deleteSheet(sheet);
      sheet = null;
    }
  }

  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
    sheet.appendRow(config.map(function(c) { return c.lbl; }));
    sheet.setFrozenRows(1);
    sheet.getRange("1:1").setFontWeight("bold").setBackground("#f0f0f0");
  }

  var row = config.map(function(c) {
    return formData[c.id] || '';
  });

  sheet.appendRow(row);
  return { success: true };
}
