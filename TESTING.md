# Testing

This is the TESTING file for the backend DRF API for [Inspyre](https://inspyre-53afb73e4a64.herokuapp.com/), a full stack application focused on content creation and sharing.

Return to the [README](./README.md)

View the TESTING file for the frontend React app [here](#)

## Table of Contents

### [Validation](#validation)

### [Manual Testing](#manual-testing)

- [Manual Testing](#manual-testing)
- [Browser Compatibility](#browser-compatibility)
- [Device Compatibility](#device-compatibility)

### [Bug Fixes](#bug-fixes)

<br>

## Validation

Tested using the [CI Python Linter](https://pep8ci.herokuapp.com/).

| **Directory**   | **admin** | **apps** | **models** | **permissions** | **serializers** | **settings** | **urls** | **views** |
| --------------- | --------- | -------- | ---------- | --------------- | --------------- | ------------ | -------- | --------- |
| comments        | Pass      | Pass     | Pass       | n/a             | Pass            | n/a          | Pass     | Pass      |
| direct_messages | Pass      | Pass     | Pass       | n/a             | Pass            | n/a          | Pass     | Pass      |
| followers       | Pass      | Pass     | Pass       | n/a             | Pass            | n/a          | Pass     | Pass      |
| inspyre_api     | n/a       | n/a      | n/a        | Pass            | Pass            | Pass         | Pass     | Pass      |
| likes           | Pass      | Pass     | Pass       | n/a             | Pass            | n/a          | Pass     | Pass      |
| posts           | Pass      | Pass     | Pass       | n/a             | Pass            | n/a          | Pass     | Pass      |
| profiles        | Pass      | Pass     | Pass       | n/a             | Pass            | n/a          | Pass     | Pass      |

<br>

## Manual Testing

Extensive manual testing was conducted on the backend logic of this project to ensure all were functioning as expected. The outcome of this testing is recorded in the tables below.

<br>

### Database

| **Feature**           | **Expected Outcome** | **Result** |
| --------------------- | -------------------- | ---------- |
| Create Account        |                      | Pass       |
| Delete Account        |                      | Pass       |
| Post                  |                      | Pass       |
| Post Edit             |                      | Pass       |
| Post Delete           |                      | Pass       |
| Follow                |                      | Pass       |
| Unfollow              |                      | Pass       |
| Like                  |                      | Pass       |
| Unlike                |                      | Pass       |
| Create Comment        |                      | Pass       |
| Edit Comment          |                      | Pass       |
| Delete Comment        |                      | Pass       |
| Create Comment Thread |                      | Pass       |
| Create Conversation   |                      | Pass       |
| Delete Conversation   |                      | Pass       |
| Send Message          |                      | Pass       |

<br>

### Cloudinary

| **Feature**           | **Expected Outcome** | **Result** |
| --------------------- | -------------------- | ---------- |
| File Upload           |                      | Pass       |
| Default Profile Image |                      | Pass       |

<br>

## Bug Fixes

Throughout the development of my project, I carried out the following bug fixes:

| Feature                         | Expected Outcome                                                                | Actual Outcome                                              | Fix                                                                                                                                                                                                     |
| ------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Database                        | Updating models                                                                 | Couldn't reconcile changes made                             | Error caused by deleting previous migration files, ultimately corrupting the database. A new database was created to replace the corrupted database                                                     |
| Cloudinary Security             | Secure responses received from Cloudinary                                       | HTTP responses instead of HTTPS, causing unsecure responses | Updated settings.py to configure secure responses from Cloudinary                                                                                                                                       |
| Comment Report Button           | Reported comment's status changes from 'approved' to 'reported'                 | 500 error                                                   | Bug caused by the initial report button having the same id as the report button in the confirmation modal, causing a JavaScript error. ID changed to differentiate between buttons                      |
| Comment Edit Button             | Clicking 'submit' button submits changes to comment                             | 500 error                                                   | ID 'submitButton' had been changed due to conflicting CSS, which caused a bug with the JavaScript. Html and JS updated with new ID                                                                      |
| Homework Submission Lesson Menu | Lesson dropdown menu only contains lessons associated with the selected subject | Menu empty                                                  | Created Homework Dashboard as a means for the subject to be selected prior to reaching the submission page, allowing for the subject.id to be correctly assigned prior to accessing the submission form |
| Homepage subject buttons        | Clicking a button directs the User to the respective lesson feed                | No response                                                 | href's had been left as '#'s. Updated with correct url links                                                                                                                                            |
