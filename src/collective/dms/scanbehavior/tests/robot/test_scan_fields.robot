*** Settings ***
Documentation  Scan fields of the "Scan metadata" behavior, on the ScannedDocument test type
...            (profiles/testing). Version-independent: Plone selectors are in ui_plone*.robot.
Resource  scanbehavior.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Test Cases ***
Scan fields are saved, displayed and kept in the edit form
    Add a scanned document  Scanned mail
    Fill the scan fields  IMIO-123  2  5  2024-03-15 10:30  John Doe  Canon DR-C225
    Save the form
    The status message contains  Item created
    The scan fields are displayed  IMIO-123  2  5  2024-03-15 10:30  John Doe  Canon DR-C225
    Open the edit form
    The scan fields are in the edit form  IMIO-123  2  5  2024-03-15 10:30  John Doe  Canon DR-C225

A scan date before 1990 is rejected
    Add a scanned document  Old mail
    Open the form tab  Scan
    Input the datetime  ${SCAN_DATE_ID}  1989-12-31 10:00
    Save the form
    The status message contains  There were some errors
    Open the form tab  Scan
    The field error contains  ${SCAN_DATE_ID}  Value is too small
