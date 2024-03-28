*** Comments ***
# ruff: noqa: 0203


*** Test Cases ***
Failed Test
    [Tags]    report:message_by_status
    Log    This is the first keyword call.
    Raise Exception

Skipped Test
    [Tags]    report:message_by_status
    Log    This is the first keyword call.
    Skip    msg="Testfall soll geskippt werden."


*** Keywords ***
Raise Exception
    TRY
        Should Be Equal    first=1    second=2    msg=Keyword soll fehlschlagen.
    EXCEPT
        Log    Is not equal.
    END
