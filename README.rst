Vacant to Vibrant
=================

A vacant lot viewer and organizing platform for Philadelphia, roughly based on
`596 Acres <http://596acres.org/>`_.


Installation
------------

Vacant to Vibrant uses `Django <http://djangoproject.org/>`_ and 
`GeoDjango <http://geodjango.org/>`_. The rest of the requirements are in 
`requirements.txt`.

Once the requirements are installed, create a PostGIS database as described in 
`settings/base.py`.


Organization
------------

Apps specific to Philadelphia's data are grouped in the package `phillydata`.

Apps that deal with generic "places" are grouped in the package `places`.


License
-------

Vacant to Vibrant is released under the GNU `Affero General Public License,
version 3 <http://www.gnu.org/licenses/agpl.html>`_.
