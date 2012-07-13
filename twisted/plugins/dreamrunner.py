from twisted.application.service import ServiceMaker


name = "packager"
module = "dreamrunner.packager.service"
description = "DreamHost's Packaging Tools"
tapname = name
serviceMaker = ServiceMaker(name, module, description, tapname)
