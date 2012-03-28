Usage
=====

For information on how to use this repository, see the following Google Doc:
  https://docs.google.com/a/dreamhost.com/document/d/1y3HGcIHirAnOujov0aZ5usLv_JyyHvgcccU-GprnNx8/edit

In particular, the "Initial Setup" and "Packaging Process" sections.

Structure
=========

The desire to isolate configuration information in a YAML file that could, in
turn, be used for any number of other projects, motivated the "architecture"
(or structure, if you will) of these packaging scripts.

In essence, the Makefile calls out to the Python config.py script, which reads
in any needed configuration data from config.yaml.
