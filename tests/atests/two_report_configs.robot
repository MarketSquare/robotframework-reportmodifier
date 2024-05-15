*** Comments ***
# ruff: noqa: 0203

*** Test Cases ***
Two Report Configurations
    [Tags]    report:additional    report:basic_config
    Log Info   1st message
    Main Module
    Main Module Checks
    Submodule

*** Keywords ***
Main Module
    Log Info    Called Main Module
    Log Another Info    Second info main module

Main Module Checks
    Log Info    Checks configured in main module were done.

Submodule
    Log Info    Called Sub Module
    Log Another Info    Second info submodule

Log Info
    [Arguments]    ${msg}
    Log    Current message: ${msg}

Log Another Info
    [Arguments]    ${msg}
    Log    Another message: ${msg}
