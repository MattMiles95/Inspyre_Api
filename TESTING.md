# Testing

This is the TESTING file for the backend DRF API for [Inspyre](https://inspyre-53afb73e4a64.herokuapp.com/), a full stack application focused on content creation and sharing.

Return to the [README](./README.md).

View the TESTING file for the frontend React app [here](#https://github.com/MattMiles95/PP5_Inspyre_Frontend/blob/main/TESTING.md).

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

| **Feature**            | **Expected Outcome**                                                                                                                             | **Result** |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| Create Account         | Given a user creates an account, a Profile is automatically created and assigned to that account.                                                | Pass       |
| Delete Account         | Given an account is deleted, the child data of that account is also deleted.                                                                     | Pass       |
| Post                   | Given a user creates a post, that post is created in the expected location within the database.                                                  | Pass       |
| Post Edit              | Given a user edits a post, the details of that post stored in the database are updated accordingly.                                              | Pass       |
| Post Delete            | Given a user deletes a post, the post and its associated comments and likes are removed from the database.                                       | Pass       |
| Follow                 | Given a user follows another user, a new Follower instance is created and associated with both the follower and the followed user.               | Pass       |
| Unfollow               | Given a user unfollows another user, the Follower instance is deleted from the database.                                                         | Pass       |
| Like                   | Given a user likes a post, a new Like instance is created and associated with both the user and the post.                                        | Pass       |
| Unlike                 | Given a user unlikes a post, the associated Like instance is deleted from the database.                                                          | Pass       |
| Create Comment         | Given a user creates a comment on a post, a new Comment instance is created and associated with both the user and the post.                      | Pass       |
| Edit Comment           | Given a user edits their comment, the content of the Comment instance is updated in the database.                                                | Pass       |
| Delete Comment         | Given a user deletes their comment, the Comment instance and its replies are removed from the database.                                          | Pass       |
| Create Comment Thread  | Given a user replies to a comment, the reply is associated with the parent comment, forming a comment thread.                                    | Pass       |
| Create Conversation    | Given a user sends a direct message to another user, a new Conversation instance is created if one does not already exist.                       | Pass       |
| Delete Conversation    | Given a user deletes a conversation, the Conversation instance and all associated messages are removed from the database.                        | Pass       |
| Send Message           | Given a user sends a message within a conversation, a new DirectMessage instance is created and associated with the sender and receiver.         | Pass       |
| Unread Message in Chat | When a new message is received, the read field remains False, and the `has_unread_messages` field identifies conversations with unread messages. | Pass       |
| Auto-Read Messages     | When a conversation is opened, unread messages for the user are marked as read and the `has_unread_messages` field is updated.                   | Pass       |

<br>

### Cloudinary

| **Feature**           | **Expected Outcome**                                                                                                                                                | **Result** |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| File Upload           | Given a user uploads an image, the file is successfully saved in the specified storage location within Cloudinary and associated with the relevant post or profile. | Pass       |
| Default Profile Image | Given a user creates an account, the default profile image stored within Cloudinary is assigned to their profile until they upload a custom image.                  | Pass       |

<br>

## Bug Fixes

Throughout the development of Inspyre's backend, I carried out the following bug fixes:

| Feature           | Expected Outcome                                                                 | Actual Outcome                                                  | Fix                                                                                             |
| ----------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Heroku Deployment | App successfully deploys to Heroku.                                              | Heroku build failure due to incorrect 'ALLOWED_HOSTS' settings. | Correct syntax for 'ALLOWED_HOSTS'.                                                             |
| Profile Tags      | Users can select pre-determined profile tags to display on their profile.        | Profile tags displaying as integers.                            | Change profile tags from a pk field to a string field.                                          |
| Direct Messages   | Users can send and receive messages directly between each other.                 | Sent messages not being received.                               | Update get_queryset to filter by the Conversation object rather than conversation_id.           |
| Direct Messages   | Messaging a user where no previous chat exists creates a conversation.           | Conversation not being created.                                 | Remove conversation creation from MessageListAPIView and add to serializers.                    |
| Direct Messages   | Users can preview the most recent message of a chat in their conversations list. | Previews not appearing.                                         | Update get_latest_message to explicitly filter DirectMessage objects by the conversation field. |
