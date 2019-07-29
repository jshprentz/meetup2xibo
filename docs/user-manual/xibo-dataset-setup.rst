===================
Xibo Events Dataset
===================

Xibo stores event data in a dataset.
Meetup2Xibo manages five data value columns in that dataset.
Xibo administrators may add additional formula columns to aid filtering,
sorting and formating data for layouts.

The steps below describe how to setup the dataset in Xibo.
:doc:`xibo-quick-start` provides an alternative method using an imported
dataset structure.

.. _`create-an-events-dataset`:

Create an Events Dataset
------------------------

Meetup2xibo saves, updates, and deletes event data stored in a Xibo dataset.
Click the :guilabel:`Add DataSet` button above the datasets list, as shown in
:numref:`Figure %s <add-dataset>`.

.. figure:: /images/screenshots/add-dataset.png
   :alt: Screenshot showing Xibo's datasets list
   :name: add-dataset
   :align: center

   Click :guilabel:`Datasets` (1) in the Xibo CMS menu to display the datasets
   list.
   Click the :guilabel:`Add Dataset` button (2) to open the :guilabel:`Add
   Dataset` dialog box.

Enter the new dataset's name, description, and code, as shown in
:numref:`Figure %s <add-dataset-dialog>`.
Choose any meaningful dataset name.
The description is optional, but helpful.
Choose any meaningful single-word code to identify the dataset for Xibo API
clients.
The meetup2xibo configuration must contain this code as described in
:ref:`xibo-dataset-config`.


.. figure:: /images/screenshots/add-dataset-dialog.png
   :alt: Screenshot showing the Xibo Add Dataset dialog box
   :name: add-dataset-dialog
   :align: center

   Type the dataset name (1), description (2), and code (3).
   Click :guilabel:`Save` (4) to add the new dataset.

.. _`dataset_columns`:

Dataset Columns
---------------

Meetup2xibo expects the dataset to contain five string value columns.
:numref:`Table %s <event-dataset-columns>` shows the column headings used at Nova
Labs.
Xibo administrators may choose any column headings and order.

.. tabularcolumns:: |L|L|C|C|

.. _event-dataset-columns:

.. table:: Events Dataset Value Columns
   :align: center

   +----------------+---------------------+---------------+
   |                |                     | Recommended   |
   |                |                     +--------+------+
   | Heading        | Example Value       | Filter | Sort |
   +================+=====================+========+======+
   | Name           | 3D Printing 101     | ✔      |      |
   +----------------+---------------------+--------+------+
   | Location       | Conference Room 3   | ✔      |      |
   +----------------+---------------------+--------+------+
   | Meetup ID      | fkcslpyzhbrb        | ✔      |      |
   +----------------+---------------------+--------+------+
   | ISO Start Time | 2019-05-13 18:00:00 |        | ✔    |
   +----------------+---------------------+--------+------+
   | ISO End Time   | 2019-05-13 19:30:00 |        |      |
   +----------------+---------------------+--------+------+

Xibo automatically adds one column to new datasets.
Select :guilabel:`Edit` from the events dataset's popup menu, as shown in
:numref:`Figure %s <edit-column>`.

.. figure:: /images/screenshots/edit-column.png
   :alt: Screenshot showing the events dataset column list with the popup menu
      open
   :name: edit-column
   :align: center

   In the Xibo-supplied first row, click the down arrow (1) to open the
   popup menu.
   Select :guilabel:`Edit` (2) from the menu to open the :guilabel:`Edit
   Column` dialog box.
   Click :guilabel:`Add Column` (3) to add each additional dataset column.

Correct the column heading, as shown in
:numref:`Figure %s <edit-column-dialog>`.
All value columns have the *String* data type and the *Value* column type.
The list content should be left blank.
The default column order will suffice.

Xibo administrators may choose which columns to filter and sort.
Filtering searches for events containing desired values.
For example, a Xibo administrator can filter events to show only those with a
name containing "Electronics 101."
Sorting changes the order of events listed when viewing data.
For example, a Xibo administrator can sort events by starting time.
Nova Labs filters and sorts the columns shown in
:numref:`Table %s <event-dataset-columns>`.

