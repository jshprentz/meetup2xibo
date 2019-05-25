================
Xibo Client User
================

Setup a separate Xibo user for the client application meetup2xibo.
That user will have authorization only to update data in the event dataset.
Experienced Xibo administrators can follow this outline:

1. Add a user to Xibo.
2. Authorize that user to access the dataset API.
3. Grant the new user the view and edit permissions for the event dataset.
4. Add a new application to Xibo, noting the application credentials.
5. Set the application owner to the new user.

The step-by-step instructions below demonstrate how to setup the client user,
dataset permissions, and event editor application.

Add a User for Meetup2xibo
--------------------------

A distinct meetup2xibo client user will provide secure, limited access to the
Xibo API.
Click the :guilabel:`Add User` button above the users list, as shown in 
:numref:`Figure %s <add-user>`.

.. figure:: /images/screenshots/add-user.png
   :alt: Screenshot showing Xibo's user list
   :name: add-user
   :align: center

   Click :guilabel:`Users` (1) in the Xibo CMS menu to display the users list.
   Click the :guilabel:`Add User` button (2) to open the :guilabel:`Add User`
   dialog box.

Enter the new user's user name and password, as shown in
:numref:`Figure %s <add-user-dialog>`.
Choose any meaningful user name.
The password will never be used, so choose a long, random sequence of
characters.

.. figure:: /images/screenshots/add-user-dialog.png
   :alt: Screenshot showing the Xibo Add User dialog box
   :name: add-user-dialog
   :align: center

   Type the username (1) and password (2).
   Click :guilabel:`Save` (3) to add the new user.

Authorize the User to Access Event Data
---------------------------------------

The meetup2xibo user requires access to the datasets API, but should be blocked
from other API components.
Select :guilabel:`Page Security` from the meetup2xibo user's popup menu as
shown in :numref:`Figure %s <user-page-security>`.

.. figure:: /images/screenshots/user-page-security.png
   :alt: Screenshot Xibo's user list with a popup menu open
   :name: user-page-security
   :align: center

   In the meetup2xibo user's row, click the down arrow (1) to open the popup
   menu.
   Select :guilabel:`Page Security` (2) from the menu to open the access
   control list dialog box.

Update the :abbr:`ACL (Access Control List)` for the meetup2xibo user, as shown
in :numref:`Figure %s <acl-for-event-editor-client>`

.. figure:: /images/screenshots/acl-for-event-editor-client.png
   :alt: Screenshot showing the access control list for the meetup2xibo user
   :name: acl-for-event-editor-client
   :align: center

   Click the :guilabel:`DataSets` checkbox (1) to authorize use of the datasets
   API.
   Scroll down and click :guilabel:`Save` (2) to save the changes.

Grant Dataset Permissions
-------------------------

The meetup2xibo user requires permission to view and edit event data.
Select :guilabel:`Permissions` from the event dataset's popup menu, as shown in
:numref:`Figure %s <dataset-permissions>`.

.. figure:: /images/screenshots/dataset-permissions.png
   :alt: Screenshot showing Xibo datasets with the popup menu open
   :name: dataset-permissions
   :align: center

   Click :guilabel:`DataSets` (1) in the Xibo CMS menu to display the datasets
   list.
   In the event dataset's row, click the down arrow (2) to open the popup
   menu.
   Select :guilabel:`Permissions` (3) from the menu to open the permissions
   dialog box.

Authorize the meetup2xibo user to view and edit the dataset, as shown in
:numref:`Figure %s <dataset-permissions-dialog>`.

.. figure:: /images/screenshots/dataset-permissions-dialog.png
   :alt: Screenshot showing the dataset permissions dialog box
   :name: dataset-permissions-dialog
   :align: center

   In the row for the meetup2xibo user, click the :guilabel:`View` (1) and
   :guilabel:`Edit` (2) checkboxes.
   Click :guilabel:`Save` (3) to save the changes.

Add an Application for Meetup2xibo
----------------------------------

Xibo limits API access to a limited list of client applications.
Click the :guilabel:`Add Application` button above the applications list as
shown in :numref:`Figure %s <add-application>`.

.. figure:: /images/screenshots/add-application.png
   :alt: Screenshot showing the Xibo applications list
   :name: add-application
   :align: center

   Click :guilabel:`Applications` (1) in the Xibo CMS menu to display the
   applications list.
   Click the :guilabel:`Add Application` button (2) to open the :guilabel:`Add
   User` dialog box.

Enter the new application's name, as shown in
:numref:`Figure %s <add-application-dialog>`.
Choose any meaningful application name.

.. figure:: /images/screenshots/add-application-dialog.png
   :alt: Screenshot showing the Add Application dialog box
   :name: add-application-dialog
   :align: center

   Enter the application name (1).
   Click :guilabel:`Save` (2) to add the new application.

.. _`authorize-the-application`:

Authorize the Application
-------------------------

The new application must allow API access from the unattended application
meetup2xibo.
Select :guilabel:`Edit` from the meetup2xibo application's popup menu as
shown in :numref:`Figure %s <edit-application>`.

.. figure:: /images/screenshots/edit-application.png
   :alt: Screenshot showing the application list with the popup menu open
   :name: edit-application
   :align: center

   In the meetup2xibo application's row, click the down arrow (1) to open the
   popup menu.
   Select :guilabel:`Edit` (2) from the menu to open the :guilabel:`Edit
   Application` dialog box.

The :ref:`Xibo CMS API credentials configuration <xibo-cms-api-credentials>`
requires the client ID and secret shown in the :guilabel:`Edit Application`
dialog box.
Authorize the client credentials, as shown in
:numref:`Figure %s <edit-application-general>`.

.. figure:: /images/screenshots/edit-application-general.png
   :alt: Screenshot showing the Edit Application dialog box.
   :name: edit-application-general
   :align: center

   Note the client ID (1) and client secret (2) for the meetup2xibo
   configuration.
   Click the :guilabel:`Client Credentials?` checkbox (3) to authorize OAuth2
   client credentials.
   Do not save yet.

The meetup2xibo application require access to the entire Xibo scope.
Grant access and associate the application with the meetup2xibo user, as shown
in :numref:`Figure %s <edit-application-permissions>`.

.. figure:: /images/screenshots/edit-application-permissions.png
   :alt: Screenshot showing the permissions tab of the Edit Application dialog box.
   :name: edit-application-permissions
   :align: center

   Click the :guilabel:`Permissions` tab (1) to display the application
   permissions.
   Click the :guilabel:`All access` checkbox (2) to grant the application
   access to the entire scope.
   Select the meetup2xibo user from the pulldown menu (3) to assign an
   application owner.
   Click :guilabel:`Save` (4) to save the changes.


