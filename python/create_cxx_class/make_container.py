from class_cwriter import cwriter 


cc = cwriter("LKExampleTrack", "data", "This is an example description of class LKExampleTrack")
cc.add_private_par("int",     "id",        -999)
cc.add_private_par("bool",    "isPrimary", "false")
cc.add_private_par("int",     "PDGCode",   -1)
cc.add_private_par("TVector3","momentum" , "TVector3(-9.9,-9.9,-9.9)",  headers="TVector3.h")
cc.print_container(to_screen=True,to_file=True)

cc.__init__("LKExampleVertex", "data", "This is an example description of class LKExampleVertex")
cc.add_private_par("int",     "id",             -999,                       "id incase there are more then one vertex")
cc.add_private_par("bool",    "isPrimary",      "false",                    "whether it is primary vertex or non-primary vertex")
cc.add_private_par("TVector3","position"     ,  "TVector3(-9.9,-9.9,-9.9)", "position of the vertex",      headers="TVector3.h")
cc.add_private_par("TVector3","positionError",  "TVector3(-9.9,-9.9,-9.9)", "position error of the vertex",headers="TVector3.h")
cc.print_container(to_screen=True,to_file=True)

cc.__init__("LKExampleVertexSelectionTask", "data",
"""This is an example description of class LKExampleVertexSelectionTask
- If you put description here it will be shown in doxygen.
- Doxygen support markdown.""")
cc.add_input_data_array("LKExampleTrack","trackArray","recoTracks",
   data_array_comment="array of tracks (LKExampleTrack)",data_array_name_lc="trackArray", data_name="track", headers="LKExampleTrack.hh")
cc.add_output_data_array("LKExamplePrimaryVertex","primaryVertexArray","recoPrimaryVertex",
   data_array_init_size=100,data_array_comment="primary vertex (LKExampleVertex)",data_array_name_lc="primaryVertexArray", data_name="primaryVertex", headers="LKExampleVertex.hh")
cc.add_output_data_array("LKExampleVertex","vertexArray","recoVertex",
   data_array_init_size=100,data_array_comment="array of vertex (LKExampleVertex)",data_array_name_lc="vertexArray", data_name="vertex", headers="LKExampleVertex.hh")
cc.add_private_par("double", "cut", 12)
cc.print_task(to_screen=True,to_file=True)