.. figure:: /images/screenshots/edit-column-dialog.png
   :alt: Screenshot showing the Edit Column dialog box.
   :name: edit-column-dialog
   :align: center

   Edit the heading (1) to "Name" or the heading chosen for the first column.
   Optionally check the boxes for :guilabel:`Filter?` (2) and/or
   :guilabel:`Sort?` (3).
   Click the :guilabel:`Save` button (4) to save the changes.

Click :guilabel:`Add Column` (:numref:`Figure %s <edit-column>`) to add
each of the remaining columns to the dataset.
The :guilabel:`Add Column` form is similar to the :guilabel:`Edit Column` form
shown in :numref:`Figure %s <edit-column-dialog>`.
When complete, the events dataset columns should appear in a list similar to 
:numref:`Figure %s <value-columns>`.

.. figure:: /images/screenshots/value-columns.png
   :alt: Screenshot showing the list of value columns for the events dataset
   :name: value-columns
   :align: center

   The events dataset columns after the five value columns have been created.

Formula Columns
---------------

Xibo administrators may add formula columns for filtering, data formatting, or
CSS styling.
:numref:`Table %s <event-dataset-formulas>` shows examples of formula columns
used at Nova Labs.
The example values were calculated at 6:06 PM for the example event in 
:numref:`Table %s <event-dataset-columns>`.

.. _event-dataset-formulas:

.. table:: Events Dataset Formulas
   :widths: auto
   :align: center

   +--------------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Heading            | Example Value | Purpose    | Formula                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
   +====================+===============+============+===============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================+
   | Cancelled          |               | CSS class  | ``IF(`Location` = 'Cancelled', 'cancelled', '')``                                                                                                                                                                                                                                                                                                                                                                                                                                             |
   +--------------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Compact End Time   | 7:30 PM       | Formatting | ``IF(TIME(`ISO End Time`) = '12:00:00.000000', 'Noon', IF(TIME(`ISO End Time`) = '00:00:00.000000', 'Midnight', IF(MINUTE(`ISO Start Time`) = 0 AND MINUTE(`ISO End Time`) = 0, DATE_FORMAT(`ISO End Time`, '%l %p'), DATE_FORMAT(`ISO End Time`, '%l:%i %p'))))``                                                                                                                                                                                                                            |
   +--------------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Compact Start Time | 6:00          | Formatting | ``IF(TIME(`ISO Start Time`) = '12:00:00.000000', 'Noon', IF(TIME(`ISO Start Time`) = '00:00:00.000000', 'Midnight', IF(MINUTE(`ISO Start Time`) = 0 AND MINUTE(`ISO End Time`) = 0, IF((HOUR(`ISO Start Time`) < 12) XOR (HOUR(`ISO End Time`) < 12), DATE_FORMAT(`ISO Start Time`, '%l %p'), DATE_FORMAT(`ISO Start Time`, '%l')), IF((HOUR(`ISO Start Time`) < 12) XOR (HOUR(`ISO End Time`) < 12), DATE_FORMAT(`ISO Start Time`, '%l:%i %p'), DATE_FORMAT(`ISO Start Time`, '%l:%i')))))`` |
   +--------------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Day Name or Date   | Today         | Formatting | ``IF(DATEDIFF(`ISO Start Time`, NOW()) = 0, 'Today', IF(DATEDIFF(`ISO Start Time`, NOW()) BETWEEN 1 AND 5, DATE_FORMAT(`ISO Start Time`, '%W'), DATE_FORMAT(`ISO Start Time`, '%M %e')))``                                                                                                                                                                                                                                                                                                    |
   +--------------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Days Till Start    | 0             | Filtering  | ``DATEDIFF(`ISO Start Time`, NOW())``                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
   +--------------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Minutes Past End   | -84           | Filtering  | ``TIMESTAMPDIFF(MINUTE, `ISO End Time`, NOW())``                                                                                                                                                                                                                                                                                                                                                                                                                                              |
   +--------------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Month and Day      | May 13        | Formatting | ``DATE_FORMAT(`ISO Start Time`, '%M %e')``                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
   +--------------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Past Day           |               | CSS class  | ``IF(DATEDIFF(`ISO Start Time`, NOW()) < 0, 'pastday', '')``                                                                                                                                                                                                                                                                                                                                                                                                                                  |
   +--------------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Start Time         | 6:00 PM       | Formatting | ``DATE_FORMAT(`ISO Start Time`, "%l:%i %p")``                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
   +--------------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

