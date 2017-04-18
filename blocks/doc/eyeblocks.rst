ExpEYES-Blocks
==============

``eyeblocks`` is a module to make easier for end users to develop
small apllication with ExpEYES measurement boxes.

Main window
---------------

.. automodule:: eyeBlocks.mainwindow
	:members:

Working space for blocks
------------------------
The blocks, also named components, can be dragged and dropped in
this working space. Dragging blocks from the working space to the list
allows one to erase a block.

Some blocks can be connected to other ones, in order to build
chains to manage signals and display them properly.		   

.. automodule:: eyeBlocks.blockwidget
	:members:

The left-side list for components
---------------------------------
This list can be considered as a store for components. Drag them to
the working area to create them, drag them back to the list to erase
them.   

.. automodule:: eyeBlocks.componentslist
	:members:

Base class for components of blocks
-----------------------------------
This class cannot be used directly, it is an absctract class,
providing features by the means of inheritance.
  
.. automodule:: eyeBlocks.component
	:private-members:
	:members:

Time base of the oscilloscope
-----------------------------
This component permits to specify a time base for the oscilloscope,
one can choose a dealy and a number of samples, hence the duration of
measurements.

.. automodule:: eyeBlocks.timecomponent
	:members:

Editing properties of an Input Block
------------------------------------
Input blocks can be any input of ExpEYES, like A1, A2, and so on.
They can be also a time base, which is a particular case. For voltage
inputs, features like the voltage range may be modified; for the time
base, more parameters can be tuned.

.. automodule:: eyeBlocks.inputdialog
	:members:

A block to modify signals
-------------------------
This block is meant to modify signals by some formula, or
to extract some particular feature of the signal to provide
side-effects, like synchronizing the time base.

.. automodule:: eyeBlocks.modifcomponent
	:members:

Components featuring a channel of the scope
--------------------------------------------
There are several channels for the scope:
* channel 1
* channel 2
* channel 3
* channel 4
* abscissa

Usually the channel "abscissa" is used for the time base, but other
signals connected to it can build Lissajous figures.

.. automodule:: eyeBlocks.channelcomponent
	:members:
		   
Compiling the blocks construction into something useful
-------------------------------------------------------
When blocks are assembled in the working area, it may be time
to build an application's prototype. When blocks are not assembled
in a meaningful way, warnings should be emitted.

.. automodule:: eyeBlocks.wizard
	:members:
