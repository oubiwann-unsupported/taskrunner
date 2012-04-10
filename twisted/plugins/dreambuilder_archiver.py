from twisted.application.service import ServiceMaker


name = "archiver"
module = "dreambuilder.archiver.service"
description = "DreamHost's Archive-building Tools"
tapname = name
serviceMaker = ServiceMaker(name, module, description, tapname)
