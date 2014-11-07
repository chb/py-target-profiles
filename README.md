Target Profiles
===============

This is a Python 3 implementation of a [target-profiles](https://github.com/lillyoi/target-profiles/) parser, codifier and model class.


Target Profile Model
--------------------

Provides Python classes to represent target profiles in memory.
...


Parser
------

> ON HOLD: The parser generates a JSON format different from Lilly's official implementation and is not currently being actively developed.

The parser consumes plain target profiles and returns the content in JSON format.
Each profile is an array of dictionaries, where each dictionary represents one rule of the profile.
The parser leverages `pyparsing` ([HowTo](http://pyparsing.wikispaces.com/HowToUsePyparsing), [documentation](https://pythonhosted.org/pyparsing/)) to parse the rather strict target profiles syntax.

Codifier
--------

The codifier consumes JSON files from the parser and adds codes for the identified concepts. These currently are:

- _RxNorm_ codes for prescriptions
- ...
