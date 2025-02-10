*** Settings ***
Library    SeleniumLibrary
Library    ../libraries/AIUtility.py    WITH NAME    Utility
Resource   ../resources/xpath.robot

*** Variables ***
${URL}            https://practice.expandtesting.com/register
${BROWSER}        Chrome
${VALID_USERNAME}     my_test_user
${VALID_PASSWORD}     securepassword123

*** Test Cases ***

Successful Registration
    Open Browser    ${URL}    ${BROWSER}    options=add_argument("--ignore-certificate-errors")
    Maximize Browser Window
    ${username_xpath}=    Utility.Generate Xpath        Username field
    ${password_xpath}=    Utility.Generate Xpath        Password field
    Input Text    xpath=${username_xpath}    ${VALID_USERNAME}
    Input Text    xpath=${password_xpath}    ${VALID_PASSWORD}
    Click Button    Register
    Close Browser


#Registration With Missing Username
#    [Documentation]  Verify error message when Username is left blank
#    Open Browser    ${URL}    ${BROWSER}
#    Input Text    xpath=${password_xpath}    ${VALID_PASSWORD}
#    Input Text    xpath=${confirm_xpath}     ${VALID_PASSWORD}
#    Click Element     xpath=${register_xpath}
#    Wait Until Page Contains    All fields are required.
#    Close Browser
#
#Registration With Missing Password
#    [Documentation]  Verify error message when Password is missing
#    Open Browser    ${URL}    ${BROWSER}
#    Input Text    xpath=${username_xpath}    ${VALID_USERNAME}
#    Input Text    xpath=${confirm_xpath}     dummy_value
#    Click Element     xpath=${register_xpath}
#    Wait Until Page Contains    All fields are required.
#    Close Browser
#
#Registration With Non-Matching Passwords
#    [Documentation]  Verify error message for mismatched passwords
#    Open Browser    ${URL}    ${BROWSER}
#    Input Text    xpath=${username_xpath}    ${VALID_USERNAME}
#    Input Text    xpath=${password_xpath}    ${VALID_PASSWORD}
#    Input Text    xpath=${confirm_xpath}     wrongpassword123
#    Click Element     xpath=${register_xpath}
#    Wait Until Page Contains    Passwords do not match.
#    Close Browser
#
#*** Keywords ***
#Generate And Store XPath
#    [Arguments]    ${element_description}    ${identifier}
#    ${xpath}=    Utility.generate_xpath('${element_description}')
#    Utility.store_xpath('${identifier}', '${xpath}')
#    RETURN    ${xpath}
#
