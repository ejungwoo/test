from class_cwriter import cwriter 
cc = cwriter()

cc.set_name("LKExampleContainer2")
cc.set_file_path("data")
cc.set_description("""This is an example description of class LKExampleContainer
- If you put description here it will be shown in doxygen.
- Doxygen support markdown."""
)
cc.add_private_par("int","id","-999","id incase there are more then one vertex")
cc.add_private_par("bool","isPrimary","false","whether it is primary vertex or non-primary vertex")
cc.add_private_par("TVector3","position"     ,"TVector3(-9.99,-9.99,-9.99)","position of the vertex",headers="TVector3.h")
cc.add_private_par("TVector3","positionError","TVector3(-9.99,-9.99,-9.99)","position error of the vertex",headers="TVector3.h")

cc.print_container(to_screen=True,to_file=True)
