# USER MANUAL – HOW TO USE PSEUDONIMIZATION TOOL

This manual explains how to make new Geneticlines participation numbers based on UMCG number. For geneticlines a "pseudonym app" was developed to generate pseudonyms, all versions can be found in [Nexus repository](https://registry.molgenis.org/#browse/browse:appstore:molgenis-app-pseudonym-registration), latest version should be used on [Geneticlines website](https://geneticlines.molgeniscloud.org).

# 1. How to use Pseudonimization tool
At first, users need to have permission to create new geneticlines participation numbers (identifiers). If the app is not opening, contact geneticlines administration to add you to the list of users that need permissions for Pseudonimization tool.

1. In menubar on top left "Add new GENnumber " button is shown, press menu-item to go to the pseudonimization tool.![menubar](/Geneticlines/images/menubar.png)
2. Pseudonym app opens.
3. Copy UMCG from EPIC or somewhere else, paste it in the textfield.
4. Press the "Generate" button.![pseudo_app](/Geneticlines/images/pseudo_app.png)
5. A new identifiers is made, shown in the same textbox. Format of identifiers are "GEN-" and 7 numbers.![GENnumber](/Geneticlines/images/newID.png)
6. Copy new identifier(GENnumber) to EPIC or somewhere else, use the "Copy to clipboard" button. When you copied, button change color to green.![greenButton](/Geneticlines/images/copied_button.png)
7. Use "Back" button to generate new Geneticlines participation numbers.

# 2. Notifications
- When using the same UMCG number twice you get a notification; "This pseudonym already existed in the database, you might want to check if patient's data was already entered". You can copy Geneticlines number using "Copy to clipboard" button. Use "Back" button to go back and enter new UMCG number.![doubleUMCG](/Geneticlines/images/sameUMCG.png)
- When entering invalid UMCG number you get error message; "Error:(statuscode:400). If you think this is a big,please inform us at:https://github.com/molgenis/molgenis-app-pseudonym-registration/issues". A valid UMCG number consists of 7 digits.![error](/Geneticlines/images/error.png)
