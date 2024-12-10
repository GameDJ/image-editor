# SIMPLE: Simple IMage Processor for Lazy Editors

Initial release for end of Fall 2024 semester.


### Functionalities: 

- Create blank canvas or load an image
  - Supported file types: PNG, JPG
- Export image
  -  Supported file types: PNG, JPG
- Zoom in/out 
  - Editing is currently not supported while zoomed in or out
- History
  - Remembers up to the 10 latest edits
  - Undo/Redo/jump to history entry
- Drawing
  - Rectangle is the only currently supported drawing tool
  - Color picking
    - Use the OS color chooser
    - Or use the Eyedropper tool to select a color from the image
- Resize Image
  - Currently uses linear interpolation
- Apply filter
  - Blur
  - Invert colors
  - Flip horizontal/vertical
  - Convert to grayscale
  - Adjust brightness
- Select (rectangular) area
  - Filters and drawings will only affect the selected area
  - Crop image to selection
  - Duplicate selected area
- Keybinds:
  - Undo: Ctrl+Z
  - Redo: Ctrl+Y
    - alternatively: Ctrl + Shift + Z
  - Selection tool: S
  - Clear Selection: C
  - Eyedropper tool: I
  - Draw tool: D
  - Zoom in: =
  - Zoom out: -


### Contributors:
&ensp;&ensp;Addison Casner  
&ensp;&ensp;Derek Jennings  
&ensp;&ensp;Quinn Pulley  
&ensp;&ensp;Will Verplaetse


# Development

run:  
`python SIMPLE.py`

build:  
`pyinstaller --onefile .\SIMPLE.py --paths .\Classes\ --workpath .\dist\build\ --specpath .\dist\build\ --clean`
