from twisted.application.service import ServiceMaker


name = "packager"
module = "dreambuilder.packager.service"
description = "DreamBuilder's Packaging Tools"
tapname = name
serviceMaker = ServiceMaker(name, module, description, tapname)
