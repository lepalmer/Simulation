//Build single CSI Cube

// Single cube 9.4 cm x 9.4 cm x 1.27 cm
//Nominal
//Volume CSICube
//CSICube.Material CsI
//CSICube.Visibility 1
//CSICube.Color 2
//CSICube.Shape BOX 4.7 4.7 0.635

// Single cube 9.4 cm x 9.4 cm x 0.635 cm
//thin
//Volume CSICube
//CSICube.Material CsI
//CSICube.Visibility 1
//CSICube.Color 2
//CSICube.Shape BOX 4.7 4.7 0.3175

// Single cube 9.4 cm x 9.4 cm x 2.54 cm
//thick
Volume CSICube
CSICube.Material CsI
CSICube.Visibility 1
CSICube.Color 2
CSICube.Shape BOX 4.7 4.7 1.27

// Single cylinder
Volume CSICylinder
CSICylinder.Material CsI
CSICylinder.Visibility 1
CSICylinder.Color 2
CSICylinder.Shape TUBE 0. 5. 1.27  0. 360. 

// Single cylinder
Volume NaICylinder
NaICylinder.Material NaI
NaICylinder.Visibility 1
NaICylinder.Color 2
NaICylinder.Shape TUBE 0. 5. 1.27  0. 360. 

// Single cylinder
Volume BGOCylinder
BGOCylinder.Material BGO
BGOCylinder.Visibility 1
BGOCylinder.Color 2
BGOCylinder.Shape TUBE 0. 5. 1.27  0. 360. 

// Single cylinder
Volume PbWO4Cylinder
PbWO4Cylinder.Material PbWO4
PbWO4Cylinder.Visibility 1
PbWO4Cylinder.Color 2
PbWO4Cylinder.Shape TUBE 0. 5. 1.27  0. 360. 

