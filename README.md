# ASCII renderer

🚧 WIP 🚧

## Demos

#### pulsar shader
![demo eye gif](images/demo-eye.gif)

#### wave shader and another grayscale palette
[![demo py gif](images/demo-py.gif)](https://asciinema.org/a/210121)

#### wireframe of 3d cube
![demo cube gif](images/demo-cube.gif)

#### filled 3d cube 
![demo cube gif](images/demo-cube2.gif)


## Used materials

- http://www.opengl-tutorial.org/beginners-tutorials
- https://github.com/ssloy/tinyrenderer/wiki (only first 2 tuts so far)
- https://fenix.tecnico.ulisboa.pt/downloadFile/3779573130568/The


## TODO

- [ ] logically split code (because now it's just a mess grouped in random files)
- [x] add basic shading directly mapped to screen
- [ ] 3d model rendering
  - [x] load hardcoded model vertices/faces
  - [x] render wireframe
  - [x] render filled faces (with colors based on normals and camera direction)
  - [ ] allow to apply all kind of transformations on vertices
  - [ ] add texture 
  - [ ] add vertex shaders (?)
  - [ ] add fragment shaders
- [ ] allow to change camera position/rotation
- [ ] add perspective projection
- [ ] allow to add multiple models
- [ ] load models from files (standadized or custom format, could be pickled list of numpy arrays)
- [ ] separate rendering pipeline, scene setup and "game logic"
- [ ] add keyboard cotrol (if possible)
- [ ] ...
