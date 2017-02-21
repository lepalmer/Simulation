//Stacking 4 "layers" of CSI, 
//Each layer is 19.6 cm x 19.6 cm x 4 cm with .5 cm spacing between cubes

///// Uncomment these lines to run standalone 
//SurroundingSphere 300.0 0.0 0.0 0.0 300.0
//Include $MEGALIB/resource/examples/geomega/materials/Materials.geo
/////

Include CalorimeterCSILayer.geo 

//This builds one tower of the CsI Detector
Volume CSIDetector
CSIDetector.Material Vacuum
CSIDetector.Visibility 0
CSIDetector.Shape BRIK 9.8 9.8 2.0
// Include this to run stand-alone
//CSIDetector.Mother 0

// Add the CsI layer to the CSIDetector 
//For I 2 -4.95 9.9
//	For J 2 -4.95 9.9
//		CSICube.Copy CSICube_%I_%J
//		CSICube_%I_%J Position $I $J 0.0
//		CSICube_1_1.Rotation 7.0 -7.0 0.0
//		CSICube_1_2.Rotation -7.0 -7.0 0.0
//		CSICube_2_1.Rotation 7.0 7.0 0.0
//		CSICube_2_2.Rotation -7.0 7.0 0.0
//		CSICube_%I_%J.Mother CSIDetector
//	Done
//Done