All columns have the *String* data type and the *Formula* column type.
The List Content should be left blank.
Xibo administrators may choose any column headings and order.

Click :guilabel:`Add Column` (:numref:`Figure %s <edit-column>`) to add
each of the formula columns to the dataset.
The :guilabel:`Add Column` form is shown in
:numref:`Figure %s <add-formula-column-dialog>`.

.. figure:: /images/screenshots/add-formula-column-dialog.png
   :alt: Screenshot showing the Add Column dialog box.
   :name: add-formula-column-dialog
   :align: center

   Edit the heading (1) to formula column heading.
   Select :guilabel:`Formula` (2) from the :guilabel:`Column Type` menu.
   Enter the formula into the :guilabel:`Formula` text field (3).
   Click the :guilabel:`Save` button (4) to save the changes.


CSS Class Formulas
^^^^^^^^^^^^^^^^^^

The CSS class formulas check a condition and compute either a blank value or a
CSS class name.
Use these formulas in the source view of a Xibo layout ticker widget appearance
tab.

Cancelled
   The CSS class name *cancelled* when an event is cancelled; blank otherwise.
   For example, the Agenda layout (:numref:`Figure %s <xibo_agenda_screenshot>`)
   uses the *cancelled* CSS class to strike through cancelled events names.

   .. code-block:: html

      <div class="event-name [Cancelled|65]">[Name|1]</div>  

   The widget's optional stylesheet contains the CSS class definition.

   .. code-block:: css

      .cancelled {
          text-decoration: line-through;
	  }

Past Day
   The CSS class name *pastday* when an event occured before today; blank
   otherwise.
   For example, the Nova Labs weekly calendar grid layout uses the *pastday*
   CSS class to dim events on days before today.

   .. code-block:: html

      <p class="[Past Day|64] [Cancelled|65]"><span class="time">[Start Time|6]</span> [Name|1]</p>

   The widget's optional stylesheet contains the CSS class definition.

   .. code-block:: css

      .pastday {
          color: #B1B0B5;
	  }

Date and Time Formatting Formulas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The date and time formatting formulas render start and end dates and times in
formats appropriate for various layouts.
Use these formulas in a Xibo layout ticker widget appearance tab.

Month and Day
   The spelled out month and start date of an event.

Day Name or Date
   The word "Today" for today's events.
   The spelled out day name for events one to five days ahead.
   The month and day of other events.

Start Time
   The start time in 12-hour AM/PM format.

Compact Start Time and Compact End Time
   Used together to render event time ranges such as 2--4 PM.

   Shows minutes when either the start or end time do not occur on the hour,
   such as 1:30--4:00 PM.

   Shows the start time AM/PM indicator when the start and end AM/PM time
   values differ, such as 10 AM--4 PM.

   Shows the words "midnight" and "noon" as needed, such as Noon--4 PM.

Filtering Formulas
^^^^^^^^^^^^^^^^^^

The filtering formulas compute date and time differences useful for selecting
events.
Use these formulas in a Xibo layout ticker widget filter tab.

For example, the Agenda layout (:numref:`Figure %s <xibo_agenda_screenshot>`)
displays today's events until 30 minutes after their end time.
The layout's "Use advanced filter clause?" checkbox is checked and this filter
clause selects the desired events:

.. code-block:: mysql

   `Days Till Start` = 0 AND `Minutes Past End` < 30

Days Till Start
   The number of days until the event starts.
   This value is 0 for today's events, 1 for tomorrow's events, and so on.
   Past events have negative values.

Minutes Past End
   The number of minutes since the event ended.

