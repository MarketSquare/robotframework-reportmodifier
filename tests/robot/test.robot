*** Settings ***

*** Test Cases ***
My First Test Case
    [Tags]    report:custom
    First Level Keyword

*** Keywords ***
First Level Keyword
    Second Level Keyword

Second Level Keyword
    Third Level Keyword

Third Level Keyword
    Log    I'm the 3rd level keyword.