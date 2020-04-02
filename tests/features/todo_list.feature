Feature: To-do List
    As a user,
    I want to see my to-do items,
    So I know what things I need to do.

    Scenario: Existing items are listed
        Given there are existing items
        When I am on the index page
        Then I can see a list of items
