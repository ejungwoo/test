from class_cwriter import cwriter 

to_screen=False
to_file=True

################################################################################################### 
cc = cwriter("LKHit", "data", "This is an example description of class LKHit")
cc.add_private_par("int",     "id",             -1,                         "id incase there are more then one vertex")
cc.add_private_par("TVector3","position"     ,  "TVector3(-9.9,-9.9,-9.9)", "position of the vertex",      includes="TVector3.h")
cc.add_private_par("TVector3","positionError",  "TVector3(-9.9,-9.9,-9.9)", "position error of the vertex",includes="TVector3.h")
cc.print_container(to_screen=to_screen,to_file=to_file)


################################################################################################### 
cc = cwriter("LKVertex", "data", "This is an example description of class LKVertex")
cc.add_private_par("std::vector<int>", "trackIDArray", "{x}.clear()", includes="<vector>", par_persistency=False)
cc.add_private_par("int", "trackMult", 0, "track multiplicity to create this vertex")
cc.print_container(to_screen=to_screen,to_file=to_file, inheritance="public LKHit", includes="LKHit.hh")


################################################################################################### 
cc.__init__("LKTrack", "data", "This is an example description of class LKTrack")
cc.add_private_par("int",     "id",        -999)
cc.add_private_par("bool",    "isPrimary", "false")
cc.add_private_par("int",     "PDGCode",   -1)
cc.add_private_par("TVector3","momentum" , "TVector3(-9.9,-9.9,-9.9)",  includes="TVector3.h")
cc.print_container(to_screen=to_screen,to_file=to_file)


################################################################################################### 
cc.__init__("LKVertexSelectionTask", "data",
"""This is an example description of class LKVertexSelectionTask
- If you put description here it will be shown in doxygen.
- Doxygen support markdown.""")

cc.add_input_data_array("LKTrack","trackArray","tracks",
                        data_array_comment="array of tracks (LKTrack)",
                        data_array_name_lc="trackArray",
                        data_name="track",
                        includes="LKTrack.hh")

cc.add_output_data_array("LKVertex","vertexArray","vertex",
                         data_array_init_size=100,
                         data_array_comment="array of vertex (LKVertex)",
                         data_array_name_lc="vertexArray",
                         data_name="vertex",
                         includes="LKVertex.hh")

cc.add_private_par("double", "cut", 12)
cc.print_task(to_screen=to_screen,to_file=to_file)
