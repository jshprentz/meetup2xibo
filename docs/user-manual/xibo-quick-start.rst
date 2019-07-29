================
Xibo Quick Start
================

Meetup2xibo stores event data in a Xibo dataset.
The steps below describe a quick alternative to manually creating the dataset
as described in :doc:`xibo-dataset-setup`.

Download Agenda Layout and Dataset Structure
--------------------------------------------

Xibo can import or export dataset structures only when associated with a
layout.
Download the agenda layout and event dataset structure, which was exported from
Xibo as a zip file: :github-raw:`/data/export_quick-start-agenda-for-xibo-1-8.zip`.

Import Agenda Layout
--------------------

Import the downloaded agenda layout and associated event dataset structure.
Click the :guilabel:`Import` button above the layouts list, as shown in
:numref:`Figure %s <import-layout>`.

.. figure:: /images/screenshots/import-layout.png
   :alt: Screenshot showing Xibo's layouts list
   :name: import-layout
   :align: center

   Import layout.
   Click :guilabel:`Layouts` (1) in the Xibo CMS menu to display the layouts
   list.
   Click the :guilabel:`Import` button (2) to open the :guilabel:`Upload
   Layout` dialog box.

Select and upload the agenda layout zip file as shown in
:numref:`Figure %s <upload-layout-dialog>`.

.. figure:: /images/screenshots/upload-layout-dialog.png
   :alt: Screenshot showing Xibo's Upload Layout dialog box
   :name: upload-layout-dialog
   :align: center

   Upload layout.
   Click the :guilabel:`Add ZIP Files` button (1) to open the 
   :guilabel:`File Upload` dialog box.
   Navigate to folder containing the downloaded zip file.
   Select the zip file (2).
   Click the :guilabel:`Open` button (3) to add the zip file to the
   :guilabel:`File Upload` dialog box's list of files.
   Click the :guilabel:`Start upload` button (4) to upload the zip file.
   When the upload completes, click the :guilabel:`Done` button (5) to close
   the dialog box.

Observe that the layout list contains the imported layout as shown in
:numref:`Figure %s <layout-listing-with-quick-start-agenda>`.

.. figure:: /images/screenshots/layout-listing-with-quick-start-agenda.png
   :alt: Screenshot showing Xibo's layouts list containing the imported layout
   :name: layout-listing-with-quick-start-agenda
   :align: center

   Xibo's layout list includes the imported layout (1).

Review and Rename Imported Dataset
----------------------------------

Observe that the dataset list contains the imported dataset as shown in
:numref:`Figure %s <review-imported-dataset>`.

.. figure:: /images/screenshots/review-imported-dataset.png
   :alt: Screenshot showing Xibo's datasets list containing the imported dataset
   :name: review-imported-dataset
   :align: center

   Review dataset.
   Click :guilabel:`Datasets` (1) in the Xibo CMS menu to display the datasets
   list.
   Observe that the list includes the imported dataset (2).
   In the imported dataset's row, click the down arrow (3) to open the popup
   menu.
   Select :guilabel:`Edit` (4) from the menu to open the :guilabel:`Edit
   Dataset` dialog box.

Edit the dataset's name, description, and code, as shown in
:numref:`Figure %s <edit-dataset-dialog>`.
Choose any meaningful dataset name.
The description is optional, but helpful.
Choose any meaningful single-word code to identify the dataset for Xibo API
clients.
The meetup2xibo configuration must contain this code as described in
:ref:`xibo-dataset-config`.

.. figure:: /images/screenshots/edit-dataset-dialog.png
   :alt: Screenshot showing the Xibo Edit Dataset dialog box
   :name: edit-dataset-dialog
   :align: center

   Edit dataset.
   Edit the dataset name (1), description (2), and code (3).
   Click :guilabel:`Save` (4) to save the changes.

The Agenda Layout
-----------------

:numref:`Figure %s <quick_start_agenda_screenshot>` shows the imported quick
start agenda layout.
Xibo administrators may customize the layout with Xibo's layout design tools.

.. figure:: /images/screenshots/quick-start-agenda.png
   :alt: Screenshot of a Xibo displayed daily agenda, which lists event titles,
         locations, and start times
   :name: quick_start_agenda_screenshot
   :align: center

   The quick start agenda displays a schedule of today's events.
