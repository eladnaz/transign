SETUP STEPS
--------------------------------------------------------
1.This application will require a few modules to be installed 
  into your python environment first before it can run.
  Below is a list of commands for the modules to be installed :

	i. OpenCV
	   [pip install opencv-python]

	ii. Google Translator
	    [pip install googletrans]

	iii.Tensorflow
	    [pip install tensorflow]

	iv. Python Text-to-Speech
	    [pip install pyttsx3]


2. Once all that is completed, navigate to the project folder (./project)
   through the cmd and run install_tf.py
   [python install_tf.py]

3. After that, the Object Detection API needs to be setup. Run the following commands to install it
   [cd models/research/]
   [protoc object_detection/protos/*.proto --python_out=.]
   [cp object_detection/packages/tf2/setup.py]
   [python -m pip install .]

4. Once all that is complete, the application is ready to be ran. This can be done with
   [python GUI.py]

   Disclaimer : Loading may take a while as the model is loaded into the application
