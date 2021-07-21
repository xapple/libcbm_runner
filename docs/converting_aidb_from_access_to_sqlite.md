
The purpose of this document is to explain the conversion of the Archive Index Database 
(AIDB) from the old MS Access AIDb format to the libcbm SQLite format.


# Dependencies

Cloned the cbm_defaults repo by setting up a public copy of the private repo (this might 
not have been necessary).

Cloned the libcbm_aidb repo 

   git clone git@gitlab.com:bioeconomy/libcbm/libcbm_aidb.git


# Convert



Typically you would run this file from a command line like this:

     ipython3.exe -i -- /c/repos/libcbm_runner/scripts/conversion/aidb.py

You need to run this on a machine that has a Microsoft Access driver installed.
So likely this will mean a Windows machine.

If you want to run only one country for testing, you can place
this line in the main loop:

        if converter.cbmcfs3_country.iso2_code != 'ZZ': continue


