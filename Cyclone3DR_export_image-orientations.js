// Script à utiliser avec l'API Cyclone 3DR
// Exportation des données d'orientation (en degré) des vues panoramiques

var cameras = SImage.FromSel()
//var cameras = SImage.FromName('Khufu_v2 <Khufu_v2>_90_chambre-roi_herses')




function returnElements(camera){
    var orientation = camera.GetCameraExternalParameters().CameraExternal.GetOrientation()
    var nom = camera.GetName()
    print([nom, orientation.RotX, orientation.RotY, orientation.RotZ])
}


for (var i = 0; i < cameras.length; i++){
    returnElements(cameras[i])
}
