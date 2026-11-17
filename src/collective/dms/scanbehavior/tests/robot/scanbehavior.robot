*** Settings ***
Documentation  collective.dms.scanbehavior keywords, built on the ui_plone${PLONE_MAJOR}.robot keywords.
...            Robot Framework 3.0 syntax (shared with the Plone 4.3 environment).
Resource  ui_plone${PLONE_MAJOR}.robot


*** Variables ***
${SCAN_DATE_ID}  form-widgets-IScanFields-scan_date


*** Keywords ***
Open a manager browser
    Open test browser
    Enable autologin as  Manager

Add a scanned document
    [Arguments]  ${title}
    Go to  ${PLONE_URL}/++add++ScannedDocument
    Wait until page contains element  css=#form-widgets-IBasic-title
    Input text  css=#form-widgets-IBasic-title  ${title}

Fill the scan fields
    [Documentation]  ${scan_date}: YYYY-MM-DD HH:MM
    [Arguments]  ${scan_id}  ${version}  ${pages_number}  ${scan_date}  ${scan_user}  ${scanner}
    Open the form tab  Scan
    Input text  css=#form-widgets-IScanFields-scan_id  ${scan_id}
    Input text  css=#form-widgets-IScanFields-version  ${version}
    Input text  css=#form-widgets-IScanFields-pages_number  ${pages_number}
    Input the datetime  ${SCAN_DATE_ID}  ${scan_date}
    Input text  css=#form-widgets-IScanFields-scan_user  ${scan_user}
    Input text  css=#form-widgets-IScanFields-scanner  ${scanner}

Save the form
    Click button  css=#form-buttons-save

The scan fields are displayed
    [Arguments]  ${scan_id}  ${version}  ${pages_number}  ${scan_date}  ${scan_user}  ${scanner}
    Element should contain  css=#form-widgets-IScanFields-scan_id  ${scan_id}
    Element should contain  css=#form-widgets-IScanFields-version  ${version}
    Element should contain  css=#form-widgets-IScanFields-pages_number  ${pages_number}
    The datetime is displayed  ${SCAN_DATE_ID}  ${scan_date}
    Element should contain  css=#form-widgets-IScanFields-scan_user  ${scan_user}
    Element should contain  css=#form-widgets-IScanFields-scanner  ${scanner}

Open the edit form
    Click link  css=#contentview-edit a
    Wait until page contains element  css=#form-buttons-save

The scan fields are in the edit form
    [Arguments]  ${scan_id}  ${version}  ${pages_number}  ${scan_date}  ${scan_user}  ${scanner}
    Open the form tab  Scan
    Textfield value should be  css=#form-widgets-IScanFields-scan_id  ${scan_id}
    Textfield value should be  css=#form-widgets-IScanFields-version  ${version}
    Textfield value should be  css=#form-widgets-IScanFields-pages_number  ${pages_number}
    The datetime input contains  ${SCAN_DATE_ID}  ${scan_date}
    Textfield value should be  css=#form-widgets-IScanFields-scan_user  ${scan_user}
    Textfield value should be  css=#form-widgets-IScanFields-scanner  ${scanner}

The datetime is displayed
    [Documentation]  Display widget of a datetime (short locale format, 3/15/24 10:30 AM on Plone 4 and 6),
    ...              ${datetime}: YYYY-MM-DD HH:MM
    [Arguments]  ${id}  ${datetime}
    ${text}=  Evaluate  datetime.datetime.strptime('${datetime}', '%Y-%m-%d %H:%M').strftime('%-m/%-d/%y %-I:%M %p')
    ...  modules=datetime
    Element should contain  css=#formfield-${id}  ${text}

The field error contains
    [Arguments]  ${id}  ${text}
    Element should contain  css=#formfield-${id}  ${text}
