MSP430DLL
===
---
[![Code Climate](https://codeclimate.com/github/christoph2/msp430dll/badges/gpa.svg)](https://codeclimate.com/github/christoph2/msp430dll)
[![Build status](https://ci.appveyor.com/api/projects/status/ayd40voeq9r6qte9?svg=true)](https://ci.appveyor.com/project/christoph2/msp430dll)
[![Coverage Status](https://coveralls.io/repos/github/christoph2/msp430dll/badge.svg?branch=HEAD)](https://coveralls.io/github/christoph2/msp430dll?branch=HEAD)
[![GPL License](http://img.shields.io/badge/license-GPL-blue.svg)](http://opensource.org/licenses/GPL-2.0)

Welcome to MSP430DLL!

MSP430DLL is a convenient Python wrapper for TI MSP430 (tool) developers.

This is still work in progress and reasonable documentation has still to be written...

### Prerequisites

**Note**: If you are using out-of-the-box DLLs (32-bit), you also need a 32-bit Python version (PyPy also works fine)!

### Installation
> $git clone https://github.com/christoph2/msp430dll.git msp430dll

> $cd msp430dll

> $python setup.py develop

Since this project is currently under development, be sure to use `develop` **not** `install` -- for a discussion see [here](http://stackoverflow.com/questions/19048732/python-setup-py-develop-vs-install).

### Examples
This package contains a script called `msp-info`, which automatically gets installed by setup.

#### Usage
>$ msp430-info --help<br>
>Usage: msp430-info [options] path-to-msp430.dll<br>
><br>
>Display informations about connected MSP430 controllers.<br>
><br>
>Options:<br>
>  --version             show program's version number and exit<br>
>  -h, --help            show this help message and exit<br>
>  -n DLLNAME, --dll-name=DLLNAME<br>
>                        Name of DLL<br>
><br>

Argument *path-to-msp430.dll* denotes the location where to find *msp430.dll* (Defaults to current working directory).
If your DLL has a divergent name, say *msp430v3.dll* or *msp430mspgcc.dll*, use -n option (.dll  extension can be omitted).

This little program may or may not be useful, but but it exists mainly to demonstrate basic API usage. Anyways, you may use it as a starting point for "real" command line utilities.

If I run `msp430-info`against my `eZ430-2013` the outcome is as follows:

> Controller   : MSP430F20x3<br>
> Architekture : CPU_ARCH_ORIGINAL<br>
> 
> 
> Memory<br>
>  \------------------------------------------------------------<br>
> RAM          : from 0x0200 to 0x027f (   128 bytes)<br>
> RAM2         : [Not implemented]<br>
> FLASH        : from 0xf800 to 0xffff (  2048 bytes)<br>
> INFO         : from 0x1000 to 0x10ff (   256 bytes)<br>
> BSL          : [Not implemented]<br>
> LCD          : [Not implemented]<br>
> FRAM         : no<br>
> 
> 
> Voltages<br>
> \------------------------------------------------------------<br>
> VCC          : 3.50 V<br>
> ext. VCC     : NO_EX_POWER<br>
> Min. VCC     : 1.80 V<br>
> Max. VCC     : 3.60 V<br>
> Test VCC     : yes<br>
> 
> 
> Debugging<br>
> \------------------------------------------------------------<br>
> Brk.-Points. : 2<br>
> Combinations : 2<br>
> Cycle-ctr.   : no<br>
> Sequencer    : no<br>
> State storage: no<br>
> 
> 
> Registers<br>
> \------------------------------------------------------------<br>
> PC  = 0xf80c<br>
> SP  = 0x027e<br>
> CG1 = 0x0000<br>
> CG2 = 0x0000<br>
> R4  = 0x1ebf<br>
> R5  = 0x1267<br>
> R6  = 0xfffb<br>
> R7  = 0xffff<br>
> R8  = 0xfcf7<br>
> R9  = 0x3fb7<br>
> R10 = 0xf800<br>
> R11 = 0x77ff<br>
> R12 = 0xf800<br>
> R13 = 0xf800<br>
> R14 = 0x0002<br>
> R15 = 0x0020<br>
