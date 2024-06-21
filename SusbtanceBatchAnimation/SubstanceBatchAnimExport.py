import glob
import os
import sd
from sd.tools import export
from sd.api.sdvaluefloat import SDValueFloat
from sd.api.sdproperty import SDPropertyCategory


#Loop and Path Variables
min_value = 0
max_value = 1
difference = max_value - min_value
frames = 10
input_value = 0
step = difference/frames
id = 'pan'
folder_path = 'D:\Projects\SD Water Test\Test3'
file_name = 'Animation_Frame'
file_type = '\*.png'

#Getting the Graph
sd_context = sd.getContext()
sd_application = sd_context.getSDApplication()
sd_ui_mgr = sd_application.getUIMgr()
graph = sd_ui_mgr.getCurrentGraph()

#Getting the Properties Setup
category = SDPropertyCategory.Input
label_property = graph.getPropertyFromId(id, category)

#Batch Exporter
for frame in range(frames):
    #exporter method
    export.exportSDGraphOutputs(graph, folder_path, '{}.png'.format(str(frame)))
    #updating the step value
    input_value = round((input_value + step), 5)
    print(input_value)
    #setting the property as the step value
    graph.setPropertyValue(label_property, SDValueFloat.sNew(input_value))
    #Locating and renameing the latest file
    files = glob.glob(folder_path + file_type)
    newest = max(files , key = os.path.getctime)
    new_name = '{0}_{1}.png'.format(file_name,str(frame))
    os.rename(newest, os.path.join(folder_path, new_name))
    print('{} frame exported'.format(str(frame)))


