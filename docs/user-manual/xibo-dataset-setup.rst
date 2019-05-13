===================
Xibo Events Dataset
===================

Xibo stores event data in a dataset.
Meetup2Xibo manages five data value columns in that dataset.
Xibo administrators may add additional formula columns to aid filtering,
sorting and formating data for layouts.
Step-by-step instructions below demonstrate how to setup the event dataset.

Dataset Columns
---------------

Meetup2xibo expects the dataset to contain five string value columns.
:numref:`Table %s <event-table-columns>` shows the recommended column headings.

.. _event-table-columns:

.. table:: Event Table Value Columns
   :widths: auto
   :align: center

   +----------------+---------------------+
   | Heading        | Example Value       |
   +================+=====================+
   | Name           | 3D Printing 101     |
   +----------------+---------------------+
   | Location       | Conference Room 3   |
   +----------------+---------------------+
   | Meetup ID      | fkcslpyzhbrb        |
   +----------------+---------------------+
   | ISO Start Time | 2019-05-13 18:00:00 |
   +----------------+---------------------+
   | ISO End Time   | 2019-05-13 19:30:00 |
   +----------------+---------------------+

All columns have the *String* data type and the *Value* column type.
The List Content should be left blank.
Xibo administrators may choose any column headings and order.

Formula Columns
---------------

Xibo administrators may add formula columns for filtering, data formatting, or
CSS styling.
:numref:`Table %s <event-table-formulas>` shows examples of formula columns
used at Nova Labs.
The example values were calculated at 6:06 PM for the example event in 
:numref:`Table %s <event-table-columns>`.

.. _event-table-formulas:

.. table:: Event Table Formulas
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

