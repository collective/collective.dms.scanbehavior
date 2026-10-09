*** Settings ***
Documentation  Plone 4.3 keywords. Same keyword names and arguments as ui_plone6.robot.
...            Robot Framework 3.0 syntax (Python 2 environment).
...            Checked on Plone 4.3 (collective.dms.scanbehavior master): The status message contains,
...            Open the form tab, the datetime keywords. The others are NOT CHECKED YET.
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote


*** Variables ***
${MODAL}  css=div.overlay-ajax
${ERROR_PAGE_TEXT}  there seems to be an error
${NOT_FOUND_TEXT}  This page does not seem to exist


*** Keywords ***
Log in with the login form
    [Documentation]  Real login (creates the user folder), unlike autologin
    [Arguments]  ${username}  ${password}
    Disable autologin
    Go to  ${PLONE_URL}/login_form
    Input text  css=#__ac_name  ${username}
    Input password  css=#__ac_password  ${password}
    Click button  css=input[name="submit"]
    Wait until page contains element  css=#portal-personaltools

Click the content action
    [Documentation]  Item of the Actions menu (object_buttons), by action id
    [Arguments]  ${action_id}
    Click element  css=#plone-contentmenu-actions dt.actionMenuHeader a
    Wait until element is visible  css=#plone-contentmenu-actions-${action_id}
    Click element  css=#plone-contentmenu-actions-${action_id}

The content action is available
    [Arguments]  ${action_id}  ${expected}=${True}
    Click element  css=#plone-contentmenu-actions dt.actionMenuHeader a
    Wait until element is visible  css=#plone-contentmenu-actions dd.actionMenuContent
    Run keyword if  ${expected}
    ...  Page should contain element  css=#plone-contentmenu-actions-${action_id}
    ...  ELSE  Page should not contain element  css=#plone-contentmenu-actions-${action_id}

Open the add menu
    Click element  css=#plone-contentmenu-factories dt.actionMenuHeader a
    Wait until element is visible  css=#plone-contentmenu-factories dd.actionMenuContent

The personal action links to
    [Documentation]  Item of the user menu (user actions), by action id
    [Arguments]  ${action_id}  ${url}
    Element attribute value should be  css=#personaltools-${action_id} a  href  ${url}

The personal action is not available
    [Arguments]  ${action_id}
    Page should not contain element  css=#personaltools-${action_id}

The modal is open
    [Documentation]  Overlay (Plone 4) or modal (Plone 6) showing a form
    Wait until element is visible  ${MODAL} form

Modal element
    [Documentation]  Locator of the element with this id inside the modal
    ...              (an argument starting with # would be a robot comment)
    [Arguments]  ${id}
    [Return]  ${MODAL} [id="${id}"]

Save the modal
    Click button  ${MODAL} #form-buttons-save

Cancel the modal
    Click button  ${MODAL} #form-buttons-cancel

The modal is closed
    Wait until element is not visible  ${MODAL}

The status message contains
    [Documentation]  Skips the hidden, empty #kssPortalMessage placeholder
    [Arguments]  ${text}
    Wait until element contains  css=.portalMessage:not(#kssPortalMessage)  ${text}

The page is not an error
    Page should not contain  ${ERROR_PAGE_TEXT}

The page is not found
    Page should contain  ${NOT_FOUND_TEXT}

The edit link is not available
    Page should not contain element  css=#contentview-edit

Open the form tab
    [Documentation]  Fieldset tab of a z3c.form form, by label
    [Arguments]  ${label}
    Click element  xpath=//ul[contains(@class, "formTabs")]//a[normalize-space(.)="${label}"]

Input the datetime
    [Documentation]  collective.z3cform.datetimewidget (day, month, year, hour, minute, AM/PM),
    ...              ${datetime}: YYYY-MM-DD HH:MM
    [Arguments]  ${id}  ${datetime}
    ${day}  ${month}  ${year}  ${hour}  ${minute}  ${ampm}=  Datetime widget values  ${datetime}
    Input text  css=#${id}-day  ${day}
    Select from list by value  css=#${id}-month  ${month}
    Input text  css=#${id}-year  ${year}
    Input text  css=#${id}-hour  ${hour}
    Input text  css=#${id}-min  ${minute}
    Select from list by value  css=#${id}-ampm  ${ampm}

The datetime input contains
    [Arguments]  ${id}  ${datetime}
    ${day}  ${month}  ${year}  ${hour}  ${minute}  ${ampm}=  Datetime widget values  ${datetime}
    Textfield value should be  css=#${id}-day  ${day}
    List selection should be  css=#${id}-month  ${month}
    Textfield value should be  css=#${id}-year  ${year}
    Textfield value should be  css=#${id}-hour  ${hour}
    Textfield value should be  css=#${id}-min  ${minute}
    List selection should be  css=#${id}-ampm  ${ampm}

Datetime widget values
    [Documentation]  day, month, year, hour (12h), minute, AM/PM of ${datetime}: YYYY-MM-DD HH:MM
    [Arguments]  ${datetime}
    ${values}=  Evaluate  (lambda d: (str(d.day), str(d.month), str(d.year), d.strftime('%I'), d.strftime('%M'), d.strftime('%p')))(datetime.datetime.strptime('${datetime}', '%Y-%m-%d %H:%M'))
    ...  modules=datetime
    [Return]  ${values}
