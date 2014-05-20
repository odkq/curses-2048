===============================
curses-2048
===============================

        
.. image:: http://i.imgur.com/ASZCWBQ.png


A terminal/ncurses/python version of the original game at http://gabrielecirulli.github.io/2048

* Free software: GPL license

Install
--------

Open your terminal and type:


.. code:: bash

 $ pip install curses-2048

or 

.. code:: bash  
    
 $ easy_install curses-2048


Usage
------

.. code:: bash  
    
 $ 2048

256 colors
----------
If your terminal has support for 256 colors you will see colors mimicking the
original game, something like the screenshot above. If your terminal only
supports 16 colors, you will se something like this:

.. image:: http://i.imgur.com/S4F4wgW.png

Recent versions of xterm and gnome terminal are known to support 256 colors,
if you do not see them, probably your environment variable TERM is not set
accordingly. Do

.. code:: bash
 
 $ export TERM=xterm-256color

or, if you are using screen or tmux

.. code:: bash

 $ export TERM=screen-256color

to enjoy curses-2048 in full 256 colors glory.

Use the cursor keys to move and join tiles. Get to the 2048 tile!
