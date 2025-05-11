mkdir dirTest
mkdir '<case>'
mkdir 0
cd '<case>'
    mkdir 0  0.orig  '<time directories>'  constant  system  tests
cd ../system
    mkdir blockMeshDict controlDict decomposeParDict fvSchemes fvSolution
cd ../0
    mkdir k  omega  p  U
cp -r 0 0.orig
