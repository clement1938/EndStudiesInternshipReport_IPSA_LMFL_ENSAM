rm -rf '<case>'
mkdir '<case>'
cd '<case>'
    mkdir 0  0.orig  '<time directories>'  constant  system  tests
    cd system
        mkdir blockMeshDict controlDict decomposeParDict fvSchemes fvSolution
    cd ../0
        mkdir k  omega  p  U
    cd ..
    cp -r 0 0.orig
cd ..
tree -L 3
gnome-screenshot
xwd -out arbo.xwd
