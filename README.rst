Installation
------------
Windows
~~~~~~~
- Perl_ (for Windows): 
- `Python Imaging Library`_ (PIL)

Mac
~~~
- easy_install pip
- brew install libjpeg
- pip install Pillow

Useful Commands
---------------
- rsync -crhvtP --perms --stats --delete --exclude='\*.cache' --exclude='Thumbs.db' <user>@<server>:<source_directory> <destination_dir>
- icacls * /reset /T
  
  * To be run from the /photos directory after rsync. Removes all deny permissions


FAQ
----
- Where does the name 'light bucket' come from?
  
  - It's another term for a fast lens. Light bucket is also used to describe a photosite on a digital camera sensor (the element that ‘captures’ the light to make an exposure).


Authors
~~~~~~~

* `Rachel Nienaber`_
* `Richard Nienaber`_

.. _Perl: http://www.activestate.com/activeperl/downloads
.. _Python Imaging Library: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil

.. _`Rachel Nienaber`: https://github.com/rnienaber
.. _`Richard Nienaber`: https://github.com/rjnienaber