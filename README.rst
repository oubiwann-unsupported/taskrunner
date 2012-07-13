Usage
=====

TBD

Structure
=========

The desire to isolate configuration information in a YAML file that could, in
turn, be used for any number of other projects, motivated the "architecture"
(or structure, if you will) of these packaging scripts.

In essence, the Makefile calls out to the Python config.py script, which reads
in any needed configuration data from config.yaml.
